from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from ..models.user import User
from ..config import settings

# Настройка хеширования паролей
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class AuthService:
    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        """Проверяет пароль"""
        return pwd_context.verify(plain_password, hashed_password)
    
    @staticmethod
    def get_password_hash(password: str) -> str:
        """Хеширует пароль"""
        return pwd_context.hash(password)
    
    @staticmethod
    def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
        """Создает JWT токен"""
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=settings.access_token_expire_minutes)
        
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)
        return encoded_jwt
    
    @staticmethod
    def verify_token(token: str) -> Optional[str]:
        """Проверяет JWT токен и возвращает email пользователя"""
        try:
            payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
            email: str = payload.get("sub")
            if email is None:
                return None
            return email
        except JWTError:
            return None
    
    @staticmethod
    def authenticate_user(db: Session, email: str, password: str) -> Optional[User]:
        """Аутентифицирует пользователя"""
        user = db.query(User).filter(User.email == email).first()
        if not user:
            return None
        if not AuthService.verify_password(password, user.password_hash):
            return None
        return user
    
    @staticmethod
    def get_user_by_email(db: Session, email: str) -> Optional[User]:
        """Получает пользователя по email"""
        return db.query(User).filter(User.email == email).first()
    
    @staticmethod
    def create_user(db: Session, email: str, password: str, **kwargs) -> User:
        """Создает нового пользователя"""
        hashed_password = AuthService.get_password_hash(password)
        user = User(
            email=email,
            password_hash=hashed_password,
            **kwargs
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        return user 