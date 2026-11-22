"""Render the 22 November 2026 one-page world news sheet to entry.png.

The sheet is a 1024x1024 square: masthead with the date in red, one
wide lead panel, a two-panel row, a wide politics panel, an ALSO TODAY
grid and a sources footer. Drawn with PIL primitives only, so the
output is byte-for-byte reproducible.
"""

from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

W = H = 1024
M = 48
CW = W - 2 * M
PAPER = (250, 247, 240)
INK = (24, 24, 28)
RED = (178, 30, 38)
GREY = (96, 96, 102)
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


def panel(draw, x, y, w, h, kicker, headline, body, head_size, body_size):
    draw.rectangle([x, y, x + w, y + h], fill=PANEL, outline=INK, width=2)
    draw.rectangle([x, y, x + w, y + 30], fill=INK)
    draw.text((x + 13, y + 6), kicker, font=font(SANS_B, 17), fill=(250, 247, 240))
    ty = y + 44
    for line in wrap(draw, headline, font(SERIF_B, head_size), w - 30):
        draw.text((x + 15, ty), line, font=font(SERIF_B, head_size), fill=INK)
        ty += head_size + 7
    ty += 4
    for line in wrap(draw, body, font(SERIF, body_size), w - 30):
        draw.text((x + 15, ty), line, font=font(SERIF, body_size), fill=(52, 52, 58))
        ty += body_size + 6


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # Masthead
    d.text((M, 28), "THE WORLD IN ONE PAGE", font=font(SERIF_B, 57), fill=INK)
    d.line([M, 108, W - M, 108], fill=INK, width=4)
    d.line([M, 118, W - M, 118], fill=INK, width=2)
    d.text((M, 130), "SUNDAY, NOVEMBER 22, 2026", font=font(SANS_B, 32), fill=RED)
    d.text((M + 2, 172), "The day's world news, on a single sheet", font=font(SERIF, 20), fill=GREY)
    d.line([M, 202, W - M, 202], fill=INK, width=2)

    # Lead panel
    panel(
        d, M, 218, CW, 208, "BRAZIL · LEAD STORY",
        "'We lost everything': town clears rubble after deadly storm",
        "Residents of a Brazilian town picked through the wreckage of their "
        "homes after a deadly storm tore through the region, leaving families "
        "with nothing and rescue crews clearing rubble street by street.",
        head_size=31, body_size=20,
    )

    # Two-panel row
    panel(
        d, M, 442, 454, 296, "TECHNOLOGY · UNITED STATES",
        "Nvidia faces US accounting probe amid deepening turmoil",
        "The chipmaker at the centre of the AI boom is reported to face a US "
        "accounting probe, adding regulatory pressure to a company whose "
        "results now move whole markets.",
        head_size=27, body_size=19,
    )
    panel(
        d, M + 474, 442, 454, 296, "MIDDLE EAST",
        "Iran strikes three tankers as it shows off missile launchers",
        "Iran struck three tankers and paraded missile launchers in a show "
        "of force, as Houthi forces launched revenge strikes on the Saudi "
        "capital and regional tensions kept climbing.",
        head_size=27, body_size=19,
    )

    # Wide panel
    panel(
        d, M, 754, CW, 128, "UNITED STATES · POLITICS",
        "Trump vows to work with Democrats to cap credit card interest at 10%",
        "",
        head_size=27, body_size=19,
    )

    # Also today, two by two
    y = 898
    d.rectangle([M, y, W - M, y + 28], fill=RED)
    d.text((M + 14, y + 5), "ALSO TODAY", font=font(SANS_B, 17), fill=(255, 255, 255))
    items = [
        "6.7 quake hits Peru; no deaths reported",
        "Rohingyas hail genocide verdict on Myanmar",
        "Pentagon restricts US-Canada defence ties",
        "COP31 deadlocked over fossil fuels",
    ]
    for i, it in enumerate(items):
        cx = M + 14 + (i % 2) * 474
        cy = y + 40 + (i // 2) * 26
        d.ellipse([cx, cy + 7, cx + 8, cy + 15], fill=RED)
        d.text((cx + 18, cy), it, font=font(SANS, 16), fill=INK)

    d.line([M, H - 30, W - M, H - 30], fill=INK, width=2)
    d.text((M, H - 24),
           "Compiled from wire and newspaper headlines of 22 November 2026 (AFP, AP, Reuters).",
           font=font(SANS, 15), fill=GREY)

    out = Path(__file__).with_name("entry.png")
    img.save(out, optimize=True)
    print("wrote", out, out.stat().st_size, "bytes, size", img.size)


if __name__ == "__main__":
    main()
