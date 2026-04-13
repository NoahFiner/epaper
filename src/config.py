import os
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(__file__), ".env"))

API_KEY = os.environ["API_KEY"]
STOP_CODE_OB = "13909"   # Carl + Cole, westbound (toward Ocean Beach)
STOP_CODE_IB = "13911"   # Carl + Cole, eastbound (toward Caltrain/Ballpark)
AGENCY = "SF"
REFRESH_SECONDS = 180
FONT_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "font", "Gorditas", "Gorditas-Regular.ttf")
FONT_PATH_BOLD = os.path.join(os.path.dirname(os.path.dirname(__file__)), "font", "Gorditas", "Gorditas-Bold.ttf")
FONT_PATH_GRANDSTANDER = os.path.join(os.path.dirname(os.path.dirname(__file__)), "font", "Grandstander", "static", "Grandstander-Regular.ttf")
IMG_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "img")
GBFS_DISCOVERY_URL = "https://gbfs.baywheels.com/gbfs/2.3/gbfs.json"
WALLER_STATION_ID = "7d15210b-55fb-4456-8281-781cfa9d5594"
COLE_STATION_ID   = "dd34aaa2-dd91-4d83-9f92-e8a2f1cc2f93"
