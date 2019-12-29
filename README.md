# Bandwidth-Monitor

Bandwidth-Monitor is a tool with which you can use to measure and monitor your latency and bandwidth. Bandwidth-Monitor automatically creates statistics from your measured data and displays it in Grafana over a webUI.

## Prerequisites

When you want to run this service directly from your CLI, first get this repository and switch into its directory:

```bash
git clone https://github.com/racoon63/bandwidth-monitor.git
cd bandwidth-monitor/
```

Install the dependencies with:

```bash
pip3 install -r requirements.txt
```

Create a `config.ini` according to the provided [config](#config) section.

Afterwards you can start the service with:

```bash
python3 bandwidth-monitor/main.py
```

The data will be stored relatively to the bandwidth-monitor directory in: `../data/data.json`

## Configuration

The service can be configured either by providing a `config.ini` configuration file or setting the required environment variables. The following table shows you which options are available, if they are required and what the default values are:

|Parameter|Required|Values|Comments|
|---|---|---|---|
|**speedtest-server**|no|default: `auto`|If you want to use a specific speedtest-server you can enter its ID here. If no ID is provided, the service will determine the nearest server.|
|**interval**|no|default: `60`|No value under 60 is allowed and recommended for now, beacause the data gathering takes some time to proceed.|
|**type**|no|default: `tinydb`|TinyDB is a lightweight database which uses plain JSON files to store data. MongoDB is a document-oriented database in which you can store your data.|
|**datapath**|yes|default: `../data/data.json`|The default path is relative to the `main.py` file.|
|**host**|yes||Everything in the form of an IP address or FQDN/DNS name like `1.2.3.4` or `database.example.com`|
|**user**|yes||For example: `root`|
|**password**|yes||For example: `123456`|

## Missing

* Implementing database drivers
  * tinyDB
  * mongoDB
* Implement webUI possibility

## Maintainer

racoon63 <racoon63@gmx.net>
