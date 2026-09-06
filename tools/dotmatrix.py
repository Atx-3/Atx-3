"""
Dot-matrix art generator.
  - text mode : renders words as an LED dot-matrix panel
  - face mode : converts a photo into braille/dot art
Usage:
  python dotmatrix.py text "AYUSH TIWARI" --cols 60
  python dotmatrix.py face path/to/photo.jpg --cols 80
"""
import sys, argparse
from PIL import Image, ImageDraw, ImageFont, ImageOps

ON, OFF = "●", "·"

def load_font(size):
    for name in ("arialbd.ttf", "arial.ttf", "consola.ttf", "DejaVuSans-Bold.ttf"):
        try:
            return ImageFont.truetype(name, size)
        except Exception:
            continue
    return ImageFont.load_default()

def text_matrix(text, cols):
    font = load_font(48)
    tmp = Image.new("L", (10, 10))
    d = ImageDraw.Draw(tmp)
    box = d.textbbox((0, 0), text, font=font)
    w, h = box[2] - box[0], box[3] - box[1]
    img = Image.new("L", (w + 8, h + 8), 0)
    ImageDraw.Draw(img).text((4 - box[0], 4 - box[1]), text, fill=255, font=font)
    rows = max(1, round(cols * img.height / img.width / 1.05))
    img = img.resize((cols, rows))
    px = img.load()
    out = []
    for y in range(rows):
        out.append("".join(ON if px[x, y] > 90 else OFF for x in range(cols)))
    return "\n".join(out)

def face_matrix(path, cols):
    img = Image.open(path).convert("L")
    img = ImageOps.autocontrast(img)
    rows = max(1, round(cols * img.height / img.width / 2.0))
    img = img.resize((cols, rows))
    px = img.load()
    ramp = " .·:-=+*#%@"          # dark -> light density
    out = []
    for y in range(rows):
        line = ""
        for x in range(cols):
            v = px[x, y]
            line += ramp[min(len(ramp) - 1, v * len(ramp) // 256)]
        out.append(line)
    return "\n".join(out)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("mode", choices=["text", "face"])
    ap.add_argument("value")
    ap.add_argument("--cols", type=int, default=60)
    a = ap.parse_args()
    print(text_matrix(a.value, a.cols) if a.mode == "text" else face_matrix(a.value, a.cols))

if __name__ == "__main__":
    main()
