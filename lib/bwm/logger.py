#!/usr/bin/env python3

import logging


log = logging.getLogger(__name__)


def setup(loglevel="info", logpath="log/bwm.log"):
    
    level = {
        "debug":    logging.DEBUG,
        "info":     logging.INFO,
        "warning":  logging.WARNING,
        "error":    logging.ERROR,
        "critical": logging.CRITICAL
    }

    formatter = logging.Formatter('%(asctime)-22s %(levelname)-11s %(message)s', datefmt="%Y-%m-%d %H:%M:%S")

    output_handler = logging.StreamHandler()
    output_handler.setFormatter(formatter)

    file_handler = logging.FileHandler(logpath)
    file_handler.setFormatter(formatter)
    
    log.setLevel(level[loglevel.lower()])
    log.addHandler(output_handler)
    log.addHandler(file_handler)
