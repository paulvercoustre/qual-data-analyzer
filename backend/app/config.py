from pydantic_settings import BaseSettings, SettingsConfigDict
import os

class Settings(BaseSettings):
    # Load environment variables from .env file if it exists, case_sensitive=True
    # model_config = SettingsConfigDict(env_file='.env', case_sensitive=True, extra='ignore') 
    # Using docker-compose env vars primarily for now, but .env support is here if needed.
    model_config = SettingsConfigDict(case_sensitive=True, extra='ignore')

    # Database
    DATABASE_URL: str

    # JWT Authentication (placeholders - generate strong secrets later)
    SECRET_KEY: str = "## CHANGE ME IN PRODUCTION ##"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

# Create a single instance of the settings to be imported elsewhere
settings = Settings() 