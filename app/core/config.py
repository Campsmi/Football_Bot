from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    app_name: str = "Football Analyzer"
    port: int = 8000
    debug: bool = True
    
    class Config:
        env_file = ".env"

def get_settings():
    return Settings()