# Big Data Systems - Seoul 1

> [!IMPORTANT]
> Codebase running on `seoul-1` RaspberryPi 3B+

The `bds-seoul-1` repository contains an implementation of a `Scrapy` webscraper. THe scraper will be deployed on the
RaspberryPi, and is a part of the term project in the course `DE7600042 Big data systems` at Pusan National University

> [!TIP] Read the docs

- [Coding convention](./docs/coding-convention.md)
- [Architecture](./docs/architecture.md)
- [SQLAlchemy and Alembic](./docs/database.md)

## Project requirements

| Software | Required Version |
|----------|------------------|
| Python   | `3.11.2`         |
| WSL      | `2`              |

We use `Python 3.11.2`  as most frameworks and libraries have optimized for it. By using newer
versions we may risk running into compatibility issues.

## Installation

> [!IMPORTANT]  
> This installation guide is only for Windows

### Python

> [Python installer](https://www.python.org/downloads/release/python-3112/)

Download the `Windows installer (64-bit)` and open the `.exe`-file. In the installation window ensure that check off the
option **Add python.exe to PATH**. It should look something like the image below

<div align="center">
  <img src="https://github.com/user-attachments/assets/ca85b102-c5ad-4716-a108-f79f1d065492" alt="Python installer window" width="50%">
</div>

And then click **Install now** and close the installer when done. Open a new terminal window and
write `python --version` and the expected outcome is `Python 3.11.2`.

## Setup

First thing first, create a virtual environment (also known as a `venv`). On Windows this can be done using

```powershell
python -m venv venv
```

and then activate the environment with

```powershell
venv/Scripts/activate
```

If you now type `python --version` the expected outcome is `3.11.2`. To install the project requirements defined in [
`requirements.txt`](requirements.txt) use the command

```powershell
pip install -r requirements.txt
```

You should run this command whenever you know a new package have been installed, or if you encounter a
`ModuleNotFoundError`.

In your IDE ensure that the `venv` have been selected as the Python interpreter. If you have installed a new package,
ensure that it is included in the `requirements.txt` by using `pip freeze > requirements.txt` Please ensure that the
`venv` is activated.

## Connect to RaspberryPi with ssh

All RaspberryPi's are connected to the network `Einar's S24`. The IP-addresses can be accessed from the phone. When
connected to Einar's network use `ssh seoul-1@192.168.x.x`.

