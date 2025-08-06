#!/usr/bin/env python3
"""
Автоматическая настройка OpenAI API ключа для Upwork Proposal Generator
"""

import os
import secrets
import subprocess
import sys

def print_banner():
    print("=" * 60)
    print("🔑 НАСТРОЙКА OPENAI API КЛЮЧА")
    print("=" * 60)
    print("Автоматическая настройка для Upwork Proposal Generator")
    print("=" * 60)

def generate_secret_key():
    """Генерирует безопасный секретный ключ"""
    return secrets.token_urlsafe(32)

def create_env_file():
    """Создает файл .env с настройками"""
    print("📝 Создание файла .env...")
    
    # Генерируем секретный ключ
    secret_key = generate_secret_key()
    
    # Содержимое файла .env
    env_content = f"""# OpenAI API Key (замените на ваш реальный ключ)
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

def get_openai_api_key():
    """Получает OpenAI API ключ от пользователя"""
    print("\n🔑 НАСТРОЙКА OPENAI API КЛЮЧА")
    print("=" * 40)
    print("Для работы генерации предложений нужен OpenAI API ключ.")
    print("Получите его на https://platform.openai.com/api-keys")
    print()
    
    while True:
        api_key = input("Введите ваш OpenAI API ключ (или нажмите Enter для пропуска): ").strip()
        
        if not api_key:
            print("⚠️  API ключ не указан. Генерация предложений будет работать в демо-режиме.")
            return None
        
        if api_key.startswith("sk-") and len(api_key) > 20:
            print("✅ API ключ выглядит корректно!")
            return api_key
        else:
            print("❌ Неверный формат API ключа. Ключ должен начинаться с 'sk-' и быть длиннее 20 символов.")
            retry = input("Попробовать снова? (y/n): ").strip().lower()
            if retry != 'y':
                return None

def update_env_file(env_path, api_key):
    """Обновляет файл .env с реальным API ключом"""
    if not api_key:
        return
    
    print("📝 Обновление файла .env с API ключом...")
    
    # Читаем текущий файл
    with open(env_path, "r", encoding="utf-8") as f:
        content = f.read()
    
    # Заменяем placeholder на реальный ключ
    content = content.replace("sk-your-openai-api-key-here", api_key)
    
    # Записываем обновленный файл
    with open(env_path, "w", encoding="utf-8") as f:
        f.write(content)
    
    print("✅ API ключ добавлен в .env файл")

def test_openai_connection(api_key):
    """Тестирует подключение к OpenAI API"""
    if not api_key:
        print("⚠️  API ключ не настроен. Пропускаем тест.")
        return False
    
    print("🧪 Тестирование подключения к OpenAI API...")
    
    try:
        import openai
        openai.api_key = api_key
        
        # Простой тест API
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": "Привет! Это тест."}],
            max_tokens=10
        )
        
        print("✅ Подключение к OpenAI API успешно!")
        return True
        
    except Exception as e:
        print(f"❌ Ошибка подключения к OpenAI API: {e}")
        print("💡 Проверьте правильность API ключа и наличие кредитов на аккаунте.")
        return False

def restart_servers():
    """Перезапускает серверы с новыми настройками"""
    print("\n🔄 Перезапуск серверов...")
    
    # Останавливаем серверы
    subprocess.run([sys.executable, "stop_servers.py"], check=True)
    
    # Запускаем заново
    subprocess.run([sys.executable, "quick_start.py"], check=True)
    
    print("✅ Серверы перезапущены с новыми настройками!")

def main():
    print_banner()
    
    # Создаем файл .env
    env_path = create_env_file()
    
    # Получаем API ключ от пользователя
    api_key = get_openai_api_key()
    
    # Обновляем файл с API ключом
    update_env_file(env_path, api_key)
    
    # Тестируем подключение
    if api_key:
        test_openai_connection(api_key)
    
    # Показываем инструкции
    print("\n" + "=" * 60)
    print("🎉 НАСТРОЙКА ЗАВЕРШЕНА!")
    print("=" * 60)
    
    if api_key:
        print("✅ OpenAI API ключ настроен")
        print("✅ Генерация предложений будет работать полностью")
    else:
        print("⚠️  OpenAI API ключ не настроен")
        print("⚠️  Генерация предложений будет работать в демо-режиме")
    
    print("\n📋 Следующие шаги:")
    print("1. Перезапустите серверы: python3 stop_servers.py && python3 quick_start.py")
    print("2. Откройте сайт: http://192.168.0.124:3000")
    print("3. Протестируйте генерацию предложений")
    
    # Спрашиваем о перезапуске
    restart = input("\n🔄 Перезапустить серверы сейчас? (y/n): ").strip().lower()
    if restart == 'y':
        restart_servers()
    
    print("\n🎯 Готово! Проект настроен и готов к использованию!")

if __name__ == "__main__":
    main() 