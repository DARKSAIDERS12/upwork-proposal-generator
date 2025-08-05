from pydantic_settings import BaseSettings
from typing import Optional
import os
import secrets
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    # База данных
    database_url: str = "sqlite:///./upwork_proposals.db"
    
    # JWT настройки - генерируем безопасный ключ
    secret_key: str = secrets.token_urlsafe(32)
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    
    # OpenAI настройки
    openai_api_key: Optional[str] = None
    
    # Настройки приложения
    app_name: str = "Upwork Proposal Generator"
    app_version: str = "1.0.0"
    debug: bool = False  # Отключаем debug для продакшена
    
    # CORS настройки - разрешаем внешний доступ
    allowed_origins: list = [
        "http://localhost:3000", 
        "http://localhost:8000",
        "http://192.168.0.124:3000",
        "http://192.168.0.124:8000",
        "https://192.168.0.124:3000",
        "https://192.168.0.124:8000"
    ]
    
    # Настройки безопасности
    enable_rate_limiting: bool = True
    max_requests_per_minute: int = 60
    
    class Config:
        env_file = ".env"

# Создаем экземпляр настроек
settings = Settings()

# Обновляем настройки из переменных окружения
if os.getenv("OPENAI_API_KEY"):
    settings.openai_api_key = os.getenv("OPENAI_API_KEY")

if os.getenv("SECRET_KEY"):
    settings.secret_key = os.getenv("SECRET_KEY")

if os.getenv("DATABASE_URL"):
    settings.database_url = os.getenv("DATABASE_URL") 