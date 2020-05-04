""" Provides configuration feature for bwm service. """

from os import environ
import configparser


class Config:
    """Config class stores config values for the bwm service."""
    def __init__(self, config_file_path="config.ini"):
        self.config_file_path = config_file_path

        self.set_defaults()
        self.get_file_conf()
        self.get_env_conf()

    def set_defaults(self):
        """ Sets the default variable values. """
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
            self.loglevel = config_file["log"]["loglevel"]
            self.logpath = config_file["log"]["logpath"]
        except configparser.ParsingError:
            pass
        except configparser.NoSectionError:
            pass
        except configparser.NoOptionError:
            pass

    @property
    def speedtest_server(self):
        """ Returns the speedtest server config variable. """
        return self.speedtest_server

    @speedtest_server.setter
    def speedtest_server(self, value):
        """ Sets the speedtest server config variable. """
        if value == "auto" or value > 0 and value < 50000:
            self.speedtest_server = value
        else:
            raise KeyError("Speedtest server is not valid.")

    @property
    def interval(self):
        """ Returns the interval config variable. """
        return self.interval

    @interval.setter
    def interval(self, value):
        """ Sets the interval config variable. """
        self.interval = value
    
    @property
    def dbtype(self):
        """ Returns the dbtype config variable. """
        return self.dbtype

    @dbtype.setter
    def dbtype(self, value):
        """ Sets the dbtype config variable. """
        self.dbtype = value

    @property
    def datapath(self):
        """ Returns the datapath config variable. """
        return self.datapath

    @datapath.setter
    def datapath(self, value):
        """ Sets the datapath config variable. """
        self.datapath = value

    @property
    def dbhost(self):
        """ Returns the dbhost config variable. """
        return self.dbhost

    @dbhost.setter
    def dbhost(self, value):
        """ Sets the dbhost config variable. """
        self.dbhost = value

    @property
    def dbuser(self):
        """ Returns the dbuser config variable. """
        return self.dbuser

    @dbuser.setter
    def dbuser(self, value):
        """ Sets the dbuser config variable. """
        self.dbuser = value

    @property
    def dbpassword(self):
        """ Returns the dbpassword config variable. """
        return self.dbpassword

    @dbpassword.setter
    def dbpassword(self, value):
        """ Sets the dbpassword config variable. """
        self.dbpassword = value

    @property
    def loglevel(self):
        """ Returns the loglevel config variable. """
        return self.loglevel

    @loglevel.setter
    def loglevel(self, value):
        """ Sets the loglevel config variable. """
        self.loglevel = value

    @property
    def logpath(self):
        """ Returns the logpath config variable. """
        return self.logpath

    @logpath.setter
    def logpath(self, value):
        """ Sets the logpath config variable. """
        self.logpath = value
