"""Render the 22 November 2026 one-page world news sheet to entry.png.

Layout, top to bottom: masthead with the date in red, one wide lead
panel, a two-panel row, one more wide panel, an ALSO TODAY strip and a
sources footer. Everything is drawn with PIL primitives so the output
is byte-for-byte reproducible.
"""

from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

W, H = 1200, 1500
PAPER = (250, 247, 240)
INK = (24, 24, 28)
RED = (178, 30, 38)
GREY = (96, 96, 102)
RULE = (24, 24, 28)
PANEL = (255, 254, 250)

F = "/usr/share/fonts/truetype/dejavu"
SERIF_B = f"{F}/DejaVuSerif-Bold.ttf"
SERIF = f"{F}/DejaVuSerif.ttf"
SANS_B = f"{F}/DejaVuSans-Bold.ttf"
SANS = f"{F}/DejaVuSans.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, width):
    words, lines, cur = text.split(), [], ""
    for w in words:
        trial = f"{cur} {w}".strip()
        if draw.textlength(trial, font=fnt) <= width:
            cur = trial
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def panel(draw, x, y, w, h, kicker, headline, body, head_size=40, body_size=24):
    draw.rectangle([x, y, x + w, y + h], fill=PANEL, outline=RULE, width=2)
    draw.rectangle([x, y, x + w, y + 34], fill=INK)
    draw.text((x + 16, y + 7), kicker, font=font(SANS_B, 20), fill=(250, 247, 240))
    ty = y + 52
    for line in wrap(draw, headline, font(SERIF_B, head_size), w - 36):
        draw.text((x + 18, ty), line, font=font(SERIF_B, head_size), fill=INK)
        ty += head_size + 8
    ty += 6
    for line in wrap(draw, body, font(SERIF, body_size), w - 36):
        draw.text((x + 18, ty), line, font=font(SERIF, body_size), fill=(52, 52, 58))
        ty += body_size + 7


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # Masthead
    d.text((60, 42), "THE WORLD IN ONE PAGE", font=font(SERIF_B, 74), fill=INK)
    d.line([60, 140, W - 60, 140], fill=RULE, width=5)
    d.line([60, 152, W - 60, 152], fill=RULE, width=2)
    d.text((60, 168), "SUNDAY, NOVEMBER 22, 2026", font=font(SANS_B, 40), fill=RED)
    d.text((62, 224), "The day's world news, on a single sheet", font=font(SERIF, 25), fill=GREY)
    d.line([60, 262, W - 60, 262], fill=RULE, width=2)

    # Lead panel
    panel(
        d, 60, 282, W - 120, 270, "BRAZIL · LEAD STORY",
        "'We lost everything': town clears rubble after deadly storm",
        "Residents of a Brazilian town picked through the wreckage of their "
        "homes after a deadly storm tore through the region, leaving families "
        "with nothing and rescue crews clearing rubble street by street.",
    )

    # Two-panel row
    panel(
        d, 60, 572, 530, 380, "TECHNOLOGY · UNITED STATES",
        "Nvidia faces US accounting probe amid deepening turmoil",
        "The chipmaker at the centre of the AI boom is reported to face a US "
        "accounting probe, adding regulatory pressure to a company whose "
        "results now move whole markets.",
        head_size=34, body_size=22,
    )
    panel(
        d, 610, 572, 530, 380, "MIDDLE EAST",
        "Iran strikes three tankers as it shows off missile launchers",
        "Iran struck three tankers and paraded missile launchers in a show "
        "of force, as Houthi forces launched revenge strikes on the Saudi "
        "capital and regional tensions kept climbing.",
        head_size=34, body_size=22,
    )

    # Wide panel
    panel(
        d, 60, 972, W - 120, 250, "UNITED STATES · POLITICS",
        "Trump vows to work with Democrats to cap credit card interest at 10%",
        "President Trump pledged to work with Democrats on capping credit "
        "card interest rates at 10 percent, a cross-party promise aimed at "
        "households squeezed by the cost of borrowing.",
        head_size=36,
    )

    # Also today
    y = 1242
    d.rectangle([60, y, W - 60, y + 36], fill=RED)
    d.text((76, y + 7), "ALSO TODAY", font=font(SANS_B, 21), fill=(255, 255, 255))
    items = [
        "Magnitude 6.7 earthquake hits Peru; no deaths reported",
        "Rohingyas hail genocide verdict against Myanmar",
        "Pentagon moves to restrict US-Canada defence ties",
        "South Korea's Lee: speed is decisive in the AI race",
        "COP31 climate summit deadlocked over fossil fuels",
    ]
    ty = y + 46
    for it in items:
        d.ellipse([76, ty + 9, 86, ty + 19], fill=RED)
        d.text((100, ty), it, font=font(SANS, 25), fill=INK)
        ty += 29

    d.line([60, H - 58, W - 60, H - 58], fill=RULE, width=2)
    d.text((60, H - 46),
           "Compiled from wire and newspaper headlines of 22 November 2026 (AFP, AP, Reuters).",
           font=font(SANS, 19), fill=GREY)

    out = Path(__file__).with_name("entry.png")
    img.save(out, optimize=True)
    print("wrote", out, out.stat().st_size, "bytes")


if __name__ == "__main__":
    main()
