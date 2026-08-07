from PIL import Image, ImageOps, ImageEnhance
from pathlib import Path

ROOT = Path(__file__).parent.parent

INPUT = ROOT / "assets" / "source-photo.png"
OUTPUT = ROOT / "assets" / "source-prepped.png"

# Load image
img = Image.open(INPUT).convert("L")

w, h = img.size

# Crop to head & shoulders
left = int(w * 0.12)
right = int(w * 0.88)

top = int(h * 0.08)
bottom = int(h * 0.62)

img = img.crop((left, top, right, bottom))

# Improve contrast
img = ImageOps.autocontrast(img)

contrast = ImageEnhance.Contrast(img)
img = contrast.enhance(2.0)

brightness = ImageEnhance.Brightness(img)
img = brightness.enhance(1.05)

# Resize
WIDTH = 110
aspect = img.height / img.width
HEIGHT = int(WIDTH * aspect * 0.55)

img = img.resize((WIDTH, HEIGHT), Image.LANCZOS)

img.save(OUTPUT)

print("Saved:", OUTPUT)