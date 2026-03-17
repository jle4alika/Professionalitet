from authx import AuthXConfig, AuthX
from dotenv import find_dotenv
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """
    Объявление переменных окружения
    """

    DB_HOST: str = "localhost"
    DB_PORT: int = 5432
    DB_USER: str = "postgres"
    DB_PASS: str = "postgres"
    DB_NAME: str = "professionalitet"
    TEST_DATABASE_URL: str | None = None  # sqlite+aiosqlite:///:memory: для тестов

    @property
    def DATABASE_URL_asyncpg(self):
        if self.TEST_DATABASE_URL:
            return self.TEST_DATABASE_URL
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    @property
    def DATABASE_URL_psycopg(self):
        # DSN
        # postgresql+psycopg://postgres:postgres@localhost:5432/sa
        return f"postgresql+psycopg2://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    class Config:
        """
        Настройки конфигурации Pydantic
        """

        env_file = find_dotenv(".env")
        env_file_encoding = "utf-8"


settings: Settings = Settings()

config = AuthXConfig()
config.JWT_SECRET_KEY = "SECRET_KEY"
config.JWT_ACCESS_COOKIE_NAME = "my_access_token"
config.JWT_TOKEN_LOCATION = ["cookies"]

security = AuthX(config=config)
