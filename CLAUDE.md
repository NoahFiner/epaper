# Epaper Train Display — Project Guide

## What this project does
Fetches N Judah Muni arrival times from the 511.org API and renders them to a Waveshare 4inch e-Paper HAT+ (E) display (600×400, E Ink Spectra 6, 6-color). Also fetches current temperature from Open-Meteo. Runs on a Raspberry Pi.

## File structure
```
src/
  index.py          # Main loop — fetches trains + weather, renders, updates display
  config.py         # Constants: API keys, stop codes, font paths, refresh interval
  trains.py         # 511.org API fetch + parse → {"West": ["7:00", "7:10"], "East": [...]}
  weather.py        # Open-Meteo fetch → int °F for Cole Valley, SF
  render.py         # PIL image builder → 600×400 RGB Image
  display.py        # Waveshare EPD wrapper (init/show/shutdown)
  waveshare_epd/    # Vendor driver — do not modify
img/
  bg.bmp            # Full-screen background image (600×400)
  judah.bmp, lyft.bmp, "Weather 512.bmp"  # Legacy icons (not used in current layout)
font/
  Gorditas/         # Dynamic value font (Gorditas-Regular.ttf, Gorditas-Bold.ttf)
  Grandstander/     # Static label font (static/Grandstander-Regular.ttf)
```

## Running
```bash
# On laptop — generate output.png preview with live API data
python3 src/render.py

# On Raspberry Pi — start the display loop manually
python3 src/index.py
```

## Systemd service (Pi auto-start)

The Pi runs `src/index.py` as a systemd service (`epaper`) that starts automatically on boot.

```bash
# Start / stop
sudo systemctl start epaper
sudo systemctl stop epaper

# Enable / disable auto-start on boot
sudo systemctl enable epaper
sudo systemctl disable epaper

# Logs
journalctl -u epaper -f
```

## Key facts for agents

### Display hardware
- Model: Waveshare epd4in0e (E Ink Spectra 6, 6-color)
- Resolution: 600×400 (rendered as landscape; driver handles rotation)
- **Partial refresh is NOT supported** — full refresh takes ~19s and flickers. This is a hardware limitation with no workaround.
- `REFRESH_SECONDS = 180` (3 minutes) — Waveshare recommends ≥180s between refreshes
- The display only repaints when data changes (to minimize flicker)

### Layout (sentence-style, overlaid on bg.bmp)
All text at 34px, starting at x=32, y=22, line height=44px.

| Line | Static (Grandstander Regular) | Dynamic (Gorditas Regular) |
|------|-------------------------------|---------------------------|
| 1 | "Good morning!! Today is " | "[temp]°F" |
| 2 | "N-Caltrain at " | "[7:45 & 7:56]" (East arrivals) |
| 3 | "N-Beach is at " | "[7:45 & 7:56]" (West arrivals) |
| 4 | "Waller has " + "  Cole has " | "3e, 4a" (placeholder ×2) |

- Gorditas = bold-looking dynamic values; Grandstander = static sentence labels
- Baselines are aligned per-line using `font.getmetrics()[0]` ascent offset
- Arrival times are PST clock times (e.g. "7:45"), separator is " & "

### 511.org API
- Stop 13909 = Carl + Cole, **westbound** (OB, toward Ocean Beach) — labeled "West" / "N-Beach"
- Stop 13911 = Carl + Cole, **eastbound** (IB, toward Caltrain/Ballpark) — labeled "East" / "N-Caltrain"
- Each direction uses a separate stop code — the API does not return both directions from one stop
- Timestamps use `Z` suffix (not `+00:00`) — must be normalized before `datetime.fromisoformat()`
- SSL verification is disabled in `trains.py` due to macOS CA cert issues; leave it that way
- Returns PST-formatted strings (e.g. "7:45") — NOT minutes-until

### Weather API
- Provider: Open-Meteo (free, no API key needed)
- Coordinates: lat=37.766910, lon=-122.451070 (Cole Valley, SF)
- Returns current `temperature_2m` in °F, rounded to nearest int

### Fonts
- `FONT_PATH` → Gorditas-Regular.ttf (dynamic values — already looks bold)
- `FONT_PATH_BOLD` → Gorditas-Bold.ttf (available but not currently used)
- `FONT_PATH_GRANDSTANDER` → Grandstander-Regular.ttf (static labels)
- All defined in `config.py`, resolved relative to project root

## Parallel agent tips
- `render.py`, `trains.py`, and `weather.py` are independent — safe to modify in parallel
- `config.py` is imported by all; changing constants there affects everything
- The `waveshare_epd/` vendor directory should never be modified
- To test rendering without a Pi: `python3 src/render.py` — output saved to `output.png` at repo root
- API calls require network; render/layout changes do not
