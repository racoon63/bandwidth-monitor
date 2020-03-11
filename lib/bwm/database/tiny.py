#!/usr/bin/env python3.7

__author__ = "racoon63 <racoon63@gmx.net>"

from tinydb import TinyDB

from ..logger import log

class Tiny(object):

    def __init__(self, datapath):
        
        self.datapath = datapath

        db = TinyDB(self.datapath, indent=4)
        bwm_table = db.table(name="bwm")
        db.purge_table("_default")

        self.close(db)

    def open(self):
        try:
            log.debug("Creating database session")
            return TinyDB(self.datapath, indent=4, sort_keys=True)

        except Exception as err:
            log.debug("Could not create database session")

    def insert(self, data):
        try:
            db = self.open()
            
            log.debug("Trying to write data to database")
            bwm_table = db.table(name="bwm")
            bwm_table.insert(data)
            
            if "_default" in db.tables():
                db.purge_table("_default")

            self.close(db)

        except Exception as err:
            log.exception(err)
            log.error("Could not write data to database")

        else:
            log.info("Recorded data successfully")
            return

    def close(self, session):
        try:
            session.close()

        except:
            log.debug("Could not close database session")
