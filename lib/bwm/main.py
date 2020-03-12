#!/usr/bin/env python3

__author__ = "racoon63 <racoon63@gmx.net>"

import os
import sys
import time

from .config import Config
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

    def run(self):
        try:
            log.info("Bandwidth-Monitor started successfully")
            while True:

                starttime = time.time()

                test = Speedtest(self.conf.speedtest_server)
                test.run()

                data = test.get_results()
                self.db.insert(data)

                time.sleep(self.conf.interval - ((time.time() - starttime) % self.conf.interval))

        except KeyboardInterrupt:
            log.info("Bandwidth-Monitor was stopped by user")
            sys.exit(0)

        except Exception as err:
            self._set_up_down_zero()
            log.error("Could not measure bandwidth")
            log.exception(err)
            self._set_up_down_zero()
