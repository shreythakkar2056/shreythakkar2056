from pathlib import Path
from PIL import Image, ImageOps
import html

ROOT = Path(__file__).parent.parent

INPUT = ROOT / "assets" / "source-prepped.png"
OUTPUT = ROOT / "ascii2.svg"

# Light → Dark
RAMP = " .,:-=+*#%@"

# ----------------------------
# Settings
# ----------------------------

FONT_SIZE = 8
CHAR_WIDTH = 6.1
LINE_HEIGHT = 9

BACKGROUND = "#0d1117"
TEXT = "#7ee787"

WHITE_THRESHOLD = 225
BLACK_THRESHOLD = 18

# ----------------------------

img = Image.open(INPUT).convert("L")
img = ImageOps.autocontrast(img)

pixels = img.load()

width, height = img.size

ascii_rows = []

for y in range(height):

    row = ""

    for x in range(width):

        value = pixels[x, y]

        # Remove background
        if value >= WHITE_THRESHOLD:
            row += " "
            continue

        # Make very dark regions solid
        if value <= BLACK_THRESHOLD:
            row += "@"
            continue

        # Map brightness
        idx = int((255 - value) / 255 * (len(RAMP) - 1))
        idx = max(0, min(idx, len(RAMP) - 1))

        row += RAMP[idx]

    # Remove useless trailing spaces
    ascii_rows.append(row.rstrip())

svg_width = int(width * CHAR_WIDTH + 40)
svg_height = int(height * LINE_HEIGHT + 30)

svg = f'''<svg xmlns="http://www.w3.org/2000/svg"
width="{svg_width}"
height="{svg_height}"
viewBox="0 0 {svg_width} {svg_height}">

<rect width="100%" height="100%" fill="{BACKGROUND}"/>

<text
x="20"
y="20"
font-family="'JetBrains Mono','Cascadia Code','Fira Code',monospace"
font-size="{FONT_SIZE}"
fill="{TEXT}"
xml:space="preserve"
shape-rendering="crispEdges">
'''

for i, row in enumerate(ascii_rows):

    svg += f'<tspan x="20" y="{20+i*LINE_HEIGHT}">{html.escape(row)}</tspan>\n'

svg += """
</text>

</svg>
"""

OUTPUT.write_text(svg, encoding="utf8")

print()
print("=" * 40)
print(" ASCII SVG generated")
print("=" * 40)
print(OUTPUT)