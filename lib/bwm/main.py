#!/usr/bin/env python3

__author__ = "racoon63 <racoon63@gmx.net>"

import os
import sys
import time

from .config import Config
from .data import Data
from .logger import log
from .speedtest import Speedtest


class Main(object):

    def __init__(self, workdir):
        
        self.workdir = workdir
        self._create_dir_tree()
        self.conf = Config(self.workdir)
        self.db = self.conf.dbdriver

    def _create_dir_tree(self):
        """ Creates all needed directories before bwm can start. """

        logdir  = self.workdir + "/log"
        log.debug("Logdir is: %s", logdir)

        try:
            if not os.path.exists(logdir):
                log.debug("Logdir does not exist. Creating ...")
                os.makedirs(logdir, exist_ok=True)
                
                if os.path.exists(logdir):
                    log.debug("Logdir created successfully!")
        except Exception as err:
            log.exception(err)
            sys.exit(1)

        datadir  = self.workdir + "/data"
        log.debug("Datadir is: %s", datadir)

        try:
            if not os.path.exists(datadir):
                log.debug("Datadir does not exist. Creating ...")
                os.makedirs(datadir, exist_ok=True)

                if os.path.exists(datadir):
                    log.debug("Datadir created successfully!")
        except Exception as err:
            log.exception(err)
            sys.exit(1)

        return

    def _leading_zero(self, number):
        """ Helper function to create a clean time format. """

        if len(str(number)) == 1:
            return "{}{}".format(0, number)
        else:
            return number

    def _get_timestamp(self):
        c_year   = self._leading_zero(time.localtime().tm_year)
        c_month  = self._leading_zero(time.localtime().tm_mon)
        c_day    = self._leading_zero(time.localtime().tm_mday)
        c_hour   = self._leading_zero(time.localtime().tm_hour)
        c_minute = self._leading_zero(time.localtime().tm_min)
        c_second = self._leading_zero(time.localtime().tm_sec)

        return "{}-{}-{} {}:{}:{}".format(c_year, c_month, c_day, c_hour, c_minute, c_second)

    def run(self):
        try:
            log.info("Bandwidth-Monitor started successfully")
            while True:

                starttime = time.time()

                test = Speedtest(self.conf.speedtest_server)
                test.run()

                ts = self._get_timestamp()
                data = test.get_stat_map()
                self.db.insert(data)

                time.sleep(self.conf.interval - ((time.time() - starttime) % self.conf.interval))

        except KeyboardInterrupt:
            log.info("Bandwidth-Monitor was stopped by user")
            sys.exit(0)
