from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from ..database import Base

class Proposal(Base):
    __tablename__ = "proposals"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Данные проекта
    project_description = Column(Text, nullable=False)
    budget_range = Column(String(50), nullable=False)  # $100-500, $500-1000, $1000-5000, $5000+
    specialization = Column(String(100), nullable=False)  # Веб-разработка, Дизайн, Копирайтинг, Маркетинг, Другое
    experience_level = Column(String(50), nullable=False)  # 1-2 года, 3-5 лет, 5+ лет
    key_requirements = Column(Text)
    
    # Сгенерированный контент
    generated_content = Column(Text, nullable=False)
    template_used = Column(String(100))  # Название использованного шаблона
    tone = Column(String(50))  # формальный, дружелюбный, профессиональный
    
    # Метаданные
    tokens_used = Column(Integer)  # Количество токенов OpenAI
    generation_time = Column(Integer)  # Время генерации в секундах
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Связи
    user = relationship("User", back_populates="proposals")
    
    def __repr__(self):
        return f"<Proposal(id={self.id}, user_id={self.user_id}, specialization='{self.specialization}')>" 