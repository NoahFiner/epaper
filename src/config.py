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
