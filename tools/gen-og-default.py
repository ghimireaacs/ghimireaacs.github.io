#!/usr/bin/env python3
"""Build the site-wide Open Graph card used by the home page, tabs and archives.

Pages without their own `image:` fall back to `social_preview_image` in
_config.yml, which points at the file this writes.

Usage: python3 tools/gen-og-default.py
"""

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent.parent
AVATAR = ROOT / "assets/img/propic.webp"
TARGET = ROOT / "assets/img/og/site-preview.jpg"
SIZE = (1200, 630)
BG = (27, 27, 30)
ACCENT = (134, 168, 231)
FONT_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FONT_REGULAR = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

TITLE = "Ashish Ghimire"
TAGLINE = "IT | Cybersecurity | HomeLab | Self-Hosting"
URL = "ashishghimire.com"


def circular(img, diameter):
    img = img.convert("RGB").resize((diameter, diameter), Image.LANCZOS)
    mask = Image.new("L", (diameter * 4, diameter * 4), 0)
    ImageDraw.Draw(mask).ellipse((0, 0, diameter * 4 - 1, diameter * 4 - 1), fill=255)
    img.putalpha(mask.resize((diameter, diameter), Image.LANCZOS))
    return img


def main():
    card = Image.new("RGB", SIZE, BG)
    draw = ImageDraw.Draw(card)
    draw.rectangle((0, 0, SIZE[0], 8), fill=ACCENT)

    with Image.open(AVATAR) as avatar:
        face = circular(avatar, 220)
    card.paste(face, (90, 205), face)

    text_x = 360
    draw.text((text_x, 225), TITLE, font=ImageFont.truetype(FONT_BOLD, 68), fill=(255, 255, 255))
    draw.text((text_x, 320), TAGLINE, font=ImageFont.truetype(FONT_REGULAR, 32), fill=(178, 178, 184))
    draw.text((text_x, 385), URL, font=ImageFont.truetype(FONT_BOLD, 30), fill=ACCENT)

    TARGET.parent.mkdir(parents=True, exist_ok=True)
    card.save(TARGET, "JPEG", quality=88, optimize=True, progressive=True)
    print(f"{TARGET.relative_to(ROOT)} ({TARGET.stat().st_size // 1024} KB)")


if __name__ == "__main__":
    main()
