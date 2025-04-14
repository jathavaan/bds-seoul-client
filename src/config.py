import os
from enum import Enum

from dotenv import load_dotenv

load_dotenv()


class Config(Enum):
    SQLALCHEMY_DATABASE_URI = f"mariadb+mariadbconnector://{os.getenv('db_username')}:{os.getenv('db_password')}@{os.getenv('db_host')}:{os.getenv('db_port')}/{os.getenv('db_name')}"
