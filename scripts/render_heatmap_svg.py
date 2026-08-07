
from pathlib import Path
import json
from datetime import datetime

ROOT = Path(__file__).parent.parent

INPUT = ROOT / "data" / "contributions.json"
OUTPUT = ROOT / "contrib-heatmap.svg"

# --------------------------------------------------
# Load contribution data
# --------------------------------------------------

data = json.loads(INPUT.read_text(encoding="utf8"))

days = data["days"]
total = data["total"]

# --------------------------------------------------
# SVG SETTINGS
# --------------------------------------------------

CELL = 12
GAP = 3

ROWS = 7
COLS = 53

LEFT = 40
TOP = 55

WIDTH = LEFT + COLS * (CELL + GAP) + 30
HEIGHT = 180

BACKGROUND = "#0d1117"
TEXT = "#c9d1d9"
SUBTEXT = "#8b949e"

COLORS = {
    "NONE": "#161b22",
    "FIRST_QUARTILE": "#0e4429",
    "SECOND_QUARTILE": "#006d32",
    "THIRD_QUARTILE": "#26a641",
    "FOURTH_QUARTILE": "#39d353"
}

# --------------------------------------------------
# Build SVG
# --------------------------------------------------

svg = []

svg.append(f"""
<svg
xmlns="http://www.w3.org/2000/svg"
width="{WIDTH}"
height="{HEIGHT}"
viewBox="0 0 {WIDTH} {HEIGHT}">

<style>

text {{
font-family:
Inter,
Segoe UI,
Arial,
sans-serif;
}}

.small {{
font-size:11px;
fill:{SUBTEXT};
}}

.title {{
font-size:18px;
font-weight:bold;
fill:{TEXT};
}}

.footer {{
font-size:12px;
fill:{SUBTEXT};
}}

</style>

<rect
width="100%"
height="100%"
fill="{BACKGROUND}"
rx="12"/>

""")

# --------------------------------------------------
# Title
# --------------------------------------------------

svg.append(f"""

<text
x="20"
y="28"
class="title">

GitHub Contributions

</text>

""")

# --------------------------------------------------
# Month Labels
# --------------------------------------------------

months = [
"Jan",
"Feb",
"Mar",
"Apr",
"May",
"Jun",
"Jul",
"Aug",
"Sep",
"Oct",
"Nov",
"Dec"
]

current_month = None

for i, day in enumerate(days):

    dt = datetime.fromisoformat(day["date"])

    if dt.month != current_month:

        current_month = dt.month

        col = i // 7

        x = LEFT + col * (CELL + GAP)

        svg.append(f"""

<text
x="{x}"
y="42"
class="small">

{months[current_month-1]}

</text>

""")

# --------------------------------------------------
# Weekday Labels
# --------------------------------------------------

weekday_labels = [
"Mon",
"Wed",
"Fri"
]

weekday_rows = [
1,
3,
5
]

for label, row in zip(weekday_labels, weekday_rows):

    y = TOP + row * (CELL + GAP) + CELL - 2

    svg.append(f"""

<text
x="5"
y="{y}"
class="small">

{label}

</text>

""")
    # --------------------------------------------------
# Contribution Grid
# --------------------------------------------------

level_map = {
    "NONE": COLORS["NONE"],
    "FIRST_QUARTILE": COLORS["FIRST_QUARTILE"],
    "SECOND_QUARTILE": COLORS["SECOND_QUARTILE"],
    "THIRD_QUARTILE": COLORS["THIRD_QUARTILE"],
    "FOURTH_QUARTILE": COLORS["FOURTH_QUARTILE"]
}

for i, day in enumerate(days):

    col = i // 7
    row = i % 7

    x = LEFT + col * (CELL + GAP)
    y = TOP + row * (CELL + GAP)

    level = day["level"]

    # Support both GraphQL strings and numeric values
    if isinstance(level, int):
        color = [
            COLORS["NONE"],
            COLORS["FIRST_QUARTILE"],
            COLORS["SECOND_QUARTILE"],
            COLORS["THIRD_QUARTILE"],
            COLORS["FOURTH_QUARTILE"]
        ][min(level, 4)]
    else:
        color = level_map.get(level, COLORS["NONE"])

    delay = round(i * 0.008, 3)

    svg.append(f"""
<rect
x="{x}"
y="{y}"
width="{CELL}"
height="{CELL}"
rx="2"
fill="{color}"
opacity="0">

<title>{day['date']} • {day['count']} contributions</title>

<animate
attributeName="opacity"
from="0"
to="1"
begin="{delay}s"
dur="0.25s"
fill="freeze"/>

<animateTransform
attributeName="transform"
type="translate"
from="0 -6"
to="0 0"
begin="{delay}s"
dur="0.25s"
fill="freeze"/>

</rect>
""")
    # --------------------------------------------------
# Terminal Header
# --------------------------------------------------

svg.insert(
    1,
    f"""
<text
x="20"
y="18"
font-size="12"
fill="{SUBTEXT}"
font-family="Consolas, monospace">

shrey@github:~$ ./contributions.sh

</text>

<text
x="{WIDTH-165}"
y="18"
font-size="11"
fill="{SUBTEXT}"
font-family="Consolas, monospace">

Generated with GraphQL API

</text>
"""
)

# --------------------------------------------------
# Close SVG
# --------------------------------------------------

svg.append("""

</svg>

""")

# --------------------------------------------------
# Save SVG
# --------------------------------------------------

OUTPUT.write_text(
    "".join(svg),
    encoding="utf8"
)

print()
print("=" * 50)
print("Contribution heatmap generated successfully!")
print(f"Output : {OUTPUT}")
print("=" * 50)