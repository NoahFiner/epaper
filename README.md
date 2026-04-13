# Epaper Train Display

Fetches N Judah Muni arrival times and current temperature, renders them to a Waveshare 4-inch e-Paper display (600×400, 6-color). Runs on a Raspberry Pi.

## Running on laptop (preview)

```bash
python3 src/render.py   # generates output.png with live API data
```

## Running on the Pi (service)

The display runs as a systemd service (`epaper`) that auto-starts on boot.

```bash
# Start / stop manually
sudo systemctl start epaper
sudo systemctl stop epaper

# Enable / disable auto-start on boot
sudo systemctl enable epaper
sudo systemctl disable epaper

# Check status
sudo systemctl status epaper

# View live logs
journalctl -u epaper -f
```

### First-time setup on the Pi

```bash
sudo cp /home/noahfiner/epaper/epaper.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable epaper
sudo systemctl start epaper
```

`src/.env` must exist with `API_KEY=<your_511_key>` (not committed to git — create manually).
