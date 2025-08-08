#!/usr/bin/env python3
"""
Система платежей для Upwork Proposal Generator
Интеграция со Stripe для монетизации
"""

import os
import stripe
import json
from datetime import datetime, timedelta
from typing import Dict, Any, Optional
import sqlite3

class PaymentSystem:
    """Система управления платежами и подписками"""
    
    def __init__(self):
        # Инициализация Stripe
        self.stripe_secret_key = os.getenv('STRIPE_SECRET_KEY', 'sk_test_...')
        self.stripe_publishable_key = os.getenv('STRIPE_PUBLISHABLE_KEY', 'pk_test_...')
        stripe.api_key = self.stripe_secret_key
        
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
        
        # Таблица платежей
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS payments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                stripe_payment_id TEXT,
                amount INTEGER,
                currency TEXT DEFAULT 'usd',
                status TEXT,
                subscription_id TEXT,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')
        
        # Таблица подписок
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS subscriptions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                stripe_subscription_id TEXT,
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
    
    def create_customer(self, email: str, user_id: int) -> str:
        """Создает клиента в Stripe"""
        try:
            customer = stripe.Customer.create(
                email=email,
                metadata={'user_id': user_id}
            )
            return customer.id
        except Exception as e:
            print(f"Ошибка создания клиента Stripe: {e}")
            return None
    
    def create_subscription(self, user_id: int, plan_type: str = 'premium') -> Dict[str, Any]:
        """Создает подписку в Stripe"""
        
        # Получаем данные пользователя
        user = self.get_user(user_id)
        if not user:
            return {'error': 'Пользователь не найден'}
        
        # Цены в Stripe (в центах)
        prices = {
            'premium': {
                'monthly': 'price_monthly_premium',  # $9.99/мес
                'yearly': 'price_yearly_premium'     # $99.99/год
            }
        }
        
        try:
            # Создаем или получаем клиента
            customer_id = self.get_stripe_customer_id(user_id)
            if not customer_id:
                customer_id = self.create_customer(user['email'], user_id)
            
            # Создаем подписку
            subscription = stripe.Subscription.create(
                customer=customer_id,
                items=[{'price': prices[plan_type]['monthly']}],
                payment_behavior='default_incomplete',
                payment_settings={'save_default_payment_method': 'on_subscription'},
                expand=['latest_invoice.payment_intent'],
            )
            
            # Сохраняем в базу данных
            self.save_subscription(user_id, subscription.id, plan_type, subscription.status)
            
            return {
                'subscription_id': subscription.id,
                'client_secret': subscription.latest_invoice.payment_intent.client_secret,
                'status': subscription.status
            }
            
        except Exception as e:
            print(f"Ошибка создания подписки: {e}")
            return {'error': str(e)}
    
    def cancel_subscription(self, user_id: int) -> bool:
        """Отменяет подписку"""
        try:
            subscription_id = self.get_user_subscription_id(user_id)
            if subscription_id:
                stripe.Subscription.modify(subscription_id, cancel_at_period_end=True)
                self.update_subscription_status(user_id, 'canceled')
                return True
            return False
        except Exception as e:
            print(f"Ошибка отмены подписки: {e}")
            return False
    
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
        
        if result:
            status, expires = result
            if status == 'premium' and expires:
                # Проверяем, не истекла ли подписка
                if datetime.fromisoformat(expires) < datetime.now():
                    self.update_user_subscription(user_id, 'free')
                    return 'free'
            return status
        return 'free'
    
    def can_generate_proposal(self, user_id: int) -> Dict[str, Any]:
        """Проверяет, может ли пользователь генерировать предложение"""
        user = self.get_user(user_id)
        if not user:
            return {'can_generate': False, 'reason': 'Пользователь не найден'}
        
        subscription_status = self.get_user_subscription_status(user_id)
        
        if subscription_status == 'premium':
            return {'can_generate': True, 'subscription': 'premium'}
        
        # Проверяем лимиты для бесплатной версии
        today = datetime.now().date()
        last_proposal_date = user.get('last_proposal_date')
        
        if last_proposal_date:
            last_proposal_date = datetime.fromisoformat(last_proposal_date).date()
        
        # Сбрасываем счетчик, если новый день
        if not last_proposal_date or last_proposal_date < today:
            self.reset_daily_proposals_count(user_id)
            daily_count = 0
        else:
            daily_count = user.get('daily_proposals_count', 0)
        
        # Лимит: 3 предложения в день для бесплатной версии
        if daily_count >= 3:
            return {
                'can_generate': False, 
                'reason': 'Достигнут дневной лимит (3 предложения)',
                'subscription': 'free',
                'upgrade_required': True
            }
        
        return {
            'can_generate': True, 
            'subscription': 'free',
            'daily_remaining': 3 - daily_count
        }
    
    def increment_proposal_count(self, user_id: int):
        """Увеличивает счетчик предложений пользователя"""
        conn = sqlite3.connect('upwork_proposals.db')
        cursor = conn.cursor()
        
        today = datetime.now().date()
        
        cursor.execute('''
            UPDATE users 
            SET proposals_count = proposals_count + 1,
                daily_proposals_count = daily_proposals_count + 1,
                last_proposal_date = ?
            WHERE id = ?
        ''', (today.isoformat(), user_id))
        
        conn.commit()
        conn.close()
    
    def get_user(self, user_id: int) -> Optional[Dict[str, Any]]:
        """Получает данные пользователя"""
        conn = sqlite3.connect('upwork_proposals.db')
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM users WHERE id = ?', (user_id,))
        result = cursor.fetchone()
        conn.close()
        
        if result:
            columns = [description[0] for description in cursor.description]
            return dict(zip(columns, result))
        return None
    
    def get_stripe_customer_id(self, user_id: int) -> Optional[str]:
        """Получает ID клиента в Stripe"""
        # В реальной реализации здесь была бы связь с Stripe
        return None
    
    def save_subscription(self, user_id: int, subscription_id: str, plan_type: str, status: str):
        """Сохраняет подписку в базу данных"""
        conn = sqlite3.connect('upwork_proposals.db')
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO subscriptions (user_id, stripe_subscription_id, plan_type, status)
            VALUES (?, ?, ?, ?)
        ''', (user_id, subscription_id, plan_type, status))
        
        # Обновляем статус пользователя
        expires = datetime.now() + timedelta(days=30)  # 30 дней для месячной подписки
        cursor.execute('''
            UPDATE users 
            SET subscription_status = ?, subscription_expires = ?
            WHERE id = ?
        ''', (plan_type, expires.isoformat(), user_id))
        
        conn.commit()
        conn.close()
    
    def update_subscription_status(self, user_id: int, status: str):
        """Обновляет статус подписки"""
        conn = sqlite3.connect('upwork_proposals.db')
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE subscriptions 
            SET status = ? 
            WHERE user_id = ? AND status != 'canceled'
        ''', (status, user_id))
        
        conn.commit()
        conn.close()
    
    def update_user_subscription(self, user_id: int, status: str):
        """Обновляет статус подписки пользователя"""
        conn = sqlite3.connect('upwork_proposals.db')
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE users 
            SET subscription_status = ?
            WHERE id = ?
        ''', (status, user_id))
        
        conn.commit()
        conn.close()
    
    def reset_daily_proposals_count(self, user_id: int):
        """Сбрасывает дневной счетчик предложений"""
        conn = sqlite3.connect('upwork_proposals.db')
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE users 
            SET daily_proposals_count = 0
            WHERE id = ?
        ''', (user_id,))
        
        conn.commit()
        conn.close()
    
    def get_user_subscription_id(self, user_id: int) -> Optional[str]:
        """Получает ID подписки пользователя"""
        conn = sqlite3.connect('upwork_proposals.db')
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT stripe_subscription_id 
            FROM subscriptions 
            WHERE user_id = ? AND status = 'active'
            ORDER BY created_at DESC
            LIMIT 1
        ''', (user_id,))
        
        result = cursor.fetchone()
        conn.close()
        
        return result[0] if result else None

# Глобальный экземпляр системы платежей
payment_system = PaymentSystem() 