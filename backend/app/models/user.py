from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from ..database import Base

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    first_name = Column(String(100))
    last_name = Column(String(100))
    specialization = Column(String(100))  # Веб-разработка, Дизайн, Копирайтинг и т.д.
    experience_level = Column(String(50))  # 1-2 года, 3-5 лет, 5+ лет
    bio = Column(Text)
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Связи
    proposals = relationship("Proposal", back_populates="user")
    subscription = relationship("Subscription", back_populates="user", uselist=False)
    
    def __repr__(self):
        return f"<User(id={self.id}, email='{self.email}')>" 