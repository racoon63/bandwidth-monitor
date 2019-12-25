#!/usr/bin/env python3.7

__author__ = 'racoon63 <racoon63@gmx.net>'

import json
import logging
import sys
import time

from speedtest import Speedtest

import data

if __name__ == "__main__":    
    
    logging.basicConfig(#filename='/bwm/log/bandwidth-monitor.log', 
                        format='[%(asctime)s] %(levelname)s: %(message)s', 
                        level=logging.INFO, 
                        datefmt='%Y-%m-%d %H:%M:%S')

    logging.info('Bandwidth-Monitor service started.')
    
    d = data.Data('../data/data.json')

    while True:
        try:
            starttime = time.time()
            
            speedtest = Speedtest()

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

            '''
            # handles current values into current.json
            current_data = handler.read_current()
            handler.write_current(current_data, timestamp, ping, download, upload)

            # handles data for the whole day in daily.json
            daily_data = handler.read_daily()

            # if day of daily.json is not current day then data have to be exported and daily resetted
            if time.strftime("%d") != daily_data['stats']['day_in_month']:
                handler.export_daily(daily_data)
                handler.reset_daily()
                handler.reset_current()

            daily_data = handler.update_daily(daily_data, timestamp, ping, download, upload)
            handler.write_daily(daily_data)

            logging.info("Wrote values to file successfully!")
            '''

            time.sleep(60.0 - ((time.time() - starttime) % 60.0))

        except KeyboardInterrupt:
            logging.info('Bandwidth-Monitor was stopped by user.')
            sys.exit('Bandwidth-Monitor was stopped by user.')
