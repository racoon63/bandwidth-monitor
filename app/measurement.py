from datetime import datetime

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
                "timestamp": datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
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
