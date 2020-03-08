#!/usr/bin/env python3

__author__ = "racoon63 <racoon63@gmx.net>"

import json
import logging
import os
import sys
import time

from .config import Config
from .data import Data
from .logger import Logger
from .speedtest import Speedtest


class Main(object):

    def __init__(self, workdir):
        
        self.workdir = workdir
        self._create_dir_tree()
        self.conf = Config(self.workdir)
        self.logger = Logger(self.conf.loglevel)
        self.db = self.conf.dbdriver

    def _create_dir_tree(self):
        """ Creates all needed directories before bwm can start. """

        logdir  = self.workdir + "/log"
        logging.debug("Logdir is: %s", logdir)

        try:
            if not os.path.exists(logdir):
                logging.debug("Logdir does not exist. Creating ...")
                os.makedirs(logdir, exist_ok=True)
                
                if os.path.exists(logdir):
                    logging.debug("Logdir created successfully!")
        except Exception as err:
            logging.exception(err)
            sys.exit(1)

        datadir  = self.workdir + "/data"
        logging.debug("Datadir is: %s", datadir)

        try:
            if not os.path.exists(datadir):
                logging.debug("Datadir does not exist. Creating ...")
                os.makedirs(datadir, exist_ok=True)

                if os.path.exists(datadir):
                    logging.debug("Datadir created successfully!")
        except Exception as err:
            logging.exception(err)
            sys.exit(1)

        return

    def _leading_zero(self, number):
        """ Helper function to create a clean time format. """

        if len(str(number)) == 1:
            return "{}{}".format(0, number)
        else:
            return number

    def run(self):

        try:

            logging.info("Bandwidth-Monitor started successfully")

            while True:

                starttime = time.time()
                
                test = Speedtest(self.conf.speedtest_server)
                test.run()

                timestamp = test.timestamp # is not used yet because of too complicate time format
                ping      = test.ping
                download  = test.download
                upload    = test.upload
                
                c_year   = self._leading_zero(time.gmtime().tm_year)
                c_month  = self._leading_zero(time.gmtime().tm_mon)
                c_day    = self._leading_zero(time.gmtime().tm_mday)
                c_hour   = self._leading_zero(time.gmtime().tm_hour)
                c_minute = self._leading_zero(time.gmtime().tm_min)
                c_second = self._leading_zero(time.gmtime().tm_sec)

                ts = "{}-{}-{}-{}-{}-{}".format(c_year, c_month, c_day, c_hour, c_minute, c_second)

                data = Data(ts, ping, download, upload)
                self.db.insert(data.create())

                time.sleep(self.conf.interval - ((time.time() - starttime) % self.conf.interval))

        except KeyboardInterrupt:
            logging.info("Bandwidth-Monitor was stopped by user")
            sys.exit(0)
