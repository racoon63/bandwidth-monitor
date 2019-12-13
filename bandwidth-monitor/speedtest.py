#!/usr/bin/env python3.7

__author__ = 'racoon <racoon63@gmx.net>'

import json
import logging
import subprocess


class Speedtest(object):

    def __init__(self):
        stats = subprocess.Popen(['speedtest-cli', '--secure', '--json'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        stdout,stderr = stats.communicate()
        
        logging.debug(stderr)

        self.results = stdout.decode('utf-8')
        self.speedtest = json.loads(self.results)

        self.json = self.speedtest
        self.timestamp = self.speedtest['timestamp']
        self.ping = round(self.speedtest['ping'], 2)
        self.download = round(((self.speedtest['download'] / 1024) / 1024), 2)
        self.upload = round(((self.speedtest['upload'] / 1024) / 1024), 2)
