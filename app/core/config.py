from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application configuration settings using Pydantic Settings."""
    
    APP_NAME: str = "FastAPI ToDo Application"
    DEBUG: bool = True
    API_V1_STR: str = "/api/v1"
    
    class Config:
        env_file = ".env"
        case_sensitive = True


# Create a global settings instance
settings = Settings()
