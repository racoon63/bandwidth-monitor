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


def init(workdir):

    datadir = workdir + "../data"
    logdir  = workdir + "../log"

    if not os.path.exists(datadir):
        os.makedirs(datadir, exist_ok=True)

    if not os.path.exists(logdir):
        os.makedirs(logdir, exist_ok=True)


if __name__ == "__main__":    
    
    try:
        workdir = os.path.dirname(os.path.abspath(__file__)) + "/"

        init(workdir)

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

        d = data.Data(datapath)

    except Exception as err:
        logging.critical(err)
        sys.exit(1)
    
    else:
        logging.info('Bandwidth-Monitor service started')

    while True:
        
        try:
            starttime = time.time()
            
            bwtest = speedtest.Speedtest()

            timestamp = bwtest.timestamp
            ping      = bwtest.ping
            download  = bwtest.download
            upload    = bwtest.upload
            
            c_year   = time.gmtime().tm_year
            c_month  = time.gmtime().tm_mon
            c_day    = time.gmtime().tm_mday
            c_hour   = time.gmtime().tm_hour
            c_minute = time.gmtime().tm_min
            c_second = time.gmtime().tm_sec

            data_object = d.create_data_object(timestamp, ping, download, upload)
            d.append(data_object)
            d.write()

            time.sleep(60.0 - ((time.time() - starttime) % 60.0))

        except KeyboardInterrupt:
            logging.info('Bandwidth-Monitor was stopped by user')
            sys.exit(0)

        except Exception as err:
            logging.critical(err)
            sys.exit(1)
