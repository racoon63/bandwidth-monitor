# Bandwidth-Monitor

Bandwidth-Monitor is a tool with which you can use to measure and monitor your latency and bandwidth. Bandwidth-Monitor automatically creates statistics from your measured data and displays it in Grafana over a webUI.

## Usage

Firstly get this repository and switch into its directory:

```bash
git clone https://github.com/racoon63/bandwidth-monitor.git
cd bandwidth-monitor/
```

Install the dependencies:

```bash
pip3 install -r requirements.txt
```

Afterwards you can start the service with:

```bash
python3 bandwidth-monitor/main.py
```

The data will be stored relatively to the bandwidth-monitor directory in: `../data/data.json`

## Missing

* Configuration handler
* Implementing database drivers
  * tinyDB
  * mongoDB

## Maintainer

racoon63 <racoon63@gmx.net>
