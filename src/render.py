import os
from PIL import Image, ImageDraw, ImageFont

from config import FONT_PATH, IMG_DIR

WIDTH, HEIGHT = 600, 400
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
ICON_SIZE = (100, 100)
ICON_X = 18
LABEL_X = 145
VALUE_X = 590


def _load_font(size, bold=False):
    return ImageFont.truetype(FONT_PATH, size)


def _format_arrivals(minutes_list):
    if not minutes_list:
        return "—"
    return ", ".join(f"{m} min" for m in minutes_list)


def _paste_icon(draw_img, bmp_name, y_center):
    path = os.path.join(IMG_DIR, bmp_name)
    try:
        icon = Image.open(path).convert("RGB")
        icon = icon.resize(ICON_SIZE, Image.LANCZOS)
        y = y_center - ICON_SIZE[1] // 2
        draw_img.paste(icon, (ICON_X, y))
    except FileNotFoundError:
        pass  # Skip missing icons gracefully


def _draw_section(img, draw, bmp_name, y_center, rows):
    """
    rows: list of (label, value) tuples — up to 2 rows drawn in the section
    """
    _paste_icon(img, bmp_name, y_center)

    font_label = _load_font(40, bold=True)
    font_value = _load_font(36)

    row_height = 48
    n = len(rows)
    # Vertically center rows around y_center
    total_h = n * row_height
    y_start = y_center - total_h // 2

    for i, (label, value) in enumerate(rows):
        y = y_start + i * row_height
        draw.text((LABEL_X, y), label, font=font_label, fill=BLACK)
        bbox = draw.textbbox((0, 0), value, font=font_value)
        text_w = bbox[2] - bbox[0]
        draw.text((VALUE_X - text_w, y), value, font=font_value, fill=BLACK)


def render(arrivals):
    img = Image.new("RGB", (WIDTH, HEIGHT), WHITE)
    draw = ImageDraw.Draw(img)

    # Divider lines
    draw.line([(0, 135), (WIDTH, 135)], fill=(200, 200, 200), width=1)
    draw.line([(0, 275), (WIDTH, 275)], fill=(200, 200, 200), width=1)

    # Section 1: Trains (y 0–135, center ~67)
    west_str = _format_arrivals(arrivals.get("West", []))
    east_str = _format_arrivals(arrivals.get("East", []))
    _draw_section(img, draw, "judah.bmp", 67, [
        ("West", west_str),
        ("East", east_str),
    ])

    # Section 2: Bikes (y 135–275, center ~205)
    _draw_section(img, draw, "lyft.bmp", 205, [
        ("Waller", "—"),
        ("Cole", "—"),
    ])

    # Section 3: Weather (y 275–400, center ~337)
    _draw_section(img, draw, "Weather 512.bmp", 337, [
        ("Temp", "—"),
        ("Rain", "—"),
    ])

    return img


if __name__ == "__main__":
    # Quick visual test — fetches live data, saves output.png for inspection
    import sys
    sys.path.insert(0, os.path.dirname(__file__))
    from trains import fetch_trains
    sample = fetch_trains()
    print(f"Live arrivals: {sample}")
    image = render(sample)
    out = os.path.join(os.path.dirname(__file__), "..", "output.png")
    image.save(out)
    print(f"Saved preview to {os.path.abspath(out)}")
