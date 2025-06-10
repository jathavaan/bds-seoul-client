# Big Data Systems Team Seoul - Client and Server

This repository contains the code for the UI and API of the Big Data Systems project. Everything runs on docker
containers. The API is written in Python using FastAPI, and the UI is built with React.

> [!NOTE]
> Make sure `bds-seoul-mariadb` and `bds-seoul-hadoop` are up and running before starting the UI and API. This is the
> third and final step in startup process. This is the correct order to start things up in:
> 1. [bds-seoul-mariadb](https://github.com/jathavaan/bds-seoul-mariadb)
> 2. [bds-seoul-hadoop](https://github.com/jathavaan/bds-seoul-hadoop)
> 3. [bds-seoul-client](https://github.com/jathavaan/bds-seoul-client)

## Table of Contents

- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Setup](#setup)
    - [Local setup](#local-setup)
    - [Raspberry Pi setup](#raspberry-pi-setup)
    - [Starting the Services](#starting-the-services)
- [Troubleshooting](#troubleshooting)

## Prerequisites

- [Docker Desktop](https://docs.docker.com/desktop/)
- [Python 3.11](https://www.python.org/downloads/release/python-3110/)

## Installation

1. Clone the repository:

   ```powershell
   git clone https://github.com/jathavaan/bds-seoul-client.git
   ```

2. Navigate to the project directory:

   ```powershell
    cd bds-seoul-client
    ```

## Setup

There are two different setups for this project: one for local development and one for running on Raspberry Pis.

## Local setup

1. Navigate to the server directory:

   ```powershell
   cd server
   ```

2. Add a `.env` file in the `server` directory with the following content:

   ```plaintext
   KAFKA_BOOTSTRAP_SERVERS=host.docker.internal
   SEQ_SERVER=host.docker.internal
   SEQ_PORT=5341
   ```
3. Navigate to the client directory:

   ```powershell
   cd ../client
   ```

4. Add a `.env` file in the `client` directory with the following content:

   ```plaintext
   VITE_BE_IP=localhost:5000
   ```

After this has been done you can check out the [Starting the Services](#starting-the-services) section to start the
services.

### Raspberry Pi setup

> [!NOTE]
> This takes a long time depending on your internet connection. It is therefore recommended to run this project
> locally.

The Raspberry Pi setup is more complex and requires multiple steps to be set up. The first step is to identify
the IP-addresses of the Raspberry Pis. Open a terminal on your computer and ssh into the Raspberry Pi:

```powershell
ssh seoul-1@<ip-address-of-raspberry-pi-1>
```

Replace `<ip-address-of-raspberry-pi-1>` with the actual IP-address of the Raspberry Pi, and enter the password
`seoul-1`.

Then change directory into the `bds-seoul-client` directory:

```powershell
cd bds-seoul-client
```

We use `envsubst` to inject the correct IP-addresses when building the docker images. The IP-addresses are set in
`~/.zshrc`. To set the IP-addresses, you can use `nano ~/.zshrc` and add the following lines:

```powershell
export SEOUL_1_IP=<ip-address-of-seoul-1-raspberry-pi>
export SEOUL_2_IP=<ip-address-of-seoul-2-raspberry-pi>
export SEOUL_3_IP=<ip-address-of-seoul-3-raspberry-pi>
export SEOUL_4_IP=<ip-address-of-seoul-4-raspberry-pi>
```

Press `CTRL + X`, then `Y` and `Enter` to save the file. After that, run

```bash
source ~/.zshrc
``` 

to apply the changes. You have now set the IP-addresses for the Raspberry Pis, and you only need to do this if the
IP-addresses of any Raspberry Pi changes.

Using `envsubst`, you can now configure the correct `.env` file. First you need to change directory to the `server`
directory with `cd server` and then you can run the following commands:

```powershell
envsubst < .env.template > .env
```

This will create a `.env` file with the correct IP-addresses for the Raspberry Pis. Run

```bash
cat .env
``` 

to verify that the environment variables are set correctly. Now change directory to the `client` directory with

```powershell
cd ../client
```

and repeat the process:

```powershell
envsubst < .env.template > .env
```

This will create a `.env` file with the correct IP-addresses for the Raspberry Pis. Run

```bash
cat .env
``` 

### Starting the Services

> [!NOTE]
> If you are doing this on a Raspberry Pi, use `sudo docker compose` instead of `docker-compose`.

The next step is to create the containers by running the following command in the root of `bds-seoul-client` directory:

```powershell
docker-compose up -d
```

The UI can be accessed at [http://localhost:5173](http://localhost:5173) and the API at [http://localhost:5000](http://localhost:5000). 

## Troubleshooting
There are some known issues with this system. Many problems can often be solved by taking down the problematic container and rebuilding it like this:

```powershell
docker-compose down -v
docker-compose build --no-cache
docker-compose up -d
```

### Kafka error: Failed to get metadata
**Info**

Repository: `bds-seoul-mariadb`

Container(s): `database-script`

**Problem**
This error occurs in the `database-script` container and is almost always due to the `database-script` container being started too early. The looks something like this

```plaintext
Traceback (most recent call last):
2025-06-09T23:50:48.644765226Z   File "/app/main.py", line 9, in <module>
2025-06-09T23:50:48.651105905Z     container.kafka_service()
2025-06-09T23:50:48.651235681Z   File "src/dependency_injector/providers.pyx", line 256, in dependency_injector.providers.Provider.__call__
2025-06-09T23:50:48.656903697Z   File "src/dependency_injector/providers.pyx", line 3052, in dependency_injector.providers.Singleton._provide
2025-06-09T23:50:48.659812683Z   File "src/dependency_injector/providers.pxd", line 650, in dependency_injector.providers.__factory_call
2025-06-09T23:50:48.662689848Z   File "src/dependency_injector/providers.pxd", line 608, in dependency_injector.providers.__call
2025-06-09T23:50:48.667693058Z   File "/app/src/application/services/kafka_service/kafka_service.py", line 19, in __init__
2025-06-09T23:50:48.684920334Z     existing_topics = self.__admin_client.list_topics(timeout=10).topics
2025-06-09T23:50:48.685069094Z                       ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
2025-06-09T23:50:48.685102151Z   File "/usr/local/lib/python3.11/site-packages/confluent_kafka/admin/__init__.py", line 639, in list_topics
2025-06-09T23:50:48.688931730Z     return super(AdminClient, self).list_topics(*args, **kwargs)
2025-06-09T23:50:48.688974157Z            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
2025-06-09T23:50:48.688980664Z cimpl.KafkaException: KafkaError{code=_TRANSPORT,val=-195,str="Failed to get metadata: Local: Broker transport failure"}
```

**Solution**
Let the Kafka container run for 30~60 seconds before starting the `database-script` container.

### Stuck on checking cache
**Info**

Repository: `bds-seoul-client`, `bds-seoul-mariadb`

Container(s): `server`, `kafka`, `zookeeper`

**Problem**

The cache check is the first message sent with Kafka. The first messeage often takes up to 5 minutes to complete. If it is stuck actions need to be taken. The logs will be stuck on this message

```plaintext
[INFO] 2025-06-09 23:59:03 application.kafka.producers.last_scraped_date_producer:20      Requested last scraped date for Steam game ID 730
```

**Solution**

Firstly, stop all containers in `bds-seoul-client` and `bds-seoul-hadoop`. The following command in each root directory.

```powershell
docker-compose stop
```

Then you need to turn off the `database-script`, `kafka` and `zookeeper` containers in the `bds-seoul-mariadb`repository. Use the following command to do so:

```powershell
docker-compose stop kafka database-script zookeeper
```

And then take down both `zookeeper` and `kafka` containers:

```powershell
docker-compose down -v zookeeper
docker-compose down -v kafka
```

Start both Zookeeper and Kafka with 30 ~ 60 seconds between each startup:
```powershell
docker-compose up -d zookeeper
docker-compose up -d kafka
```

After Kafka have been running for 30 ~ 60 seconds start the `database-script` container

```powershell
docker-compose up -d database-script
```

Then start the containers in `bds-seoul-hadoop` and `bds-seoul-client` repositories as instructed in the setup guide. Try to request data for the same game now, the `server` logs should look something like this:

```plaintext
[INFO] 2025-06-10 01:33:19 application.kafka.consumers.last_scraped_date_consumer:45      Response received from last scraped date topic
[INFO] 2025-06-10 01:33:19 application.services.scraper_service.scraper_service:44        Scraping Steam game ID 730 until 500 reviews have been scraped or review date is 2025-06-10 00:00:00 [https://steamcommunity.com/app/730/reviews/?browsefilter=mostrecent&snr=1_5_100010_&p=1&filterLanguage=all]
```

### Stuck on running MapReduce job
**Info**

Repository: `bds-seoul-hadoop`

Container(s): `namenode`

**Problem**

This mostly occurs there are messages from a previous job in the queue.

**Solution**
Stop the containers in the repositores `bds-seoul-client` and `bds-seoul-hadoop` and restart the `database-script` container in the repository `bds-seoul-mariadb`. This will clear out all messages. You can now try to restart the other containers.

