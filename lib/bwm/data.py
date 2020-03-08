#!/usr/bin/env python3

class Data(object):

    def __init__(self, timestamp, ping, download, upload):
        self.timestamp = timestamp
        self.ping = ping
        self.download = download
        self.upload = upload
        
    def create(self):
        return {"timestamp": self.timestamp, "ping": self.ping, "download": self.download, "upload": self.upload}

    def empty(self):
        return {"timestamp": None, "ping": None, "download": 0.0, "upload": 0.0}
