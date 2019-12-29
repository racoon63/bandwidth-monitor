#!/usr/bin/env python3.7

__author__ = 'racoon <racoon63@gmx.net>'

import copy
import logging
import sys
import time

import json

class Data(object):
    
    def __init__(self, path):
        self.data_path = path
        self.data = self.read()
    
    def read(self):
        try:
            logging.debug('Reading data file ' + self.data_path)
            with open(self.data_path, 'r') as f:
                self.data = json.load(f)
        except FileNotFoundError:
            logging.error('Could not find data file: ' + self.data_path)
            self.create()
            self.read()
        except json.decoder.JSONDecodeError:
            logging.critical('Could not read data file because data is not of valid JSON format or another unknown reason')
        else:
            logging.info('Read data file successfully')
            return

    def write(self):
        try:
            logging.debug('Writing data to data file')
            with open(self.data_path, 'w') as f:
                json.dump(self.data, f, indent=4)
        except Exception as e:
            logging.error('Could not write data to data file ' + self.data_path)
            print(e)
        else:
            logging.debug('Wrote data to file successfully')
            return
    
    def create(self):
        try:
            logging.info('Creating new data file ' + self.data_path)
            data = []
            with open(self.data_path, 'w') as f: 
                json.dump(data, f)
        except:
            logging.critical('Could not create data file ' + self.data_path + '. Exiting')
            sys.exit()
        else:
            logging.info('Created data file successfully')
            return

    def create_data_object(self, timestamp, ping, download, upload):
        try:
            logging.debug('Creating new data object')
            data_object = {
                "timestamp" : timestamp, 
                "ping" : ping, 
                "download" : download, 
                "upload" : upload
            }
        except:
            logging.error('Could not create new data object')
        else:
            logging.debug('Created new object successfully')
            return data_object

    def append(self, data_object):
        try:
            logging.debug('Appending data')
            if self.data == None:
                self.data = [data_object]
            else:
                self.data.append(data_object)
        except:
            logging.error('Could not update data')
        else:
            logging.debug('Updated data successfully')
            return


    '''
    def update(file, timestamp, ping, download, upload):
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
            sys.exit(1)
            
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
    '''