"""Generate favicon files from `static/images/finchatbot.jpg`.

Usage:
    python scripts/generate_favicons.py

Creates:
 - static/images/finchatbot-16.png
 - static/images/finchatbot-32.png
 - static/images/finchatbot-180.png
 - static/images/finchatbot.ico

Requires Pillow: `pip install Pillow`
"""
from PIL import Image
import os

ROOT = os.path.dirname(os.path.dirname(__file__))
SRC = os.path.join(ROOT, 'static', 'images', 'finchatbot.jpg')
OUT_DIR = os.path.join(ROOT, 'static', 'images')

sizes = {
    'finchatbot-16.png': (16, 16),
    'finchatbot-32.png': (32, 32),
    'finchatbot-180.png': (180, 180),
}

if not os.path.exists(SRC):
    print('Source image not found:', SRC)
    raise SystemExit(1)

img = Image.open(SRC).convert('RGBA')
for name, size in sizes.items():
    out_path = os.path.join(OUT_DIR, name)
    resized = img.copy()
    resized.thumbnail(size, Image.LANCZOS)
    # Ensure exact size by pasting on transparent canvas
    canvas = Image.new('RGBA', size, (255,255,255,0))
    w,h = resized.size
    canvas.paste(resized, ((size[0]-w)//2, (size[1]-h)//2), resized)
    canvas.save(out_path, format='PNG')
    print('Wrote', out_path)

# Create .ico
ico_path = os.path.join(OUT_DIR, 'finchatbot.ico')
ico_sizes = [(16,16), (32,32), (64,64), (128,128), (256,256)]
img.save(ico_path, format='ICO', sizes=ico_sizes)
print('Wrote', ico_path)
