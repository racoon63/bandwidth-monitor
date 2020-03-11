#!/usr/bin/env python3

__author__ = 'racoon63 <racoon63@gmx.net>'

import socket
import json
import subprocess
import sys

from .logger import log


class NoInternetConnection(Exception):
   """Base class for other exceptions"""
   pass

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
        self.server_url2      = None
        
        self.client_country   = None
        self.client_ip        = None
        self.client_isp       = None
        self.client_isprating = None
        self.client_rating    = None

    def run(self):
        try:
            if not self._has_connectivity():
                raise NoInternetConnection("No internet connection")
            else:
                log.info("Measuring ...")
                if self.speedtest_server == "auto":
                    self.stats = subprocess.Popen(["speedtest-cli", "--secure", "--json"], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
                else:
                    self.stats = subprocess.Popen(["speedtest-cli", "--secure", "--json", "--server", self.speedtest_server], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

                stdout,stderr = self.stats.communicate()
                self.results   = stdout.decode("utf-8")
                self.speedtest = json.loads(self.results)

                if stderr:
                    log.debug(stderr)
        except NoInternetConnection as err:
            log.error(err)
            log.error("Could not measure bandwidth")
            self._set_up_down_zero()
        except Exception as err:
            log.error("Could not measure bandwidth")
            log.exception(err)
            self._set_up_down_zero()
        else:
            self._set_stats()
            log.info("Finished measurement")
        finally:
            return

    def get_stat_map(self):
        return { 
                    "timestamp": self.timestamp, 
                    "ping": self.ping, 
                    "download": self.download, 
                    "upload": self.upload, 
                    "server": {
                        "city": self.server_city,
                        "country": self.server_country,
                        "host": self.server_host,
                        "id": self.server_id,
                        "latency": self.server_latency,
                        "sponsor": self.server_sponsor,
                        "url": self.server_url,
                        "url2": self.server_url2
                    },
                    "client": {
                        "country": self.client_country,
                        "ip": self.client_ip,
                        "isp": self.client_isp,
                        "isp-rating": self.client_isprating,
                        "rating": self.client_rating
                    }
                }

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
            log.error("Could not set speedtest results")
        else:
            log.debug("Set speedtest results")
        finally:
            return

    def _has_connectivity(self):
        url = "google.com"
        port = 80
        socket.setdefaulttimeout(5)

        try:            
            ip = socket.gethostbyname(url)
            s = socket.create_connection((ip, port))
            s.close()
        except Exception:
            return False        
        else:
            return True
            
    def _set_up_down_zero(self):
        self.download  = 0.0
        self.upload    = 0.0
        return