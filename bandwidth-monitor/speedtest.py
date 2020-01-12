#!/usr/bin/env python3.7

__author__ = 'racoon <racoon63@gmx.net>'

import json
import logging
import subprocess


class Speedtest(object):

    def __init__(self, speedtest_server):

        self.speedtest_server = speedtest_server

        self.stats     = None

        self.results   = None
        self.speedtest = None

        self.json      = None
        self.timestamp = None
        self.ping      = None
        self.download  = None
        self.upload    = None


    def run(self):

        try:

            logging.info("Measure latency and bandwidth")
            
            if self.speedtest_server == "auto":
                self.stats = subprocess.Popen(["speedtest-cli", "--secure", "--json"], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            else:
                self.stats = subprocess.Popen(["speedtest-cli", "--secure", "--json", "--server", self.speedtest_server], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

            stdout,stderr = self.stats.communicate()

            self.results   = stdout.decode("utf-8")
            self.speedtest = json.loads(self.results)

            if stderr:
                logging.debug(stderr)

        except Exception as err:
            logging.exception(err)
            logging.error("Could not measure bandwidth")

        else:
            self._set_stats()
            logging.info("Measurement finished")
            return


    def _set_stats(self):

        try:
            self.json      = self.speedtest
            self.timestamp = self.speedtest["timestamp"]
            self.ping      = round(self.speedtest["ping"], 2)
            self.download  = round(((self.speedtest["download"] / 1024) / 1024), 2)
            self.upload    = round(((self.speedtest["upload"] / 1024) / 1024), 2)

        except Exception as err:
            logging.error("Could not set speedtest results")

        else:
            logging.debug("Set speedtest results")
            return
