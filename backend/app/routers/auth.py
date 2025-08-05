from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from ..database import get_db
from ..services.auth_service import AuthService
from ..schemas import UserCreate, User, Token, LoginRequest
from ..models.user import User as UserModel

router = APIRouter(prefix="/auth", tags=["authentication"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

@router.post("/register", response_model=User)
def register(user_data: UserCreate, db: Session = Depends(get_db)):
    """Регистрация нового пользователя"""
    
    # Проверяем, существует ли пользователь с таким email
    existing_user = AuthService.get_user_by_email(db, user_data.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Пользователь с таким email уже существует"
        )
    
    # Создаем нового пользователя
    user = AuthService.create_user(
        db=db,
        email=user_data.email,
        password=user_data.password,
        first_name=user_data.first_name,
        last_name=user_data.last_name,
        specialization=user_data.specialization,
        experience_level=user_data.experience_level,
        bio=user_data.bio
    )
    
    return user

@router.post("/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """Вход пользователя"""
    
    # Аутентифицируем пользователя
    user = AuthService.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверный email или пароль",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Создаем токен доступа
    access_token = AuthService.create_access_token(data={"sub": user.email})
    
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/login-json", response_model=Token)
def login_json(login_data: LoginRequest, db: Session = Depends(get_db)):
    """Вход пользователя через JSON"""
    
    # Аутентифицируем пользователя
    user = AuthService.authenticate_user(db, login_data.email, login_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверный email или пароль",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Создаем токен доступа
    access_token = AuthService.create_access_token(data={"sub": user.email})
    
    return {"access_token": access_token, "token_type": "bearer"}

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    """Получает текущего пользователя по токену"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Не удалось проверить учетные данные",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    email = AuthService.verify_token(token)
    if email is None:
        raise credentials_exception
    
    user = AuthService.get_user_by_email(db, email)
    if user is None:
        raise credentials_exception
    
    return user

@router.get("/me", response_model=User)
def get_current_user_info(current_user: UserModel = Depends(get_current_user)):
    """Получает информацию о текущем пользователе"""
    return current_user 