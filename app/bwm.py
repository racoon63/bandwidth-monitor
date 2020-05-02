""" Core component of the Bandwidth-Monitor. """

import time

from config import Config
from measurement import Measurement
from storage import Storage


class BandwidthMonitor:
    """ BandwidthMonitor class is the core class of the bwm service. """
    def __init__(self):
        self.conf = Config()
        self.msment = Measurement()
        self.backend = Storage()

    def run(self):
        """ Runs all tasks that belong to the service. """
        while True:
            starttime = time.time()
            results = self.msment.measure()
            print(results)
            # self.backend.save(results)
            time.sleep(self.conf.interval - ((time.time() - starttime) % self.conf.interval))
