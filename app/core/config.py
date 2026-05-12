from pydantic import Field, field_validator
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment variables"""
    
    # Database
    database_url: str = Field(..., env="DATABASE_URL")
    
    # JWT/Auth
    secret_key: str = Field("CHANGE_ME_IN_PROD", env="SECRET_KEY")
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 20
    refresh_token_expire_days: int = 7
    
    # Application
    app_name: str = "Spotify Clone API"
    debug: bool = False
    # CORS
    allowed_origins: list[str] = Field(default=["http://localhost:3000", "http://localhost:8000"])
    
    @field_validator("allowed_origins", mode="before")
    @classmethod
    def parse_cors(cls, v):
        if isinstance(v, str):
            return [origin.strip() for origin in v.split(",")]
        return v
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
