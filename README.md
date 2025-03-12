# Big Data Systems - Seoul 1
> Codebase running on `seoul-1` RaspberryPi 3B+

The `bds-seoul-1` repository contains an implementation of a `Scrapy` webscraper. THe scraper will be deployed on the RaspberryPi, and is a part of the term project in the course `DE7600042 Big data systems` at Pusan National University

## Project requirements
| Software | Required Version    |
|----------|---------------------|
| Python   | `3.10.11`           |
| WSL      | `2`                 |
| Ubuntu   | `22.04`             |

We use `Python 3.10.11` and `Ubuntu 22.04` as most frameworks and libraries have optimized for it. By using newer versions we may risk running into compatibility issues.

- [Ubuntu installer](https://apps.microsoft.com/detail/9PDXGNCFSCZV?hl=neutral&gl=NO&ocid=pdpshare)

## Installation
### Python
> [Python installer](https://www.python.org/downloads/release/python-31011/)

Download the `Windows installer (64-bit)` and open the `.exe`-file. In the installation window ensure that check off the option **Add python.exe to PATH**. It should look something like the image below

<div align="center">
  <img src="https://github.com/user-attachments/assets/ca85b102-c5ad-4716-a108-f79f1d065492" alt="Python installer window" width="50%">
</div>

And then click **Install now** and close the installer when done. Open a new terminal window and write `python --version`.
