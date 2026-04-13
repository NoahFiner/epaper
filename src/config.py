import os
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(__file__), ".env"))

API_KEY = os.environ["API_KEY"]
STOP_CODE_OB = "13909"   # Carl + Cole, westbound (toward Ocean Beach)
STOP_CODE_IB = "13911"   # Carl + Cole, eastbound (toward Caltrain/Ballpark)
AGENCY = "SF"
REFRESH_SECONDS = 60
FONT_PATH = os.path.join(os.path.dirname(__file__), "pic", "Font.ttc")
IMG_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "img")
