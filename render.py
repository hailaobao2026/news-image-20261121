#!/usr/bin/env python3
"""Draw the front page for Saturday 21 November 2026 (1024x1024 PNG).

Written from scratch in this session with Pillow + DejaVu fonts.
Every fact on the page was checked against at least two independent
sources on 2026-11-22; see build-log.md for the source list.
"""
import hashlib
import os

from PIL import Image, ImageDraw, ImageFont

CANVAS = (1024, 1024)
EDGE = 36
INNER = CANVAS[0] - 2 * EDGE

PAPER = (248, 244, 235)
INK = (24, 24, 24)
BODY = (60, 58, 52)
NAVY = (20, 34, 58)
GOLD = (203, 164, 40)
CRIMSON = (178, 38, 30)
RULE = (182, 174, 157)
GREY = (92, 88, 78)

FONTS = "/usr/share/fonts/truetype/dejavu"


def load(name, size):
    return ImageFont.truetype(os.path.join(FONTS, name), size)


MASTHEAD = load("DejaVuSans-Bold.ttf", 50)
DATE = load("DejaVuSans-Bold.ttf", 32)
TAGLINE = load("DejaVuSans.ttf", 19)
KICKER = load("DejaVuSans-Bold.ttf", 20)
HEADLINE = load("DejaVuSans-Bold.ttf", 40)
DECK = load("DejaVuSans.ttf", 21)
LABEL = load("DejaVuSans-Bold.ttf", 17)
TITLE = load("DejaVuSans-Bold.ttf", 26)
TEXT = load("DejaVuSans.ttf", 19)
TITLE_S = load("DejaVuSans-Bold.ttf", 23)
TEXT_S = load("DejaVuSans.ttf", 17)
ALSO_H = load("DejaVuSans-Bold.ttf", 20)
ALSO_T = load("DejaVuSans-Bold.ttf", 18)
ALSO_D = load("DejaVuSans.ttf", 16)
FOOT = load("DejaVuSans.ttf", 14)


def wrap(text, fnt, width):
    out, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if fnt.getlength(trial) <= width:
            cur = trial
        else:
            if cur:
                out.append(cur)
            cur = word
    if cur:
        out.append(cur)
    return out


def para(draw, x, y, lines, fnt, fill, step):
    for ln in lines:
        draw.text((x, y), ln, font=fnt, fill=fill)
        y += step
    return y


canvas = Image.new("RGB", CANVAS, PAPER)
d = ImageDraw.Draw(canvas)

# ---- masthead ------------------------------------------------------------
d.rectangle([0, 0, CANVAS[0], 146], fill=NAVY)
d.text((CANVAS[0] // 2, 20), "THE WORLD IN ONE DAY", font=MASTHEAD,
       fill=(255, 255, 255), anchor="ma")
d.line([EDGE, 90, CANVAS[0] - EDGE, 90], fill=GOLD, width=2)
d.text((CANVAS[0] // 2, 100), "SATURDAY, 21 NOVEMBER 2026", font=DATE,
       fill=GOLD, anchor="ma")
d.text((CANVAS[0] // 2, 152), "The day's world news \u2014 in one picture",
       font=TAGLINE, fill=GREY, anchor="ma")

y = 186

# ---- lead story: Mexico --------------------------------------------------
d.text((EDGE, y), "MEXICO  \u00b7  CARTEL CAPTURE", font=KICKER, fill=CRIMSON)
y += 27
lead = "Mexico captures \u201cEl Chapo Isidro\u201d"
lead_lines = wrap(lead, HEADLINE, INNER)
assert len(lead_lines) == 1, lead_lines
y = para(d, EDGE, y, lead_lines, HEADLINE, INK, 48)
lead_deck = ("Mexican special forces seized Fausto Isidro Meza Flores, one "
             "of the FBI's 10 most wanted fugitives, in Sinaloa on Friday "
             "night with US intelligence help. Four soldiers and seven "
             "gunmen were killed in the operation.")
y = para(d, EDGE, y + 5,
         wrap(lead_deck, DECK, INNER), DECK, BODY, 27)
y += 10
d.line([EDGE, y, CANVAS[0] - EDGE, y], fill=RULE, width=2)
y += 16


def card(x, w, label, colour, title, body, tfnt, bfnt, tstep, bstep):
    """One story block; returns the y just below it."""
    top = y
    d.text((x, top), label, font=LABEL, fill=colour)
    ty = para(d, x, top + 24, wrap(title, tfnt, w), tfnt, INK, tstep)
    by = para(d, x, ty + 5, wrap(body, bfnt, w), bfnt, BODY, bstep)
    return by


# ---- middle row: two stories --------------------------------------------
half = (INNER - 28) // 2
row_top = y
end1 = card(EDGE, half, "CLIMATE  \u00b7  COP31", (18, 120, 58),
            "COP31 talks run into overtime with no deal in sight",
            "Negotiators in Antalya worked past Friday's deadline with "
            "the draft deal silent on fossil fuels. The EU: \u201ca good "
            "deal or no deal\u201d.",
            TITLE, TEXT, 30, 24)
end2 = card(EDGE + half + 28, half, "WAR IN UKRAINE", (14, 112, 104),
            "Russian strike kills 2 in Zelenskyy's hometown",
            "A double-tap missile attack on Kryvyi Rih killed a "
            "7-year-old boy and a 20-year-old paramedic and wounded 60, "
            "hours after a huge barrage on Kyiv.",
            TITLE, TEXT, 30, 24)
y = max(end1, end2) + 12
d.line([EDGE, y, CANVAS[0] - EDGE, y], fill=RULE, width=1)
y += 12

# ---- lower row: three stories -------------------------------------------
third = (INNER - 2 * 24) // 3
ends = []
ends.append(card(EDGE, third, "BALTIC SEA", (26, 74, 204),
                 "Russian ship ablaze after drone strike",
                 "The sanctioned cargo ship Sparta II caught fire in the "
                 "Gulf of Finland and drifted into Finnish waters. Its "
                 "16 crew were evacuated.",
                 TITLE_S, TEXT_S, 26, 21))
ends.append(card(EDGE + third + 24, third, "PERU", (176, 84, 8),
                 "Magnitude 6.7 quake shakes the Andes",
                 "The tremor struck near Jun\u00edn on Friday evening and "
                 "was felt in Lima. No deaths or serious damage were "
                 "reported.",
                 TITLE_S, TEXT_S, 27, 22))
ends.append(card(EDGE + 2 * (third + 24), third, "DIPLOMACY", (108, 40, 214),
                 "Trump told Europe it spends too much, Zelensky says",
                 "Zelensky said on Saturday that Trump, after his summit "
                 "with Putin and Xi, told European leaders they could "
                 "spend the money at home if peace is reached.",
                 TITLE_S, TEXT_S, 26, 21))
y = max(ends) + 12
d.line([EDGE, y, CANVAS[0] - EDGE, y], fill=RULE, width=2)
y += 12

# ---- also today -----------------------------------------------------------
d.text((EDGE, y), "ALSO TODAY", font=ALSO_H, fill=CRIMSON)
y += 27
also = [
    ("Tainted liquor kills at least 11 in India",
     "More than 180 people were hospitalised in Manipur after drinking "
     "suspected adulterated alcohol."),
    ("EU approves \u20ac1bn more military aid for Ukraine",
     "The package will fund drones, air defence and ammunition, to be "
     "delivered by the end of 2027."),
    ("Two tankers hit near the Strait of Hormuz",
     "The vessels were struck by projectiles on Saturday, the UK "
     "maritime trade office said, as tensions over Iran rise."),
]
bottom = y
for i, (head, deck) in enumerate(also):
    x = EDGE + i * (third + 24)
    ny = para(d, x, y, wrap(head, ALSO_T, third), ALSO_T, INK, 23)
    ny = para(d, x, ny + 4, wrap(deck, ALSO_D, third), ALSO_D, BODY, 20)
    bottom = max(bottom, ny)
y = bottom + 12
d.line([EDGE, y, CANVAS[0] - EDGE, y], fill=RULE, width=1)
y += 8
d.text((CANVAS[0] // 2, y),
       "Sources: Reuters \u00b7 AP \u00b7 CNN \u00b7 USGS \u00b7 EU Council  "
       "\u2014  21 November 2026",
       font=FOOT, fill=GREY, anchor="ma")

assert y + 20 <= CANVAS[1], f"layout overflow: footer ends at {y + 20}"

here = os.path.dirname(os.path.abspath(__file__))
assets = os.path.join(here, "assets")
os.makedirs(assets, exist_ok=True)
path = os.path.join(assets, "entry.png")
canvas.save(path, "PNG", optimize=True)

blob = open(path, "rb").read()
print(f"wrote {path}")
print(f"size: {canvas.size}, bytes: {len(blob)} "
      f"(limit 1048576: {'OK' if len(blob) <= 1048576 else 'OVER'})")
print(f"sha256: {hashlib.sha256(blob).hexdigest()}")
print(f"footer bottom: {y + 20} / {CANVAS[1]}")
