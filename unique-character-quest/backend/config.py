"""
Configuration settings for Unique Character Quest
--------------------------------------------------
Loads configuration from environment variables with sensible local defaults.
"""

import os
from pydantic import BaseModel


class Settings(BaseModel):
    APP_NAME: str = "Unique Character Quest"
    APP_VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    
    # Networking
    HOST: str = os.getenv("HOST", "127.0.0.1")
    PORT: int = int(os.getenv("PORT", "8000"))
    ALLOWED_ORIGINS: list[str] = [
        "http://localhost:8501",
        "http://127.0.0.1:8501",
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "*"
    ]
    
    # Database
    DATABASE_PATH: str = os.getenv("DATABASE_PATH", "unique_quest.db")
    
    # Multiplayer
    ROOM_EXPIRATION_SECONDS: int = int(os.getenv("ROOM_EXPIRATION_SECONDS", "3600"))
    MAX_PLAYERS_PER_ROOM: int = int(os.getenv("MAX_PLAYERS_PER_ROOM", "6"))
    ROUND_DEADLINE_TOLERANCE_SECONDS: float = float(os.getenv("ROUND_TOLERANCE", "2.0"))


settings = Settings()
