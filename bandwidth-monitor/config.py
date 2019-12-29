#!/usr/bin/env python3.7

__author__ = 'racoon63 <racoon63@gmx.net>'

import configparser
import logging
import os
import sys


class Config(object):

    def __init__(self):
        
        self.speedtest_server = None
        self.interval   = 60
        
        self.database   = tinydb
        self.datapath   = "../data/data.json"
        self.dbhost     = None
        self.dbuser     = None
        self.dbpassword = None
        
        self.loglevel   = info
        self.logpath    = "../log/bwm.log"

        if "CONFIG_PATH" in os.environ:
                logging.debug("Environment variable 'CONFIG_PATH' is available.")
                logging.debug("Environment variable 'CONFIG_PATH' is: " + self.config_path)
                self.config_path = os.environ["CONFIG_PATH"]
        else:
            logging.debug("Environment variable 'CONFIG_PATH' is not available. Fallback to default value: " + self.config_path)
            self.config_path = os.path.dirname(os.path.abspath(__file__)) + "../config.ini"
        
        self.config_exists = self.checkConfigFile()

        if self.config_exists:
            self.config = self.readConfigFile()
        else:
            self.create()
            if self.config_exists:
                self.config = self.read()
            else:
                logging.fatal("Could not create and read config file")
                sys.exit("Exiting")


    def check(self):
        
        try:
            logging.debug("Check if config file exists")
            
            if os.path.exists(self.config_path) and os.path.isfile(self.config_path):
                logging.info("Config file found")
                self.config_exists = True
            else:
                logging.error("Config file does not exist.")
                logging.info("Trying to generate a config")
                self.create()
                logging.info("Done. Checking again")
                self.check()
        
        except Exception as err:
            logging.error(err)

        finally:
            return


    def read(self):
        try:
            if self.config_exists is True:
                self.config = configparser.ConfigParser()
                self.config.sections()
                logging.debug("Reading config")
                self.config.read(self.config_path)
                logging.debug("Finished reading config file")
            
        except Exception as err:
            logging.error(err)

        finally:
            return


    def write(self):
        try:
            with open(self.config_path, 'w') as config:
                config.write(self.config)
        
        except Exception:
            logging.fatal("Could not write config to file")
            sys.exit("Exiting")


    def update(self):
        

    def create(self):
        try:
            if "SPEEDTEST_SERVER" in os.environ:
                logging.debug("Environment variable 'SPEEDTEST_SERVER' is set.")
                logging.debug("Environment variable 'SPEEDTEST_SERVER' is: " + self.speedtest_server)
                self.speedtest_server = os.environ["SPEEDTEST_SERVER"]
            else:
                logging.debug("Environment variable 'SPEEDTEST_SERVER' is not set. Fallback to default value: " + self.speedtest_server)

            if "INTERVAL" in os.environ:
                logging.debug("Environment variable 'INTERVAL' is available.")
                logging.debug("Environment variable 'INTERVAL' is: " + self.interval)
                self.interval = os.environ["INTERVAL"]
            else:
                logging.debug("Environment variable 'INTERVAL' is not available. Fallback to default value: " + self.interval)

            config['General'] = {'speedtest-server': self.speedtest_server,
                                 'interval': self.interval}

            config['Database'] = {}

            if "DATABASE" in os.environ:
                logging.debug("Environment variable 'DATABASE' is available.")
                logging.debug("Environment variable 'DATABASE' is: " + self.database)
                self.database = os.environ["DATABASE"]
                config['Database']['database'] = self.database
            else:
                logging.debug("Environment variable 'DATABASE' is not available. Fallback to default value: " + self.database)
                config['Database']['database'] = self.database

            if self.database == "tinydb":
                if "DATAPATH" in os.environ:
                    logging.debug("Environment variable 'DATAPATH' is available.")
                    logging.debug("Environment variable 'DATAPATH' is: " + self.datapath)
                    self.datapath = os.environ["DATAPATH"]
                    config['Database']['datapath'] = self.datapath
                else:
                    logging.debug("Environment variable 'DATAPATH' is not available. Fallback to default value: " + self.datapath)
                    config['Database']['datapath'] = self.datapath
            
            if self.database == "mongodb":
                if "DBHOST" in os.environ:
                    logging.debug("Environment variable 'DBHOST' is available.")
                    logging.debug("Environment variable 'DBHOST' is: " + self.dbhost)
                    self.dbhost = os.environ["DBHOST"]
                    config['Database']['dbhost'] = self.dbhost
                else:
                    logging.fatal("Environment variable 'DBHOST' is not available. Can not proceed.")
                    sys.exit("Exiting")
                
                if "DBUSER" in os.environ:
                    logging.debug("Environment variable 'DBUSER' is available.")
                    logging.debug("Environment variable 'DBUSER' is: " + self.dbuser)
                    self.dbuser = os.environ["DBUSER"]
                    config['Database']['dbuser'] = self.dbuser
                else:
                    logging.fatal("Environment variable 'DBUSER' is not available. Can not proceed.")
                    sys.exit("Exiting")
            
                if "DBPASSWORD" in os.environ:
                    logging.debug("Environment variable 'DBPASSWORD' is available.")
                    logging.debug("Environment variable 'DBPASSWORD' is: Haha don't tell you here!")
                    self.dbpassword = os.environ["DBPASSWORD"]
                    config['Database']['dbpassword'] = self.dbpassword
                else:
                    logging.fatal("Environment variable 'DBPASSWORD' is not available. Can not proceed.")
                    sys.exit("Exiting")
            
            config['Logging'] = {}

            if "LOGLEVEL" in os.environ:
                logging.debug("Environment variable 'LOGLEVEL' is available.")
                logging.debug("Environment variable 'LOGLEVEL' is: " + self.loglevel)
                self.loglevel = os.environ["LOGLEVEL"]
                config['Logging']['loglevel'] = self.loglevel
            else:
                logging.debug("Environment variable 'LOGLEVEL' is not available. Fallback to default value: " + self.loglevel)
                config['Logging']['loglevel'] = self.loglevel

            if "LOGPATH" in os.environ:
                logging.debug("Environment variable 'LOGPATH' is available.")
                logging.debug("Environment variable 'LOGPATH' is: " + self.logpath)
                self.logpath = os.environ["LOGPATH"]
                config['Logging']['logpath'] = self.logpath
            else:
                logging.debug("Environment variable 'LOGPATH' is not available. Fallback to default value: " + self.logpath)
                config['Logging']['logpath'] = self.logpath

        except Exception:
            logging.fatal("Something went horribly wrong ¯\_(ツ)_/¯")
            sys.exit("Exiting")

    @property
    def speedtestServer(self):
        return self.speedtest_server

    @speedtestServer.setter
    def speedtestServer(self):
        pass

    def validate(self):

        logging.debug("Finished reading config file")