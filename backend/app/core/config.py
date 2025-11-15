from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    # App Settings
    APP_NAME: str = "Notulen API"
    DEBUG: bool = True
    SECRET_KEY: str = "your-secret-key-change-in-production"
    API_V1_STR: str = "/api/v1"

    # Database
    DATABASE_URL: str = "sqlite:///./data/notulen.db"

    # API Keys
    OPENAI_API_KEY: Optional[str] = None
    ANTHROPIC_API_KEY: Optional[str] = None

    # Model Settings
    WHISPER_MODEL: str = "base"  # tiny, base, small, medium, large, turbo
    USE_INDONESIAN_MODEL: bool = True
    INDONESIAN_MODEL_NAME: str = "indonesian-nlp/wav2vec2-large-xlsr-indonesian"

    # Upload Settings
    UPLOAD_DIR: str = "./uploads"
    MAX_UPLOAD_SIZE: int = 104857600  # 100MB
    ALLOWED_AUDIO_EXTENSIONS: list = [".mp3", ".wav", ".m4a", ".ogg", ".flac", ".webm"]

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
