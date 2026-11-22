"""One-page world news sheet for Sunday 22 November 2026.

Draws a 1024x1024 newspaper front page with PIL: a masthead, a wide
lead panel, two half-width panels, one wide headline panel, an ALSO
TODAY grid and a footer. Pure drawing calls, no external assets, so
re-running produces the identical PNG.
"""

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

SIZE = 1024
MARGIN = 48
WIDTH = SIZE - 2 * MARGIN

PAPER = (250, 247, 240)
INK = (26, 26, 30)
BODY_INK = (54, 54, 60)
RED = (178, 30, 38)
GREY = (100, 100, 106)
PANEL_BG = (255, 254, 250)

FONTS = "/usr/share/fonts/truetype/dejavu"
SERIF_BOLD = f"{FONTS}/DejaVuSerif-Bold.ttf"
SERIF = f"{FONTS}/DejaVuSerif.ttf"
SANS_BOLD = f"{FONTS}/DejaVuSans-Bold.ttf"
SANS = f"{FONTS}/DejaVuSans.ttf"


def load(path, size):
    return ImageFont.truetype(path, size)


def wrapped(draw, text, fnt, limit):
    """Greedy word wrap against a pixel width."""
    lines = []
    current = ""
    for word in text.split():
        trial = (current + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= limit:
            current = trial
        else:
            lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def story(draw, x, y, w, h, kicker, headline, body, head_px, body_px):
    """A bordered panel with a black kicker bar, headline and body."""
    draw.rectangle([x, y, x + w, y + h], fill=PANEL_BG, outline=INK, width=2)
    draw.rectangle([x, y, x + w, y + 30], fill=INK)
    draw.text((x + 13, y + 6), kicker, font=load(SANS_BOLD, 17), fill=PAPER)
    cursor = y + 44
    head_font = load(SERIF_BOLD, head_px)
    for line in wrapped(draw, headline, head_font, w - 30):
        draw.text((x + 15, cursor), line, font=head_font, fill=INK)
        cursor += head_px + 7
    if body:
        cursor += 4
        body_font = load(SERIF, body_px)
        for line in wrapped(draw, body, body_font, w - 30):
            draw.text((x + 15, cursor), line, font=body_font, fill=BODY_INK)
            cursor += body_px + 6


def build():
    img = Image.new("RGB", (SIZE, SIZE), PAPER)
    d = ImageDraw.Draw(img)

    # Masthead block
    d.text((MARGIN, 28), "THE WORLD IN ONE PAGE",
           font=load(SERIF_BOLD, 57), fill=INK)
    d.line([MARGIN, 108, SIZE - MARGIN, 108], fill=INK, width=4)
    d.line([MARGIN, 118, SIZE - MARGIN, 118], fill=INK, width=2)
    d.text((MARGIN, 130), "SUNDAY, NOVEMBER 22, 2026",
           font=load(SANS_BOLD, 32), fill=RED)
    d.text((MARGIN + 2, 172), "The day's world news, on a single sheet",
           font=load(SERIF, 20), fill=GREY)
    d.line([MARGIN, 202, SIZE - MARGIN, 202], fill=INK, width=2)

    # Lead story, full width
    story(
        d, MARGIN, 218, WIDTH, 208,
        "BRAZIL · LEAD STORY",
        "'We lost everything': town clears rubble after deadly storm",
        "Residents of a Brazilian town picked through the wreckage of "
        "their homes after a deadly storm tore through the region, "
        "leaving families with nothing and rescue crews clearing rubble "
        "street by street.",
        head_px=31, body_px=20,
    )

    # Two half-width stories side by side
    story(
        d, MARGIN, 442, 454, 296,
        "TECHNOLOGY · UNITED STATES",
        "Nvidia faces US accounting probe amid deepening turmoil",
        "The chipmaker at the centre of the AI boom is reported to face "
        "a US accounting probe, adding regulatory pressure to a company "
        "whose results now move whole markets.",
        head_px=27, body_px=19,
    )
    story(
        d, MARGIN + 474, 442, 454, 296,
        "MIDDLE EAST",
        "Iran strikes three tankers as it shows off missile launchers",
        "Iran struck three tankers and paraded missile launchers in a "
        "show of force, as Houthi forces launched revenge strikes on "
        "the Saudi capital and regional tensions kept climbing.",
        head_px=27, body_px=19,
    )

    # Wide headline-only panel
    story(
        d, MARGIN, 754, WIDTH, 128,
        "UNITED STATES · POLITICS",
        "Trump vows to work with Democrats to cap credit card "
        "interest at 10%",
        "",
        head_px=27, body_px=19,
    )

    # ALSO TODAY: red band, four shorts in two columns
    top = 898
    d.rectangle([MARGIN, top, SIZE - MARGIN, top + 28], fill=RED)
    d.text((MARGIN + 14, top + 5), "ALSO TODAY",
           font=load(SANS_BOLD, 17), fill=(255, 255, 255))
    shorts = [
        "6.7 quake hits Peru; no deaths reported",
        "Rohingyas hail genocide verdict on Myanmar",
        "Pentagon restricts US-Canada defence ties",
        "COP31 deadlocked over fossil fuels",
    ]
    item_font = load(SANS, 16)
    for idx, text in enumerate(shorts):
        cx = MARGIN + 14 + (idx % 2) * 474
        cy = top + 40 + (idx // 2) * 26
        d.ellipse([cx, cy + 6, cx + 8, cy + 14], fill=RED)
        d.text((cx + 18, cy), text, font=item_font, fill=INK)

    # Footer
    d.line([MARGIN, SIZE - 30, SIZE - MARGIN, SIZE - 30], fill=INK, width=2)
    d.text((MARGIN, SIZE - 24),
           "Compiled from wire and newspaper headlines of "
           "22 November 2026 (AFP, AP, Reuters).",
           font=load(SANS, 15), fill=GREY)

    target = Path(__file__).with_name("entry.png")
    img.save(target, optimize=True)
    print("saved", target, target.stat().st_size, "bytes, size", img.size)


if __name__ == "__main__":
    build()
