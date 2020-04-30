__author__ = "racoon63 <racoon63@gmx.net>"

from speedtest import Speedtest

class Measurement:
    def __init__(self, servers=[]):
        self.servers = []

    def measure(self):
        s = Speedtest()

        try:
            s.get_servers(self.servers)
            s.get_best_server()
            s.download()
            s.upload()
            return s.results.dict()
        except Exception:
            
            return { 
                # TODO: Add timestamp in the following format: "2020-04-30T20:32:10.779485Z"
                "timestamp": None,
                "ping": None, 
                "download": 0.0,
                "upload": 0.0,
                "server": {
                    "city": None,
                    "country": None,
                    "host": None,
                    "id": None,
                    "latency": None,
                    "sponsor": None,
                    "url": None,
                    "url2": None
                },
                "client": {
                    "country": None,
                    "ip": None,
                    "isp": None,
                    "isp-rating": None,
                    "rating": None
                }
            }
