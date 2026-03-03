import datetime
from dotenv import find_dotenv
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """
    Объявление переменных окружения
    """

    SQLALCHEMY_URL: str

    class Config:
        """
        Настройки конфигурации Pydantic
        """

        env_file = find_dotenv(".env")
        env_file_encoding = "utf-8"


settings: Settings = Settings()
