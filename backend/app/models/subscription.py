from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from ..database import Base

class Subscription(Base):
    __tablename__ = "subscriptions"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # План подписки
    plan = Column(String(50), nullable=False)  # free, basic, pro, enterprise
    status = Column(String(50), default="active")  # active, cancelled, expired, pending
    
    # Лимиты
    proposals_per_month = Column(Integer, default=5)  # Количество предложений в месяц
    tokens_per_month = Column(Integer, default=10000)  # Лимит токенов OpenAI
    
    # Платежная информация
    stripe_subscription_id = Column(String(255))
    stripe_customer_id = Column(String(255))
    
    # Даты
    start_date = Column(DateTime, default=datetime.utcnow)
    end_date = Column(DateTime)
    cancelled_at = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Связи
    user = relationship("User", back_populates="subscription")
    
    def __repr__(self):
        return f"<Subscription(id={self.id}, user_id={self.user_id}, plan='{self.plan}')>"
    
    @property
    def is_active(self):
        """Проверяет, активна ли подписка"""
        if self.status != "active":
            return False
        if self.end_date and datetime.utcnow() > self.end_date:
            return False
        return True 