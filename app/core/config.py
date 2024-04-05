import os
from datetime import datetime

from dotenv import load_dotenv
from pydantic_settings import BaseSettings

envFile = ".env.dev" if os.getenv("ENVIRONMENT") == "dev" else ".env"

if not os.path.isfile(envFile):
    envFile = (
        "/code/app/.env.dev" if os.getenv("ENVIRONMENT") == "dev" else "/code/app/.env"
    )

    if not os.path.isfile(envFile):
        raise FileNotFoundError(f"File {envFile} not found")

load_dotenv(envFile)


class Settings(BaseSettings):
    JWT_SECRET_KEY: str = os.getenv("SECRET_KEY")
    JWT_ALGORITHM: str = os.getenv("ALGORITHM")
    JWT_EXPIRE_MINUTES: int = os.getenv("JWT_EXPIRE_MINUTES")
    AZURE_DATABASE_URL: str = os.getenv("AZURE_DATABASE_URL")
    AZURE_DATABASE_NAME: str = os.getenv("AZURE_DATABASE_NAME")
    AZURE_DATABASE_USER: str = os.getenv("AZURE_DATABASE_USER")
    AZURE_DATABASE_PASSWORD: str = os.getenv("AZURE_DATABASE_PASSWORD")

    @staticmethod
    def get_current_time():
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    class Config:
        env_file = envFile
        env_file_encoding = "utf-8"
