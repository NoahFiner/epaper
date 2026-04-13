#!/usr/bin/python
# -*- coding:utf-8 -*-
import sys
import os
import logging
import time

sys.path.insert(0, os.path.dirname(__file__))

from config import REFRESH_SECONDS
from trains import fetch_trains
from weather import fetch_temp
from bikes import fetch_bikes
from render import render
from display import Display

logging.basicConfig(level=logging.INFO)

display = Display()
display.start()

last_arrivals = None
last_temp = None
last_bikes = None
while True:
    try:
        arrivals = fetch_trains()
        temp = fetch_temp()
        bikes = fetch_bikes()
        if arrivals != last_arrivals or temp != last_temp or bikes != last_bikes:
            display.show(render(arrivals, temp, bikes))
            last_arrivals = arrivals
            last_temp = temp
            last_bikes = bikes
        time.sleep(REFRESH_SECONDS)
    except KeyboardInterrupt:
        display.shutdown()
        break
    except Exception as e:
        logging.error(e)
        time.sleep(REFRESH_SECONDS)
