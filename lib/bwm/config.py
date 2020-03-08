#!/usr/bin/env python3

__author__ = 'racoon63 <racoon63@gmx.net>'

import configparser
import hashlib
import logging
import os
import sys

from .database import mongo, tiny


class Defaults:

    def __init__(self, workdir):
        self.speedtest_server = "auto"
        self.interval         = 60
        
        self.dbtype           = "tinydb"
        self.datapath         = workdir + "/data/bwm.json"
        self.dbdriver         = tiny.Tiny(self.datapath)
        self.dbhost           = ""
        self.dbuser           = ""
        self.dbpassword       = ""
        
        self.loglevel         = "info"
        self.logpath          = workdir + "/log/bwm.log"

class Config(object):

    def __init__(self, workdir):
       
        self.workdir     = workdir
        self.defaults    = Defaults(self.workdir)
        self.config_path = self._config_path()
        self.config      = configparser.ConfigParser(empty_lines_in_values=False)

        self.speedtest_server = None
        self.interval         = None
        
        self.dbtype           = None
        self.datapath         = None
        self.dbhost           = None
        self.dbuser           = None
        self.dbpassword       = None
        self.dbdriver         = None
        
        self.loglevel         = None
        self.logpath          = None

        self._flow()

    def _flow(self):
        try:
            if not self._exists():
                self._set_env_vals()
                if self._is_valid():
                    self._generate()
                    self._write()
                else:
                    self._set_defaults()
                    if self._is_valid():
                        self._generate()
                        self._write()
                    else:
                        raise Exception("Config could not be created")

            else:
                self._read()
                self._set_config_vals()
                self._set_env_vals()
                if self._is_valid():
                    pass
            self._set_dbdriver()


        except Exception as err:
            logging.exception(err)
            logging.critical("Be pepe with you")
            print("""
                 ⢀⣀⣤⣴⣶⣶⣤⣄⡀  ⣀⣤⣤⣤⣤⡀
                ⣴⣏⣹⣿⠿⠿⠿⠿⢿⣿⣄⢿⣿⣿⣿⣿⣿⣋⣷⡄
                ⣿⢟⣩⣶⣾⣿⣿⣿⣶⣮⣭⡂⢛⣭⣭⣭⣭⣭⣍⣛⣂⡀
                ⣿⣿⣿⣿⡿⢟⣫⣭⣷⣶⣾⣭⣼⡻⢛⣛⣭⣭⣶⣶⣬⣭⣅⡀
                ⣿⡿⢏⣵⣾⣿⣿⣿⡿⢉⡉⠙⢿⣇⢻⣿⣿⣿⣿⡟⠉⠉⢻⡷
                ⣿⣷⣾⣍⣛⢿⣿⣿⣿⣤⣁⣤⣿⢏⠸⣿⣿⣿⣿⣷⣬⣥⣾⠁⣿⣿⣷
                ⣿⣿⣿⣿⣭⣕⣒⠿⠭⠭⠭⡷⢖⣫⣶⣶⣬⣭⣭⣭⣭⣥⡶⢣⣿⣿⣿
                ⣿⣿⣿⣿⣿⣿⣿⡿⣟⣛⣭⣾⣿⣿⣿⣝⡛⣿⢟⣛⣛⣁⣀⣸⣿⣿⣿⣀⣀⣀
                ⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
                ⣿⡿⢛⣛⣛⣛⣙⣛⠿⠿⣿⣿⣿⣿⣿⣿⣿⣿⣬⣭⣭⠽⣛⢻⣿⣿⣿⠛⠛⠛
                ⣿⢰⣿⣿⣿⣿⣟⣛⣛⣶⠶⠶⠶⣦⣭⣭⣭⣭⣶⡶⠶⣾⠟⢸⣿⣿⣿
                ⡻⢮⣭⣭⣭⣭⣉⣛⣛⡻⠿⠿⠷⠶⠶⠶⠶⣶⣶⣾⣿⠟⢣⣬⣛⡻⢱⣇
                ⣿⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣶⠶⠒    ⢸⣿⢟⣫⡥⡆
                ⢭⣭⣝⣛⣛⣛⣛⣛⣛⣛⣿⣿⡿⢛⣋⡉⠁      ⢸⣿⢸⣿⣧⡅
                ⣶⣶⣶⣭⣭⣭⣭⣭⣭⣵⣶⣶⣶⣿⣿⣿⣦⡀     ⠈⠡⣿⣿⡯⠁
                """)
            sys.exit(1)

    def _config_path(self):
        try:
            if self._is_env_set("CONFIG_PATH"):
                return self._get_env_val("CONFIG_PATH")
            else:
                return self.workdir + "/config.ini"

        except Exception as err:
            logging.exception(err)

    def _exists(self):
        try:
            logging.debug("Check if %s file exists", self.config_path)

            if os.path.exists(self.config_path) and os.path.isfile(self.config_path):
                logging.info("Config file found")
                return True
            else:
                logging.error("Config file could not be found")
                return False
        
        except Exception as err:
            logging.exception(err)

        else:
            return False

    def _read(self):
        try:
            logging.debug("Trying to read config file")
            self.config.read(self.config_path)
            
        except Exception as err:
            logging.exception(err)

        else:
            logging.debug("Red config file successfully")
            return

    def _generate(self):
        try:
            logging.info("Generating config file")

            for section in ["General", "Database", "Logging"]:
                logging.debug("Adding section: {}.".format(section))
                self.config.add_section(section)

            self.config["General"]["speedtest-server"] = self.speedtest_server
            self.config["General"]["interval"] = str(self.interval)
            self.config["Database"]["type"] = self.dbtype
            self.config["Database"]["datapath"] = self.datapath
            self.config["Database"]["dbhost"] = self.dbhost
            self.config["Database"]["dbuser"] = self.dbuser
            self.config["Database"]["dbpassword"] = self.dbpassword
            self.config["Logging"]["logpath"] = self.logpath
            self.config["Logging"]["loglevel"] = self.loglevel

        except Exception as err:
            logging.exception(err)
            sys.exit(1)

        else:
            logging.debug("Generated config successfully")
            return

    def _write(self):
        try: 
            logging.debug("Writing config to file")

            with open(self.config_path, "w") as config:
                self.config.write(config)
        
        except Exception as err:
            logging.critical("Could not write config to file")
            logging.exception(err)
            sys.exit(1)

        else:
            logging.debug("Wrote config to file successfully")
            return

    def _is_option_set(self, section, name):
        try:
            logging.debug("Check if option '{}' in section '{}' in config file is present and set".format(name, section))
            
            if self.config.has_option(section, name) and self.config[section][name] != "":
                logging.debug("Option '{}' is set and not empty".format(name))
                return True
            else:
                logging.debug("Option '{}' is not set or empty".format(name))
                return False

        except Exception as err:
            logging.exception(err)
            sys.exit(1)

    def _get_option_val(self, section, name):
        try:
            return self.config[section][name]

        except Exception as err:
            logging.exception(err)
            sys.exit(1)

    def _set_config_vals(self):
        try:
            logging.debug("Setting config variable values")
            
            if self._is_option_set("General", "speedtest-server"):
                self.speedtest_server = self._get_option_val("General", "speedtest-server")

            if self._is_option_set("General", "interval"):
                self.interval = self._get_option_val("General", "interval")

            if self._is_option_set("Database", "type"):
                self.dbtype = self._get_option_val("Database", "type")
            
            if self._is_option_set("Database", "datapath"):
                self.datapath = self._get_option_val("Database", "datapath")

            if self._is_option_set("Database", "host"):
                self.dbhost = self._get_option_val("Database", "host")

            if self._is_option_set("Database", "user"):
                self.dbuser = self._get_option_val("Database", "user")

            if self._is_option_set("Database", "password"):
                self.dbpassword = self._get_option_val("Database", "password")

            if self._is_option_set("Logging", "logpath"):
                self.logpath = self._get_option_val("Logging", "logpath")

            if self._is_option_set("Logging", "loglevel"):
                self.loglevel = self._get_option_val("Logging", "loglevel")

        except Exception as err:
            logging.exception(err)
        
        else:
            logging.debug("Set config variables successfully")
            return

    def _is_env_set(self, env_name):
        try:
            logging.debug("Check if environment variable '{}' is set".format(env_name))

            if env_name in os.environ and os.environ[env_name] != "":
                logging.debug("Environment variable '{}' is set".format(env_name))
                logging.debug("Environment variable '{}' is: {}".format(env_name, os.environ[env_name]))
                return True
            else:
                logging.debug("Environment variable '{}' is not set or empty".format(env_name))
                return False
    
        except Exception as err:
            logging.exception(err)

    def _get_env_val(self, env_name):
        try:
            return os.environ[env_name]
        except Exception as err:
            logging.exception(err)

    def _set_env_vals(self):
        try:
            logging.debug("Set environment variable values")
            
            if self._is_env_set("SPEEDTEST-SERVER"):
                self.speedtest_server = self._get_env_val("SPEEDTEST-SERVER")
            else:
                self.speedtest_server = self.defaults.speedtest_server

            if self._is_env_set("INTERVAL"):
                self.interval = self._get_env_val("INTERVAL")
            else:
                self.interval = self.defaults.interval

            if self._is_env_set("DBTYPE"):
                self.dbtype = self._get_env_val("DBTYPE")
            else:
                self.dbtype = self.defaults.dbtype

            if self._is_env_set("DATAPATH"):
                self.datapath = self._get_env_val("DATAPATH")
            else:
                self.datapath = self.defaults.datapath

            if self._is_env_set("DBHOST"):
                self.dbhost = self._get_env_val("DBHOST")
            else:
                self.dbhost = self.defaults.dbhost

            if self._is_env_set("DBUSER"):
                self.dbuser = self._get_env_val("DBUSER")
            else:
                self.dbuser = self.defaults.dbuser

            if self._is_env_set("DBPASSWORD"):
                self.dbpassword = self._get_env_val("DBPASSWORD")
            else:
                self.dbpassword = self.defaults.dbpassword

            if self._is_env_set("LOGPATH"):
                self.logpath = self._get_env_val("LOGPATH")
            else:
                self.logpath = self.defaults.logpath

            if self._is_env_set("LOGLEVEL"):
                self.loglevel = self._get_env_val("LOGLEVEL")
            else:
                self.loglevel = self.defaults.loglevel

        except Exception as err:
            logging.exception(err)

        else:
            logging.debug("Set environment variable values finished")
            return

    # Feature request: https://github.com/racoon63/bandwidth-monitor/issues/13
    """def get_file_hash(self, path):
        BLOCK_SIZE = 65536 # = 64 bytes

        file_hash = hashlib.sha256()
        with open(path, 'rb') as f:
            fb = f.read(BLOCK_SIZE)
            while len(fb) > 0:
                file_hash.update(fb)
                fb = f.read(BLOCK_SIZE)
        return file_hash.hexdigest()"""
    
    def _is_valid(self):

        try:
            logging.debug("Validate config")

            if self.speedtest_server == "auto" or int(self.speedtest_server) < 0 and int(self.speedtest_server) < 50000:
                pass
            else:
                raise ValueError

            if self.interval == "" or self.interval < 30:
                raise ValueError

            if self.dbtype == "" or self.dbtype != "tinydb" and self.dbtype != "mongodb":
                raise ValueError

            if self.dbtype == "tinydb":
                if self.datapath == "":
                    raise ValueError
            
            if self.dbtype == "mongodb":
                if self.dbhost == "" or self.dbuser == "" or self.dbpassword == "":
                    raise ValueError

            if self.logpath == "":
                raise ValueError

            lvl = ("info", "debug", "warning", "error", "critical")
            if not self.loglevel in lvl:
                raise ValueError

        except ValueError as err:
            logging.exception(err)
            logging.error("Config is not valid")
            return False
        
        else:
            logging.info("Config is valid")
            return True

    def _set_defaults(self):
        try:
            self.speedtest_server = self.defaults.speedtest_server
            self.interval = self.defaults.interval
            self.dbtype = self.defaults.dbtype
            self.datapath = self.defaults.datapath
            self.logpath = self.defaults.logpath
            self.loglevel = self.defaults.loglevel
        except Exception as err:
            logging.exception(err)
        else:
            logging.debug("Set default values successfully")
        finally:
            return

    def _set_dbdriver(self):
        if self.dbtype == "tinydb":
            self.dbdriver = tiny.Tiny(self.datapath)

        if self.dbtype == "mongodb":
            self.dbdriver = mongo.Mongo(self.dbhost, self.dbuser, self.dbpassword)
        
        return