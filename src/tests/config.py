from pydantic import BaseSettings


class TestsSettings(BaseSettings):
    base_path: str

    class Config:
        env_file = '.env'


tests_settings = TestsSettings()


URL_EXAMPLE = 'http://www.google.com/'
