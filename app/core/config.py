from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application configuration settings using Pydantic Settings."""
    
    APP_NAME: str = "FastAPI ToDo Application"
    DEBUG: bool = True
    API_V1_STR: str = "/api/v1"
    
    # Security
    SECRET_KEY: str = "7d4f8fb23e597c412f8e6d2c4e2316e6d7a5b3c4d5e6f7a8b9c0d1e2f3a4b5c6" # Replace with real secret in .env
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7 # 1 week
    
    class Config:
        env_file = ".env"
        case_sensitive = True


# Create a global settings instance
settings = Settings()
