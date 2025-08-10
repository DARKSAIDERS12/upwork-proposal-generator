#!/usr/bin/env python3
"""
Российская система платежей для Upwork Proposal Generator
Интеграция с ЮKassa для работы в рублях
"""

import os
import json
import sqlite3
from datetime import datetime, timedelta
from typing import Dict, Any, Optional
import requests

class RussianPaymentSystem:
    """Система управления платежами для российских пользователей"""
    
    def __init__(self):
        # Конфигурация ЮKassa
        self.yookassa_shop_id = os.getenv('YOOKASSA_SHOP_ID', 'your-shop-id')
        self.yookassa_secret_key = os.getenv('YOOKASSA_SECRET_KEY', 'your-secret-key')
        
        # Конфигурация тарифов в рублях
        self.pricing = {
            'premium': {'price': 1500, 'currency': 'RUB', 'period': 'month'},
            'pro': {'price': 3000, 'currency': 'RUB', 'period': 'month'},
            'enterprise': {'price': 9900, 'currency': 'RUB', 'period': 'month'}
        }
        
        # Инициализация базы данных
        self.init_database()
    
    def init_database(self):
        """Инициализация базы данных для платежей"""
        conn = sqlite3.connect('upwork_proposals.db')
        cursor = conn.cursor()
        
        # Таблица пользователей
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                subscription_status TEXT DEFAULT 'free',
                subscription_expires DATETIME,
                proposals_count INTEGER DEFAULT 0,
                daily_proposals_count INTEGER DEFAULT 0,
                last_proposal_date DATE,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Таблица платежей ЮKassa
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS yookassa_payments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                payment_id TEXT UNIQUE,
                amount INTEGER,
                currency TEXT DEFAULT 'RUB',
                status TEXT,
                plan_type TEXT,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')
        
        # Таблица подписок
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS subscriptions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                payment_id TEXT,
                plan_type TEXT,
                status TEXT,
                current_period_start DATETIME,
                current_period_end DATETIME,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def create_payment(self, user_id: int, plan_type: str, email: str) -> Dict[str, Any]:
        """Создает платеж в ЮKassa"""
        
        if plan_type not in self.pricing:
            return {'error': 'Неверный тип плана'}
        
        plan = self.pricing[plan_type]
        
        # Создаем платеж в ЮKassa
        payment_data = {
            'amount': {
                'value': str(plan['price']),
                'currency': plan['currency']
            },
            'confirmation': {
                'type': 'redirect',
                'return_url': f"https://darksaiders12.github.io/upwork-proposal-generator/payment_success.html?plan={plan_type}"
            },
            'capture': True,
            'description': f'Подписка {plan_type.upper()} на Upwork Proposal Generator',
            'metadata': {
                'user_id': str(user_id),
                'plan_type': plan_type,
                'email': email
            }
        }
        
        try:
            # В реальности здесь будет запрос к API ЮKassa
            # Пока используем имитацию
            payment_id = f"yookassa_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{user_id}"
            
            # Сохраняем платеж в базу
            self.save_payment(user_id, payment_id, plan['price'], plan['currency'], 'pending', plan_type)
            
            return {
                'success': True,
                'payment_id': payment_id,
                'amount': plan['price'],
                'currency': plan['currency'],
                'confirmation_url': f"https://yoomoney.ru/checkout/payments/v2/contract?orderId={payment_id}"
            }
            
        except Exception as e:
            return {'error': f'Ошибка создания платежа: {str(e)}'}
    
    def save_payment(self, user_id: int, payment_id: str, amount: int, currency: str, status: str, plan_type: str):
        """Сохраняет платеж в базу данных"""
        conn = sqlite3.connect('upwork_proposals.db')
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO yookassa_payments (user_id, payment_id, amount, currency, status, plan_type)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (user_id, payment_id, amount, currency, status, plan_type))
        
        conn.commit()
        conn.close()
    
    def confirm_payment(self, payment_id: str) -> bool:
        """Подтверждает успешный платеж"""
        conn = sqlite3.connect('upwork_proposals.db')
        cursor = conn.cursor()
        
        # Обновляем статус платежа
        cursor.execute('''
            UPDATE yookassa_payments 
            SET status = 'succeeded' 
            WHERE payment_id = ?
        ''', (payment_id,))
        
        # Получаем данные платежа
        cursor.execute('''
            SELECT user_id, plan_type FROM yookassa_payments 
            WHERE payment_id = ?
        ''', (payment_id,))
        
        result = cursor.fetchone()
        if result:
            user_id, plan_type = result
            
            # Активируем подписку
            self.activate_subscription(user_id, plan_type, payment_id)
            
            conn.commit()
            conn.close()
            return True
        
        conn.close()
        return False
    
    def activate_subscription(self, user_id: int, plan_type: str, payment_id: str):
        """Активирует подписку пользователя"""
        conn = sqlite3.connect('upwork_proposals.db')
        cursor = conn.cursor()
        
        # Обновляем статус пользователя
        cursor.execute('''
            UPDATE users 
            SET subscription_status = ?, subscription_expires = ?
            WHERE id = ?
        ''', (plan_type, datetime.now() + timedelta(days=30), user_id))
        
        # Создаем запись о подписке
        cursor.execute('''
            INSERT INTO subscriptions (user_id, payment_id, plan_type, status, current_period_start, current_period_end)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (user_id, payment_id, plan_type, 'active', datetime.now(), datetime.now() + timedelta(days=30)))
        
        conn.commit()
        conn.close()
    
    def get_user_subscription_status(self, user_id: int) -> str:
        """Получает статус подписки пользователя"""
        conn = sqlite3.connect('upwork_proposals.db')
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT subscription_status, subscription_expires 
            FROM users WHERE id = ?
        ''', (user_id,))
        
        result = cursor.fetchone()
        conn.close()
        
        if not result:
            return 'free'
        
        status, expires = result
        
        # Проверяем, не истекла ли подписка
        if expires and datetime.fromisoformat(expires) < datetime.now():
            return 'free'
        
        return status
    
    def can_generate_proposal(self, user_id: int) -> Dict[str, Any]:
        """Проверяет, может ли пользователь генерировать предложения"""
        status = self.get_user_subscription_status(user_id)
        
        # Получаем дневной лимит
        daily_limit = self.get_daily_limit(status)
        daily_used = self.get_daily_usage(user_id)
        
        can_generate = daily_used < daily_limit
        
        return {
            'can_generate': can_generate,
            'subscription_status': status,
            'daily_limit': daily_limit,
            'daily_used': daily_used,
            'daily_remaining': max(0, daily_limit - daily_used)
        }
    
    def get_daily_limit(self, subscription_status: str) -> int:
        """Получает дневной лимит для типа подписки"""
        limits = {
            'free': 3,
            'premium': 50,
            'pro': 200,
            'enterprise': -1  # Безлимит
        }
        return limits.get(subscription_status, 3)
    
    def get_daily_usage(self, user_id: int) -> int:
        """Получает количество использованных предложений за день"""
        conn = sqlite3.connect('upwork_proposals.db')
        cursor = conn.cursor()
        
        today = datetime.now().date()
        
        cursor.execute('''
            SELECT daily_proposals_count FROM users 
            WHERE id = ? AND last_proposal_date = ?
        ''', (user_id, today))
        
        result = cursor.fetchone()
        conn.close()
        
        return result[0] if result else 0
    
    def increment_proposal_count(self, user_id: int):
        """Увеличивает счетчик предложений пользователя"""
        conn = sqlite3.connect('upwork_proposals.db')
        cursor = conn.cursor()
        
        today = datetime.now().date()
        
        cursor.execute('''
            UPDATE users 
            SET daily_proposals_count = daily_proposals_count + 1,
                last_proposal_date = ?,
                proposals_count = proposals_count + 1
            WHERE id = ?
        ''', (today, user_id))
        
        conn.commit()
        conn.close()
    
    def get_pricing_info(self) -> Dict[str, Any]:
        """Возвращает информацию о тарифах"""
        return {
            'currency': 'RUB',
            'plans': self.pricing
        }
    
    def cancel_subscription(self, user_id: int) -> bool:
        """Отменяет подписку пользователя"""
        conn = sqlite3.connect('upwork_proposals.db')
        cursor = conn.cursor()
        
        # Обновляем статус пользователя
        cursor.execute('''
            UPDATE users 
            SET subscription_status = 'free', subscription_expires = NULL
            WHERE id = ?
        ''', (user_id,))
        
        # Обновляем статус подписки
        cursor.execute('''
            UPDATE subscriptions 
            SET status = 'cancelled' 
            WHERE user_id = ? AND status = 'active'
        ''', (user_id,))
        
        conn.commit()
        conn.close()
        return True

# Тестирование системы
def test_russian_payment_system():
    """Тестирует российскую систему платежей"""
    print("🧪 Тестирование российской системы платежей...")
    
    payment_system = RussianPaymentSystem()
    
    # Тест создания платежа
    payment_result = payment_system.create_payment(1, 'premium', 'test@example.com')
    print(f"✅ Создание платежа: {payment_result}")
    
    # Тест получения информации о тарифах
    pricing = payment_system.get_pricing_info()
    print(f"✅ Тарифы: {pricing}")
    
    # Тест проверки лимитов
    limits = payment_system.can_generate_proposal(1)
    print(f"✅ Проверка лимитов: {limits}")
    
    print("✅ Тестирование завершено!")

if __name__ == "__main__":
    test_russian_payment_system() 