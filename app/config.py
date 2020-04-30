__author__ = "racoon63 <racon63@gmx.net>"

from os import environ
import configparser

from log import Log


class Config:
    """Class that stores config values for the bwm service."""
    def __init__(self):
        self.config_file_path = "config.ini"
        self.config_file = configparser.ConfigParser(empty_lines_in_values=False)

        self.speedtest_server = None
        self.interval = 60
        self.dbtype = "tinydb"
        self.datapath = "data/bwm.json"
        self.dbhost = None # TODO: Provide default host
        self.dbuser = "bwm"
        self.dbpassword = "bwm"
        self.loglevel = "info"
        self.logpath = "log/bwm.log"

    def get_env_conf(self):
        try:
            self.speedtest_server = environ["SPEEDTEST_SERVER"]
            self.interval = environ["INTERVAL"]
            self.dbtype = environ["DBTYPE"]
            self.datapath = environ["DATAPATH"]
            self.dbhost = environ["DBHOST"]
            self.dbuser = environ["DBUSER"]
            self.dbpassword = environ["DBPASSWORD"]
            self.loglevel = environ["LOGLEVEL"]
            self.logpath = environ["LOGPATH"]
        except KeyError:
            pass

    def get_file_conf(self):
        try:
            self.config_file.read(self.config_file_path)

            self.speedtest_server = self.config_file["General"]["speedtest-server"]
            self.interval = self.config_file["General"]["interval"]
            self.dbtype = self.config_file["Database"]["type"]
            self.datapath = self.config_file["Database"]["datapath"]
            self.dbhost = self.config_file["Database"]["dbhost"]
            self.dbuser = self.config_file["Database"]["dbuser"]
            self.dbpassword = self.config_file["Database"]["dbpassword"]
            self.loglevel = self.config_file["log"]["loglevel"]
            self.logpath = self.config_file["log"]["logpath"]
        except configparser.ParsingError:
            pass
        except configparser.NoSectionError:
            pass
        except configparser.NoOptionError:
            pass