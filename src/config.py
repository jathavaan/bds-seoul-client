from enum import Enum


class Config(Enum):
    SQLALCHEMY_DATABASE_URI = "mariadb+mariadbconnector://root:seoul-2@127.0.0.1:3306/seoul-2-db"
