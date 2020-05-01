import logging
import os


logger = logging.getLogger(__name__)

def configure_logger(loglevel="info", logpath="log"):
    """Provides a custom logger for the Bandwidth-Monitor service:"""

    logfilepath = logpath + "/bwm.log"

    try:
        os.mkdir("log")
        loglevel = os.environ["LOGLEVEL"]
        logpath = os.environ["LOGPATH"]
    except KeyError:
        pass
    except FileExistsError:
        pass

    """Configures the handler and formatter for custom logger."""
    level = {
        "debug":    logging.DEBUG,
        "info":     logging.INFO,
        "warning":  logging.WARNING,
        "error":    logging.ERROR,
        "critical": logging.CRITICAL
    }

    formatter = logging.Formatter('%(asctime)-22s %(levelname)-11s %(message)s', datefmt="%Y-%m-%dT%H:%M:%SZ")

    output_handler = logging.StreamHandler()
    output_handler.setFormatter(formatter)

    file_handler = logging.FileHandler(logfilepath)
    file_handler.setFormatter(formatter)

    logger.setLevel(level[loglevel.lower()])
    logger.addHandler(output_handler)
    logger.addHandler(file_handler)

configure_logger()
