# Bandwidth-Monitor

Bandwidth-Monitor is a tool with which you can use to measure and monitor your latency and bandwidth. Bandwidth-Monitor automatically creates statistics from your measured data and displays it over a webUI.

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

Create a `config.ini` according to the [config](#config) section.

The data will be stored relatively to the bandwidth-monitor directory in: `../data/data.json`

## Configuration

The service can be configured either by providing a `config.ini` configuration file or setting the required environment variables. The following table shows you which options are available, if they are required and what the default values are:

|Parameter|Required|Values|Comments|
|---|---|---|---|
|**speedtest-server**|no |default: `auto`               |If you want to use a specific speedtest-server you can enter its ID here. If no ID is provided, the service will determine the nearest server.|
|**interval**        |no |default: `60`                 |No value under 60 is allowed and recommended for now, beacause the data gathering takes some time to proceed.|
|**type**            |no |default: `tinydb`             |TinyDB is a lightweight database which uses plain JSON files to store data. MongoDB is a document-oriented database in which you can store your data.|
|**datapath**        |yes|default: `../data/data.json`  |The default path is relative to the `main.py` file.|
|**host**            |yes|                              |Everything in the form of an IP address or FQDN/DNS name like `1.2.3.4` or `database.example.com`|
|**user**            |yes|                              |For example: `root`|
|**password**        |yes|                              |For example: `123456`|

### Environment Variables

|Name|Description|
|---|---|
|**SPEEDTEST-SERVER**   |`auto` or the ID of your preferred speedtest-server.|
|**INTERVAL**           |An integer which shouldn't be less than 60.|
|**DBTYPE**             |`tinydb` or `mongodb`|
|**DATAPATH**           |This can be an absolute or a relative path.|
|**DBHOST**             |An IP address or a DNS name.|
|**DBUSER**             |Your db user if you choosed `mongodb` at `DBTYPE`|
|**DBPASSWORD**         |YOUR db password for your provided db user.|
|**LOGPATH**            |This can be an absolute or a relative path.|
|**LOGLEVEL**           |Your desired logelevel. The common loglevels are available: `debug`, `info`, `warning`, `error`, `critical`.|

## Run

After all the requirements have been met you can run the service either directly from the CLI or create a docker container for it.

### CLI

```bash
python3 bandwidth-monitor/main.py
```

### Docker

To run this service in a docker container you can

* build the image by yourself and run it afterwards
* create a `config.ini` and map it into the docker container or
* just create a volume and run a new docker instance.

To build the `Dockerfile` by yourself run:

```bash
docker build -t <YOUR-TAG> .
docker run -d <YOUR-TAG>
```

If you want to provide your `config.ini` and map it into the container, run:

```bash
docker run -d \
           -v ${pwd}/config.ini:/bwm/config.ini \
           <YOUR-TAG>
```

You can also just run the image and configure the service with the available environment variables described [here](#environment-variables):

```bash
docker volume create bwm
docker run -d \
           --name bwm \
           -v bwm:/bwm/data \
           -e SPEEDTEST-SERVER="auto" \
           -e INTERVAL=60 \
           -e DBTYPE="tinydb" \
           -e DATAPATH="/bwm/data/bwm.json" \
           -e LOGPATH="/bwm/log/bwm.log" \
           -e LOGLEVEL="error" \
           racoon/bandwidth-monitor:latest
```

## Missing

* Implementing database drivers
  * tinyDB
  * mongoDB
* Implement webUI possibility

## Maintainer

racoon63 <racoon63@gmx.net>
