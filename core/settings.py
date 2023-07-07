import os
from pydantic import BaseSettings


class Settings(BaseSettings):
    APP_SECRET_KEY: str = os.getenv("SECRET_KEY")
    DATABASE_URL: str = os.getenv("DATABASE_URL")
    TOR_PROXY: str = os.getenv("TOR_PROXY")


settings = Settings()
