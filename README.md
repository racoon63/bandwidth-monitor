# Bandwidth-Monitor

Bandwidth-Monitor is an open source tool with which you can use to measure and monitor your latency and bandwidth. Bandwidth-Monitor automatically creates statistics from your measured data and displays it in Grafana over a webUI.

## Usage

Firstly get this repository:

```bash
git clone https://github.com/racoon63/bandwidth-monitor.git
```

Install the dependencies:

```bash
pip3 install -r requirements.txt
```

Afterwards you can start the service with:

```bash
cd bandwidth-monitor/
python3 main.py
```

The data will be stored relatively to the bandwidth-monitor directory: `../data/data.json`

## Missing

* Configure service
* Implementing database drivers
  * tinyDB
  * mongoDB

## Maintainer

racoon63 <racoon63@gmx.net>
