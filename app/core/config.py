from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_prefix="MINERVA_", extra="ignore")

    database_url: str = Field(
        default="mssql+pyodbc:///?odbc_connect=Driver%3D%7BODBC+Driver+18+for+SQL+Server%7D%3BServer%3Dlocalhost%3BDatabase%3Dezeas-intelligence-db%3BTrusted_Connection%3Dyes%3BEncrypt%3Dyes%3BTrustServerCertificate%3Dyes%3B"
    )
    env: str = "local"
    llm_provider: str = "stub"
    llm_base_url: str | None = None
    llm_api_key: str | None = None
    llm_model: str | None = None
    leave_studio_rendering_enabled: bool = False
    leave_studio_rendering_timeout_seconds: float = Field(default=5.0, gt=0, le=10)
    leave_studio_rendering_max_output_chars: int = Field(default=4000, gt=0, le=12000)
    leave_studio_conversation_enabled: bool = False
    leave_studio_conversation_timeout_seconds: float = Field(default=8.0, gt=0, le=18)
    leave_studio_conversation_max_output_chars: int = Field(default=4000, gt=0, le=8000)
    leave_studio_conversation_max_history_turns: int = Field(default=8, gt=0, le=12)
    leave_studio_conversation_max_history_chars: int = Field(default=12000, gt=0, le=24000)
    workforce_base_url: str | None = None
    workforce_service_token: str | None = None
    workforce_evidence_timeout_seconds: float = Field(default=5.0, gt=0, le=15)
    award_execution_inbound_service_token: str | None = None
    cors_origins: str = "http://localhost:5173,http://127.0.0.1:5173,http://localhost:5174,http://127.0.0.1:5174"
    chunk_size: int = 1200
    chunk_overlap: int = 150


@lru_cache
def get_settings() -> Settings:
    return Settings()
