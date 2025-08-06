#!/usr/bin/env python3
"""
Простой скрипт для добавления OpenAI API ключа
"""

import os

def add_api_key():
    print("🔑 ДОБАВЛЕНИЕ OPENAI API КЛЮЧА")
    print("=" * 40)
    
    # Путь к файлу .env
    env_path = "backend/.env"
    
    if not os.path.exists(env_path):
        print("❌ Файл .env не найден. Сначала запустите setup_openai.py")
        return
    
    print("📝 Введите ваш OpenAI API ключ:")
    print("💡 Получите его на https://platform.openai.com/api-keys")
    print("🔑 Ключ должен начинаться с 'sk-'")
    print()
    
    api_key = input("API ключ: ").strip()
    
    if not api_key:
        print("⚠️  Ключ не введен. Пропускаем.")
        return
    
    if not api_key.startswith("sk-"):
        print("❌ Неверный формат ключа. Ключ должен начинаться с 'sk-'")
        return
    
    # Читаем текущий файл
    with open(env_path, "r", encoding="utf-8") as f:
        content = f.read()
    
    # Заменяем placeholder на реальный ключ
    content = content.replace("sk-your-openai-api-key-here", api_key)
    
    # Записываем обновленный файл
    with open(env_path, "w", encoding="utf-8") as f:
        f.write(content)
    
    print("✅ API ключ успешно добавлен!")
    print("🔄 Перезапустите серверы для применения изменений:")
    print("   python3 stop_servers.py && python3 quick_start.py")

if __name__ == "__main__":
    add_api_key() 