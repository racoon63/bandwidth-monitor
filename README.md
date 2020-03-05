# Bandwidth-Monitor

![Docker Cloud Build Status](https://img.shields.io/docker/cloud/build/racoon/bandwidth-monitor)
![Docker Image Name](https://img.shields.io/badge/docker%20image-racoon%2Fbandwidth--monitor-blue)

Bandwidth-Monitor is a tool to measure and monitor your latency and bandwidth. This tool stores the measured data in JSON or in a MongoDB database. You can use Bandwidth-Monitor e.g. to determine the average internet-speed or measure the bandwidth from your Notebook at a certain place. Currently the measurements uses the [`speedtest-cli`](https://pypi.org/project/speedtest-cli/) python library.

## Tested Platforms

|OS|Python Version|Docker Version|
|---|---|---|
|mac OS Mojave (10.14.6)|3.7.3|19.03.5|
|Ubuntu 18.04.3|3.6.8|18.09.7|
|rancherOS on ARM (rpi3) 4.14.114|3.5.3|Not working yet|
|Raspbian 10 (kernel: 4.19.75-v7+)|Python 3.7.3|Not yet tested|

## Prerequisites

When you want to run this service directly from your CLI, first clone this repository and switch into its directory:

```bash
git clone https://github.com/racoon63/bandwidth-monitor.git
cd bandwidth-monitor/
```

Install the dependencies with:

```bash
sudo pip3 install -r requirements.txt
```

Create a `config.ini` according to the [configuration](#configuration) section.

When you didn't define a datapath, the data will be stored relatively to the bandwidth-monitor directory in: `../data/data.json`

## Configuration

The service can be configured either by providing a `config.ini` configuration file or setting the required environment variables. The following table shows you which options are available, if they are required and what the default values are:

|Parameter|Required|Values|Comments|
|---|---|---|---|
|`speedtest-server`|no                          |<1-50000><br>**default:** `auto`               |If you want to use a specific speedtest-server you can enter its ID here. If no ID is provided, the service will determine the nearest server. To get an overview of speedtest-server see [here](https://c.speedtest.net/speedtest-servers-static.php)|
|`interval`        |no                          |**default:** `60`                              |No value under 30 is allowed and recommended for now, because the data gathering takes some time to proceed.|
|`type`            |yes                         |`tinydb`<br>`mongodb`<br>**default:** `tinydb` |TinyDB is a lightweight database which uses plain JSON files to store data. MongoDB is a document-oriented database in which you can store your data.|
|`datapath`        |yes, if `type` is `tinydb`  |**default:** `../data/bwm.json`               |The default path is relative to the `main.py` file.|
|`host`            |yes, if `type` is `mongodb` |                                               |Everything in the form of an IP address or FQDN/DNS name like `1.2.3.4` or `database.example.com`|
|`user`            |yes, if `type` is `mongodb` |                                               |For example: `root`|
|`password`        |yes, if `type` is `mongodb` |                                               |For example: `123456`|

### Environment Variables

|Name|Description|
|---|---|
|`SPEEDTEST-SERVER`   |`auto` or the ID of your preferred speedtest-server.|
|`INTERVAL`           |An integer which shouldn't be less than 60 and every value under 30 isn't allowed.|
|`DBTYPE`             |`tinydb` or `mongodb`.|
|`DATAPATH`           |This can be an absolute or a relative path.|
|`DBHOST`             |An IP address or a DNS name in the form: `1.2.3.4` or `mongo.example.com`.|
|`DBUSER`             |Your MongoDB user if you choosed `mongodb` at `DBTYPE`.|
|`DBPASSWORD`         |Your MongoDB password for your provided db user.|
|`LOGPATH`            |This can be an absolute or a relative path.|
|`LOGLEVEL`           |Your desired logelevel. The common loglevels are available: `debug`, `info`, `warning`, `error`, `critical`.|

You can find a config example below:

```bash
[General]
speedtest-server = 15431
interval = 75

[Database]
type = mongodb
host = 1.2.3.4
user = my-mongodb-username
password = 123456

[Logging]
logpath = /var/log/bwm
loglevel = info
```

Or you just use the config skeleton [here](https://github.com/racoon63/bandwidth-monitor/blob/master/config.ini).

You can find a config example below:

```bash
[General]
speedtest-server = 15431
interval = 75

[Database]
type = mongodb
host = 1.2.3.4
user = my-mongodb-username
password = 123456

[Logging]
logpath = /var/log/bwm
loglevel = info
```

Or you just use the config skeleton [here](https://github.com/racoon63/bandwidth-monitor/blob/master/config.ini).

## Run

After all the requirements have been met you can run the service either directly from the CLI or create a docker container for it.

### CLI

To run this tool directly from your command-line, switch into the `bandwidth-monitor` directory (where the `main.py` is placed) and run the following command on your machine to start the bandwidth-monitor:

```bash
python3 main.py
```

### Docker

To run this service in a docker container you can

* build the image by yourself and run it afterwards
* create a `config.ini` and map it into the docker container or
* just create a volume and run a new docker instance.

To build the `Dockerfile` by yourself just run:

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
           -e LOGLEVEL="info" \
           racoon/bandwidth-monitor:latest
```

### Docker-Compose

If you want to store your data in a MongoDB database and run everything in a container environment you can use the `docker-compose.yml` file to start the services. Run it with:

```bash
docker-compose up -d
```

## Missing

* Config (-file) hashing
* Implement webUI possibility
* Info about successful measurement

## Maintainer

racoon63 <racoon63@gmx.net>
