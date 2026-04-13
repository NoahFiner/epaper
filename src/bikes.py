import urllib.request
import ssl
import json
import logging

from config import GBFS_DISCOVERY_URL, WALLER_STATION_ID, COLE_STATION_ID

_SSL_CTX = ssl.create_default_context()
_SSL_CTX.check_hostname = False
_SSL_CTX.verify_mode = ssl.CERT_NONE

_EMPTY = {"ebikes": 0, "regular": 0}


def _fetch_json(url):
    with urllib.request.urlopen(url, timeout=10, context=_SSL_CTX) as resp:
        return json.loads(resp.read())


def fetch_bikes():
    result = {"Waller": dict(_EMPTY), "Cole": dict(_EMPTY)}
    try:
        discovery = _fetch_json(GBFS_DISCOVERY_URL)
        feeds = {f["name"]: f["url"] for f in discovery["data"]["en"]["feeds"]}
        status_url = feeds["station_status"]
        stations = {s["station_id"]: s for s in _fetch_json(status_url)["data"]["stations"]}

        for label, sid in [("Waller", WALLER_STATION_ID), ("Cole", COLE_STATION_ID)]:
            s = stations.get(sid)
            if s:
                ebikes = s.get("num_ebikes_available", 0)
                total = s.get("num_bikes_available", 0)
                result[label] = {"ebikes": ebikes, "regular": total - ebikes}
    except Exception as e:
        logging.error(f"fetch_bikes: {e}")
    return result
