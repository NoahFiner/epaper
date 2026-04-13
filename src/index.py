#!/usr/bin/python
# -*- coding:utf-8 -*-
import sys
import os
import logging
import time

sys.path.insert(0, os.path.dirname(__file__))

from config import REFRESH_SECONDS
from trains import fetch_trains
from render import render
from display import Display

logging.basicConfig(level=logging.INFO)

display = Display()
display.start()

while True:
    try:
        arrivals = fetch_trains()
        image = render(arrivals)
        display.show(image)
        time.sleep(REFRESH_SECONDS)
    except KeyboardInterrupt:
        display.shutdown()
        break
    except Exception as e:
        logging.error(e)
        time.sleep(REFRESH_SECONDS)
