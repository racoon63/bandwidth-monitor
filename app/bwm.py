""" Core component of the Bandwidth-Monitor. """

import time

from config import Config
from measurement import Measurement
from storage import StorageInterface


class BandwidthMonitor:
    """ BandwidthMonitor class is the core class of the bwm service. """
    conf = Config()
    msment = Measurement()
    storage_handler = StorageInterface(datapath=conf.datapath,
                                       dbtype=conf.dbtype,
                                       dbhost=conf.dbhost,
                                       dbuser=conf.dbuser,
                                       dbpassword=conf.dbpassword,
                                       dbname="bwm")

    @classmethod
    def run(cls):
        """ Runs all tasks that belong to the service. """
        while True:
            starttime = time.time()
            results = cls.msment.measure()
            cls.storage_handler.store(cls.conf.dbtype, results)
            time.sleep(cls.conf.interval - ((time.time() - starttime) % cls.conf.interval))
