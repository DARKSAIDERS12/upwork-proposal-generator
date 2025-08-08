#!/usr/bin/env python3
"""
🧪 ТЕСТИРОВАНИЕ СИСТЕМЫ ПОДПИСОК
============================================================
Скрипт для проверки работы системы монетизации
"""

import sqlite3
import os
from datetime import datetime, timedelta
import json

def create_test_database():
    """Создание тестовой базы данных"""
    print("🗄️ Создание тестовой базы данных...")
    
    conn = sqlite3.connect('test_subscriptions.db')
    cursor = conn.cursor()
    
    # Создание таблиц
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            subscription_type TEXT DEFAULT 'free',
            daily_remaining INTEGER DEFAULT 3,
            last_reset_date DATE DEFAULT CURRENT_DATE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS payments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            amount REAL NOT NULL,
            currency TEXT DEFAULT 'USD',
            status TEXT DEFAULT 'pending',
            stripe_payment_id TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS subscriptions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            plan_type TEXT NOT NULL,
            status TEXT DEFAULT 'active',
            start_date DATE DEFAULT CURRENT_DATE,
            end_date DATE,
            stripe_subscription_id TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    
    conn.commit()
    print("✅ База данных создана")
    return conn

def add_test_users(conn):
    """Добавление тестовых пользователей"""
    print("\n👥 Добавление тестовых пользователей...")
    
    cursor = conn.cursor()
    
    # Тестовые пользователи
    test_users = [
        ('test_free@example.com', 'password123', 'free', 3),
        ('test_premium@example.com', 'password123', 'premium', 999),
        ('test_expired@example.com', 'password123', 'free', 0),
    ]
    
    for email, password, subscription, remaining in test_users:
        try:
            cursor.execute('''
                INSERT INTO users (email, password_hash, subscription_type, daily_remaining)
                VALUES (?, ?, ?, ?)
            ''', (email, f"hash_{password}", subscription, remaining))
            print(f"✅ Добавлен пользователь: {email} ({subscription})")
        except sqlite3.IntegrityError:
            print(f"⚠️ Пользователь уже существует: {email}")
    
    conn.commit()

def test_subscription_limits(conn):
    """Тестирование лимитов подписок"""
    print("\n🎯 Тестирование лимитов подписок...")
    
    cursor = conn.cursor()
    
    # Получаем всех пользователей
    cursor.execute('SELECT id, email, subscription_type, daily_remaining FROM users')
    users = cursor.fetchall()
    
    for user_id, email, subscription_type, daily_remaining in users:
        print(f"\n👤 Пользователь: {email}")
        print(f"   Подписка: {subscription_type}")
        print(f"   Осталось предложений: {daily_remaining}")
        
        # Проверяем возможность генерации
        if subscription_type == 'premium':
            can_generate = True
            reason = "Premium подписка - неограниченно"
        elif daily_remaining > 0:
            can_generate = True
            reason = f"Бесплатная подписка - осталось {daily_remaining}"
        else:
            can_generate = False
            reason = "Лимит исчерпан"
        
        print(f"   Может генерировать: {'✅ Да' if can_generate else '❌ Нет'}")
        print(f"   Причина: {reason}")
        
        # Симулируем генерацию предложения
        if can_generate and subscription_type == 'free':
            new_remaining = daily_remaining - 1
            cursor.execute('''
                UPDATE users SET daily_remaining = ? WHERE id = ?
            ''', (new_remaining, user_id))
            print(f"   🔄 После генерации останется: {new_remaining}")
    
    conn.commit()

def test_daily_reset(conn):
    """Тестирование ежедневного сброса лимитов"""
    print("\n🔄 Тестирование ежедневного сброса...")
    
    cursor = conn.cursor()
    
    # Устанавливаем вчерашнюю дату для некоторых пользователей
    yesterday = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
    
    cursor.execute('''
        UPDATE users 
        SET last_reset_date = ?, daily_remaining = 0 
        WHERE email = 'test_expired@example.com'
    ''', (yesterday,))
    
    # Проверяем сброс
    cursor.execute('''
        SELECT email, daily_remaining, last_reset_date 
        FROM users 
        WHERE email = 'test_expired@example.com'
    ''')
    user = cursor.fetchone()
    
    if user:
        email, remaining, last_reset = user
        current_date = datetime.now().strftime('%Y-%m-%d')
        
        if last_reset < current_date:
            # Сбрасываем лимит
            cursor.execute('''
                UPDATE users 
                SET daily_remaining = 3, last_reset_date = ? 
                WHERE email = ?
            ''', (current_date, email))
            print(f"✅ Сброс лимита для {email}: 0 → 3")
        else:
            print(f"⚠️ Сброс не требуется для {email}")
    
    conn.commit()

def test_payment_simulation(conn):
    """Симуляция платежей"""
    print("\n💳 Симуляция платежей...")
    
    cursor = conn.cursor()
    
    # Получаем пользователя для обновления
    cursor.execute('SELECT id, email FROM users WHERE subscription_type = "free" LIMIT 1')
    user = cursor.fetchone()
    
    if user:
        user_id, email = user
        
        # Симулируем успешный платеж
        cursor.execute('''
            INSERT INTO payments (user_id, amount, currency, status, stripe_payment_id)
            VALUES (?, ?, ?, ?, ?)
        ''', (user_id, 9.99, 'USD', 'completed', 'pi_test_123'))
        
        # Обновляем подписку
        cursor.execute('''
            UPDATE users 
            SET subscription_type = 'premium', daily_remaining = 999 
            WHERE id = ?
        ''', (user_id,))
        
        # Добавляем запись о подписке
        end_date = (datetime.now() + timedelta(days=30)).strftime('%Y-%m-%d')
        cursor.execute('''
            INSERT INTO subscriptions (user_id, plan_type, status, end_date, stripe_subscription_id)
            VALUES (?, ?, ?, ?, ?)
        ''', (user_id, 'premium', 'active', end_date, 'sub_test_123'))
        
        print(f"✅ Пользователь {email} обновлен до Premium")
    
    conn.commit()

def show_database_state(conn):
    """Показать состояние базы данных"""
    print("\n📊 Состояние базы данных:")
    
    cursor = conn.cursor()
    
    # Пользователи
    print("\n👥 Пользователи:")
    cursor.execute('''
        SELECT email, subscription_type, daily_remaining, last_reset_date 
        FROM users
    ''')
    users = cursor.fetchall()
    
    for email, subscription, remaining, reset_date in users:
        print(f"   {email}: {subscription} ({remaining} предложений, сброс: {reset_date})")
    
    # Платежи
    print("\n💳 Платежи:")
    cursor.execute('SELECT user_id, amount, status, created_at FROM payments')
    payments = cursor.fetchall()
    
    for user_id, amount, status, created_at in payments:
        print(f"   Пользователь {user_id}: ${amount} ({status}) - {created_at}")
    
    # Подписки
    print("\n📅 Подписки:")
    cursor.execute('SELECT user_id, plan_type, status, end_date FROM subscriptions')
    subscriptions = cursor.fetchall()
    
    for user_id, plan, status, end_date in subscriptions:
        print(f"   Пользователь {user_id}: {plan} ({status}) до {end_date}")

def main():
    """Основная функция тестирования"""
    print("=" * 60)
    print("🧪 ТЕСТИРОВАНИЕ СИСТЕМЫ ПОДПИСОК")
    print("=" * 60)
    
    # Создаем тестовую базу данных
    conn = create_test_database()
    
    try:
        # Добавляем тестовых пользователей
        add_test_users(conn)
        
        # Показываем начальное состояние
        show_database_state(conn)
        
        # Тестируем лимиты
        test_subscription_limits(conn)
        
        # Тестируем сброс
        test_daily_reset(conn)
        
        # Симулируем платеж
        test_payment_simulation(conn)
        
        # Показываем финальное состояние
        show_database_state(conn)
        
        print("\n" + "=" * 60)
        print("✅ ТЕСТИРОВАНИЕ ЗАВЕРШЕНО")
        print("=" * 60)
        
    finally:
        conn.close()
        # Удаляем тестовую базу данных
        if os.path.exists('test_subscriptions.db'):
            os.remove('test_subscriptions.db')
            print("🗑️ Тестовая база данных удалена")

if __name__ == "__main__":
    main() 