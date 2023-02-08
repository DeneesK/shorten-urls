from pydantic import BaseSettings, PostgresDsn


class AppSettings(BaseSettings):
    app_title: str
    database_dsn: PostgresDsn
    app_description: str

    class Config:
        env_file = '.env'


app_settings = AppSettings()
