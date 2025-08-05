from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import JSONResponse
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
import time
from .config import settings
from .database import create_tables
from .routers import auth, proposals

# Создаем лимитер для rate limiting
limiter = Limiter(key_func=get_remote_address)

# Создаем экземпляр FastAPI
app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="AI-помощник для создания выигрышных предложений на Upwork",
    docs_url="/docs",
    redoc_url="/redoc",
    debug=settings.debug
)

# Добавляем rate limiting
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# Добавляем TrustedHost middleware для безопасности
app.add_middleware(
    TrustedHostMiddleware, 
    allowed_hosts=["*"]  # В продакшене укажите конкретные домены
)

# Настраиваем CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

# Middleware для добавления security headers
@app.middleware("http")
async def add_security_headers(request: Request, call_next):
    response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
    response.headers["Content-Security-Policy"] = "default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline';"
    return response

# Middleware для логирования запросов
@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    print(f"📡 {request.method} {request.url.path} - {response.status_code} - {process_time:.3f}s")
    return response

# Подключаем роутеры
app.include_router(auth.router, prefix="/api/v1")
app.include_router(proposals.router, prefix="/api/v1")

@app.on_event("startup")
async def startup_event():
    """Событие запуска приложения"""
    # Создаем таблицы в базе данных
    create_tables()
    print("🚀 Upwork Proposal Generator запущен с защитой!")

@app.get("/")
@limiter.limit("10/minute")
async def root(request: Request):
    """Корневой эндпоинт"""
    return {
        "message": "Добро пожаловать в Upwork Proposal Generator!",
        "version": settings.app_version,
        "docs": "/docs",
        "security": "enabled"
    }

@app.get("/health")
async def health_check():
    """Проверка здоровья приложения"""
    return {
        "status": "healthy", 
        "service": settings.app_name,
        "security": "enabled",
        "rate_limiting": settings.enable_rate_limiting
    }

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    """Обработчик HTTP ошибок"""
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": exc.detail, "path": request.url.path}
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 