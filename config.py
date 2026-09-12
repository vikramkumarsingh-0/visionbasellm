from pydantic_settings import BaseSettings
from pathlib import Path

class Settings(BaseSettings):
    groq_api_key: str = ""
    action_settle_timeout: float = 5.0
    ollama_base_url: str = "http://localhost:11434"
    redis_url: str = "redis://localhost:6379"
    model_version: str = "v1.0.0"
    retrain_threshold: int = 3
    
    base_dir: Path = Path(__file__).parent
    models_dir: Path = base_dir / "models"
    data_dir: Path = base_dir / "data"
    logs_dir: Path = base_dir / "logs"
    screenshots_dir: Path = data_dir / "screenshots"
    annotations_dir: Path = data_dir / "annotations"
    
    class Config:
        env_file = ".env"

settings = Settings()
settings.models_dir.mkdir(exist_ok=True)
settings.data_dir.mkdir(exist_ok=True)
settings.logs_dir.mkdir(exist_ok=True)
settings.screenshots_dir.mkdir(exist_ok=True)
settings.annotations_dir.mkdir(exist_ok=True)
