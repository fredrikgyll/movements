from pathlib import Path

import dotenv
from pydantic import BaseSettings

__all__ = ['settings', 'PROJECT_ROOT']

PROJECT_ROOT = Path(__file__).parent.parent

dotenv.load_dotenv(PROJECT_ROOT / '.env')


class Settings(BaseSettings):
    PROJECT_NAME: str
    DATABASE_URL: str

    DEBUG: bool
    ENVIRONMENT: str


settings = Settings()
