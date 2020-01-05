#!/usr/bin/env python3.7

__author__ = 'racoon63 <racoon63@gmx.net>'

import json
import logging
import os
import sys
import time

import config
import data
import speedtest


def init():

    workdir = os.path.dirname(os.path.abspath(__file__)) + "/"

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

if __name__ == "__main__":    
    
    try:
        
        init()

        if "LOGLEVEL" in os.environ:
            loglevel = os.environ["LOGLEVEL"].lower()
        else:
            loglevel = "info"
        
        if "LOGPATH" in os.environ:
            logpath = os.environ["LOGPATH"].lower()
        else:
            logpath = "../log/bwm.log"
        
        level = {
            "debug":    logging.DEBUG,
            "info":     logging.INFO,
            "warning":  logging.WARNING,
            "error":    logging.ERROR,
            "critical": logging.CRITICAL
        }

        logging.basicConfig(format='[%(asctime)s] %(levelname)s: %(message)s',
                            level=level[loglevel],
                            datefmt='%Y-%m-%d %H:%M:%S',
                            handlers=[
                                logging.FileHandler(logpath),
                                logging.StreamHandler()
                            ])

        conf = config.Config()
        
        speedtest_server = conf.speedtest_server
        interval         = conf.interval
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
        """
        if dbtype == "tinydb":
            from database import tinydb

            db = tinydb.Tinydb(datapath)

        elif dbtype == "mongodb":
            from database import mongodb

            db = mongodb.Mongodb(dbhost, dbuser, dbpassword)

        else:"""
        db = data.Data(datapath)
        test = speedtest.Speedtest(speedtest_server)

    except Exception as err:
        logging.critical(err)
        sys.exit(1)
    
    else:
        logging.info('Bandwidth-Monitor service started')

    while True:
        
        try:
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

            data_object = db.create_data_object(ts, ping, download, upload)
            db.append(data_object)
            db.write()

            time.sleep(interval - ((time.time() - starttime) % interval))

        except KeyboardInterrupt:
            logging.info('Bandwidth-Monitor was stopped by user')
            sys.exit(0)

        except Exception as err:
            logging.critical(err)
            sys.exit(1)
