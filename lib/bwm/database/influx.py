#!/usr/bin/env python3.7

__author__ = ""

import influxdb 

from ..logger import log


class Influx(object):

    def __init__(self, host, username, password):

        self.host = host
        self.username = username
        self.password = password

        self.db_name = "bwm"

        self._check()
        

    def _check(self):

        try:
            client = influxdb.InfluxDBClient(self.host, 8086, self.username, self.password, self.db_name)

        except Exception as err:
            log.debug()

        else:
            return

    def _open(self):

        try:
            log.debug("Login to database server and create session")
            client = influxdb.InfluxDBClient(self.host, 8086, self.username, self.password, self.db_name)
        
        except Exception as err:
            log.debug("Could not create a connection to influx server")
            log.exception(err)
            sys.exit(1)

        else:
            log.debug("Login successful")
            return client

    def _close(self, session):

        try:
            session.close()

        except Exception as err:
            log.debug("Could not close database session properly")
            log.exception(err)

        else:
            log.debug("Closed database session successfully")
            return


    def _exist_db(self, client, db_name):
    
        try:
            log.debug("Check if database '{}' exists".format(db_name))
            if db_name in client.get_list_database():
                log.debug("Database '{}' exists".format(db_name))
                return True
            else:
                log.debug("Database '{}' does not exist".format(db_name))
                return False

        except Exception as err:
            log.exception(err)

    def insert(self, data):
    
        try:
            client          = self._open()
            json_body = [{
                "measurement": "speedtest_result",
                "tags": {
                  "server_city": data["server"]["city"],
                  "server_country": data["server"]["country"],
                  "server_host": data["server"]["host"],
                  "server_id": data["server"]["id"],
                  "server_latency": data["server"]["latency"],
                  "server_sponsor": data["server"]["sponsor"],
                  "server_url1": data["server"]["url"],
                  #"server_url2": data["server"]["url2"],
                  "client_country": data["client"]["country"],
                  "client_ip": data["client"]["ip"],
                  "client_isp": data["client"]["isp"],
                  "client_isp_rating": data["client"]["isp-rating"],
                  "client_rating": data["client"]["rating"],
                  "identifier" : data["timestamp"]
                },
                "time": data["timestamp"],
                "fields": {
                   "download": data["download"],
                   "upload": data["upload"],
                   "ping": data["ping"]
                }
            }]

            if client.write_points(json_body):
                client.close()
            else:
                raise influxdb.exceptions.InfluxDBClientError
            
        except influxdb.exceptions.InfluxDBClientError as err:
            log.debug("Could not insert data into database")
            log.exception(err)


        except Exception as err:
            log.debug("Could not insert data into database")
            log.exception(err)

        
        else:
            log.info("Recorded data successfully")
            log.debug("Object ID: {}".format(data["timestamp"]))
            self._close(client)
            return
