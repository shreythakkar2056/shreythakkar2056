from pathlib import Path
import json
import requests
from bs4 import BeautifulSoup

USERNAME = "shreythakkar2056"

ROOT = Path(__file__).parent.parent
DATA_DIR = ROOT / "data"
DATA_DIR.mkdir(exist_ok=True)

URL = f"https://github.com/users/{USERNAME}/contributions"

headers = {
    "User-Agent": "Mozilla/5.0"
}

response = requests.get(URL, headers=headers)

if response.status_code != 200:
    raise Exception(f"Failed to fetch contributions ({response.status_code})")

soup = BeautifulSoup(response.text, "html.parser")

days = []

for rect in soup.select("rect[data-date]"):

    days.append({
        "date": rect["data-date"],
        "count": int(rect.get("data-count", 0)),
        "level": int(rect.get("data-level", 0))
    })

output = DATA_DIR / "contributions.json"

output.write_text(
    json.dumps(days, indent=4),
    encoding="utf8"
)

print(f"Saved {len(days)} contribution days.")