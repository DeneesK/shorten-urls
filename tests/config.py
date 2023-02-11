import logging

from pydantic import BaseSettings, PostgresDsn

from logger import LOGGING


logging.basicConfig(**LOGGING)


class AppSettings(BaseSettings):
    database_dsn: PostgresDsn

    class Config:
        env_file = '.env'


test_settings = AppSettings()
