__author__ = "racoon63 <racon63@gmx.net>"

from time import sleep, time

from config import Config
from log import Log
from measurement import Measurement
from storage import Storage


class BandwidthMonitor:
    def __init__(self):
        self.conf = Config()
        self.st = Speedtest()
        self.backend = Storage()

    def run(self):
        while True:
            starttime = time()
            results = self.st.measure()
            self.backend.save(results)
            # TODO: Integrate interval as float
            sleep(60.0 - ((time() - starttime) % 60.0))