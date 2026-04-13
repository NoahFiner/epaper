import urllib.request
import json
import ssl

_WEATHER_URL = (
    "https://api.open-meteo.com/v1/forecast"
    "?latitude=37.766910&longitude=-122.451070"
    "&current=temperature_2m&temperature_unit=fahrenheit&forecast_days=1"
)

_SSL_CTX = ssl.create_default_context()
_SSL_CTX.check_hostname = False
_SSL_CTX.verify_mode = ssl.CERT_NONE


def fetch_temp():
    with urllib.request.urlopen(_WEATHER_URL, context=_SSL_CTX, timeout=10) as r:
        data = json.loads(r.read())
    return int(round(data["current"]["temperature_2m"]))
