#!/usr/bin/env python3.7

import json
import logging
import subprocess
import time
from speedtest_json import speedtest_json
from speedtest_json.handler import handler

if __name__ == "__main__":    
    starttime = time.time()
    logging.basicConfig(filename='speedtest-monitor.log', format='%(asctime)s %(levelname)-8s %(message)s', level=logging.INFO, datefmt='%Y-%m-%d %H:%M:%S')

    while True:
        try:
            speedtest_json_object = speedtest_json.speedtest_json()

            timestamp = speedtest_json_object.get_timestamp()
            ping      = round(speedtest_json_object.get_ping(), 2)
            download  = round(((speedtest_json_object.get_download() / 1024) / 1024), 2)
            upload    = round(((speedtest_json_object.get_upload() / 1024) / 1024), 2)

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

            time.sleep(60.0 - ((time.time() - starttime) % 60.0))

        except KeyboardInterrupt:
            print('speedtest-monitor was stopped by user.')
            logging.info('speedtest-monitor was stopped by user.')
            exit(1)
        
