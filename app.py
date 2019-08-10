#!/usr/bin/env python3.7

import subprocess
import time
import json

current_time = time.strftime('%d/%m/%y') + " " + time.strftime('%H:%M')
stats = subprocess.Popen(["speedtest-cli", "--json"], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
stdout,stderr = stats.communicate()
results = stdout.decode("utf-8")

#with open("stats.json", "r") as f:
#    results2 = json.load(f)
#    f.close()

#print("current time: " + current_time)

final = json.loads(results)
#print(json.dumps(final, indent=4))
#print("")

ping = final['ping']
download = final['download']
upload = final['upload']
timestamp = final['timestamp']

#with open("speedtest-stats.json", "w") as f:
#    json.dump(results1, f, indent=4)
#    f.close()