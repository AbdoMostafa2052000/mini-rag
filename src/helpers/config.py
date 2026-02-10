# pydantic-settings is used to load and validate application configuration 
# (like environment variables) into typed Python classes using Pydantic, 
# making settings safe, structured, and easy to manage.

from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List


class Settings(BaseSettings):
    APP_NAME:str
    APP_VERSION:str
    OPENAI_API_KEY:str

    FILE_ALLOWED_EXTNSION:list
    FILE_MAX_SIZE:int
    FILE_DEFAULT_CHUNK_SIZE:int




    class Config:
        env_file = ".env"

def get_settings():
    return Settings()