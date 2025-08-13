#!/usr/bin/env python3
"""
Скрипт для миграции пользователей из localStorage в новую базу данных
"""

import sqlite3
import hashlib
import os
import json
from datetime import datetime

# Путь к базе данных
DB_PATH = os.path.join(os.path.dirname(__file__), 'users.db')

def hash_password(password):
    """Хеширование пароля"""
    return hashlib.sha256(password.encode()).hexdigest()

def init_db():
    """Инициализация базы данных"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Создаем таблицу пользователей
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            subscription TEXT DEFAULT 'free',
            daily_proposals INTEGER DEFAULT 3,
            daily_remaining INTEGER DEFAULT 3,
            last_reset_date TEXT,
            created_at TEXT,
            last_login TEXT
        )
    ''')
    
    conn.commit()
    conn.close()

def migrate_from_localstorage():
    """Миграция пользователей из localStorage (если есть)"""
    print("🔄 Начинаем миграцию пользователей...")
    
    # Здесь можно добавить логику для импорта пользователей из других источников
    # Например, из JSON файла или другой базы данных
    
    # Создаем тестового пользователя для демонстрации
    test_users = [
        {
            'email': 'demo@example.com',
            'password': 'demo123',
            'subscription': 'free',
            'daily_proposals': 3,
            'daily_remaining': 3
        }
    ]
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    for user_data in test_users:
        try:
            # Проверяем, не существует ли уже пользователь
            cursor.execute('SELECT id FROM users WHERE email = ?', (user_data['email'],))
            if cursor.fetchone():
                print(f"⚠️  Пользователь {user_data['email']} уже существует")
                continue
            
            # Создаем пользователя
            today = datetime.now().date().isoformat()
            cursor.execute('''
                INSERT INTO users (email, password_hash, subscription, daily_proposals, daily_remaining, last_reset_date, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (
                user_data['email'],
                hash_password(user_data['password']),
                user_data['subscription'],
                user_data['daily_proposals'],
                user_data['daily_remaining'],
                today,
                datetime.now().isoformat()
            ))
            
            print(f"✅ Пользователь {user_data['email']} создан")
            
        except Exception as e:
            print(f"❌ Ошибка создания пользователя {user_data['email']}: {e}")
    
    conn.commit()
    conn.close()
    
    print("🎉 Миграция завершена!")

def show_users():
    """Показать всех пользователей в базе"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute('SELECT id, email, subscription, daily_remaining, created_at FROM users')
    users = cursor.fetchall()
    
    print("\n📋 Список пользователей в базе:")
    print("-" * 80)
    print(f"{'ID':<5} {'Email':<25} {'Подписка':<12} {'Лимит':<8} {'Дата создания'}")
    print("-" * 80)
    
    for user in users:
        user_id, email, subscription, daily_remaining, created_at = user
        print(f"{user_id:<5} {email:<25} {subscription:<12} {daily_remaining:<8} {created_at[:10]}")
    
    conn.close()

if __name__ == '__main__':
    print("🚀 Скрипт миграции пользователей")
    print("=" * 50)
    
    # Инициализируем базу данных
    init_db()
    print("✅ База данных инициализирована")
    
    # Мигрируем пользователей
    migrate_from_localstorage()
    
    # Показываем результат
    show_users()
    
    print("\n🎯 Теперь вы можете:")
    print("1. Запустить сервер аутентификации: python auth_server.py")
    print("2. Войти в аккаунт с любого устройства!")
    print("3. Все данные будут синхронизированы между устройствами") 