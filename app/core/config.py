import os
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):

    # Application
    PROJECT_NAME: str = os.getenv("PROJECT_NAME", "ShopAPI")
    VERSION: str = os.getenv("VERSION", "1.0.0")
    
    # Database
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./shop.db")

    # Admin user credentials
    ADMIN_EMAIL: str = os.getenv("DEFAULT_ADMIN_EMAIL", "admin@gmail.com")
    ADMIN_PASSWORD: str = os.getenv("DEFAULT_ADMIN_PASSWORD", "12345678")
    
    # JWT
    SECRET_KEY: str = os.getenv("SECRET_KEY", "shop-api-secret-key")
    ALGORITHM: str = os.getenv("ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 60 * 24)

    # Email
    SMTP_SERVER: str = os.getenv("SMTP_HOST", "smtp.gmail.com")
    SMTP_PORT: int = os.getenv("SMTP_PORT",  465)
    SMTP_USERNAME: str = os.getenv("SMTP_USERNAME", "your_email")
    SMTP_PASSWORD: str = os.getenv("SMTP_PASSWORD", "your_password")

    class Config:
        case_sensitive = True

settings = Settings()