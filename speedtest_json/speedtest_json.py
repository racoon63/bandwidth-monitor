import subprocess
import json
import logging

class speedtest_json():
    def __init__(self):
        stats = subprocess.Popen(["speedtest-cli", "--json"], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        stdout,stderr = stats.communicate()
        
        logging.debug(stderr)

        self.results = stdout.decode("utf-8")
        self.values = json.loads(self.results)

    def get_json(self):
        return self.values
    
    def get_timestamp(self):
        return self.values['timestamp']
    
    def get_ping(self):
        return self.values['ping']

    def get_download(self):
        return self.values['download']

    def get_upload(self):
        return self.values['upload']