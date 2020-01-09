#!/usr/bin/env python3.7

__author__ = "racoon63 <racoon63@gmx.net>"

import json
import logging
import os
import sys
import time

import config
import data
import speedtest


def init(workdir):

    datadir = workdir + "../data"
    logdir  = workdir + "../log"

    if not os.path.exists(datadir):
        os.makedirs(datadir, exist_ok=True)

    if not os.path.exists(logdir):
        os.makedirs(logdir, exist_ok=True)


def leading_zero(number):
    
    if len(str(number)) == 1:
        return "{}{}".format(0, number)
    else:
        return number


def create_data_object(timestamp, ping, download, upload):

    try:
        logging.debug("Creating new data object")
        data_object = {
            "timestamp" : timestamp, 
            "ping" : ping, 
            "download" : download, 
            "upload" : upload
        }

    except:
        logging.debug("Could not create new data object")

    else:
        logging.debug("Created new object successfully")
        return data_object


if __name__ == "__main__":    
    
    try:
        workdir = os.path.dirname(os.path.abspath(__file__)) + "/"

        init(workdir)

        if "LOGLEVEL" in os.environ:
            loglevel = os.environ["LOGLEVEL"].lower()
        else:
            loglevel = "info"
        
        if "LOGPATH" in os.environ:
            logpath = os.environ["LOGPATH"]
        else:
            logpath = workdir + "../log/bwm.log"
        
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

        conf = config.Config()
        
        speedtest_server = conf.speedtest_server
        interval         = int(conf.interval)
        dbtype           = conf.dbtype
        datapath         = conf.datapath
        dbhost           = conf.dbhost
        dbuser           = conf.dbuser
        dbpassword       = conf.dbpassword
        logpath          = conf.logpath
        loglevel         = conf.loglevel.lower()

        logging.basicConfig(format='[%(asctime)s] %(levelname)s: %(message)s',
                            level=level[loglevel],
                            datefmt='%Y-%m-%d %H:%M:%S',
                            handlers=[
                                logging.FileHandler(logpath),
                                logging.StreamHandler()
                            ])

        if dbtype == "tinydb":
            from database import tiny

            db = tiny.Tiny(datapath)
            #db = data.Data(datapath)

        elif dbtype == "mongodb":
            from database import mongodb

            db = mongo.Mongo(dbhost, dbuser, dbpassword)

        test = speedtest.Speedtest(speedtest_server)

        logging.info("Bandwidth-Monitor started successfully")

        while True:

            starttime = time.time()
            
            test.run()

            timestamp = test.timestamp
            ping      = test.ping
            download  = test.download
            upload    = test.upload
            
            c_year   = leading_zero(time.gmtime().tm_year)
            c_month  = leading_zero(time.gmtime().tm_mon)
            c_day    = leading_zero(time.gmtime().tm_mday)
            c_hour   = leading_zero(time.gmtime().tm_hour)
            c_minute = leading_zero(time.gmtime().tm_min)
            c_second = leading_zero(time.gmtime().tm_sec)

            ts = "{}-{}-{}-{}-{}-{}".format(c_year, c_month, c_day, c_hour, c_minute, c_second)

            data_object = create_data_object(ts, ping, download, upload)
            db.insert(data_object)

            time.sleep(interval - ((time.time() - starttime) % interval))

    except KeyboardInterrupt:
        logging.info("Bandwidth-Monitor was stopped by user")
        sys.exit(0)

    except Exception as err:
        logging.exception(err)
        sys.exit(1)
