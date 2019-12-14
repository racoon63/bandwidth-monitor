#!/usr/bin/env python3.7

__author__ = 'racoon <racoon63@gmx.net>'

import copy
import logging
import json

class Day(object):

    def __init__(self, data_path, stats_path):
        self.data_path = data_path
        self.stats_path = stats_path
        self.data = {}
        self.stats = {}
        self.stats_template = {
            "time": {
                "runs_this_day": 0,
                "day_in_month": 0,
                "month_in_year": 0,
                "year": 0
            },
            "min_max": {
                "ping_max": 0,
                "ping_min": 0,
                "download_max": 0,
                "download_min": 0,
                "upload_max": 0,
                "upload_min": 0
            },
            "avg": {
                "ping_ms_days_avg": 0,
                "download_mbit_days_avg": 0,
                "upload_mbit_days_avg": 0
            }
        }
        self.data_template = {
            "timestamp": "",
            "ping": 0,
            "download": 0
            "upload": 0
        }
        outer = self
        
    def _create(self, path, template):
        try:
            with open(outer.data_path, "w") as stream:
                json.dump(self.data_template, stream)
        except Exception:
            logging.error("Cannot create file.")

    def _refresh(self):
        try:
            with open(self.data_path, "r") as stream:
                self.data = json.load(stream)
        
        except Exception:
            logging.error("Can not read data file.")

        try:
            with open(self.stats_path) as stream:
                self.stats = json.load(stream)
        except Exception:
            logging.error("Can not load stats file.")

    def _write(self, data, path):
        try:
            with open(path, "w") as stream:
                json.dump(data, stream)
        except Exception:
            logging.error("Can not write file.")

    def template

    class data(object):

        def __init__(self):
            pass

    class stats(object):

        def __init__(self):
            pass