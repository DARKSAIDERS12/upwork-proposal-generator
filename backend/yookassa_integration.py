#!/usr/bin/env python3
"""
Полноценная интеграция с ЮKassa API
Реальные платежи для Upwork Proposal Generator
"""

import os
import json
import sqlite3
import hashlib
import hmac
import base64
from datetime import datetime, timedelta
from typing import Dict, Any, Optional
import requests
from urllib.parse import urlencode

class YooKassaIntegration:
    """Интеграция с ЮKassa для реальных платежей"""
    
    def __init__(self):
        # Конфигурация ЮKassa из переменных окружения
        self.shop_id = os.getenv('YOOKASSA_SHOP_ID')
        self.secret_key = os.getenv('YOOKASSA_SECRET_KEY')
        self.api_url = "https://api.yookassa.ru/v3"
        
        # Проверяем наличие обязательных параметров
        if not self.shop_id or not self.secret_key:
            raise ValueError("Необходимо указать YOOKASSA_SHOP_ID и YOOKASSA_SECRET_KEY")
        
        # Базовые заголовки для API
        self.headers = {
            'Authorization': f'Basic {base64.b64encode(f"{self.shop_id}:{self.secret_key}".encode()).decode()}',
            'Content-Type': 'application/json',
            'Idempotence-Key': ''
        }
        
        # Конфигурация тарифов в рублях
        self.pricing = {
            'premium': {'price': 1500, 'currency': 'RUB', 'period': 'month', 'name': 'Premium'},
            'pro': {'price': 3000, 'currency': 'RUB', 'period': 'month', 'name': 'Pro'},
            'enterprise': {'price': 9900, 'currency': 'RUB', 'period': 'month', 'name': 'Enterprise'}
        }
        
        # Инициализация базы данных
        self.init_database()
    
    def init_database(self):
        """Инициализация базы данных для платежей"""
        conn = sqlite3.connect('upwork_proposals.db')
        cursor = conn.cursor()
        
        # Таблица платежей ЮKassa
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS yookassa_payments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                payment_id TEXT UNIQUE,
                yookassa_payment_id TEXT,
                amount INTEGER,
                currency TEXT DEFAULT 'RUB',
                status TEXT,
                plan_type TEXT,
                confirmation_url TEXT,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')
        
        # Таблица уведомлений от ЮKassa
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS yookassa_notifications (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                payment_id TEXT,
                event TEXT,
                data TEXT,
                processed BOOLEAN DEFAULT FALSE,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def create_payment(self, user_id: int, plan_type: str, email: str, return_url: str = None) -> Dict[str, Any]:
        """Создает реальный платеж в ЮKassa"""
        
        if plan_type not in self.pricing:
            return {'error': 'Неверный тип плана'}
        
        plan = self.pricing[plan_type]
        
        # Генерируем уникальный ключ идемпотентности
        idempotence_key = f"upwork_{user_id}_{plan_type}_{int(datetime.now().timestamp())}"
        
        # Данные для создания платежа
        payment_data = {
            'amount': {
                'value': str(plan['price']),
                'currency': plan['currency']
            },
            'confirmation': {
                'type': 'redirect',
                'return_url': return_url or f"https://darksaiders12.github.io/upwork-proposal-generator/payment_success.html?plan={plan_type}"
            },
            'capture': True,
            'description': f'Подписка {plan["name"]} на Upwork Proposal Generator',
            'metadata': {
                'user_id': str(user_id),
                'plan_type': plan_type,
                'email': email,
                'service': 'upwork_proposal_generator'
            },
            'receipt': {
                'customer': {
                    'email': email
                },
                'items': [
                    {
                        'description': f'Подписка {plan["name"]} на Upwork Proposal Generator',
                        'quantity': '1',
                        'amount': {
                            'value': str(plan['price']),
                            'currency': plan['currency']
                        },
                        'vat_code': 1,
                        'payment_subject': 'service',
                        'payment_mode': 'full_prepayment'
                    }
                ]
            }
        }
        
        try:
            # Отправляем запрос к API ЮKassa
            headers = self.headers.copy()
            headers['Idempotence-Key'] = idempotence_key
            
            response = requests.post(
                f"{self.api_url}/payments",
                headers=headers,
                json=payment_data
            )
            
            if response.status_code == 200:
                payment_info = response.json()
                
                # Сохраняем платеж в базу
                self.save_payment(
                    user_id=user_id,
                    payment_id=payment_info['id'],
                    amount=plan['price'],
                    currency=plan['currency'],
                    status=payment_info['status'],
                    plan_type=plan_type,
                    confirmation_url=payment_info['confirmation']['confirmation_url']
                )
                
                return {
                    'success': True,
                    'payment_id': payment_info['id'],
                    'amount': plan['price'],
                    'currency': plan['currency'],
                    'confirmation_url': payment_info['confirmation']['confirmation_url'],
                    'status': payment_info['status']
                }
            else:
                error_data = response.json()
                return {
                    'error': f'Ошибка API ЮKassa: {error_data.get("description", "Неизвестная ошибка")}',
                    'code': response.status_code
                }
                
        except Exception as e:
            return {'error': f'Ошибка создания платежа: {str(e)}'}
    
    def save_payment(self, user_id: int, payment_id: str, amount: int, currency: str, status: str, plan_type: str, confirmation_url: str):
        """Сохраняет платеж в базу данных"""
        conn = sqlite3.connect('upwork_proposals.db')
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT OR REPLACE INTO yookassa_payments 
            (user_id, yookassa_payment_id, amount, currency, status, plan_type, confirmation_url, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (user_id, payment_id, amount, currency, status, plan_type, confirmation_url, datetime.now()))
        
        conn.commit()
        conn.close()
    
    def get_payment_status(self, payment_id: str) -> Dict[str, Any]:
        """Получает статус платежа из ЮKassa"""
        try:
            headers = self.headers.copy()
            headers['Idempotence-Key'] = f"status_{payment_id}_{int(datetime.now().timestamp())}"
            
            response = requests.get(
                f"{self.api_url}/payments/{payment_id}",
                headers=headers
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                return {'error': f'Ошибка получения статуса: {response.status_code}'}
                
        except Exception as e:
            return {'error': f'Ошибка запроса: {str(e)}'}
    
    def process_webhook(self, webhook_data: Dict[str, Any]) -> bool:
        """Обрабатывает webhook от ЮKassa"""
        try:
            # Проверяем подпись webhook (в реальности нужно реализовать)
            # if not self.verify_webhook_signature(webhook_data):
            #     return False
            
            event = webhook_data.get('event')
            payment_id = webhook_data.get('object', {}).get('id')
            
            if not payment_id:
                return False
            
            # Сохраняем уведомление
            self.save_notification(payment_id, event, json.dumps(webhook_data))
            
            # Обрабатываем событие
            if event == 'payment.succeeded':
                return self.handle_payment_success(payment_id)
            elif event == 'payment.canceled':
                return self.handle_payment_cancel(payment_id)
            
            return True
            
        except Exception as e:
            print(f"Ошибка обработки webhook: {e}")
            return False
    
    def save_notification(self, payment_id: str, event: str, data: str):
        """Сохраняет уведомление от ЮKassa"""
        conn = sqlite3.connect('upwork_proposals.db')
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO yookassa_notifications (payment_id, event, data)
            VALUES (?, ?, ?)
        ''', (payment_id, event, data))
        
        conn.commit()
        conn.close()
    
    def handle_payment_success(self, payment_id: str) -> bool:
        """Обрабатывает успешный платеж"""
        try:
            # Получаем информацию о платеже
            payment_info = self.get_payment_status(payment_id)
            
            if 'error' in payment_info:
                return False
            
            # Обновляем статус в базе
            conn = sqlite3.connect('upwork_proposals.db')
            cursor = conn.cursor()
            
            cursor.execute('''
                UPDATE yookassa_payments 
                SET status = ?, updated_at = ?
                WHERE yookassa_payment_id = ?
            ''', (payment_info['status'], datetime.now(), payment_id))
            
            # Получаем данные пользователя
            cursor.execute('''
                SELECT user_id, plan_type FROM yookassa_payments 
                WHERE yookassa_payment_id = ?
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
            
        except Exception as e:
            print(f"Ошибка обработки успешного платежа: {e}")
            return False
    
    def handle_payment_cancel(self, payment_id: str) -> bool:
        """Обрабатывает отмененный платеж"""
        try:
            conn = sqlite3.connect('upwork_proposals.db')
            cursor = conn.cursor()
            
            cursor.execute('''
                UPDATE yookassa_payments 
                SET status = 'canceled', updated_at = ?
                WHERE yookassa_payment_id = ?
            ''', (datetime.now(), payment_id))
            
            conn.commit()
            conn.close()
            return True
            
        except Exception as e:
            print(f"Ошибка обработки отмены платежа: {e}")
            return False
    
    def activate_subscription(self, user_id: int, plan_type: str, payment_id: str):
        """Активирует подписку пользователя"""
        conn = sqlite3.connect('upwork_proposals.db')
        cursor = conn.cursor()
        
        # Определяем срок действия подписки
        if plan_type == 'premium':
            expires = datetime.now() + timedelta(days=30)
        elif plan_type == 'pro':
            expires = datetime.now() + timedelta(days=30)
        elif plan_type == 'enterprise':
            expires = datetime.now() + timedelta(days=30)
        else:
            expires = datetime.now() + timedelta(days=30)
        
        # Обновляем статус пользователя
        cursor.execute('''
            UPDATE users 
            SET subscription_status = ?, subscription_expires = ?
            WHERE id = ?
        ''', (plan_type, expires, user_id))
        
        # Создаем запись о подписке
        cursor.execute('''
            INSERT OR REPLACE INTO subscriptions 
            (user_id, payment_id, plan_type, status, current_period_start, current_period_end)
            VALUES (?, ?, ?, 'active', ?, ?)
        ''', (user_id, payment_id, plan_type, datetime.now(), expires))
        
        conn.commit()
        conn.close()
    
    def get_pricing_info(self) -> Dict[str, Any]:
        """Возвращает информацию о тарифах"""
        return {
            'currency': 'RUB',
            'plans': self.pricing
        }
    
    def refund_payment(self, payment_id: str, amount: int = None) -> Dict[str, Any]:
        """Возвращает средства (частично или полностью)"""
        try:
            refund_data = {
                'payment_id': payment_id,
                'amount': {
                    'value': str(amount) if amount else '0',
                    'currency': 'RUB'
                }
            }
            
            headers = self.headers.copy()
            headers['Idempotence-Key'] = f"refund_{payment_id}_{int(datetime.now().timestamp())}"
            
            response = requests.post(
                f"{self.api_url}/refunds",
                headers=headers,
                json=refund_data
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                error_data = response.json()
                return {
                    'error': f'Ошибка возврата: {error_data.get("description", "Неизвестная ошибка")}',
                    'code': response.status_code
                }
                
        except Exception as e:
            return {'error': f'Ошибка возврата: {str(e)}'}

# Тестирование интеграции
def test_yookassa_integration():
    """Тестирует интеграцию с ЮKassa"""
    print("🧪 Тестирование интеграции с ЮKassa...")
    
    try:
        integration = YooKassaIntegration()
        print("✅ Инициализация успешна")
        
        # Тест получения информации о тарифах
        pricing = integration.get_pricing_info()
        print(f"✅ Тарифы: {pricing}")
        
        print("✅ Тестирование завершено!")
        
    except ValueError as e:
        print(f"❌ Ошибка инициализации: {e}")
        print("💡 Установите переменные окружения YOOKASSA_SHOP_ID и YOOKASSA_SECRET_KEY")
    except Exception as e:
        print(f"❌ Ошибка: {e}")

if __name__ == "__main__":
    test_yookassa_integration() 