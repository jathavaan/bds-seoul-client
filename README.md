# Big Data Systems Team Seoul - Client and Server

This repository contains the code for the UI and API of the Big Data Systems project. Everything runs on docker
containers. The API is written in Python using FastAPI, and the UI is built with React.

> [!NOTE]
> Make sure `bds-seoul-mariadb` and `bds-seoul-hadoop` are up and running before starting the UI and API. This is the
> third and final step in startup process.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Setup](#setup)
    - [Local setup](#local-setup)
    - [Raspberry Pi setup](#raspberry-pi-setup)
    - [Starting the Services](#starting-the-services)

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

The next step is to create the containers by running the following command in the root of `bds-seoul-mariadb` directory:

```powershell
docker-compose up -d
```

The UI can be accessed at `http://localhost:5173` and the API at `http://localhost:5000`. 
