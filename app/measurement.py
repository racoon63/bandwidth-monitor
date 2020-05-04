""" Provides bandwidth measurement functionality for bwm service. """

from datetime import datetime

from speedtest import Speedtest, SpeedtestException


class Measurement:
    """ Measurement class provides bandwidth measurement capability. """
    def __init__(self, servers=None):
        self.servers = servers

    def measure(self):
        """ Returns a dict with the measured results. """
        sptest = Speedtest()

        try:
            sptest.get_servers(self.servers)
            sptest.get_best_server()
            sptest.download()
            sptest.upload()
            return sptest.results.dict()
        except SpeedtestException:
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
