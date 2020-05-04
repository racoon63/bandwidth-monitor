""" Provides configuration feature for bwm service. """

import configparser
from os import environ
from os.path import isfile

from log import logger

class Config:
    """ Config class stores config values for the bwm service. """
    def __init__(self, config_file_path="config.ini"):
        logger.debug("Getting config")
        self.config_file_path = config_file_path
        try:
            self.get_file_conf()
            self.get_env_conf()
        except ValueError as err:
            logger.error(err)

    def get_env_conf(self):
        """ Sets config values from available environment variables. """
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
        """ Sets config values from the config.ini file. """
        try:
            config_file = configparser.ConfigParser(
                empty_lines_in_values=False)
            config_file.read(self.config_file_path)

            self.speedtest_server = config_file["General"]["speedtest-server"]
            self.interval = config_file["General"]["interval"]
            self.dbtype = config_file["Database"]["type"]
            self.datapath = config_file["Database"]["datapath"]
            self.dbhost = config_file["Database"]["dbhost"]
            self.dbuser = config_file["Database"]["dbuser"]
            self.dbpassword = config_file["Database"]["dbpassword"]
            self.loglevel = config_file["Logging"]["loglevel"]
            self.logpath = config_file["Logging"]["logpath"]
        except configparser.ParsingError:
            pass
        except configparser.NoSectionError:
            pass
        except configparser.NoOptionError:
            pass

    @property
    def speedtest_server(self):
        """ Returns the speedtest server config variable. """
        return self._speedtest_server

    @speedtest_server.setter
    def speedtest_server(self, value):
        """ Sets the speedtest server config variable. """
        if value is None or not value:
            self._speedtest_server = None
        elif int(value) < 0 or int(value) > 50000:
            raise ValueError("Speedtest server is not valid.")
        else:
            self._speedtest_server = value
        logger.debug("Speedtest server is: {}".format(self.speedtest_server))

    @property
    def interval(self):
        """ Returns the interval config variable. """
        return self._interval

    @interval.setter
    def interval(self, value):
        """ Sets the interval config variable. """
        if value is None or not value:
            self._interval = 60
        elif value and value < 30:
            raise ValueError("Interval can not be less than 30.")
        else:
            self._interval = value
        logger.debug("Interval is: {}".format(self.interval))

    @property
    def dbtype(self):
        """ Returns the dbtype config variable. """
        return self._dbtype

    @dbtype.setter
    def dbtype(self, value):
        """ Sets the dbtype config variable. """
        if value is None or not value:
            self._dbtype = "tinydb"
        elif value != "tinydb" or value != "mongodb" or value != "influxdb":
            raise ValueError("dbtype have to be: tinydb, mongodb or influxdb.")
        else:
            self._dbtype = value
        logger.debug("DBtype is: {}".format(self.dbtype))

    @property
    def datapath(self):
        """ Returns the datapath config variable. """
        return self._datapath

    @datapath.setter
    def datapath(self, value):
        """ Sets the datapath config variable. """
        if value is None or not value:
            self._datapath = "data/bwm.json"
        elif not isfile(value):
            raise ValueError("Datapath can not be found.")
        else:
            self._datapath = value
        logger.debug("Datapath is: {}".format(self.datapath))

    @property
    def dbhost(self):
        """ Returns the dbhost config variable. """
        return self._dbhost

    @dbhost.setter
    def dbhost(self, value):
        """ Sets the dbhost config variable. """
        if value is None or not value:
            self._dbhost = "bwm"
        else:
            self._dbhost = value
        logger.debug("DBhost is: {}".format(self.dbhost))

    @property
    def dbuser(self):
        """ Returns the dbuser config variable. """
        return self._dbuser

    @dbuser.setter
    def dbuser(self, value):
        """ Sets the dbuser config variable. """
        if value is None or not value:
            self._dbuser = "bwm"
        else:
            self._dbuser = value
        logger.debug("DBuser is: {}".format(self.dbuser))

    @property
    def dbpassword(self):
        """ Returns the dbpassword config variable. """
        return self._dbpassword

    @dbpassword.setter
    def dbpassword(self, value):
        """ Sets the dbpassword config variable. """
        if value is None or not value:
            self._dbpassword = "bwm"
        else:
            self._dbpassword = value
        logger.debug("DBpassword is: {}".format(self.dbpassword))

    @property
    def loglevel(self):
        """ Returns the loglevel config variable. """
        return self._loglevel

    @loglevel.setter
    def loglevel(self, value):
        """ Sets the loglevel config variable. """
        if value is None or not value:
            self._loglevel = "info"
        elif value.lower() not in ["info", "warning", "error", "fatal", "critical"]:
            raise ValueError("No valid loglevel specified.")
        else:
            self._loglevel = value
        logger.debug("Loglevel is: {}".format(self.loglevel))

    @property
    def logpath(self):
        """ Returns the logpath config variable. """
        return self._logpath

    @logpath.setter
    def logpath(self, value):
        """ Sets the logpath config variable. """
        if value is None or not value:
            self._logpath = "log/bwm.log"
        elif not isfile(value):
            raise ValueError("Logpath can not be found.")
        else:
            self._logpath = value
        logger.debug("Logpath is: {}".format(self.logpath))
