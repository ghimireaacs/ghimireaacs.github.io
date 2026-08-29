#!/usr/bin/env python3
"""Build a 1200x630 social card for every post.

The card puts the post header behind a dark scrim and prints the things a reader
wants at a glance: category, title, reading time and date. Cards are JPEG because
LinkedIn does not render WebP, and 1200x630 because that is the large-card size
Facebook/LinkedIn/X expect; the page itself keeps serving the WebP header.

Reading time follows the theme's own formula (words / 180, minimum 1) and is read
off the built pages in _site/ when they exist, so the card agrees with the byline
on the post. Run `bundle exec jekyll build` first, then this script, then build
again to publish the cards.

Output: assets/img/og/<post-slug>.jpg, picked up by _includes/head.html.
Usage:  python3 tools/gen-og-images.py
"""

import re
from datetime import date
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT = Path(__file__).resolve().parent.parent
POSTS = ROOT / "_posts"
SITE_POSTS = ROOT / "_site/posts"
AVATAR = ROOT / "assets/img/propic.webp"
OUT_DIR = ROOT / "assets/img/og"

SIZE = (1200, 630)
QUALITY = 82
PAD = 72
BG = (27, 27, 30)
ACCENT = (134, 168, 231)
MUTED = (196, 196, 202)
WPM = 180
SUFFIXES = {".webp", ".png", ".jpg", ".jpeg"}
# Below this width an upscale to 1200px turns to mush, so the header is used as a
# blurred backdrop only.
MIN_COVER_WIDTH = 600

FONT_DIRS = ["/usr/share/fonts/truetype/lato", "/usr/share/fonts/truetype/dejavu"]
FONT_NAMES = {"bold": ["Lato-Bold.ttf", "DejaVuSans-Bold.ttf"],
              "black": ["Lato-Black.ttf", "DejaVuSans-Bold.ttf"],
              "regular": ["Lato-Regular.ttf", "DejaVuSans.ttf"]}


def font_path(weight):
    for name in FONT_NAMES[weight]:
        for directory in FONT_DIRS:
            candidate = Path(directory) / name
            if candidate.is_file():
                return str(candidate)
    raise SystemExit(f"no font found for weight '{weight}' in {FONT_DIRS}")


def font(weight, size):
    return ImageFont.truetype(font_path(weight), size)


# --- post parsing -----------------------------------------------------------

FM_SPLIT = re.compile(r"^---\s*$", re.MULTILINE)
CODE_FENCE = re.compile(r"^(```|~~~).*$", re.MULTILINE)
HTML_TAG = re.compile(r"<[^>]+>")
LIQUID = re.compile(r"\{[%{].*?[%}]\}", re.DOTALL)
MD_IMAGE = re.compile(r"!\[[^\]]*\]\([^)]*\)")
MD_LINK = re.compile(r"\[([^\]]*)\]\([^)]*\)")
KRAMDOWN_ATTR = re.compile(r"\{:[^}]*\}")
ALNUM = re.compile(r"[0-9A-Za-z]")
FM_KEY = re.compile(r"^(\w+):\s*(.*)$")
CONTENT_DIV = re.compile(r'<div class="content">(.*?)</div>\s*<div class="post-tail-wrapper', re.DOTALL)


def front_matter(text):
    parts = FM_SPLIT.split(text, maxsplit=2)
    if len(parts) < 3:
        return {}, text
    data, body = {}, parts[2]
    current = None
    for line in parts[1].splitlines():
        match = FM_KEY.match(line)
        if match:
            current, value = match.group(1), match.group(2).strip()
            data[current] = value
        elif current and line.strip().startswith("path:"):
            data[current] = line.split("path:", 1)[1].strip()
    return {k: v.strip("'\"") for k, v in data.items()}, body


def category(data):
    """Deepest category, e.g. 'Walkthrough' out of [Security, Walkthrough].

    The leaf is the specific one, and it is what the reader glancing at the card
    wants; the parent is already implied by the title.
    """
    listed = data.get("categories", "").strip("[]")
    if listed:
        return [part.strip().strip("'\"") for part in listed.split(",")][-1]
    return data.get("category")


def rendered_words(slug):
    """Word count of the built page, i.e. exactly what the theme counts.

    Only available once `jekyll build` has run; the Markdown estimate below is
    within a minute of it but can round the other way, so a build first keeps the
    card and the on-page byline identical.
    """
    for path in SITE_POSTS.glob("*/index.html"):
        if path.parent.name.lower() != slug:
            continue
        html = path.read_text(errors="ignore")
        match = CONTENT_DIV.search(html)
        return len(HTML_TAG.sub(" ", match.group(1) if match else html).split())
    return None


def estimated_words(body):
    text = LIQUID.sub(" ", body)
    text = CODE_FENCE.sub(" ", text)          # fence markers only; code text counts
    text = MD_IMAGE.sub(" ", text)            # images render as no text
    text = MD_LINK.sub(r"\1", text)           # links keep their label
    text = HTML_TAG.sub(" ", text)
    text = KRAMDOWN_ATTR.sub(" ", text)
    return len([w for w in text.split() if ALNUM.search(w)])


def read_time(body, slug):
    """Match the theme's read-time include: words / 180, minimum 1."""
    words = rendered_words(slug)
    if words is None:
        words = estimated_words(body)
        print(f"note: no build for '{slug}', estimating reading time from Markdown")
    return max(words // WPM, 1)


def post_date(data, path):
    raw = data.get("date", "")[:10] or path.name[:10]
    try:
        return date.fromisoformat(raw)
    except ValueError:
        return None


# --- drawing ----------------------------------------------------------------

def cover(img, size=SIZE):
    scale = max(size[0] / img.width, size[1] / img.height)
    resized = img.resize((round(img.width * scale), round(img.height * scale)), Image.LANCZOS)
    left = (resized.width - size[0]) // 2
    top = (resized.height - size[1]) // 2
    return resized.crop((left, top, left + size[0], top + size[1]))


def backdrop(header):
    """Header image, darkened enough that white text stays readable over it."""
    if header is None:
        return Image.new("RGB", SIZE, BG)

    with Image.open(header) as src:
        img = src.convert("RGB")
        # Always blurred: the headers carry their own titles, and a sharp one
        # behind the card text reads as two overlapping posters.
        blur = 14 if img.width >= MIN_COVER_WIDTH else 30
        canvas = cover(img).filter(ImageFilter.GaussianBlur(blur))

    canvas = Image.blend(canvas, Image.new("RGB", SIZE, BG), 0.68)

    # Extra shade at the bottom where the title and byline sit.
    scrim = Image.new("L", (1, SIZE[1]))
    for y in range(SIZE[1]):
        scrim.putpixel((0, y), int(225 * max(0.0, (y / SIZE[1] - 0.18) / 0.82) ** 1.3))
    shade = Image.new("RGB", SIZE, BG)
    return Image.composite(shade, canvas, scrim.resize(SIZE))


def wrap(draw, text, fnt, max_width):
    lines, line = [], ""
    for word in text.split():
        probe = f"{line} {word}".strip()
        if draw.textlength(probe, font=fnt) <= max_width or not line:
            line = probe
        else:
            lines.append(line)
            line = word
    if line:
        lines.append(line)
    return lines


def balance(draw, text, fnt, max_width):
    """Wrap into the same number of lines, but as evenly as possible.

    Greedy wrapping likes to leave one orphan word on the last line; narrowing
    the measure until the line count would grow spreads the words out instead.
    """
    target = len(wrap(draw, text, fnt, max_width))
    lo, hi = 1, max_width
    while lo < hi:
        mid = (lo + hi) // 2
        if len(wrap(draw, text, fnt, mid)) <= target:
            hi = mid
        else:
            lo = mid + 1
    return wrap(draw, text, fnt, lo)


def fit_title(draw, title, max_width, max_lines=4):
    for size in (66, 60, 54, 48, 42):
        fnt = font("black", size)
        lines = balance(draw, title, fnt, max_width)
        if len(lines) <= max_lines:
            return fnt, lines, size
    return fnt, lines[:max_lines], size


def circular(img, diameter):
    img = img.convert("RGB").resize((diameter, diameter), Image.LANCZOS)
    mask = Image.new("L", (diameter * 4, diameter * 4), 0)
    ImageDraw.Draw(mask).ellipse((0, 0, diameter * 4 - 1, diameter * 4 - 1), fill=255)
    img.putalpha(mask.resize((diameter, diameter), Image.LANCZOS))
    return img


def tracked(draw, xy, text, fnt, fill, tracking):
    x, y = xy
    for char in text:
        draw.text((x, y), char, font=fnt, fill=fill)
        x += draw.textlength(char, font=fnt) + tracking


def build_card(header, category, title, minutes, published):
    card = backdrop(header)
    draw = ImageDraw.Draw(card)
    draw.rectangle((0, 0, SIZE[0], 8), fill=ACCENT)

    max_width = SIZE[0] - 2 * PAD

    if category:
        tracked(draw, (PAD, 118), category.upper(), font("bold", 28), ACCENT, 3)

    title_font, lines, size = fit_title(draw, title, max_width)
    line_height = round(size * 1.22)
    y = 400 - line_height * (len(lines) - 1)
    for line in lines:
        draw.text((PAD, y), line, font=title_font, fill=(255, 255, 255))
        y += line_height

    byline = f"{minutes} min read"
    if published:
        byline += f"   ·   {published.strftime('%d %b %Y')}"
    draw.text((PAD, 492), byline, font=font("bold", 32), fill=MUTED)

    if AVATAR.is_file():
        with Image.open(AVATAR) as avatar:
            face = circular(avatar, 56)
        card.paste(face, (PAD, 528), face)
        draw.text((PAD + 76, 538), "ashishghimire.com", font=font("bold", 30), fill=ACCENT)

    return card


# --- driver -----------------------------------------------------------------

def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    seen = set()

    for path in sorted(POSTS.glob("*.md")):
        data, body = front_matter(path.read_text(encoding="utf-8"))
        title = data.get("title", path.stem)
        src = data.get("image", "")

        header = None
        if src.startswith("/"):
            candidate = ROOT / src.lstrip("/")
            if candidate.is_file() and candidate.suffix.lower() in SUFFIXES:
                header = candidate
            else:
                print(f"warning: {path.name} references missing image {src}")

        # Keyed by Jekyll's page.slug, so two posts sharing a header still get
        # their own card.
        slug = re.sub(r"^\d{4}-\d{2}-\d{2}-", "", path.stem).lower()
        if slug in seen:
            print(f"warning: duplicate slug '{slug}', card overwritten")
        seen.add(slug)

        minutes = read_time(body, slug)
        card = build_card(header, category(data), title, minutes,
                          post_date(data, path))
        target = OUT_DIR / f"{slug}.jpg"
        card.save(target, "JPEG", quality=QUALITY, optimize=True, progressive=True)
        print(f"{target.relative_to(ROOT)}  {minutes} min  {title[:48]}")


if __name__ == "__main__":
    main()
