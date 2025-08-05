#!/usr/bin/env python3
"""
Тестовый скрипт для демонстрации работы Upwork Proposal Generator API
"""

import requests
import json
import time

# Конфигурация
BASE_URL = "http://localhost:8000"
API_BASE = f"{BASE_URL}/api/v1"

def print_section(title):
    print(f"\n{'='*50}")
    print(f"  {title}")
    print(f"{'='*50}")

def test_health():
    """Тест проверки здоровья сервера"""
    print_section("ПРОВЕРКА ЗДОРОВЬЯ СЕРВЕРА")
    
    try:
        response = requests.get(f"{BASE_URL}/health")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Сервер работает: {data['service']}")
            print(f"📊 Статус: {data['status']}")
            return True
        else:
            print(f"❌ Ошибка: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Ошибка подключения: {e}")
        return False

def test_registration():
    """Тест регистрации пользователя"""
    print_section("РЕГИСТРАЦИЯ ПОЛЬЗОВАТЕЛЯ")
    
    user_data = {
        "email": f"test_{int(time.time())}@example.com",
        "password": "testpass123",
        "first_name": "Тестовый",
        "last_name": "Пользователь",
        "specialization": "Веб-разработка",
        "experience_level": "3-5 лет"
    }
    
    try:
        response = requests.post(f"{API_BASE}/auth/register", json=user_data)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Пользователь зарегистрирован!")
            print(f"📧 Email: {data['email']}")
            print(f"👤 Имя: {data['first_name']} {data['last_name']}")
            print(f"🆔 ID: {data['id']}")
            return data
        else:
            print(f"❌ Ошибка регистрации: {response.status_code}")
            print(f"📝 Ответ: {response.text}")
            return None
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        return None

def test_login(email, password):
    """Тест входа в систему"""
    print_section("ВХОД В СИСТЕМУ")
    
    login_data = {
        "email": email,
        "password": password
    }
    
    try:
        response = requests.post(f"{API_BASE}/auth/login-json", json=login_data)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Вход выполнен успешно!")
            print(f"🔑 Токен получен: {data['token_type']}")
            print(f"⏰ Токен действителен 30 минут")
            return data['access_token']
        else:
            print(f"❌ Ошибка входа: {response.status_code}")
            print(f"📝 Ответ: {response.text}")
            return None
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        return None

def test_proposal_generation(token):
    """Тест генерации предложения"""
    print_section("ГЕНЕРАЦИЯ ПРЕДЛОЖЕНИЯ")
    
    proposal_data = {
        "project_description": "Нужен разработчик для создания интернет-магазина на WordPress с интеграцией платежных систем. Требуется современный дизайн и адаптивная верстка.",
        "budget_range": "$1000-5000",
        "specialization": "Веб-разработка",
        "experience_level": "3-5 лет",
        "key_requirements": "WordPress, WooCommerce, PHP, JavaScript",
        "tone": "профессиональный"
    }
    
    headers = {"Authorization": f"Bearer {token}"}
    
    try:
        print("🔄 Генерируем предложение...")
        response = requests.post(f"{API_BASE}/proposals/generate", json=proposal_data, headers=headers)
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Предложение сгенерировано!")
            print(f"📊 Использовано токенов: {data['tokens_used']}")
            print(f"⏱️ Время генерации: {data['generation_time']} сек")
            print(f"🤖 Модель: {data['model']}")
            print(f"\n📝 СОДЕРЖАНИЕ ПРЕДЛОЖЕНИЯ:")
            print(f"{'='*50}")
            print(data['content'])
            print(f"{'='*50}")
            return data
        else:
            print(f"❌ Ошибка генерации: {response.status_code}")
            print(f"📝 Ответ: {response.text}")
            return None
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        return None

def test_get_proposals(token):
    """Тест получения списка предложений"""
    print_section("СПИСОК ПРЕДЛОЖЕНИЙ")
    
    headers = {"Authorization": f"Bearer {token}"}
    
    try:
        response = requests.get(f"{API_BASE}/proposals/", headers=headers)
        if response.status_code == 200:
            proposals = response.json()
            print(f"✅ Получено предложений: {len(proposals)}")
            for i, proposal in enumerate(proposals, 1):
                print(f"\n📄 Предложение #{i}:")
                print(f"   🆔 ID: {proposal['id']}")
                print(f"   💰 Бюджет: {proposal['budget_range']}")
                print(f"   🎯 Специализация: {proposal['specialization']}")
                print(f"   📅 Создано: {proposal['created_at']}")
            return proposals
        else:
            print(f"❌ Ошибка получения: {response.status_code}")
            return None
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        return None

def main():
    """Основная функция тестирования"""
    print("🚀 ТЕСТИРОВАНИЕ UPWORK PROPOSAL GENERATOR API")
    print("=" * 60)
    
    # 1. Проверка здоровья сервера
    if not test_health():
        print("❌ Сервер не работает. Запустите backend!")
        return
    
    # 2. Регистрация пользователя
    user = test_registration()
    if not user:
        print("❌ Не удалось зарегистрировать пользователя")
        return
    
    # 3. Вход в систему
    token = test_login(user['email'], "testpass123")
    if not token:
        print("❌ Не удалось войти в систему")
        return
    
    # 4. Генерация предложения
    proposal = test_proposal_generation(token)
    if not proposal:
        print("❌ Не удалось сгенерировать предложение")
        return
    
    # 5. Получение списка предложений
    proposals = test_get_proposals(token)
    
    print_section("ТЕСТИРОВАНИЕ ЗАВЕРШЕНО")
    print("✅ Все основные функции работают корректно!")
    print("🎯 Backend готов к использованию!")
    print("\n📚 Документация API: http://localhost:8000/docs")
    print("🌐 Swagger UI: http://localhost:8000/docs")

if __name__ == "__main__":
    main() 