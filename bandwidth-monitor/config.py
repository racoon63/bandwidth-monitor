#!/usr/bin/env python3.7

__author__ = 'racoon63 <racoon63@gmx.net>'

import configparser
import logging
import os
import sys


class Config(object):

    def __init__(self):

        try:

            self.workdir = os.path.dirname(os.path.abspath(__file__)) + "/"

            self.speedtest_server = "auto"
            self.interval   = 60
            
            self.dbtype   = "tinydb"
            self.datapath   = self.workdir + "../data/data.json"
            self.dbhost     = None
            self.dbuser     = None
            self.dbpassword = None
            
            self.loglevel   = "info"
            self.logpath    = self.workdir + "../log/bwm.log"

            self.config_path   = self.config_path()
            self.config_exists = self.check()
            
            self.config = configparser.ConfigParser()

            if self.config_exists:
                self.read()            
            else:
                self.create()

                if self.config_exists:
                    self.config = self.read()
                else:
                    logging.critical("Could not create and read config file.")
                    sys.exit(1)

        except Exception as err:
            logging.critical(err)


    def envval(self, env_name):

        if env_name in os.environ:
            logging.debug("Environment variable '{}' is set.".format(env_name))
            logging.debug("Environment variable '{}' is: {}".format(env_name, os.environ[env_name]))
            return os.environ[env_name]
        else:
            logging.debug("Environment variable '{}' is not set.".format(env_name))
            return


    def config_path(self):
        
        if self.envval("CONFIG_PATH"):
            return self.envval("CONFIG_PATH")
        else:
            return self.workdir + "../config.ini"


    def check(self):
        
        try:
            logging.debug("Check if config file exists.")
            logging.debug("Set config file path is: " + self.config_path)

            if os.path.exists(self.config_path) and os.path.isfile(self.config_path):
                logging.info("Config file found.")
                return True
            else:
                logging.error("Config file could not be found.")
                return False
        
        except Exception as err:
            logging.error(err)

        else:
            return False


    def read(self):
        try:
            logging.debug("Trying to read config file.")
            
            self.config.read(self.config_path)
            
        except Exception as err:
            logging.error(err)

        else:
            logging.debug("Finished reading config file.")
            self.validate()
            self.update()

        finally:
            return


    def write(self):
        try:
            with open(self.config_path, 'w') as config:
                config.write(self.config)
        
        except Exception:
            logging.critical("Could not write config to file.")
            sys.exit(1)


    def update(self):
        
        try:

            if self.config.has_option("General", "speedtest-server"):
                self.speedtest_server = self.config["General"]["speedtest-server"]
            if self.envval("SPEEDTEST_SERVER"):
                self.speedtest_server = self.envval("SPEEDTEST_SERVER")

            if self.config.has_option("General", "interval"):
                self.interval = self.config["General"]["interval"]
            if self.envval("INTERVAL"):
                self.interval = self.envval("INTERVAL")
            
            if self.config.has_option("Database", "type"):
                self.dbtype = self.config["Database"]["type"]
            if self.envval("DBTYPE"):
                self.dbtype = self.envval("DBTYPE")

            if self.dbtype == "tinydb":
                if self.config.has_option("Database", "datapath"):
                    self.datapath = self.config["Database"]["datapath"]
                if self.envval("DATAPATH"):
                    self.datapath = self.envval("DATAPATH")
            
            if self.dbtype == "mongodb":
                if self.config.has_option("Database", "host"):
                    self.datapath = self.config["Database"]["host"]
                elif self.envval("DBHOST"):
                    self.datapath = self.envval("DBHOST")
                else:
                    logging.critical("No database host defined.")
                    sys.exit(1)
                
                if self.config.has_option("Database", "user"):
                    self.datapath = self.config["Database"]["user"]
                elif self.envval("DBUSER"):
                    self.datapath = self.envval("DBUSER")
                else:
                    logging.critical("No database user defined.")
                    sys.exit(1)

                if self.config.has_option("Database", "password"):
                    self.datapath = self.config["Database"]["password"]
                elif self.envval("DBPASSWORD"):
                    self.datapath = self.envval("DBPASSWORD")
                else:
                    logging.critical("No database password defined.")
                    sys.exit(1)

            if self.config.has_option("Logging", "logpath"):
                self.dbtype = self.config["Logging"]["logpath"]
            if self.envval("LOGPATH"):
                self.dbtype = self.envval("LOGPATH")

            if self.config.has_option("Logging", "loglevel"):
                self.dbtype = self.config["Logging"]["loglevel"]
            if self.envval("LOGLEVEL"):
                self.dbtype = self.envval("LOGLEVEL")

        except Exception:
            pass


    def create(self):
        try:
            logging.debug("Trying to generate config file.")
            
            logging.debug("Adding section 'General'.")
            self.config.add_section("General")

            logging.debug("Adding section 'Database'.")
            self.config.add_section("Database")

            logging.debug("Adding section 'Logging'.")
            self.config.add_section("Logging")

            if "SPEEDTEST_SERVER" in os.environ:
                logging.debug("Environment variable 'SPEEDTEST_SERVER' is set.")
                logging.debug("Environment variable 'SPEEDTEST_SERVER' is: " + os.environ["SPEEDTEST_SERVER"])
                self.speedtest_server = os.environ["SPEEDTEST_SERVER"]
            else:
                logging.debug("Environment variable 'SPEEDTEST_SERVER' is not set.")

            if "INTERVAL" in os.environ:
                logging.debug("Environment variable 'INTERVAL' is set.")
                logging.debug("Environment variable 'INTERVAL' is: " + os.environ["INTERVAL"])
                self.interval = os.environ["INTERVAL"]
            else:
                logging.debug("Environment variable 'INTERVAL' is not set.")

            self.config['General'] = {'speedtest-server': self.speedtest_server,
                                 'interval': self.interval}

            self.config['Database'] = {}

            if "DATABASE" in os.environ:
                logging.debug("Environment variable 'DATABASE' is set.")
                logging.debug("Environment variable 'DATABASE' is: " + os.environ["DATABASE"])
                self.database = os.environ["DATABASE"]
                self.config['Database']['database'] = self.database
            else:
                logging.debug("Environment variable 'DATABASE' is not set.")
                self.config['Database']['database'] = self.database

            if self.database == "tinydb":
                if "DATAPATH" in os.environ:
                    logging.debug("Environment variable 'DATAPATH' is set.")
                    logging.debug("Environment variable 'DATAPATH' is: " + os.environ["DATAPATH"])
                    self.datapath = os.environ["DATAPATH"]
                    self.config['Database']['datapath'] = self.datapath
                else:
                    logging.debug("Environment variable 'DATAPATH' is not set.")
                    self.config['Database']['datapath'] = self.datapath
            
            if self.database == "mongodb":
                if "DBHOST" in os.environ:
                    logging.debug("Environment variable 'DBHOST' is set.")
                    logging.debug("Environment variable 'DBHOST' is: " + os.environ["DBHOST"])
                    self.dbhost = os.environ["DBHOST"]
                    self.config['Database']['dbhost'] = self.dbhost
                else:
                    logging.critical("Environment variable 'DBHOST' is not set. Can not proceed.")
                    sys.exit(1)
                
                if "DBUSER" in os.environ:
                    logging.debug("Environment variable 'DBUSER' is available.")
                    logging.debug("Environment variable 'DBUSER' is: " + os.environ["DBUSER"])
                    self.dbuser = os.environ["DBUSER"]
                    self.config['Database']['dbuser'] = self.dbuser
                else:
                    logging.critical("Environment variable 'DBUSER' is not set. Can not proceed.")
                    sys.exit(1)
            
                if "DBPASSWORD" in os.environ:
                    logging.debug("Environment variable 'DBPASSWORD' is set.")
                    logging.debug("Environment variable 'DBPASSWORD' is: Haha don't tell you here!")
                    self.dbpassword = os.environ["DBPASSWORD"]
                    self.config['Database']['dbpassword'] = self.dbpassword
                else:
                    logging.critical("Environment variable 'DBPASSWORD' is not set. Can not proceed.")
                    sys.exit(1)
            
            self.config['Logging'] = {}

            if "LOGLEVEL" in os.environ:
                logging.debug("Environment variable 'LOGLEVEL' is set.")
                logging.debug("Environment variable 'LOGLEVEL' is: " + os.environ["LOGLEVEL"])
                self.loglevel = os.environ["LOGLEVEL"]
                self.config['Logging']['loglevel'] = self.loglevel
            else:
                logging.debug("Environment variable 'LOGLEVEL' is not set.")
                config['Logging']['loglevel'] = self.loglevel

            if "LOGPATH" in os.environ:
                logging.debug("Environment variable 'LOGPATH' is set.")
                logging.debug("Environment variable 'LOGPATH' is: " + os.environ["LOGPATH"])
                self.logpath = os.environ["LOGPATH"]
                self.config['Logging']['logpath'] = self.logpath
            else:
                logging.debug("Environment variable 'LOGPATH' is not set.")
                self.config['Logging']['logpath'] = self.logpath

        except Exception as err:
            logging.fatal("Something went horribly wrong and I don't know what")
            print("""
                ⠄⢀⣀⣤⣴⣶⣶⣤⣄⡀⠄⠄⣀⣤⣤⣤⣤⡀⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄
                ⣴⣏⣹⣿⠿⠿⠿⠿⢿⣿⣄⢿⣿⣿⣿⣿⣿⣋⣷⡄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄
                ⣿⢟⣩⣶⣾⣿⣿⣿⣶⣮⣭⡂⢛⣭⣭⣭⣭⣭⣍⣛⣂⡀⠄⠄⠄⠄⠄⠄⠄⠄
                ⣿⣿⣿⣿⡿⢟⣫⣭⣷⣶⣾⣭⣼⡻⢛⣛⣭⣭⣶⣶⣬⣭⣅⡀⠄⠄⠄⠄⠄⠄
                ⣿⡿⢏⣵⣾⣿⣿⣿⡿⢉⡉⠙⢿⣇⢻⣿⣿⣿⣿⡟⠉⠉⢻⡷⠄⠄⠄⠄⠄⠄
                ⣿⣷⣾⣍⣛⢿⣿⣿⣿⣤⣁⣤⣿⢏⠸⣿⣿⣿⣿⣷⣬⣥⣾⠁⣿⣿⣷⠄⠄⠄
                ⣿⣿⣿⣿⣭⣕⣒⠿⠭⠭⠭⡷⢖⣫⣶⣶⣬⣭⣭⣭⣭⣥⡶⢣⣿⣿⣿⠄⠄⠄
                ⣿⣿⣿⣿⣿⣿⣿⡿⣟⣛⣭⣾⣿⣿⣿⣝⡛⣿⢟⣛⣛⣁⣀⣸⣿⣿⣿⣀⣀⣀
                ⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
                ⣿⡿⢛⣛⣛⣛⣙⣛⠿⠿⣿⣿⣿⣿⣿⣿⣿⣿⣬⣭⣭⠽⣛⢻⣿⣿⣿⠛⠛⠛
                ⣿⢰⣿⣿⣿⣿⣟⣛⣛⣶⠶⠶⠶⣦⣭⣭⣭⣭⣶⡶⠶⣾⠟⢸⣿⣿⣿⠄⠄⠄
                ⡻⢮⣭⣭⣭⣭⣉⣛⣛⡻⠿⠿⠷⠶⠶⠶⠶⣶⣶⣾⣿⠟⢣⣬⣛⡻⢱⣇⠄⠄
                ⣿⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣶⠶⠒⠄⠄⠄⢸⣿⢟⣫⡥⡆⠄⠄
                ⢭⣭⣝⣛⣛⣛⣛⣛⣛⣛⣿⣿⡿⢛⣋⡉⠁⠄⠄⠄⠄⠄⢸⣿⢸⣿⣧⡅⠄⠄
                ⣶⣶⣶⣭⣭⣭⣭⣭⣭⣵⣶⣶⣶⣿⣿⣿⣦⡀⠄⠄⠄⠄⠈⠡⣿⣿⡯⠁⠄⠄
                """)
            logging.critical(err)
            sys.exit(1)


    def validate(self):
        
        logging.debug("Validating config.")
        
        try:
            
            for section in ['General', 'Database']:
                logging.debug("Check if section is present: {}".format(section))
                self.config.has_section(section)
        
        except Exception as err:
            logging.critical(err)
            logging.critical("Config is not valid. Exiting...")
            sys.exit(1)
        
        else:
            logging.info("Config is valid.")
            return True
