""" Provides configuration feature for bwm service. """

import configparser
import os
import sys

from log import logger

class Config:
    """ Config class stores config values for the bwm service. """
    def __init__(self, config_file_path="config.ini"):
        logger.debug("Getting config")
        self.config_file_path = config_file_path

        try:
            self.get_file_conf()
            self.get_env_conf()
            self.print_config()
        except Exception as err:
            logger.critical("Config could not be processed correctly.")
            logger.error(err)
            sys.exit(1)

    def get_file_conf(self):
        """ Sets config values from the config.ini file. """
        try:
            config_file = configparser.ConfigParser(
                empty_lines_in_values=False)
            config_file.read(self.config_file_path)
        except configparser.ParsingError:
            logger.error("Could not read config file")

        sections = ["General", "Database", "Logging"]
        options = ["speedtest-server",
                   "interval",
                   "dbtype",
                   "datapath",
                   "dbhost",
                   "dbuser",
                   "dbpassword",
                   "logpath",
                   "loglevel"]

        conf_vars = [
            [sections[0], options[0], "speedtest_server"],
            [sections[0], options[1], "interval"],
            [sections[1], options[2], "dbtype"],
            [sections[1], options[3], "datapath"],
            [sections[1], options[4], "dbhost"],
            [sections[1], options[5], "dbuser"],
            [sections[1], options[6], "dbpassword"],
            [sections[2], options[7], "logpath"],
            [sections[2], options[8], "loglevel"]
        ]

        for var in conf_vars:
            try:
                setattr(self, var[2], config_file[var[0]][var[1]])
            except KeyError:
                logger.debug("Option {} is not present in {}".format(
                    var[1],
                    self.config_file_path))
                setattr(self, var[2], None)

    def get_env_conf(self):
        """ Sets config values from available environment variables. """
        env_vars = [
            ["SPEEDTEST_SERVER", "speedtest_server"],
            ["INTERVAL", "interval"],
            ["DBTYPE", "dbtype"],
            ["DATAPATH", "datapath"],
            ["DBHOST", "dbhost"],
            ["DBUSER", "dbuser"],
            ["DBPASSWORD", "dbpassword"],
            ["LOGLEVEL", "loglevel"],
            ["LOGPATH", "logpath"]
        ]

        for var in env_vars:
            try:
                setattr(self, var[1], os.environ[var[0]])
            except KeyError:
                logger.debug("Environment variable {} is not set".format(var[0]))

    def print_config(self):
        """ Prints the set config for debugging purposes. """
        logger.debug("Speedtest server is: {}".format(self.speedtest_server))
        logger.debug("Interval is: {}".format(self.interval))
        logger.debug("DBtype is: {}".format(self.dbtype))
        logger.debug("Datapath is: {}".format(self.datapath))
        logger.debug("DBhost is: {}".format(self.dbhost))
        logger.debug("DBuser is: {}".format(self.dbuser))
        logger.debug("DBpassword is: {}".format(self.dbpassword))
        logger.debug("Loglevel is: {}".format(self.loglevel))
        logger.debug("Logpath is: {}".format(self.logpath))

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

    @property
    def interval(self):
        """ Returns the interval config variable. """
        return int(self._interval)

    @interval.setter
    def interval(self, value):
        """ Sets the interval config variable. """
        if value is None or not value:
            self._interval = 60
        elif value and int(value) < 30:
            raise ValueError("Interval can not be less than 30.")
        else:
            self._interval = value

    @property
    def dbtype(self):
        """ Returns the dbtype config variable. """
        return self._dbtype

    @dbtype.setter
    def dbtype(self, value):
        """ Sets the dbtype config variable. """
        if value is None or not value:
            self._dbtype = "tinydb"
        elif value not in ["tinydb", "mongodb", "influxdb"]:
            raise ValueError("dbtype has to be: tinydb or influxdb.")
        else:
            self._dbtype = value

    @property
    def datapath(self):
        """ Returns the datapath config variable. """
        return self._datapath

    @datapath.setter
    def datapath(self, value):
        """ Sets the datapath config variable. """
        if value is None or not value:
            self._datapath = "data/bwm.json"
        elif not os.path.isfile(value):
            raise ValueError("Datapath can not be found.")
        else:
            self._datapath = value

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

    @property
    def logpath(self):
        """ Returns the logpath config variable. """
        return self._logpath

    @logpath.setter
    def logpath(self, value):
        """ Sets the logpath config variable. """
        if value is None or not value:
            self._logpath = "log/bwm.log"
        elif not os.path.isfile(value):
            raise ValueError("Logpath can not be found.")
        else:
            self._logpath = value
