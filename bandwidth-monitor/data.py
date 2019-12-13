#!/usr/bin/env python3.7

__author__ = 'racoon <racoon63@gmx.net>'

import json
import logging
import sys
import time

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
    file['stats']['day_in_month']  = time.strftime("%d")
    file['stats']['month_in_year'] = time.strftime("%m")
    file['stats']['year']          = time.strftime("%Y")

    file['current']['timestamp']     = timestamp
    file['current']['ping_ms']       = ping
    file['current']['download_mbit'] = download
    file['current']['upload_mbit']   = upload
    
    if ping < file['min_max']['ping_min']: file['min_max']['ping_min']             = ping
    if ping > file['min_max']['ping_max']: file['min_max']['ping_max']             = ping
    if download < file['min_max']['download_min']: file['min_max']['download_min'] = download
    if download > file['min_max']['download_max']: file['min_max']['download_max'] = download
    if upload < file['min_max']['upload_min']: file['min_max']['upload_min']       = upload
    if upload > file['min_max']['upload_max']: file['min_max']['upload_max']       = upload

    current = read_current()
    
    ping_sum = 0
    downlaod_sum = 0
    upload_sum = 0

    for i in current:
        ping_sum = ping_sum + i['ping_ms']
        downlaod_sum = downlaod_sum + i['download_mbit']
        upload_sum = upload_sum + i['upload_mbit']
    
    avg_ping = ping_sum / file['stats']['runs_this_day']
    avg_download = downlaod_sum / file['stats']['runs_this_day']
    avg_upload = upload_sum / file['stats']['runs_this_day']
    
    file['avg']['ping_ms_days_avg'] = round(avg_ping, 2)
    file['avg']['download_mbit_days_avg'] = round(avg_download, 2)
    file['avg']['upload_mbit_days_avg'] = round(avg_upload, 2)

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