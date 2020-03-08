#!/usr/bin/env python3

import logging
import os


class Logger(object):

    def __init__(self, loglevel="info", logpath="../../log"):
        
        self.loglevel = loglevel
        self.logpath = logpath

        self.loglevel = self.get_env_loglevel()
        self.logpath = self.get_env_logpath()
        
        level = {
            "debug":    logging.DEBUG,
            "info":     logging.INFO,
            "warning":  logging.WARNING,
            "error":    logging.ERROR,
            "critical": logging.CRITICAL
        }

        logging.basicConfig(format="[%(asctime)s] %(levelname)s: %(message)s",
                        level=level[loglevel],
                        datefmt="%Y-%m-%d %H:%M:%S",
                        handlers=[
                            logging.FileHandler(logpath),
                            logging.StreamHandler()
                        ])


    def get_env_loglevel(self):

        if "LOGLEVEL" in os.environ:
            return os.environ["LOGLEVEL"].lower()
        else:
            return "info"


    def get_env_logpath(self):

        if "LOGPATH" in os.environ:
            return os.environ["LOGPATH"]
        else:
            return "../../log/bwm.log"