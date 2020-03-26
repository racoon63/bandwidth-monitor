#!/usr/bin/env python3

import logging
import os


log = logging.getLogger(__name__)


def setup(loglevel="info", logpath="log/bwm.log"):

    level = {
        "debug":    logging.DEBUG,
        "info":     logging.INFO,
        "warning":  logging.WARNING,
        "error":    logging.ERROR,
        "critical": logging.CRITICAL
    }

    if "LOGLEVEL" in os.environ:
        loglevel = os.environ["LOGLEVEL"]

    if "LOGPATH" in os.environ:
        loglevel = os.environ["LOGPATH"]

    formatter = logging.Formatter('%(asctime)-22s %(levelname)-11s %(message)s', datefmt="%Y-%m-%d %H:%M:%S")

    output_handler = logging.StreamHandler()
    output_handler.setFormatter(formatter)

    file_handler = logging.FileHandler(logpath)
    file_handler.setFormatter(formatter)
    
    log.setLevel(level[loglevel.lower()])
    log.addHandler(output_handler)
    log.addHandler(file_handler)
    return

def reset():
    global log
    del log
    globals()['log'] = logging.getLogger(__name__)
    return