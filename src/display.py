import sys
import os

sys.path.insert(0, os.path.dirname(__file__))

from waveshare_epd import epd4in0e


class Display:
    def __init__(self):
        self.epd = epd4in0e.EPD()

    def start(self):
        self.epd.init()
        self.epd.Clear()

    def show(self, image):
        self.epd.display(self.epd.getbuffer(image))

    def shutdown(self):
        self.epd.sleep()
