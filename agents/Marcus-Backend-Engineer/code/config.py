from pydantic import BaseSettings

class Settings(BaseSettings):
    SECRET_KEY: str = "change-me-to-secure-secret"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    DATABASE_URL: str = "sqlite:///./test.db"

settings = Settings()
