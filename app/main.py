#!/usr/bin/env python3

""" Bandwidth-Monitor is a tool to measure your internet speed. """

from bwm import BandwidthMonitor
from log import logger

def main():
    """ This is the entrypoint for the Bandwidth-Monitor service. """
    try:
        BandwidthMonitor.run()
    except KeyboardInterrupt:
        logger.info("Bandwidth-Monitor service was stopped by user")

if __name__ == "__main__":
    main()