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


if __name__ == "__main__":    
    
    loglevel = logging.INFO
    
    logging.basicConfig(#filename='/bwm/log/bandwidth-monitor.log', 
                        format='[%(asctime)s] %(levelname)s: %(message)s', 
                        level=loglevel, 
                        datefmt='%Y-%m-%d %H:%M:%S')

    d = data.Data('../data/data.json')
    
    logging.info('Bandwidth-Monitor service started.')
    
    while True:
        try:
            starttime = time.time()
            
            speedtest = speedtest.Speedtest()

            timestamp = speedtest.timestamp
            ping      = speedtest.ping
            download  = speedtest.download
            upload    = speedtest.upload
            
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
            logging.info('Bandwidth-Monitor was stopped by user.')
            sys.exit()
