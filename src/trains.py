import urllib.request
import urllib.error
import ssl
import json
import logging
from datetime import datetime, timezone
from zoneinfo import ZoneInfo

from config import API_KEY, STOP_CODE_OB, STOP_CODE_IB, AGENCY

LOCAL_TZ = ZoneInfo("America/Los_Angeles")

# macOS often lacks system CA certs for Python; skip verification as fallback
_SSL_CTX = ssl.create_default_context()
_SSL_CTX.check_hostname = False
_SSL_CTX.verify_mode = ssl.CERT_NONE


def _fetch_stop(stop_code):
    url = (
        f"https://api.511.org/transit/StopMonitoring"
        f"?api_key={API_KEY}&agency={AGENCY}&stopCode={stop_code}&format=json"
    )
    with urllib.request.urlopen(url, timeout=10, context=_SSL_CTX) as resp:
        raw = resp.read().decode("utf-8-sig")
    data = json.loads(raw)
    return (
        data["ServiceDelivery"]
        ["StopMonitoringDelivery"]
        .get("MonitoredStopVisit", [])
    )


def _parse_times(visits):
    times = []
    for visit in visits:
        try:
            journey = visit["MonitoredVehicleJourney"]
            expected_str = journey["MonitoredCall"]["ExpectedArrivalTime"]
            expected = datetime.fromisoformat(expected_str.replace("Z", "+00:00"))
            if expected.tzinfo is None:
                expected = expected.replace(tzinfo=timezone.utc)
            times.append(expected.astimezone(LOCAL_TZ).strftime("%-I:%M"))
        except (KeyError, TypeError, ValueError) as e:
            logging.debug(f"Skipping visit: {e}")
    return times[:2]


def fetch_trains():
    result = {"West": [], "East": []}

    for stop_code, label in [(STOP_CODE_OB, "West"), (STOP_CODE_IB, "East")]:
        try:
            visits = _fetch_stop(stop_code)
            result[label] = _parse_times(visits)
        except Exception as e:
            logging.error(f"fetch_trains({stop_code}): {e}")

    return result
