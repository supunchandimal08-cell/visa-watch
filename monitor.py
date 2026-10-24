import hashlib
import json
import os
import re
import time
from datetime import datetime, timezone
from html.parser import HTMLParser
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError

ROOT = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(ROOT, "data")
STATE = os.path.join(DATA, "monitor_state.json")
UPDATES = os.path.join(DATA, "updates.json")
SOURCES_FILE = os.path.join(DATA, "sources.json")

FALLBACK_SOURCES = [
    {"country": "UK", "name": "UK Student visa guidance", "url": "https://www.gov.uk/student-visa"},
    {"country": "Canada", "name": "Canada study permit", "url": "https://www.canada.ca/en/immigration-refugees-citizenship/services/study-canada.html"},
    {"country": "Australia", "name": "Australia student visa", "url": "https://immi.homeaffairs.gov.au/visas/getting-a-visa/visa-listing/student-500"},
    {"country": "New Zealand", "name": "New Zealand student visa", "url": "https://www.immigration.govt.nz/new-zealand-visas/visas/visa/student-visa"},
    {"country": "USA", "name": "US student visa information", "url": "https://travel.state.gov/content/travel/en/us-visas/study/student-visa.html"},
    {"country": "UAE / Dubai", "name": "UAE government portal", "url": "https://u.ae/en/information-and-services/education"},
    {"country": "Europe / Schengen", "name": "EU Immigration Portal", "url": "https://immigration-portal.ec.europa.eu/index_en"},
]

class VisibleTextParser(HTMLParser):
    """Extract readable page text while ignoring script/style/template contents."""
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.parts = []
        self.hidden_depth = 0

    def handle_starttag(self, tag, attrs):
        if tag.lower() in ("script", "style", "noscript", "template", "svg"):
            self.hidden_depth += 1

    def handle_endtag(self, tag):
        if tag.lower() in ("script", "style", "noscript", "template", "svg") and self.hidden_depth:
            self.hidden_depth -= 1

    def handle_data(self, data):
        if not self.hidden_depth:
            text = re.sub(r"\s+", " ", data).strip()
            if text:
                self.parts.append(text)

def read_json(path, default):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except (OSError, json.JSONDecodeError):
        return default

def save_json(path, data):
    temp = path + ".tmp"
    with open(temp, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        f.write("\n")
    os.replace(temp, path)

def load_sources():
    data = read_json(SOURCES_FILE, {})
    configured = data.get("sources", []) if isinstance(data, dict) else []
    sources = []
    for item in configured:
        if not isinstance(item, dict) or not item.get("url") or not item.get("country"):
            continue
        sources.append({
            "country": item["country"],
            "name": item.get("name") or item["country"] + " official immigration source",
            "url": item["url"],
        })
    return sources or FALLBACK_SOURCES

def check_source(source, previous):
    last_error = None
    for attempt in range(3):
        request = Request(source["url"], headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.9",
            "Cache-Control": "no-cache",
        })
        try:
            with urlopen(request, timeout=25) as response:
                status_code = response.status
                content_type = response.headers.get("Content-Type", "")
                body = response.read(3_000_000)
            if status_code < 200 or status_code >= 300:
                return {**source, "checked_at": datetime.now(timezone.utc).isoformat(),
                        "status": "http_error", "http_status": status_code,
                        "change_detected": False,
                        "note": "Official page returned an HTTP response that needs manual review."}
            if "html" not in content_type.lower() and body[:100].lstrip().startswith(b"%PDF"):
                return {**source, "checked_at": datetime.now(timezone.utc).isoformat(),
                        "status": "reachable", "http_status": status_code,
                        "change_detected": False,
                        "note": "Source reachable, but content was not compared because it is not an HTML page."}
            decoded = body.decode("utf-8", errors="replace")
            parser = VisibleTextParser()
            parser.feed(decoded)
            visible_text = re.sub(r"\s+", " ", " ".join(parser.parts)).strip()
            if not visible_text:
                visible_text = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", decoded)).strip()
            digest = hashlib.sha256(visible_text.encode("utf-8")).hexdigest()
            previous_hash = previous.get(source["url"])
            changed = bool(previous_hash and previous_hash != digest)
            first_check = not previous_hash
            if changed:
                note = "Possible page-text change detected since the previous successful check. Review the official page; this is not proof of a policy change."
            elif first_check:
                note = "Initial baseline saved. Future successful checks can be compared for possible page-text changes."
            else:
                note = "No page-text change detected since the previous successful check. This does not guarantee that every policy detail was checked."
            return {**source, "checked_at": datetime.now(timezone.utc).isoformat(),
                    "status": "reachable", "http_status": status_code,
                    "content_hash": digest, "change_detected": changed,
                    "baseline_created": first_check, "note": note}
        except HTTPError as e:
            if source["country"] == "USA" and e.code == 403:
                return {**source, "checked_at": datetime.now(timezone.utc).isoformat(),
                        "status": "manual_review", "http_status": e.code,
                        "change_detected": False,
                        "note": "Automated access was denied (HTTP 403). Open the official page in a browser and verify manually; no page comparison was possible."}
            return {**source, "checked_at": datetime.now(timezone.utc).isoformat(),
                    "status": "http_error", "http_status": e.code,
                    "change_detected": False,
                    "note": "Official source returned HTTP " + str(e.code) + "; review manually. No page comparison was possible."}
        except (URLError, TimeoutError, OSError, ValueError) as e:
            last_error = str(e)
            if attempt < 2:
                time.sleep(2)
    note = ("Failed after 3 attempts: " + str(last_error or "unknown connection error"))[:250]
    result = {**source, "checked_at": datetime.now(timezone.utc).isoformat(),
              "status": "unreachable", "http_status": None,
              "change_detected": False, "note": note}
    # For sources that block automated requests or intermittently time out,
    # keep the official link visible and explicitly direct staff to manual review.
    if source["country"] == "USA" and "403" in note:
        result["status"] = "manual_review"
        result["note"] = "Automated access was denied. Open the official page in a browser and verify manually; no page comparison was possible."
    return result

def main():
    os.makedirs(DATA, exist_ok=True)
    old_state = read_json(STATE, {})
    previous_hashes = old_state.get("content_hashes", {}) if isinstance(old_state, dict) else {}
    if not isinstance(previous_hashes, dict):
        previous_hashes = {}
    sources = load_sources()
    results = [check_source(source, previous_hashes) for source in sources]

    new_hashes = dict(previous_hashes)
    for item in results:
        if item.get("content_hash"):
            new_hashes[item["url"]] = item["content_hash"]

    output = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "items": results,
        "change_candidates": [
            {"country": item["country"], "name": item["name"], "url": item["url"],
             "checked_at": item["checked_at"], "note": item["note"]}
            for item in results if item.get("change_detected")
        ],
        "monitor_errors": [
            {"country": item["country"], "source": item["url"], "error": item["note"]}
            for item in results if item["status"] != "reachable"
        ],
        "disclaimer": "The monitor compares visible page text and checks availability only. A detected page-text difference is a candidate for human review, not a confirmed immigration rule change."
    }
    state = {
        "last_checked_at": output["generated_at"],
        "content_hashes": new_hashes,
        "sources": {item["url"]: item["status"] for item in results},
    }
    save_json(UPDATES, output)
    save_json(STATE, state)
    print("VisaWatch page-text monitor completed.")
    print(f"Sources checked: {len(results)}")
    print(f"Reachable: {sum(x['status'] == 'reachable' for x in results)}")
    print(f"Possible page-text changes to review: {len(output['change_candidates'])}")
    print(f"Sources needing connectivity review: {len(output['monitor_errors'])}")

if __name__ == "__main__":
    main()
