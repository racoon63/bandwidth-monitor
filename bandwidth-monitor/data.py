#!/usr/bin/env python3.7

__author__ = "racoon63 <racoon63@gmx.net>"

import copy
import logging
import os
import sys
import time

import json

class Data(object):
    
    def __init__(self, path):
        
        #self.workdir   = os.path.dirname(os.path.abspath(__file__)) + "/"
        self.data_path = path
        self.data      = None
        self.read()


    def read(self):

        try:
            logging.debug("Reading data file from: {}".format(self.data_path))
            with open(self.data_path, "r") as f:
                self.data = json.load(f)
        
        except FileNotFoundError:
            logging.error("Could not find data file")
            self.create()
            self.read()
        
        except json.decoder.JSONDecodeError:
            logging.critical("Could not read data file because data is not of valid JSON format or another unknown reason")
        
        else:
            logging.info("Read data file successfully")
            return


    def write(self):

        try:
            logging.debug("Writing data to data file")
            with open(self.data_path, "w") as f:
                json.dump(self.data, f, indent=4)
        
        except Exception as e:
            logging.error("Could not write data to data file")
            print(e)
        
        else:
            logging.debug("Wrote data to file successfully")
            return


    def create(self):
        
        try:
            logging.info("Creating new data file at: {}".format(self.data_path))
            data = []
            with open(self.data_path, "w") as f: 
                json.dump(data, f)
        
        except:
            logging.critical("Could not create data file because of unsufficient permissions or path does not exist. Exiting")
            sys.exit()
       
        else:
            logging.info("Created data file successfully")
            return


    def create_data_object(self, timestamp, ping, download, upload):
        
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


    def append(self, data_object):
        
        try:
            logging.debug("Appending data")
            if self.data == None:
                self.data = [data_object]
            else:
                self.data.append(data_object)
        
        except:
            logging.error("Could not update data")
        
        else:
            logging.debug("Updated data successfully")
            return
