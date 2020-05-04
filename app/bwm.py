""" Core component of the Bandwidth-Monitor. """

import time

from config import Config
from measurement import Measurement
from storage import Storage


class BandwidthMonitor:
    """ BandwidthMonitor class is the core class of the bwm service. """
    conf = Config()
    msment = Measurement()
    backend = Storage()

    @classmethod
    def run(cls):
        """ Runs all tasks that belong to the service. """
        while True:
            starttime = time.time()
            results = cls.msment.measure()
            print(results)
            # self.backend.save(results)
            time.sleep(cls.conf.interval - ((time.time() - starttime) % cls.conf.interval))
