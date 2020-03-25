#!/usr/bin/env python3

__author__ = "racoon63 <racoon63@gmx.net>"

import os
import sys
import time

from .config import Config
from .logger import log
from .speedtest import Speedtest
from.speedtest import NoInternetConnection


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

    def _record(self, data):
        self.db.insert(data)
        return

    def _wait(self, starttime):
        time.sleep(self.conf.interval - ((time.time() - starttime) % self.conf.interval))
        return

    def run(self):
        
            log.info("Bandwidth-Monitor started successfully")
            while True:
                try:
                    starttime = time.time()

                    test = Speedtest(self.conf.speedtest_server)    
                    test.run()

                except NoInternetConnection as err:
                    log.exception(err)
                    data = test.get_results()
                    self._record(data)
                    self._wait(starttime)                    

                except KeyboardInterrupt:
                    log.info("Bandwidth-Monitor was stopped by user")
                    sys.exit(0)

                except Exception as err:
                    log.error("Could not measure bandwidth")
                    log.exception(err)
                
                else:
                    data = test.get_results()
                    self._record(data)
                    self._wait(starttime)
