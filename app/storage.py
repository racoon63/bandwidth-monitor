""" Storage is a class that should provide an interface to the backend. """

import abc
import os

import influxdb
from tinydb import TinyDB

from log import logger


class Storage(metaclass=abc.ABCMeta):
    """ Base class for all storage backend classes. """
    @classmethod
    def __subclasshook__(cls, subclass):
        return (hasattr(subclass, 'save') and
                callable(subclass.save))

    @abc.abstractmethod
    def save(self, data: dict):
        """ Stores given data in storage backend. """
        pass

    @abc.abstractmethod
    def cleanup(self):
        """ Closes all remaining session and connections to database. """
        pass

class Tiny(Storage):
    """ Class to interact with a TinyDB database. """
    def __init__(self, datapath="data/bwm"):
        try:
            os.mkdir("data")
        except FileExistsError:
            pass
        try:
            self.client = TinyDB(datapath, indent=4)
            self.table = self.client.table(name="bwm")
            self.client.drop_table("_default")
        except Exception as err:
            logger.exception(err)

    def save(self, data: dict):
        """ Stores given data in influx database. """
        try:
            self.table.insert(data)

            if "_default" in self.client.tables():
                self.client.drop_table("_default")
        except Exception as err:
            logger.exception(err)

    def cleanup(self):
        self.client.close()

class Influx(Storage):
    """ Class to interact with an InfluxDB database. """
    def __init__(self, dbhost="bwm", dbuser="bwm", dbpassword="bwm", dbname="bwm"):
        try:
            self.client = influxdb.InfluxDBClient(dbhost,
                                                  8086,
                                                  dbuser,
                                                  dbpassword,
                                                  dbname,
                                                  timeout=10,
                                                  retries=0)
        except influxdb.exceptions.InfluxDBServerError:
            logger.error("Could not establish connection to database. Retrying")

    def save(self, data: dict):
        """ Stores given data in influx database. """
        try:
            self.client.write_points(data)
        except influxdb.exceptions.InfluxDBClientError as err:
            logger.exception(err)

    def cleanup(self):
        """ Closes an influx client connection. """
        self.client.close()

class StorageInterface:
    """ Class to interact with the storage backend. """
    def __init__(self, **kwargs):
        self.tiny = Tiny(kwargs["datapath"])
        self.influx = Influx(kwargs["dbhost"],
                             kwargs["dbuser"],
                             kwargs["dbpassword"],
                             kwargs["dbname"])

    def store(self, dbtype, data):
        """ Storage interface function to store the data in backend """
        if dbtype == "tinydb":
            self.tiny.save(data)
        if dbtype == "influxdb":
            self.influx.save(data)
