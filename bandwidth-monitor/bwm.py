#!/usr/bin/env python3.7

__author__ = 'racoon <racoon63@gmx.net>'

import json
import logging
import time

#from bandwidth-monitor import config
from speedtest import Speedtest

#from bandwidth-monitor import handler
#from bandwidth-monitor import daily
#from bandwidth-monitor import monthly
#from bandwidth-monitor import yearly

if __name__ == "__main__":    
    
    logging.basicConfig(filename='speedtest-monitor.log', format='[%(asctime)s] %(levelname)s: %(message)s', level=logging.INFO, datefmt='%Y-%m-%d %H:%M:%S')

    while True:
        try:
            starttime = time.time()

            speedtest = Speedtest()

            timestamp = starttime
            ping      = speedtest.ping
            download  = speedtest.download
            upload    = speedtest.upload

            print(speedtest.json)
            print(timestamp)
            print(ping)
            print(download)
            print(upload)

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
            print('speedtest-monitor was stopped by user.')
            logging.info('speedtest-monitor was stopped by user.')
            exit(1)
