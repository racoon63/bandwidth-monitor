""" Provides a custom logger with that logs to stdout and a log file. """

import logging
import os


logger = logging.getLogger(__name__)

def configure_logger(loglevel="info", logpath="log"):
    """Provides a custom logger for the Bandwidth-Monitor service:"""

    logfilepath = logpath + "/bwm.log"

    env_vars = [
        ["LOGPATH", logpath],
        ["LOGLEVEL", loglevel]
    ]

    for var in env_vars:
        try:
            setattr(object, var[1], os.environ[var[0]])
        except KeyError:
            pass

    try:
        os.mkdir("log")
    except FileExistsError:
        pass

    level = {
        "debug":    logging.DEBUG,
        "info":     logging.INFO,
        "warning":  logging.WARNING,
        "error":    logging.ERROR,
        "critical": logging.CRITICAL
    }

    formatter = logging.Formatter('%(asctime)-22s %(levelname)-11s %(message)s',
                                  datefmt="%Y-%m-%dT%H:%M:%SZ")

    output_handler = logging.StreamHandler()
    output_handler.setFormatter(formatter)

    file_handler = logging.FileHandler(logfilepath)
    file_handler.setFormatter(formatter)

    logger.setLevel(level[loglevel.lower()])
    logger.addHandler(output_handler)
    logger.addHandler(file_handler)

configure_logger()
