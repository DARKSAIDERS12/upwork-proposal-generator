from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime

# Схемы для пользователей
class UserBase(BaseModel):
    email: EmailStr
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    specialization: Optional[str] = None
    experience_level: Optional[str] = None
    bio: Optional[str] = None

class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    specialization: Optional[str] = None
    experience_level: Optional[str] = None
    bio: Optional[str] = None

class User(UserBase):
    id: int
    is_active: bool
    is_verified: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# Схемы для аутентификации
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

# Схемы для предложений
class ProposalBase(BaseModel):
    project_description: str
    budget_range: str
    specialization: str
    experience_level: str
    key_requirements: Optional[str] = None

class ProposalCreate(ProposalBase):
    tone: Optional[str] = "профессиональный"

class ProposalUpdate(BaseModel):
    generated_content: Optional[str] = None
    template_used: Optional[str] = None
    tone: Optional[str] = None

class Proposal(ProposalBase):
    id: int
    user_id: int
    generated_content: str
    template_used: Optional[str] = None
    tone: Optional[str] = None
    tokens_used: Optional[int] = None
    generation_time: Optional[int] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# Схемы для генерации предложений
class ProposalGenerationRequest(BaseModel):
    project_description: str
    budget_range: str
    specialization: str
    experience_level: str
    key_requirements: Optional[str] = None
    tone: Optional[str] = "профессиональный"
    generate_multiple: Optional[bool] = False

class ProposalGenerationResponse(BaseModel):
    content: str
    tokens_used: int
    generation_time: int
    model: str

class MultipleProposalsResponse(BaseModel):
    proposals: List[ProposalGenerationResponse]

# Схемы для подписок
class SubscriptionBase(BaseModel):
    plan: str
    status: str = "active"

class SubscriptionCreate(SubscriptionBase):
    user_id: int

class Subscription(SubscriptionBase):
    id: int
    user_id: int
    proposals_per_month: int
    tokens_per_month: int
    start_date: datetime
    end_date: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# Схемы для ответов API
class MessageResponse(BaseModel):
    message: str

class ErrorResponse(BaseModel):
    detail: str 