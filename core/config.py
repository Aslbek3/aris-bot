import os
from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()

class Settings(BaseSettings):
    BOT_TOKEN: str = os.getenv("BOT_TOKEN", "")
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    DATABASE_URL: str = os.getenv("DATABASE_URL", "postgresql+asyncpg://user:pass@localhost/aris_db")
    
    # Media paths
    VOICE_DIR: str = "aris_bot/media/voice"
    REPORTS_DIR: str = "aris_bot/media/reports"

settings = Settings()
