#!/usr/bin/env python3

__author__ = 'racoon63 <racoon63@gmx.net>'

import socket
import json
import subprocess
import sys

import speedtest

from .logger import log


class NoInternetConnection(Exception):
   """Base class for other exceptions"""
   pass

class Speedtest(object):

    def __init__(self, speedtest_server):
        if speedtest_server == "auto":
            self.servers = []
        else:
            self.servers = [speedtest_server]

        self.threads = None

        self.results   = None

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

        if not self._has_connectivity():
            raise NoInternetConnection("No internet connection")
        else:
            log.info("Measuring ...")

            s = speedtest.Speedtest()

            s.get_servers(self.servers)
            s.get_best_server()
            s.download(threads=self.threads)
            s.upload(threads=self.threads)

            self.results = s.results.dict()

        self._set_stats()
        log.info("Finished measurement")

    def get_results(self):
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
        self.timestamp = self.results["timestamp"]
        self.ping      = round(self.results["ping"], 2)
        self.download  = round(((self.results["download"] / 1024) / 1024), 2)
        self.upload    = round(((self.results["upload"] / 1024) / 1024), 2)
        
        self.server_city    = self.results["server"]["city"]
        self.server_country = self.results["server"]["country"]
        self.server_host    = self.results["server"]["host"]
        self.server_id      = self.results["server"]["id"]
        self.server_latency = self.results["server"]["latency"]
        self.server_sponsor = self.results["server"]["sponsor"]
        self.server_url     = self.results["server"]["url"]
        self.server_url2    = self.results["server"]["url2"]
        
        self.client_country   = self.results["client"]["country"]
        self.client_ip        = self.results["client"]["ip"]
        self.client_isp       = self.results["client"]["isp"]
        self.client_isprating = self.results["client"]["isprating"]
        self.client_rating    = self.results["client"]["rating"]

    def _has_connectivity(self):
        url = "google.com"
        port = 80
        socket.setdefaulttimeout(5)
   
        try:
            ip = socket.gethostbyname(url)
            s = socket.create_connection((ip, port))
        except Exception as err:
            return False
        else:
            s.close()
            return True
            
    def _set_up_down_zero(self):
        self.download  = 0.0
        self.upload    = 0.0
        return
