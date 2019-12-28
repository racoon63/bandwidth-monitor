#!/usr/bin/env python3.7

__author__ = 'racoon <racoon63@gmx.net>'

import logging
import os

class Config(object):

    def __init__(self, config_path):
        
        self.speedtest-server = None
        self.datapath   = "../data/data.json"
        self.database   = tinydb
        self.interval   = 60
        
        self.dbuser     = None
        self.dbpassword = None
        self.dbhost     = None
        
        self.loglevel   = info
        self.logpath    = "../log/bwm.log"

        self.config_path = config_path

        self.environment()
        self.configFile()

    def environment(self):
        logging.info("Reading environment variables")

        if 

        return

    def configFile(self):
        return