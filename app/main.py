#!/usr/bin/env python3

__author__ = "racoon63 <racoon63@gmx.net>"

from .bwm import BandwidthMonitor


if __name__ == "__main__":

    bwm = BandwidthMonitor()
    bwm.run()
