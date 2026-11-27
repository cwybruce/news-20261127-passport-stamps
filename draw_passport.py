#!/usr/bin/env python3
"""Build-time renderer for the passport-stamps news image.

Draws entry.png (1024x1024) for make.fun news-image-20261127:
Friday 27 November 2026 world news as six passport visa stamps.

Run at BUILD time only, on this machine. Never imported by main.py:
the grader image has no PIL and no fonts, so main.py is a pure
stdlib copier of the pre-rendered entry.png this script produces.
"""

import math
import random
import textwrap

from PIL import Image, ImageDraw, ImageFont

W = H = 1024
OUT = "entry.png"

FONT_DIR = "/usr/share/fonts/truetype/dejavu/"
BOLD = FONT_DIR + "DejaVuSans-Bold.ttf"
REG = FONT_DIR + "DejaVuSans.ttf"

PAPER = (243, 233, 210)      # warm passport-page paper
PAPER_DARK = (232, 219, 190)
CARD = (250, 244, 228)
NAVY = (28, 42, 68)          # header band
NAVY_SOFT = (52, 68, 100)
INK = (32, 32, 36)           # headline text
GOLD = (176, 141, 60)

# One ink colour per stamp, so each country reads as a different stamp.
STAMPS = [
    {
        "country": "UNITED STATES",
        "icon": "balloon",
        "ink": (27, 68, 128),
        "headline": "100th Macy's parade postponed by storm - a first in its history",
    },
    {
        "country": "EGYPT",
        "icon": "flame",
        "ink": (150, 32, 32),
        "headline": "Tanker fire on Cairo ring road kills 31; driver arrested",
    },
    {
        "country": "UKRAINE",
        "icon": "bolt",
        "ink": (18, 92, 120),
        "headline": "Zelensky: Russia readying mass strike on power grid",
    },
    {
        "country": "UNITED KINGDOM",
        "icon": "star",
        "ink": (74, 52, 110),
        "headline": "UK writes to 100,000 reservists: be ready for call-up",
    },
    {
        "country": "SPAIN",
        "icon": "ship",
        "ink": (16, 96, 74),
        "headline": "Diesel tanker capsizes off Ibiza; 1 crew dead, spill feared",
    },
    {
        "country": "DR CONGO",
        "icon": "cross",
        "ink": (168, 84, 16),
        "headline": "Ebola passes 12,000 cases as fighting forces medics out",
    },
]


def font(path, size):
    return ImageFont.truetype(path, size)


def draw_balloon(d, cx, cy, s, ink):
    """Parade balloon: round envelope, basket, strings."""
    d.ellipse([cx - s, cy - s, cx + s, cy + s * 0.85], outline=ink, width=4)
    d.arc([cx - s, cy - s, cx + s, cy + s * 0.85], 20, 160, fill=ink, width=4)
    d.line([cx - s * 0.55, cy + s * 0.7, cx - s * 0.3, cy + s * 1.35], fill=ink, width=3)
    d.line([cx + s * 0.55, cy + s * 0.7, cx + s * 0.3, cy + s * 1.35], fill=ink, width=3)
    d.line([cx, cy + s * 0.85, cx, cy + s * 1.35], fill=ink, width=3)
    d.rectangle([cx - s * 0.32, cy + s * 1.35, cx + s * 0.32, cy + s * 1.7],
                outline=ink, width=3)


def draw_flame(d, cx, cy, s, ink):
    """Stylised flame."""
    pts = [
        (cx, cy - s * 1.6),
        (cx + s * 0.55, cy - s * 0.7),
        (cx + s * 0.95, cy + s * 0.1),
        (cx + s * 0.7, cy + s * 0.9),
        (cx + s * 0.2, cy + s * 1.25),
        (cx - s * 0.35, cy + s * 1.25),
        (cx - s * 0.85, cy + s * 0.7),
        (cx - s * 0.8, cy - s * 0.2),
        (cx - s * 0.35, cy - s * 0.9),
    ]
    d.polygon(pts, outline=ink, width=4)
    d.polygon([
        (cx, cy - s * 0.4), (cx + s * 0.35, cy + s * 0.3),
        (cx, cy + s * 0.95), (cx - s * 0.35, cy + s * 0.3),
    ], fill=ink)


def draw_bolt(d, cx, cy, s, ink):
    """Lightning bolt."""
    d.polygon([
        (cx + s * 0.25, cy - s * 1.6), (cx - s * 0.75, cy + s * 0.25),
        (cx - s * 0.05, cy + s * 0.25), (cx - s * 0.3, cy + s * 1.6),
        (cx + s * 0.8, cy - s * 0.15), (cx + s * 0.05, cy - s * 0.15),
    ], fill=ink)


def draw_star(d, cx, cy, s, ink):
    """Five-pointed star."""
    pts = []
    for i in range(10):
        r = s * 1.5 if i % 2 == 0 else s * 0.62
        a = -math.pi / 2 + i * math.pi / 5
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    d.polygon(pts, outline=ink, width=4)


def draw_ship(d, cx, cy, s, ink):
    """Capsized tanker: tilted hull above waves."""
    d.polygon([
        (cx - s * 1.5, cy - s * 0.4), (cx + s * 1.5, cy - s * 0.9),
        (cx + s * 1.1, cy + s * 0.35), (cx - s * 1.1, cy + s * 0.7),
    ], outline=ink, width=4)
    d.line([cx - s * 0.9, cy - s * 0.55, cx - s * 0.5, cy - s * 1.15], fill=ink, width=4)
    d.line([cx + s * 0.5, cy - s * 0.75, cx + s * 0.9, cy - s * 1.3], fill=ink, width=4)
    for k, yy in enumerate((cy + s * 0.85, cy + s * 1.15)):
        d.arc([cx - s * 1.6, yy - s * 0.3, cx - s * 0.2, yy + s * 0.3],
              200, 340, fill=ink, width=3)
        d.arc([cx - s * 0.1, yy - s * 0.35, cx + s * 1.3, yy + s * 0.35],
              200, 340, fill=ink, width=3)
        d.arc([cx + s * 0.9, yy - s * 0.35, cx + s * 1.7, yy + s * 0.35],
              200, 340, fill=ink, width=3)


def draw_cross(d, cx, cy, s, ink):
    """Medical cross."""
    d.rectangle([cx - s * 0.32, cy - s * 1.4, cx + s * 0.32, cy + s * 1.4], fill=ink)
    d.rectangle([cx - s * 1.4, cy - s * 0.32, cx + s * 1.4, cy + s * 0.32], fill=ink)


ICONS = {
    "balloon": draw_balloon,
    "flame": draw_flame,
    "bolt": draw_bolt,
    "star": draw_star,
    "ship": draw_ship,
    "cross": draw_cross,
}


def wrap_headline(text, fnt, max_w, draw):
    """Greedy wrap to at most 3 lines; shrink font if it still overflows."""
    size = fnt.size
    while size >= 24:
        f = font(BOLD, size)
        lines = []
        for raw in text.split("\n"):
            words = raw.split()
            cur = ""
            for w in words:
                trial = (cur + " " + w).strip()
                if draw.textlength(trial, font=f) <= max_w or not cur:
                    cur = trial
                else:
                    lines.append(cur)
                    cur = w
            if cur:
                lines.append(cur)
        if len(lines) <= 3:
            return lines, f
        size -= 2
    return lines[:3], font(BOLD, 24)


def draw_stamp(base, box, stamp, angle):
    """Draw one rotated ink stamp (rounded double border + icon +
    country + date) onto the base image, centred in box."""
    x0, y0, x1, y1 = box
    w, h = x1 - x0, y1 - y0
    ink = stamp["ink"]
    layer = Image.new("RGBA", (w + 40, h + 40), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    cx, cy = layer.width // 2, layer.height // 2
    sw, sh = w - 16, h - 16
    # Double rounded border, the classic visa-stamp look.
    d.rounded_rectangle([cx - sw // 2, cy - sh // 2, cx + sw // 2, cy + sh // 2],
                        radius=18, outline=ink + (255,), width=5)
    d.rounded_rectangle([cx - sw // 2 + 9, cy - sh // 2 + 9,
                         cx + sw // 2 - 9, cy + sh // 2 - 9],
                        radius=13, outline=ink + (255,), width=2)
    # Icon at the top of the stamp, in its own zone.
    ICONS[stamp["icon"]](d, cx, cy - sh // 2 + 22, 13, ink)
    # Country name, fitted to the stamp width.
    size = 30
    while size > 20:
        f = font(BOLD, size)
        if d.textlength(stamp["country"], font=f) <= sw - 30:
            break
        size -= 2
    d.text((cx, cy + 2), stamp["country"], font=f, fill=ink + (255,),
           anchor="mm")
    # Date line.
    f_date = font(BOLD, 22)
    d.text((cx, cy + sh // 2 - 20), "27 NOV 2026", font=f_date,
           fill=ink + (255,), anchor="mm")
    rotated = layer.rotate(angle, resample=Image.BICUBIC, expand=False)
    base.alpha_composite(rotated, (x0 - 20, y0 - 20))


def main():
    rng = random.Random(20261127)
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # Paper grain: faint speckles so the page reads as paper, not flat.
    for _ in range(2600):
        x, y = rng.randrange(W), rng.randrange(H)
        shade = rng.choice([PAPER_DARK, (247, 240, 224)])
        d.point((x, y), fill=shade)

    # ---- Header band -------------------------------------------------
    d.rectangle([0, 0, W, 140], fill=NAVY)
    d.rectangle([0, 140, W, 146], fill=GOLD)
    # Small globe mark at the left of the header.
    gx, gy, gr = 62, 70, 34
    d.ellipse([gx - gr, gy - gr, gx + gr, gy + gr], outline=(240, 220, 160), width=4)
    d.ellipse([gx - gr // 2, gy - gr, gx + gr // 2, gy + gr], outline=(240, 220, 160), width=3)
    d.line([gx - gr, gy, gx + gr, gy], fill=(240, 220, 160), width=3)
    d.arc([gx - gr, gy - gr // 2, gx + gr, gy + gr // 2], 200, 340,
          fill=(240, 220, 160), width=3)
    d.arc([gx - gr, gy - gr // 2, gx + gr, gy + gr // 2], 20, 160,
          fill=(240, 220, 160), width=3)
    f_title = font(BOLD, 52)
    d.text((118, 46), "WORLD NEWS PASSPORT", font=f_title,
           fill=(248, 244, 232))
    f_sub = font(BOLD, 30)
    d.text((120, 102), "FRIDAY  27  NOVEMBER  2026", font=f_sub,
           fill=(224, 196, 120))

    # ---- Six stamp cells: 2 columns x 3 rows -------------------------
    margin, gap = 26, 14
    cell_w = (W - 2 * margin - gap) // 2
    cell_h = 252
    top = 160
    angles = [-2.5, 2.0, 1.5, -2.0, 2.5, -1.5]
    base = img.convert("RGBA")
    for i, stamp in enumerate(STAMPS):
        col, row = i % 2, i // 2
        x0 = margin + col * (cell_w + gap)
        y0 = top + row * (cell_h + gap)
        x1, y1 = x0 + cell_w, y0 + cell_h
        # Card with a soft edge and a stitched border.
        d_card = ImageDraw.Draw(base)
        d_card.rounded_rectangle([x0, y0, x1, y1], radius=14, fill=CARD + (255,),
                                 outline=(196, 178, 140, 255), width=2)
        # Stamp at the top of the card.
        stamp_h = 128
        draw_stamp(base, (x0 + 66, y0 + 12, x1 - 66, y0 + 12 + stamp_h),
                   stamp, angles[i])
        # Headline beneath the stamp.
        d2 = ImageDraw.Draw(base)
        lines, f_head = wrap_headline(stamp["headline"], font(BOLD, 28),
                                      cell_w - 44, d2)
        ly = y0 + 12 + stamp_h + 10
        for line in lines:
            d2.text((x0 + cell_w // 2, ly), line, font=f_head,
                    fill=INK + (255,), anchor="ma")
            ly += f_head.size + 4

    img = base.convert("RGB")
    d = ImageDraw.Draw(img)

    # ---- Footer -------------------------------------------------------
    d.line([40, 958, W - 40, 958], fill=(176, 141, 60), width=3)
    f_foot = font(BOLD, 34)
    d.text((W // 2, 978), "SIX STAMPS, ONE DAY", font=f_foot,
           fill=NAVY, anchor="ma")

    img.save(OUT, "PNG", optimize=True)
    print(f"wrote {OUT}: {img.size[0]}x{img.size[1]}")


if __name__ == "__main__":
    main()
