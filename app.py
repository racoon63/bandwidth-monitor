#!/usr/bin/env python3.7

import json
import logging
import subprocess
import time
from speedtest_json import speedtest_json

def read_daily():
    try:
        with open('daily.json', 'r') as f:
            daily = json.load(f)
            return daily
    except:
        pass
        logging.error("File cannot be read!")
        exit(1)

def update_daily(file, timestamp, ping, download, upload):
    file['stats']['runs_this_day'] = file['stats']['runs_this_day'] + 1
    file['stats']['day_in_month'] = time.strftime("%d")
    file['stats']['month_in_year'] = time.strftime("%m")
    file['stats']['year'] = time.strftime("%Y")

    file['current']['timestamp'] = timestamp
    file['current']['ping_ms'] = ping
    file['current']['download_mbit'] = download
    file['current']['upload_mbit'] = upload
    
    if ping < file['min_max']['ping_min']: file['min_max']['ping_min'] = ping
    if ping > file['min_max']['ping_max']: file['min_max']['ping_max'] = ping
    if download < file['min_max']['download_min']: file['min_max']['download_min'] = download
    if download > file['min_max']['download_max']: file['min_max']['download_max'] = download
    if upload < file['min_max']['upload_min']: file['min_max']['upload_min'] = upload
    if upload > file['min_max']['upload_max']: file['min_max']['upload_max'] = upload

    file['avg']['ping_ms_days_avg'] = 0
    file['avg']['download_mbit_days_avg'] = 0
    file['avg']['upload_mbit_days_avg'] = 0

    return file

def write_daily(file):
    try:
        with open('daily.json', 'w') as f:
            json.dump(file, f, indent=4)
    except:
        pass

def read_current():
    try:
        with open('current.json', 'r') as f:
            current = json.load(f)
            return current
    except:
        pass
        logging.error("File cannot be read!")
        exit(1)
        
def write_current(file, timestamp, ping, download, upload):
    data_string = {
        "timestamp" : timestamp, 
        "ping_ms" : ping, 
        "download_mbit" : download, 
        "upload_mbit" : upload
    }

    file.append(data_string)
    
    try:
        with open('current.json', 'w') as f:
            json.dump(file, f, indent=4)
    except:
        pass

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

            daily_data = read_daily()
            daily_data = update_daily(daily_data, timestamp, ping, download, upload)
            write_daily(daily_data)

            current_data = read_current()
            write_current(current_data, timestamp, ping, download, upload)

            logging.info("Wrote values to file successfully!")

            time.sleep(60.0 - ((time.time() - starttime) % 60.0))

        except KeyboardInterrupt:
            print('speedtest-monitor was stopped by user.')
            logging.info('speedtest-monitor was stopped by user.')
            exit(1)
        
