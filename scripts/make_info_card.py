from pathlib import Path
import json

ROOT = Path(__file__).parent.parent

PROFILE = ROOT / "data" / "profile.json"
OUTPUT = ROOT / "info-card.svg"

data = json.loads(PROFILE.read_text(encoding="utf8"))

WIDTH = 560
HEIGHT = 360

BACKGROUND = "#0d1117"
BORDER = "#30363d"
TEXT = "#c9d1d9"
GREEN = "#7ee787"
BLUE = "#58a6ff"
GRAY = "#8b949e"

svg = f'''
<svg xmlns="http://www.w3.org/2000/svg"
width="{WIDTH}"
height="{HEIGHT}"
viewBox="0 0 {WIDTH} {HEIGHT}">

<style>

text{{
font-family:Consolas,'JetBrains Mono',monospace;
font-size:16px;
dominant-baseline:hanging;
}}

.fade{{
opacity:0;
animation:fade .45s forwards;
}}

@keyframes fade{{
from{{opacity:0;transform:translateY(6px);}}
to{{opacity:1;transform:translateY(0);}}
}}

</style>

<rect width="100%" height="100%" rx="14" fill="{BACKGROUND}" stroke="{BORDER}"/>

<circle cx="22" cy="22" r="6" fill="#ff5f57"/>
<circle cx="42" cy="22" r="6" fill="#febc2e"/>
<circle cx="62" cy="22" r="6" fill="#28c840"/>

<text x="90" y="15" fill="{GRAY}">$ neofetch</text>
'''

lines = [
("Name",data["name"]),
("Title",data["title"]),
("Location",data["location"]),
("Company",data["company"]),
("Current",data["current"]),
("Frontend",data["frontend"]),
("Backend",data["backend"]),
("Database",data["database"]),
("Languages",data["languages"]),
("Tools",data["tools"]),
("Website",data["website"]),
("GitHub",data["github"])
]

y = 55

for i,(key,val) in enumerate(lines):

    delay=i*0.18

    svg+=f'''

<text
class="fade"
x="28"
y="{y}"
fill="{GREEN}"
style="animation-delay:{delay}s">

{key:<11}

</text>

<text
class="fade"
x="150"
y="{y}"
fill="{TEXT}"
style="animation-delay:{delay}s">

: {val}

</text>

'''

    y+=25

svg += """

<text
x="28"
y="335"
fill="#58a6ff">

Powered by Python + SVG

</text>

</svg>

"""

OUTPUT.write_text(svg,encoding="utf8")

print("info-card.svg generated.")