#!/usr/bin/env python3.7

__author__ = 'racoon63 <racoon63@gmx.net>'

import configparser
import logging
import os
import sys


class Config(object):

    def __init__(self):

        try:
            # Set workdir
            self.workdir = os.path.dirname(os.path.abspath(__file__)) + "/"

            # Default values
            self.speedtest_server = "auto"
            self.interval         = 60
            
            self.dbtype           = "tinydb"
            self.datapath         = self.workdir + "../data/bwm.json"
            self.dbhost           = None
            self.dbuser           = None
            self.dbpassword       = None
            
            self.loglevel         = "info"
            self.logpath          = self.workdir + "../log/bwm.log"

            # Set configpath
            self.config_path = self._config_path()

            # Create config object
            self.config = configparser.ConfigParser(empty_lines_in_values=False)

            # Config flow
            if self._exists():
                self._read()
                self._validate()
                self._set_config_vals()
                self._set_env_vals()
                self._update()
            else:
                self._create()
                self._write()
                
                if self._exists():
                    self._read()
                    self._validate()
                    self._set_config_vals()
                    self._set_env_vals()
                    self._update()
                else:
                    logging.critical("Could not create and read config file")
                    sys.exit(1)

        except Exception as err:
            logging.critical(err)
            logging.critical("Dunno what happened but be pepe with you")
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
                return self.workdir + "../config.ini"

        except Exception as err:
            logging.critical(err)

    def _exists(self):
        
        try:
            logging.debug("Check if config file exists")
            logging.debug("Set config file path is: " + self.config_path)

            if os.path.exists(self.config_path) and os.path.isfile(self.config_path):
                logging.info("Config file found")
                return True
            else:
                logging.error("Config file could not be found")
                return False
        
        except Exception as err:
            logging.error(err)

        else:
            return False


    def _read(self):

        try:
            logging.debug("Trying to read config file")
            self.config.read(self.config_path)
            
        except Exception as err:
            logging.error(err)

        else:
            logging.debug("Read config file successfully")
            return


    def _create(self):

        try:
            logging.info("Generating config file")

            for section in ["General", "Database", "Logging"]:
                logging.debug("Adding section: {}.".format(section))
                self.config.add_section(section)

            if self._is_env_set("SPEEDTEST_SERVER"):
                self.config["General"]["speedtest-server"] = self._get_env_val("SPEEDTEST_SERVER")
            else:
                self.config["General"]["speedtest-server"] = self.speedtest_server

            if self._is_env_set("INTERVAL"):
                self.config["General"]["interval"] = self._get_env_val("INTERVAL")
            else:
                self.config["General"]["interval"] = str(self.interval)

            if self._is_env_set("DBTYPE"):
                self.config["Database"]["type"] = self._get_env_val("DBTYPE")
            else:
                self.config["Database"]["type"] = self.dbtype

            if self.config["Database"]["type"] == "tinydb":

                if self._is_env_set("DATAPATH"):
                    self.config["Database"]["datapath"] = self._get_env_val("DATAPATH")
                else:
                    self.config["Database"]["datapath"] = self.datapath

            elif self.config["Database"]["type"] == "mongodb":

                if self._is_env_set("DBHOST"):
                    self.config["Database"]["host"] = self._get_env_val("DBHOST")
                else:
                    logging.critical("Environment variable 'DBHOST' is not set. Can not proceed")
                    sys.exit(1)

                if self._is_env_set("DBUSER"):
                    self.config["Database"]["user"] = self._get_env_val("DBUSER")
                else:
                    logging.critical("Environment variable 'DBUSER' is not set. Can not proceed")
                    sys.exit(1)

                if self._is_env_set("DBPASSWORD"):
                    self.config["Database"]["password"] = self._get_env_val("DBPASSWORD")
                else:
                    logging.critical("Environment variable 'DBPASSWORD' is not set. Can not proceed")
                    sys.exit(1)

            if self._is_env_set("LOGPATH"):
                self.config["Logging"]["logpath"] = self._get_env_val("LOGPATH")
            else:
                self.config["Logging"]["logpath"] = self.logpath

            if self._is_env_set("LOGLEVEL"):
                self.config["Logging"]["loglevel"] = self._get_env_val("LOGLEVEL")
            else:
                self.config["Logging"]["loglevel"] = self.loglevel

        except Exception as err:
            logging.critical(err)
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
            logging.critical(err)
            sys.exit(1)

        else:
            logging.debug("Wrote config to file successfully")
            return


    def _validate(self):
        
        try:
            logging.debug("Validating config")

            if self.config.has_section("General"):

                if self.config.has_option("General", "speedtest-server") and self.config["General"]["speedtest-server"] != "":

                    if self.config["General"]["speedtest-server"] != "auto":
                        
                        if int(self.config["General"]["speedtest-server"]) == 0 or int(self.config["General"]["speedtest-server"]) > 50000:
                            raise ValueError("speedtest-server ID is not valid. ID is: {}".format(self.config["General"]["speedtest-server"]))
                
                else:
                    logging.debug("The option speedtest-server is not present or empty")
                
                if self.config.has_option("General", "interval") and self.config["General"]["interval"] != "":

                    if int(self.config["General"]["interval"]) < 30:
                        raise ValueError("The interval is lower than 30.")
                
                else:
                    logging.debug("The option interval is not present or empty")

            if self.config.has_section("Database"):

                if self.config.has_option("Database", "type") and self.config["Database"]["type"] != "":

                    if self.config["Database"]["type"] == "tinydb" or self.config["Database"]["type"] == "mongodb":

                        if self.config["Database"]["type"] == "tinydb":
                            logging.debug("Database type is: tinydb")
                            logging.debug("Check if option datapath is present")

                            if not self.config.has_option("Database", "datapath"):
                                raise ValueError("The required option 'tinydb' is not present")
                                
                            if self.config["Database"]["datapath"] == "":
                                raise ValueError("The required option datapath is empty")

                            logging.debug("All required options are present")

                        elif self.config["Database"]["type"] == "mongodb":
                            logging.debug("Database type is: mongodb")
                            logging.debug("Check if required database variables host, user and password are present")

                            if not self.config.has_option("Database", "host"):
                                raise ValueError("The required option 'host' is not present")

                            if self.config["Database"]["host"] == "":
                                raise ValueError("The required option host is empty")
                                
                            else:
                                logging.debug("Option database host is present and not empty")

                            if not self.config.has_option("Database", "user"):
                                raise ValueError("The required option 'user' is not present")

                            if self.config["Database"]["user"] == "":
                                raise ValueError("The required option user is empty")
                                
                            else:
                                logging.debug("Option database user is present and not empty")

                            if not self.config.has_option("Database", "password"):
                                raise ValueError("The required option password is not present")

                            if self.config["Database"]["password"] == "":
                                ("The required option password is empty")
                            
                            else:
                                logging.debug("Option database password is present and not empty")

                            logging.debug("All required options are present")

                    else:
                        raise ValueError("The database type is neither tinydb nor mongodb")

                else:
                    raise ValueError("The option database type is not present or empty")

            else:
                raise ValueError("The section Database is not present")

            if self.config.has_section("Logging"):

                if self.config["Logging"]["loglevel"].lower() != "info" and self.config["Logging"]["loglevel"].lower() != "warning" and self.config["Logging"]["loglevel"].lower() != "error" and self.config["Logging"]["loglevel"].lower() != "critical" and self.config["Logging"]["loglevel"].lower() != "debug":
                    logging.debug("Set loglevel is: {}".format(self.config["Logging"]["loglevel"].lower()))
                    raise ValueError("No valid loglevel was specified. Allowed loglevel are: info, warning, error, critical, debug")

        except ValueError as ve:
            logging.critical(ve)
            sys.exit(1)    
        
        except Exception as err:
            logging.exception(err)
            logging.critical("Config is not valid. Exiting")
            sys.exit(1)
        
        else:
            logging.info("Config is valid")
            return True


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
            logging.error(err)
            sys.exit(1)


    def _get_option_val(self, section, name):

        try:
            return self.config[section][name]

        except Exception as err:
            logging.error(err)
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
            logging.error(err)
        
        else:
            logging.debug("Set config variables successfully")
            return


    def _is_env_set(self, env_name):

        try:
            logging.debug("Check if environment variable '{}' is set".format(env_name))

            if env_name in os.environ:
                logging.debug("Environment variable '{}' is set".format(env_name))
                logging.debug("Environment variable '{}' is: {}".format(env_name, os.environ[env_name]))
                return True
            else:
                logging.debug("Environment variable '{}' is not set".format(env_name))
                return False
    
        except Exception as err:
            logging.error(err)


    def _get_env_val(self, env_name):

        try:
            return os.environ[env_name]

        except Exception as err:
            logging.error(err)


    def _set_env_vals(self):

        try:
            logging.debug("Set environment variable values")
            
            if self._is_env_set("SPEEDTEST-SERVER"):
                self.speedtest_server = self._get_env_val("SPEEDTEST-SERVER")

            if self._is_env_set("INTERVAL"):
                self.interval = self._get_env_val("INTERVAL")

            if self._is_env_set("TYPE"):
                self.dbtype = self._get_env_val("TYPE")

            if self._is_env_set("DATAPATH"):
                self.datapath = self._get_env_val("DATAPATH")

            if self._is_env_set("DBHOST"):
                self.dbhost = self._get_env_val("DBHOST")

            if self._is_env_set("DBUSER"):
                self.dbuser = self._get_env_val("DBUSER")

            if self._is_env_set("DBPASSWORD"):
                self.dbpassword = self._get_env_val("DBPASSWORD")

            if self._is_env_set("LOGPATH"):
                self.logpath = self._get_env_val("LOGPATH")

            if self._is_env_set("LOGLEVEL"):
                self.loglevel = self._get_env_val("LOGLEVEL")

        except Exception as err:
            logging.error(err)

        else:
            logging.debug("Set environment variable values successfully")
            return


    def _update(self):

        try:
            logging.debug("Updating config file")

            if self.speedtest_server:
                self.config["General"]["speedtest-server"] = self.speedtest_server
            
            if self.interval:
                self.config["General"]["interval"] = str(self.interval)

            if self.dbtype:
                self.config["Database"]["type"] = self.dbtype

            if self.datapath:
                self.config["Database"]["datapath"] = self.datapath

            if self.dbhost:
                self.config["Database"]["host"] = self.dbhost

            if self.dbuser:
                self.config["Database"]["user"] = self.dbuser

            if self.dbpassword:
                self.config["Database"]["password"] = self.dbpassword

            if self.loglevel:
                self.config["Logging"]["loglevel"] = self.loglevel

            if self.logpath:
                self.config["Logging"]["logpath"] = self.logpath

            self._write()

        except Exception as err:
            logging.error(err)

        else:
            logging.debug("Updated config file successfully")
            return
