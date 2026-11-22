"""Render the 21 November 2026 front page: a 1024x1024 newspaper infographic.

Everything is drawn in code with PIL. No network, no external assets.
Layout (own design): masthead, one lead story with a drawn badge, a
two-column story grid, a numbers box, an ALSO TODAY band, and a sources
footer.
"""

import math

from PIL import Image, ImageDraw, ImageFont

W = 1024
H = 1024
MARGIN = 36

PAPER = (246, 241, 230)
INK = (26, 26, 26)
NAVY = (22, 50, 79)
RED = (180, 35, 24)
GREY = (91, 91, 91)
LIGHT_GREY = (200, 192, 175)
WHITE = (255, 255, 255)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"


def _font(name, size):
    return ImageFont.truetype(f"{FONT_DIR}/{name}", size)


def serif_bold(size):
    return _font("DejaVuSerif-Bold.ttf", size)


def serif(size):
    return _font("DejaVuSerif.ttf", size)


def sans_bold(size):
    return _font("DejaVuSans-Bold.ttf", size)


def sans(size):
    return _font("DejaVuSans.ttf", size)


def wrap(draw, text, font, max_width):
    """Greedy word wrap; returns a list of lines that fit max_width."""
    lines = []
    for paragraph in text.split("\n"):
        words = paragraph.split()
        if not words:
            lines.append("")
            continue
        current = words[0]
        for word in words[1:]:
            trial = current + " " + word
            if draw.textlength(trial, font=font) <= max_width:
                current = trial
            else:
                lines.append(current)
                current = word
        lines.append(current)
    return lines


def text_block(draw, x, y, lines, font, fill, leading):
    """Draw lines starting at (x, y); return the y after the last line."""
    for line in lines:
        draw.text((x, y), line, font=font, fill=fill)
        y += leading
    return y


def rule(draw, x0, x1, y, fill, width=2):
    draw.line([(x0, y), (x1, y)], fill=fill, width=width)


def star_points(cx, cy, outer, inner, points=5, rotation=-90):
    pts = []
    for i in range(points * 2):
        r = outer if i % 2 == 0 else inner
        angle = math.radians(rotation + i * 180 / points)
        pts.append((cx + r * math.cos(angle), cy + r * math.sin(angle)))
    return pts


def story(draw, x, y, width, kicker, headline, body,
          headline_size=21, body_size=15):
    """One story: red kicker, bold headline, grey body. Returns end y."""
    draw.text((x, y), kicker, font=sans_bold(13), fill=RED)
    y += 22
    lines = wrap(draw, headline, serif_bold(headline_size), width)
    y = text_block(draw, x, y, lines, serif_bold(headline_size), INK,
                   headline_size + 6)
    y += 2
    lines = wrap(draw, body, sans(body_size), width)
    y = text_block(draw, x, y, lines, sans(body_size), GREY,
                   body_size + 5)
    return y


def render_page():
    img = Image.new("RGB", (W, H), PAPER)
    draw = ImageDraw.Draw(img)

    # Outer double border.
    draw.rectangle([14, 14, W - 15, H - 15], outline=INK, width=2)
    draw.rectangle([20, 20, W - 21, H - 21], outline=LIGHT_GREY, width=1)

    # ---- Masthead ----
    title = "THE WORLD IN ONE DAY"
    title_font = serif_bold(54)
    tw = draw.textlength(title, font=title_font)
    draw.text(((W - tw) / 2, 34), title, font=title_font, fill=NAVY)
    dateline = "SATURDAY, 21 NOVEMBER 2026  ·  SIX STORIES THAT DEFINED THE DAY"
    dl_font = sans(16)
    dw = draw.textlength(dateline, font=dl_font)
    draw.text(((W - dw) / 2, 108), dateline, font=dl_font, fill=GREY)
    rule(draw, MARGIN, W - MARGIN, 140, NAVY, width=3)

    # ---- Lead story ----
    y = 160
    draw.text((MARGIN, y), "TOP STORY  ·  MEXICO", font=sans_bold(15),
              fill=RED)
    y += 28
    y = text_block(draw, MARGIN, y,
                   ["Mexico captures", "\u201cEl Chapo Isidro\u201d"],
                   serif_bold(44), INK, 52)
    y += 8
    deck = ("FBI most-wanted kingpin seized in a Sinaloa raid "
            "backed by U.S. intelligence.")
    y = text_block(draw, MARGIN, y,
                   wrap(draw, deck, serif(20), 640), serif(20), INK, 27)
    y += 6
    body = ("Fausto Isidro Meza Flores was taken in Guasave late on "
            "20 November and the arrest was announced on 21 November. "
            "Four soldiers and seven gunmen were killed in the operation.")
    y = text_block(draw, MARGIN, y,
                   wrap(draw, body, sans(16), 640), sans(16), GREY, 22)

    # Drawn badge on the right of the lead story.
    cx, cy, r = 862, 292, 92
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=RED,
                 outline=NAVY, width=4)
    draw.ellipse([cx - r + 14, cy - r + 14, cx + r - 14, cy + r - 14],
                 outline=WHITE, width=2)
    draw.polygon(star_points(cx, cy - 26, 40, 17), fill=WHITE)
    badge_font = sans_bold(15)
    for i, word in enumerate(["FBI TOP 10", "MOST WANTED"]):
        ww = draw.textlength(word, font=badge_font)
        draw.text((cx - ww / 2, cy + 24 + i * 22), word, font=badge_font,
                  fill=WHITE)

    rule(draw, MARGIN, W - MARGIN, 436, INK, width=2)

    # ---- Middle grid ----
    left_x = MARGIN
    right_x = 526
    col_w = 462
    mid_y = 456

    y = mid_y
    y = story(
        draw, left_x, y, col_w,
        "CLIMATE  ·  COP31",
        "Climate talks run into overtime with no deal",
        "Negotiators in Bel\u00e9m stayed past the deadline as a draft "
        "text dropped all mention of fossil fuels.")
    y += 12
    y = story(
        draw, left_x, y, col_w,
        "UKRAINE  ·  KRYVYI RIH",
        "Missile strike hits Zelenskyy\u2019s home city",
        "Two people were killed and 60 injured in a Russian strike; "
        "a second missile hit rescue workers.")
    y += 12
    y = story(
        draw, left_x, y, col_w,
        "BALTIC SEA",
        "Russian freighter ablaze after drone attack",
        "Sparta II caught fire and drifted toward Finnish waters; "
        "all 16 crew members were evacuated.")
    assert y <= 836, f"left column overflow: {y}"

    y = mid_y
    y = story(
        draw, right_x, y, col_w,
        "PERU",
        "Magnitude 6.7 quake shakes Jun\u00edn",
        "The tremor struck north of Jun\u00edn. No deaths and no "
        "serious damage were reported.")
    y += 12
    y = story(
        draw, right_x, y, col_w,
        "UKRAINE  ·  DIPLOMACY",
        "Zelenskyy: Trump told Europe it spends too much",
        "Ukraine\u2019s president said the U.S. president pressed "
        "European leaders over their Ukraine spending.")
    assert y <= 700, f"right column overflow: {y}"

    # Numbers box.
    box_y0, box_y1 = 700, 836
    draw.rectangle([right_x, box_y0, W - MARGIN, box_y1], fill=NAVY)
    draw.text((right_x + 16, box_y0 + 12), "THE DAY IN NUMBERS",
              font=sans_bold(15), fill=WHITE)
    numbers = [
        ("6.7", "magnitude of the Peru earthquake"),
        ("2 killed \u00b7 60 injured", "Kryvyi Rih strike"),
        ("16", "crew evacuated from Sparta II"),
        ("11 dead \u00b7 180+ in hospital", "India hooch tragedy"),
    ]
    ny = box_y0 + 40
    for big, small in numbers:
        draw.text((right_x + 16, ny), big, font=sans_bold(14), fill=WHITE)
        bw = draw.textlength(big, font=sans_bold(14))
        draw.text((right_x + 16 + bw + 8, ny), "\u2014 " + small,
                  font=sans(14), fill=(200, 210, 225))
        ny += 23

    # ---- ALSO TODAY band ----
    band_y0, band_y1 = 856, 962
    draw.rectangle([MARGIN, band_y0, W - MARGIN, band_y1], fill=INK)
    draw.text((MARGIN + 16, band_y0 + 10), "ALSO TODAY",
              font=sans_bold(15), fill=(255, 200, 90))
    also = [
        ("INDIA", "At least 11 dead and 180 hospitalised after "
         "drinking tainted liquor in Manipur."),
        ("BRUSSELS", "EU approves a further \u20ac1bn in military aid "
         "for Ukraine."),
        ("HORMUZ", "Two oil tankers attacked near the Strait of "
         "Hormuz."),
    ]
    col_w3 = 292
    for i, (place, text) in enumerate(also):
        ax = MARGIN + 16 + i * (col_w3 + 12)
        lines = wrap(draw, text, sans(14), col_w3)
        yy = band_y0 + 36
        draw.text((ax, yy), place, font=sans_bold(13),
                  fill=(255, 200, 90))
        text_block(draw, ax, yy + 20, lines, sans(14), WHITE, 19)

    # ---- Footer ----
    footer = ("Sources: Reuters \u00b7 AP \u00b7 CNN \u00b7 WSJ \u00b7 USGS \u00b7 "
              "EU Council \u00b7 UKMTO  —  Image drawn entirely in code.")
    ff = sans(13)
    fw = draw.textlength(footer, font=ff)
    draw.text(((W - fw) / 2, 978), footer, font=ff, fill=GREY)

    return img
