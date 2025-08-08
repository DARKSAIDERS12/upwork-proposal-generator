#!/usr/bin/env python3
"""
Настройка AI провайдеров для пользователей из России
"""

import os
import secrets
import subprocess
import sys

def print_banner():
    print("=" * 60)
    print("🇷🇺 НАСТРОЙКА AI ДЛЯ РОССИЙСКИХ ПОЛЬЗОВАТЕЛЕЙ")
    print("=" * 60)
    print("Альтернативные решения для работы с AI из России")
    print("=" * 60)

def create_env_file():
    """Создает файл .env с настройками для российских провайдеров"""
    print("📝 Создание файла .env...")
    
    # Генерируем секретный ключ
    secret_key = secrets.token_urlsafe(32)
    
    # Содержимое файла .env
    env_content = f"""# AI Provider Settings (для пользователей из России)
# Выберите один из провайдеров: demo, yandex, gigachat
AI_PROVIDER=demo

# Yandex GPT API Key (опционально)
# Получите на https://cloud.yandex.ru/docs/foundation-models/quickstart
YANDEX_API_KEY=your-yandex-api-key-here

# GigaChat API Key (опционально)
# Получите на https://developers.sber.ru/portal/products/gigachat
GIGACHAT_API_KEY=your-gigachat-api-key-here

# OpenAI API Key (если используете VPN)
# Получите на https://platform.openai.com/api-keys
OPENAI_API_KEY=sk-your-openai-api-key-here

# Секретный ключ для JWT (автоматически сгенерирован)
SECRET_KEY={secret_key}

# URL базы данных
DATABASE_URL=sqlite:///./upwork_proposals.db

# Настройки приложения
DEBUG=false
APP_NAME=Upwork Proposal Generator
APP_VERSION=1.0.0

# Настройки безопасности
ENABLE_RATE_LIMITING=true
MAX_REQUESTS_PER_MINUTE=60
"""
    
    # Путь к файлу .env
    env_path = os.path.join("backend", ".env")
    
    # Создаем файл
    with open(env_path, "w", encoding="utf-8") as f:
        f.write(env_content)
    
    print(f"✅ Файл .env создан: {env_path}")
    return env_path

def select_ai_provider():
    """Выбор AI провайдера"""
    print("\n🤖 ВЫБОР AI ПРОВАЙДЕРА")
    print("=" * 40)
    print("Доступные варианты:")
    print("1. demo - Демо-режим (работает без API, для тестирования)")
    print("2. yandex - Yandex GPT (российский аналог OpenAI)")
    print("3. gigachat - GigaChat (от Сбера)")
    print("4. openai - OpenAI (требует VPN)")
    print()
    
    while True:
        choice = input("Выберите провайдера (1-4): ").strip()
        
        providers = {
            "1": "demo",
            "2": "yandex", 
            "3": "gigachat",
            "4": "openai"
        }
        
        if choice in providers:
            return providers[choice]
        else:
            print("❌ Неверный выбор. Введите число от 1 до 4.")

def get_api_key(provider):
    """Получает API ключ для выбранного провайдера"""
    
    if provider == "demo":
        return "demo_key"
    
    print(f"\n🔑 ПОЛУЧЕНИЕ API КЛЮЧА ДЛЯ {provider.upper()}")
    print("=" * 40)
    
    if provider == "yandex":
        print("📋 Инструкция для получения Yandex GPT API ключа:")
        print("1. Перейдите на https://cloud.yandex.ru/")
        print("2. Создайте аккаунт или войдите")
        print("3. Перейдите в раздел 'AI Services'")
        print("4. Активируйте Yandex GPT")
        print("5. Создайте API ключ")
        print()
    
    elif provider == "gigachat":
        print("📋 Инструкция для получения GigaChat API ключа:")
        print("1. Перейдите на https://developers.sber.ru/")
        print("2. Создайте аккаунт разработчика")
        print("3. Перейдите в раздел 'GigaChat'")
        print("4. Получите API ключ")
        print()
    
    elif provider == "openai":
        print("📋 Инструкция для получения OpenAI API ключа:")
        print("1. Используйте VPN (США/Европа)")
        print("2. Перейдите на https://platform.openai.com/")
        print("3. Создайте аккаунт")
        print("4. Получите API ключ")
        print()
    
    api_key = input(f"Введите API ключ для {provider} (или нажмите Enter для пропуска): ").strip()
    
    if not api_key:
        print(f"⚠️  API ключ для {provider} не указан. Будет использован демо-режим.")
        return "demo_key"
    
    return api_key

def update_env_file(env_path, provider, api_key):
    """Обновляет файл .env с выбранным провайдером и API ключом"""
    print("📝 Обновление файла .env...")
    
    # Читаем текущий файл
    with open(env_path, "r", encoding="utf-8") as f:
        content = f.read()
    
    # Обновляем провайдера
    content = content.replace("AI_PROVIDER=demo", f"AI_PROVIDER={provider}")
    
    # Обновляем соответствующий API ключ
    if provider == "yandex":
        content = content.replace("your-yandex-api-key-here", api_key)
    elif provider == "gigachat":
        content = content.replace("your-gigachat-api-key-here", api_key)
    elif provider == "openai":
        content = content.replace("sk-your-openai-api-key-here", api_key)
    
    # Записываем обновленный файл
    with open(env_path, "w", encoding="utf-8") as f:
        f.write(content)
    
    print("✅ Настройки обновлены в .env файле")

def test_ai_provider(provider, api_key):
    """Тестирует выбранный AI провайдер"""
    print(f"\n🧪 Тестирование {provider.upper()}...")
    
    try:
        # Импортируем наш модуль
        sys.path.append(os.path.join("backend"))
        from alternative_ai_providers import get_ai_provider
        
        # Создаем провайдера
        ai_provider = get_ai_provider(provider, api_key)
        
        # Тестовые данные
        test_data = {
            "title": "Website Development",
            "description": "Need a modern responsive website",
            "budget": "$1000-2000",
            "specialization": "Web Development",
            "tone": "Professional"
        }
        
        # Генерируем тестовое предложение
        result = ai_provider.generate_proposal(test_data)
        
        print("✅ AI провайдер работает!")
        print(f"📝 Тестовое предложение: {result[:100]}...")
        return True
        
    except Exception as e:
        print(f"❌ Ошибка тестирования {provider}: {e}")
        return False

def show_instructions():
    """Показывает инструкции по использованию"""
    print("\n" + "=" * 60)
    print("🎉 НАСТРОЙКА ЗАВЕРШЕНА!")
    print("=" * 60)
    
    print("\n📋 Следующие шаги:")
    print("1. Перезапустите серверы: python3 stop_servers.py && python3 quick_start.py")
    print("2. Откройте сайт: http://localhost:3000")
    print("3. Протестируйте генерацию предложений")
    
    print("\n🔗 Полезные ссылки:")
    print("• Yandex GPT: https://cloud.yandex.ru/docs/foundation-models/quickstart")
    print("• GigaChat: https://developers.sber.ru/portal/products/gigachat")
    print("• OpenAI (с VPN): https://platform.openai.com/api-keys")
    
    print("\n💡 Советы:")
    print("• Демо-режим работает без API ключей")
    print("• Для продакшена рекомендуется использовать Yandex GPT или GigaChat")
    print("• OpenAI доступен только через VPN")

def main():
    print_banner()
    
    # Создаем файл .env
    env_path = create_env_file()
    
    # Выбираем AI провайдера
    provider = select_ai_provider()
    
    # Получаем API ключ
    api_key = get_api_key(provider)
    
    # Обновляем файл с настройками
    update_env_file(env_path, provider, api_key)
    
    # Тестируем провайдера
    test_ai_provider(provider, api_key)
    
    # Показываем инструкции
    show_instructions()
    
    # Спрашиваем о перезапуске
    restart = input("\n🔄 Перезапустить серверы сейчас? (y/n): ").strip().lower()
    if restart == 'y':
        print("🔄 Перезапуск серверов...")
        subprocess.run([sys.executable, "stop_servers.py"], check=True)
        subprocess.run([sys.executable, "quick_start.py"], check=True)
        print("✅ Серверы перезапущены!")
    
    print("\n🎯 Готово! Проект настроен для работы из России!")

if __name__ == "__main__":
    main() 