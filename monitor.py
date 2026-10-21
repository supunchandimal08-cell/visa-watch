
import json
import os
from datetime import datetime, timezone
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError

ROOT = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(ROOT, "data")
STATE = os.path.join(DATA, "monitor_state.json")
UPDATES = os.path.join(DATA, "updates.json")

SOURCES = [
    {
        "country": "UK",
        "name": "UK Student visa guidance",
        "url": "https://www.gov.uk/student-visa"
    },
    {
        "country": "Canada",
        "name": "Canada study permit",
        "url": "https://www.canada.ca/en/immigration-refugees-citizenship/services/study-canada.html"
    },
    {
        "country": "Australia",
        "name": "Australia student visa",
        "url": "https://immi.homeaffairs.gov.au/visas/getting-a-visa/visa-listing/student-500"
    },
    {
        "country": "New Zealand",
        "name": "New Zealand student visa",
        "url": "https://www.immigration.govt.nz/new-zealand-visas/visas/visa/student-visa"
    },
    {
        "country": "USA",
        "name": "US student visa information",
        "url": "https://travel.state.gov/content/travel/en/us-visas/study/student-visa.html"
    },
    {
        "country": "UAE / Dubai",
        "name": "UAE government portal",
        "url": "https://u.ae/en/information-and-services/education"
    },
    {
        "country": "Europe / Schengen",
        "name": "EU immigration portal",
        "url": "https://immigration-portal.ec.europa.eu/index_en"
    }
]

def read_json(path, default):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except (OSError, json.JSONDecodeError):
        return default

def save_json(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def check_source(source):
    request = Request(
        source["url"],
        headers={"User-Agent": "VisaWatch-Monitor/1.0"}
    )
    try:
        with urlopen(request, timeout=25) as response:
            status = response.status
            return {
                **source,
                "checked_at": datetime.now(timezone.utc).isoformat(),
                "status": "reachable" if status == 200 else "http_error",
                "http_status": status,
                "note": "Official source checked. Page content has not been reviewed for rule changes."
            }
    except HTTPError as e:
        return {
            **source,
            "checked_at": datetime.now(timezone.utc).isoformat(),
            "status": "http_error",
            "http_status": e.code,
            "note": "Check the source manually."
        }
    except (URLError, TimeoutError, OSError) as e:
        return {
            **source,
            "checked_at": datetime.now(timezone.utc).isoformat(),
            "status": "unreachable",
            "http_status": None,
            "note": str(e)[:250]
        }

def main():
    os.makedirs(DATA, exist_ok=True)
    old_state = read_json(STATE, {})
    results = [check_source(source) for source in SOURCES]

    output = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "items": results,
        "monitor_errors": [
            {
                "country": item["country"],
                "source": item["url"],
                "error": item["note"]
            }
            for item in results
            if item["status"] != "reachable"
        ],
        "disclaimer": (
            "Source availability checks only. No immigration rule changes "
            "are confirmed automatically. Review official pages manually."
        )
    }

    state = {
        "last_checked_at": output["generated_at"],
        "sources": {
            item["url"]: item["status"] for item in results
        }
    }

    save_json(UPDATES, output)
    save_json(STATE, state)

    print("VisaWatch source check completed.")
    print(f"Sources checked: {len(results)}")
    print(f"Reachable: {sum(x['status'] == 'reachable' for x in results)}")
    print(f"Needs review: {len(output['monitor_errors'])}")

if __name__ == "__main__":
    main()

