from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_prefix="MINERVA_", extra="ignore")

    database_url: str = Field(
        default="mssql+pyodbc:///?odbc_connect=DRIVER%3D%7BODBC%20Driver%2018%20for%20SQL%20Server%7D%3BSERVER%3Dlocalhost%3BDATABASE%3Dezeas-intelligence-db%3BTrusted_Connection%3Dyes%3BTrustServerCertificate%3Dyes"
    )
    env: str = "local"
    llm_provider: str = "stub"
    chunk_size: int = 1200
    chunk_overlap: int = 150


@lru_cache
def get_settings() -> Settings:
    return Settings()
