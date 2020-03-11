#!/usr/bin/env python3.7

__author__ = "racoon63 <racoon63@gmx.net>"

import pymongo

from ..logger import log


class Mongo(object):

    def __init__(self, host, username, password):

        self.host = host
        self.username = username
        self.password = password

        self.db_url               = "mongodb://{}:27017/".format(host)
        self.db_name              = "bwm"
        self.data_collection_name = "data"

        self._check()
        

    def _check(self):

        try:
            client = self._open()
            db     = self._create_db(client, self.db_name)
            
            self._exist_db(client, self.db_name)
            self._exist_collection(db, self.data_collection_name)

            self._close(client)

        except Exception as err:
            log.debug()

        else:
            return

    def _open(self):

        try:
            log.debug("Login to database server and create session")
            client = pymongo.MongoClient(self.db_url, 
                                         username=self.username, 
                                         password=self.password,
                                         authMechanism='SCRAM-SHA-256')
        
        except Exception as err:
            log.debug("Could not create a connection to mongodb server")
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
            if db_name in client.list_database_names():
                log.debug("Database '{}' exists".format(db_name))
                return True
            else:
                log.debug("Database '{}' does not exist".format(db_name))
                return False

        except Exception as err:
            log.exception(err)


    def _create_db(self, client, db_name):
        
        try:
            return client[db_name]

        except Exception as err:
            log.exception(err)


    def _exist_collection(self, db, collection_name):

        try:
            log.debug("Check if collection '{}' exists".format(collection_name))
            if collection_name in db.list_collection_names():
                log.debug("Collection '{}' exists".format(collection_name))
                return True
            else:
                log.debug("Collection '{}' does not exist".format(collection_name))
                return False
        
        except Exception as err:
            log.exception(err)


    def _create_collection(self, db, collection_name):

        try:
            return db[collection_name]

        except Exception as err:
            log.exception(err)


    def insert(self, data):
    
        try:
            client          = self._open()
            db              = self._create_db(client, self.db_name)
            collection_data = self._create_collection(db, self.data_collection_name)
            identifier      = collection_data.insert_one(data)

        except Exception as err:
            log.debug("Could not insert data into database")
            log.exception(err)

        else:
            log.info("Recorded data successfully")
            log.debug("Object ID: {}".format(identifier.inserted_id))
            self._close(client)
            return
