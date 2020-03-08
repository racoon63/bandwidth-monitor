#!/usr/bin/env python3

__author__ = 'racoon63 <racoon63@gmx.net>'

import socket
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

        self.server_city      = None
        self.server_country   = None
        self.server_host      = None
        self.server_id        = None
        self.server_latency   = None
        self.server_sponsor   = None
        self.server_url       = None
        
        self.client_country   = None
        self.client_ip        = None
        self.client_isp       = None
        self.client_isprating = None
        self.client_rating    = None

    def run(self):
        try:
            logging.info("Measuring ...")
            
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
            logging.info("Finished measurement")
            return

    def _set_stats(self):
        try:
            self.json      = self.speedtest
            self.timestamp = self.speedtest["timestamp"]
            self.ping      = round(self.speedtest["ping"], 2)
            self.download  = round(((self.speedtest["download"] / 1024) / 1024), 2)
            self.upload    = round(((self.speedtest["upload"] / 1024) / 1024), 2)
            
            self.server_city    = self.speedtest["server"]["name"]
            self.server_country = self.speedtest["server"]["country"]
            self.server_host    = self.speedtest["server"]["host"]
            self.server_id      = self.speedtest["server"]["id"]
            self.server_latency = self.speedtest["server"]["latency"]
            self.server_sponsor = self.speedtest["server"]["sponsor"]
            self.server_url     = self.speedtest["server"]["url"]
            self.server_url2    = self.speedtest["server"]["url2"]
            
            self.client_country   = self.speedtest["client"]["country"]
            self.client_ip        = self.speedtest["client"]["ip"]
            self.client_isp       = self.speedtest["client"]["isp"]
            self.client_isprating = self.speedtest["client"]["isprating"]
            self.client_rating    = self.speedtest["client"]["rating"]
        except Exception as err:
            logging.error("Could not set speedtest results")
        else:
            logging.debug("Set speedtest results")
        finally:
            return

    def has_connectivity(self):
        url = "google.com"
        port = 80
        socket.setdefaulttimeout(5)

        try:            
            ip = socket.gethostbyname(url)
            s = socket.create_connection((ip, port))
            s.close()
        except Exception:
            logging.error("Bandwidth-Monitor can not connect to the internet. Please make sure there is an active internet connection")
            return False        
        else:
            return True
            
            