import os
from PIL import Image, ImageDraw, ImageFont

from config import FONT_PATH, FONT_PATH_GRANDSTANDER, IMG_DIR

FONT_SIZE = 34
LINE_HEIGHT = 44
X_START, Y_START = 32, 22
BLACK = (0, 0, 0)


def _load_fonts(size):
    gs = ImageFont.truetype(FONT_PATH_GRANDSTANDER, size)
    gd = ImageFont.truetype(FONT_PATH, size)  # Gorditas Regular
    return gs, gd


def _draw_mixed(draw, x, y, segments, fill=BLACK):
    # Align all segments to the tallest ascender so baselines match
    max_ascent = max(font.getmetrics()[0] for _, font in segments)
    for text, font in segments:
        ascent = font.getmetrics()[0]
        y_offset = max_ascent - ascent
        draw.text((x, y + y_offset), text, font=font, fill=fill)
        x = draw.textbbox((x, y + y_offset), text, font=font)[2]


def render(arrivals, temp):
    img = Image.open(os.path.join(IMG_DIR, "bg.bmp")).convert("RGB")
    draw = ImageDraw.Draw(img)
    gs, gd = _load_fonts(FONT_SIZE)

    east = arrivals.get("East", [])
    west = arrivals.get("West", [])
    east_str = " & ".join(east) if east else "—"
    west_str = " & ".join(west) if west else "—"

    lines = [
        [("Good morning!! Today is ", gs), (f"{temp}°F", gd)],
        [("N-Caltrain at ", gs), (east_str, gd)],
        [("N-Beach is at ", gs), (west_str, gd)],
        [("Waller has ", gs), ("3e, 4a", gd), ("  Cole has ", gs), ("3e, 4a", gd)],
    ]

    for i, segments in enumerate(lines):
        _draw_mixed(draw, X_START, Y_START + i * LINE_HEIGHT, segments)

    return img


if __name__ == "__main__":
    import sys
    sys.path.insert(0, os.path.dirname(__file__))
    from trains import fetch_trains
    from weather import fetch_temp
    arrivals = fetch_trains()
    temp = fetch_temp()
    print(f"Arrivals: {arrivals}, Temp: {temp}°F")
    image = render(arrivals, temp)
    out = os.path.join(os.path.dirname(__file__), "..", "output.png")
    image.save(out)
    print(f"Saved preview to {os.path.abspath(out)}")
