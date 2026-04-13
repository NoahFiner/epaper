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
from render import render
from display import Display

logging.basicConfig(level=logging.INFO)

display = Display()
display.start()

last_arrivals = None
last_temp = None
while True:
    try:
        arrivals = fetch_trains()
        temp = fetch_temp()
        if arrivals != last_arrivals or temp != last_temp:
            display.show(render(arrivals, temp))
            last_arrivals = arrivals
            last_temp = temp
        time.sleep(REFRESH_SECONDS)
    except KeyboardInterrupt:
        display.shutdown()
        break
    except Exception as e:
        logging.error(e)
        time.sleep(REFRESH_SECONDS)
