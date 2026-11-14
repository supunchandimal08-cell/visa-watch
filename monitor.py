import hashlib
import json
import os
import re
import time
from datetime import datetime, timezone
from concurrent.futures import ThreadPoolExecutor
from html.parser import HTMLParser
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError

ROOT = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(ROOT, "data")
STATE = os.path.join(DATA, "monitor_state.json")
UPDATES = os.path.join(DATA, "updates.json")
SOURCES_FILE = os.path.join(DATA, "sources.json")

FALLBACK_SOURCES = [
    {"country": "UK", "name": "GOV.UK Immigration Rules — Appendix Student", "url": "https://www.gov.uk/guidance/immigration-rules/immigration-rules-appendix-student"},
    {"country": "Canada", "name": "IRCC Study Permit — Eligibility", "url": "https://www.canada.ca/en/immigration-refugees-citizenship/services/study-canada/study-permit/eligibility.html", "compare_text": False},
    {"country": "Australia", "name": "Department of Home Affairs — Student visa subclass 500", "url": "https://immi.homeaffairs.gov.au/visas/getting-a-visa/visa-listing/student-500"},
    {"country": "New Zealand", "name": "Immigration New Zealand — Fee Paying Student Visa", "url": "https://www.immigration.govt.nz/visas/fee-paying-student-visa/"},
    {"country": "USA", "name": "ICE Study in the States — SEVP School Search", "url": "https://studyinthestates.dhs.gov/school-search"},
    {"country": "UAE / Dubai", "name": "GDRFA Dubai — Issuing a residency permit to a student", "url": "https://gdrfad.gov.ae/en/services/f52024e0-b812-11ed-5210-4cd98f768936"},
    {"country": "UAE / Dubai", "name": "Federal ICP — Renewal of residence permits (student grace-period categories)", "url": "https://icp.gov.ae/en/services-details/?serviceid=64afe3c1035448005bd52e66"},
    {"country": "Europe / Schengen", "name": "European Commission — Who does what in EU immigration", "url": "https://home-affairs.ec.europa.eu/policies/migration-and-asylum/eu-immigration-portal/who-does-what_en"},
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
            "compare_text": item.get("compare_text", True) is not False,
        })
    return sources or FALLBACK_SOURCES

def check_source(source, previous):
    last_error = None
    for attempt in range(2):
        request = Request(source["url"], headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.9",
            "Cache-Control": "no-cache",
        }, method="HEAD" if source.get("compare_text") is False else "GET")
        try:
            # Keep each source check bounded so one slow site does not delay the full run.
            request_timeout = 10
            with urlopen(request, timeout=request_timeout) as response:
                status_code = response.status
                content_type = response.headers.get("Content-Type", "")
                if source.get("compare_text") is False:
                    return {**source, "checked_at": datetime.now(timezone.utc).isoformat(),
                            "status": "reachable", "http_status": status_code,
                            "content_compared": False, "change_detected": False,
                            "note": "Official source returned HTTP " + str(status_code) + ". Text comparison is disabled for this slow page; counsellors must review the live IRCC page manually. Availability only, not policy-change monitoring."}
                try:
                    body = response.read(1_000_000)  # Bound large government pages; first 1 MB is sufficient for change fingerprinting.
                except (TimeoutError, OSError) as read_error:
                    return {**source, "checked_at": datetime.now(timezone.utc).isoformat(),
                            "status": "reachable", "http_status": status_code,
                            "content_compared": False, "change_detected": False,
                            "note": "Official page returned HTTP " + str(status_code) + ", but reading its page text timed out (" + str(read_error)[:100] + "). Availability is confirmed; manual policy review is required and no text-change comparison was possible."}
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
            if e.code == 403:
                return {**source, "checked_at": datetime.now(timezone.utc).isoformat(),
                        "status": "manual_review", "http_status": e.code,
                        "change_detected": False,
                        "note": "Automated access was denied (HTTP 403). This does not prove the official URL is broken. Open the official page in a browser and verify manually; no page comparison was possible."}
            return {**source, "checked_at": datetime.now(timezone.utc).isoformat(),
                    "status": "http_error", "http_status": e.code,
                    "change_detected": False,
                    "note": "Official source returned HTTP " + str(e.code) + "; review manually. No page comparison was possible."}
        except (URLError, TimeoutError, OSError, ValueError) as e:
            if source.get("compare_text") is False:
                return {**source, "checked_at": datetime.now(timezone.utc).isoformat(),
                        "status": "manual_review", "http_status": None,
                        "content_compared": False, "change_detected": False,
                        "note": "Automated availability check timed out or was blocked (" + str(e)[:120] + "). Open the official IRCC page in a browser and verify manually; no policy text comparison was possible."}
            last_error = str(e)
            if attempt < 1:
                time.sleep(1)
    note = ("Failed after 2 attempts: " + str(last_error or "unknown connection error"))[:250]
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
    # Check sources concurrently so slow government websites do not make the daily run take hours.
    # Keep concurrency modest to avoid overloading official sites.
    with ThreadPoolExecutor(max_workers=8) as executor:
        results = list(executor.map(lambda source: check_source(source, previous_hashes), sources))

    # Keep hashes only for currently configured sources. Preserve the last
    # successful hash for active sources that temporarily fail to load.
    active_urls = {source["url"] for source in sources}
    new_hashes = {
        url: previous_hashes[url]
        for url in active_urls
        if url in previous_hashes
    }
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
            for item in results if item["status"] in ("unreachable", "http_error")
        ],
        "manual_review_required": [
            {"country": item["country"], "source": item["url"], "reason": item["note"]}
            for item in results if item["status"] == "manual_review" or item.get("content_compared") is False
        ],
        "disclaimer": "The monitor checks official-source availability and compares visible page text where enabled. Canada is availability-only because the page read times out; manual review is required. A detected page-text difference is only a candidate for human review, not a confirmed immigration rule change."
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
    for item in results:
        print(f"Source result: {item['country']} | {item['status']} | HTTP {item.get('http_status')} | {item['note']}")
    print(f"Reachable: {sum(x['status'] == 'reachable' for x in results)}")
    print(f"Possible page-text changes to review: {len(output['change_candidates'])}")
    print(f"Sources needing connectivity review: {len(output['monitor_errors'])}")
    print(f"Sources requiring manual content review: {len(output['manual_review_required'])}")

if __name__ == "__main__":
    main()
