from pathlib import Path
from PIL import Image
import html

ROOT = Path(__file__).parent.parent

INPUT = ROOT / "assets" / "source-prepped.png"
OUTPUT = ROOT / "ascii.svg"

RAMP = " .'`^\",:;Il!i~+_-?][}{1)(|\\/tfjrxnuvczXYUJCLQ0OZmwqpdbkhao*#MW&8%B@$"

img = Image.open(INPUT).convert("L")

pixels = img.load()

width, height = img.size

lines = []

for y in range(height):

    row = ""

    for x in range(width):

        value = pixels[x, y]

        idx = int(value / 255 * (len(RAMP) - 1))

        row += RAMP[idx]

    lines.append(row)

FONT_SIZE = 9
LINE_HEIGHT = 10
SVG_WIDTH = width * 6.2
SVG_HEIGHT = height * LINE_HEIGHT + 20

svg = f'''<svg xmlns="http://www.w3.org/2000/svg"
width="{SVG_WIDTH}"
height="{SVG_HEIGHT}"
viewBox="0 0 {SVG_WIDTH} {SVG_HEIGHT}">

<rect width="100%" height="100%" fill="#0d1117"/>

<text
x="10"
y="20"
font-family="Consolas, monospace"
font-size="{FONT_SIZE}"
fill="#c9d1d9"
xml:space="preserve">
'''

for i, line in enumerate(lines):
    svg += f'<tspan x="10" y="{20+i*LINE_HEIGHT}">{html.escape(line)}</tspan>\n'

svg += "</text></svg>"

OUTPUT.write_text(svg, encoding="utf8")

print("ASCII SVG generated!")