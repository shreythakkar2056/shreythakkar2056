from pathlib import Path
from datetime import datetime, timedelta
from dotenv import load_dotenv
import os
import json
import requests

load_dotenv()

TOKEN = os.getenv("TOKEN")
USERNAME = os.getenv("GITHUB_USERNAME")

if not TOKEN:
    raise RuntimeError("TOKEN not found in .env")

ROOT = Path(__file__).parent.parent
DATA = ROOT / "data"
DATA.mkdir(exist_ok=True)

today = datetime.utcnow().date()
start = today - timedelta(days=370)

query = """
query($login:String!, $from:DateTime!, $to:DateTime!) {
  user(login:$login) {
    contributionsCollection(from:$from,to:$to) {
      contributionCalendar {
        totalContributions
        weeks {
          contributionDays {
            contributionCount
            contributionLevel
            date
            weekday
          }
        }
      }
    }
  }
}
"""

variables = {
    "login": USERNAME,
    "from": f"{start}T00:00:00Z",
    "to": f"{today}T23:59:59Z"
}

headers = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json"
}

r = requests.post(
    "https://api.github.com/graphql",
    json={
        "query": query,
        "variables": variables
    },
    headers=headers
)

data = r.json()

if "errors" in data:
    print(json.dumps(data["errors"], indent=2))
    raise SystemExit()

calendar = data["data"]["user"]["contributionsCollection"]["contributionCalendar"]

days = []

for week in calendar["weeks"]:
    for day in week["contributionDays"]:
        days.append({
            "date": day["date"],
            "count": day["contributionCount"],
            "level": day["contributionLevel"],
            "weekday": day["weekday"]
        })

output = {
    "total": calendar["totalContributions"],
    "days": days
}

(DATA / "contributions.json").write_text(
    json.dumps(output, indent=4),
    encoding="utf8"
)

print(f"Total Contributions : {output['total']}")
print(f"Days fetched        : {len(days)}")
print("Saved data/contributions.json")