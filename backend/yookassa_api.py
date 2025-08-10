#!/usr/bin/env python3
"""
Flask API для интеграции с ЮKassa
Обработка платежей и webhook'ов
"""

from flask import Flask, request, jsonify, render_template_string
from flask_cors import CORS
import os
import json
import sqlite3
from datetime import datetime
from yookassa_integration import YooKassaIntegration

app = Flask(__name__)
CORS(app)  # Разрешаем CORS для фронтенда

# Инициализация интеграции с ЮKassa
try:
    yookassa = YooKassaIntegration()
    print("✅ Интеграция с ЮKassa инициализирована")
except Exception as e:
    print(f"❌ Ошибка инициализации ЮKassa: {e}")
    yookassa = None

@app.route('/')
def index():
    """Главная страница API"""
    return jsonify({
        'service': 'Upwork Proposal Generator - ЮKassa API',
        'status': 'active',
        'version': '1.0.0'
    })

@app.route('/api/pricing', methods=['GET'])
def get_pricing():
    """Получение информации о тарифах"""
    if not yookassa:
        return jsonify({'error': 'ЮKassa не инициализирована'}), 500
    
    try:
        pricing = yookassa.get_pricing_info()
        return jsonify(pricing)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/payment/create', methods=['POST'])
def create_payment():
    """Создание платежа"""
    if not yookassa:
        return jsonify({'error': 'ЮKassa не инициализирована'}), 500
    
    try:
        data = request.get_json()
        
        # Проверяем обязательные поля
        required_fields = ['user_id', 'plan_type', 'email']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Отсутствует обязательное поле: {field}'}), 400
        
        user_id = data['user_id']
        plan_type = data['plan_type']
        email = data['email']
        return_url = data.get('return_url')
        
        # Создаем платеж
        result = yookassa.create_payment(user_id, plan_type, email, return_url)
        
        if 'error' in result:
            return jsonify(result), 400
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/payment/status/<payment_id>', methods=['GET'])
def get_payment_status(payment_id):
    """Получение статуса платежа"""
    if not yookassa:
        return jsonify({'error': 'ЮKassa не инициализирована'}), 500
    
    try:
        result = yookassa.get_payment_status(payment_id)
        
        if 'error' in result:
            return jsonify(result), 400
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/webhook/yookassa', methods=['POST'])
def yookassa_webhook():
    """Webhook от ЮKassa для уведомлений о платежах"""
    if not yookassa:
        return jsonify({'error': 'ЮKassa не инициализирована'}), 500
    
    try:
        # Получаем данные webhook'а
        webhook_data = request.get_json()
        
        if not webhook_data:
            return jsonify({'error': 'Пустые данные webhook'}), 400
        
        # Обрабатываем webhook
        success = yookassa.process_webhook(webhook_data)
        
        if success:
            return jsonify({'status': 'processed'}), 200
        else:
            return jsonify({'error': 'Ошибка обработки webhook'}), 400
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/subscription/status/<int:user_id>', methods=['GET'])
def get_subscription_status(user_id):
    """Получение статуса подписки пользователя"""
    try:
        conn = sqlite3.connect('upwork_proposals.db')
        cursor = conn.cursor()
        
        # Получаем информацию о пользователе
        cursor.execute('''
            SELECT subscription_status, subscription_expires, proposals_count, daily_proposals_count
            FROM users WHERE id = ?
        ''', (user_id,))
        
        result = cursor.fetchone()
        conn.close()
        
        if not result:
            return jsonify({'error': 'Пользователь не найден'}), 404
        
        subscription_status, subscription_expires, proposals_count, daily_proposals_count = result
        
        # Проверяем, не истекла ли подписка
        if subscription_expires:
            expires_date = datetime.fromisoformat(subscription_expires)
            if expires_date < datetime.now():
                subscription_status = 'expired'
        
        return jsonify({
            'user_id': user_id,
            'subscription_status': subscription_status,
            'subscription_expires': subscription_expires,
            'proposals_count': proposals_count,
            'daily_proposals_count': daily_proposals_count
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/subscription/cancel/<int:user_id>', methods=['POST'])
def cancel_subscription(user_id):
    """Отмена подписки пользователя"""
    try:
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
        
        return jsonify({'success': True, 'message': 'Подписка отменена'})
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/payment/history/<int:user_id>', methods=['GET'])
def get_payment_history(user_id):
    """Получение истории платежей пользователя"""
    try:
        conn = sqlite3.connect('upwork_proposals.db')
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT yookassa_payment_id, amount, currency, status, plan_type, created_at, updated_at
            FROM yookassa_payments 
            WHERE user_id = ? 
            ORDER BY created_at DESC
        ''', (user_id,))
        
        payments = []
        for row in cursor.fetchall():
            payments.append({
                'payment_id': row[0],
                'amount': row[1],
                'currency': row[2],
                'status': row[3],
                'plan_type': row[4],
                'created_at': row[5],
                'updated_at': row[6]
            })
        
        conn.close()
        
        return jsonify({'payments': payments})
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/test', methods=['GET'])
def test_api():
    """Тестовая страница для проверки API"""
    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Тест ЮKassa API</title>
        <meta charset="utf-8">
        <style>
            body { font-family: Arial, sans-serif; margin: 40px; }
            .test-section { margin: 20px 0; padding: 20px; border: 1px solid #ddd; border-radius: 5px; }
            button { padding: 10px 20px; margin: 5px; background: #007bff; color: white; border: none; border-radius: 3px; cursor: pointer; }
            button:hover { background: #0056b3; }
            .result { margin-top: 10px; padding: 10px; background: #f8f9fa; border-radius: 3px; }
        </style>
    </head>
    <body>
        <h1>🧪 Тест ЮKassa API</h1>
        
        <div class="test-section">
            <h3>Получение тарифов</h3>
            <button onclick="testPricing()">Получить тарифы</button>
            <div id="pricingResult" class="result"></div>
        </div>
        
        <div class="test-section">
            <h3>Создание тестового платежа</h3>
            <button onclick="testCreatePayment()">Создать платеж</button>
            <div id="paymentResult" class="result"></div>
        </div>
        
        <div class="test-section">
            <h3>Статус API</h3>
            <button onclick="testStatus()">Проверить статус</button>
            <div id="statusResult" class="result"></div>
        </div>
        
        <script>
            async function testPricing() {
                try {
                    const response = await fetch('/api/pricing');
                    const data = await response.json();
                    document.getElementById('pricingResult').innerHTML = '<pre>' + JSON.stringify(data, null, 2) + '</pre>';
                } catch (error) {
                    document.getElementById('pricingResult').innerHTML = 'Ошибка: ' + error.message;
                }
            }
            
            async function testCreatePayment() {
                try {
                    const response = await fetch('/api/payment/create', {
                        method: 'POST',
                        headers: {'Content-Type': 'application/json'},
                        body: JSON.stringify({
                            user_id: 1,
                            plan_type: 'premium',
                            email: 'test@example.com'
                        })
                    });
                    const data = await response.json();
                    document.getElementById('paymentResult').innerHTML = '<pre>' + JSON.stringify(data, null, 2) + '</pre>';
                } catch (error) {
                    document.getElementById('paymentResult').innerHTML = 'Ошибка: ' + error.message;
                }
            }
            
            async function testStatus() {
                try {
                    const response = await fetch('/');
                    const data = await response.json();
                    document.getElementById('statusResult').innerHTML = '<pre>' + JSON.stringify(data, null, 2) + '</pre>';
                } catch (error) {
                    document.getElementById('statusResult').innerHTML = 'Ошибка: ' + error.message;
                }
            }
        </script>
    </body>
    </html>
    """
    return html

if __name__ == '__main__':
    # Получаем порт из переменных окружения или используем 5000
    port = int(os.environ.get('PORT', 5000))
    
    print(f"🚀 Запуск ЮKassa API на порту {port}")
    print("📱 API доступен по адресу: http://localhost:5000")
    print("🧪 Тестовая страница: http://localhost:5000/api/test")
    
    app.run(host='0.0.0.0', port=port, debug=True) 