#!/usr/bin/env python3

import logging
import os


log = logging.getLogger(__name__)


def setup(loglevel="info", logpath="/bwm/log"):

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
        logpath = os.environ["LOGPATH"]

    try:
        os.mkdir(logpath)
    except Exception:
        logging.error("Could not create logging directory at {:s}", logpath)

    formatter = logging.Formatter('%(asctime)-22s %(levelname)-11s %(message)s', datefmt="%Y-%m-%d %H:%M:%S")

    output_handler = logging.StreamHandler()
    output_handler.setFormatter(formatter)

    file_handler = logging.FileHandler(logpath + "/bwm.log")
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