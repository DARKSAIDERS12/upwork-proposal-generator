from flask import Flask, request, jsonify, session
from flask_cors import CORS
import sqlite3
import hashlib
import os
import json
from datetime import datetime, timedelta
import secrets

app = Flask(__name__)
app.secret_key = secrets.token_hex(32)
CORS(app, supports_credentials=True)

# Путь к базе данных
DB_PATH = os.path.join(os.path.dirname(__file__), 'users.db')

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
    
    # Создаем таблицу сессий
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS sessions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            session_token TEXT UNIQUE NOT NULL,
            created_at TEXT,
            expires_at TEXT,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    
    conn.commit()
    conn.close()

def hash_password(password):
    """Хеширование пароля"""
    return hashlib.sha256(password.encode()).hexdigest()

def create_session(user_id):
    """Создание сессии для пользователя"""
    session_token = secrets.token_hex(32)
    expires_at = (datetime.now() + timedelta(days=30)).isoformat()
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute('''
        INSERT INTO sessions (user_id, session_token, created_at, expires_at)
        VALUES (?, ?, ?, ?)
    ''', (user_id, session_token, datetime.now().isoformat(), expires_at))
    
    conn.commit()
    conn.close()
    
    return session_token

def validate_session(session_token):
    """Проверка валидности сессии"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT user_id, expires_at FROM sessions 
        WHERE session_token = ? AND expires_at > ?
    ''', (session_token, datetime.now().isoformat()))
    
    result = cursor.fetchone()
    conn.close()
    
    if result:
        user_id, expires_at = result
        return user_id
    return None

def get_user_by_id(user_id):
    """Получение пользователя по ID"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM users WHERE id = ?', (user_id,))
    user = cursor.fetchone()
    conn.close()
    
    if user:
        return {
            'id': user[0],
            'email': user[1],
            'subscription': user[3],
            'daily_proposals': user[4],
            'daily_remaining': user[5],
            'last_reset_date': user[6],
            'created_at': user[7]
        }
    return None

@app.route('/api/register', methods=['POST'])
def register():
    """Регистрация нового пользователя"""
    try:
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')
        
        if not email or not password:
            return jsonify({'error': 'Email и пароль обязательны'}), 400
        
        # Хешируем пароль
        password_hash = hash_password(password)
        
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # Проверяем, не существует ли уже пользователь
        cursor.execute('SELECT id FROM users WHERE email = ?', (email,))
        if cursor.fetchone():
            conn.close()
            return jsonify({'error': 'Пользователь с таким email уже существует'}), 409
        
        # Создаем пользователя
        today = datetime.now().date().isoformat()
        cursor.execute('''
            INSERT INTO users (email, password_hash, last_reset_date, created_at)
            VALUES (?, ?, ?, ?)
        ''', (email, password_hash, today, datetime.now().isoformat()))
        
        user_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        # Создаем сессию
        session_token = create_session(user_id)
        
        return jsonify({
            'success': True,
            'message': 'Регистрация успешна',
            'session_token': session_token,
            'user': get_user_by_id(user_id)
        }), 201
        
    except Exception as e:
        return jsonify({'error': f'Ошибка регистрации: {str(e)}'}), 500

@app.route('/api/login', methods=['POST'])
def login():
    """Вход пользователя"""
    try:
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')
        
        if not email or not password:
            return jsonify({'error': 'Email и пароль обязательны'}), 400
        
        password_hash = hash_password(password)
        
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # Ищем пользователя
        cursor.execute('SELECT id FROM users WHERE email = ? AND password_hash = ?', 
                      (email, password_hash))
        user = cursor.fetchone()
        
        if not user:
            conn.close()
            return jsonify({'error': 'Неверный email или пароль'}), 401
        
        user_id = user[0]
        
        # Обновляем время последнего входа
        cursor.execute('UPDATE users SET last_login = ? WHERE id = ?', 
                      (datetime.now().isoformat(), user_id))
        conn.commit()
        conn.close()
        
        # Создаем новую сессию
        session_token = create_session(user_id)
        
        return jsonify({
            'success': True,
            'message': 'Вход выполнен успешно',
            'session_token': session_token,
            'user': get_user_by_id(user_id)
        }), 200
        
    except Exception as e:
        return jsonify({'error': f'Ошибка входа: {str(e)}'}), 500

@app.route('/api/user', methods=['GET'])
def get_user():
    """Получение информации о текущем пользователе"""
    session_token = request.headers.get('Authorization', '').replace('Bearer ', '')
    
    if not session_token:
        return jsonify({'error': 'Токен сессии не предоставлен'}), 401
    
    user_id = validate_session(session_token)
    if not user_id:
        return jsonify({'error': 'Недействительная сессия'}), 401
    
    user = get_user_by_id(user_id)
    if not user:
        return jsonify({'error': 'Пользователь не найден'}), 404
    
    return jsonify({'user': user}), 200

@app.route('/api/logout', methods=['POST'])
def logout():
    """Выход пользователя"""
    session_token = request.headers.get('Authorization', '').replace('Bearer ', '')
    
    if session_token:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute('DELETE FROM sessions WHERE session_token = ?', (session_token,))
        conn.commit()
        conn.close()
    
    return jsonify({'success': True, 'message': 'Выход выполнен'}), 200

@app.route('/api/reset-daily-limits', methods=['POST'])
def reset_daily_limits():
    """Сброс ежедневных лимитов"""
    session_token = request.headers.get('Authorization', '').replace('Bearer ', '')
    
    if not session_token:
        return jsonify({'error': 'Токен сессии не предоставлен'}), 401
    
    user_id = validate_session(session_token)
    if not user_id:
        return jsonify({'error': 'Недействительная сессия'}), 401
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Получаем пользователя
    cursor.execute('SELECT subscription, daily_proposals FROM users WHERE id = ?', (user_id,))
    user = cursor.fetchone()
    
    if user:
        subscription, daily_proposals = user
        today = datetime.now().date().isoformat()
        
        # Сбрасываем лимиты
        daily_remaining = 3 if subscription == 'free' else 999
        
        cursor.execute('''
            UPDATE users 
            SET daily_remaining = ?, last_reset_date = ? 
            WHERE id = ?
        ''', (daily_remaining, today, user_id))
        
        conn.commit()
        
        return jsonify({
            'success': True,
            'daily_remaining': daily_remaining
        }), 200
    
    conn.close()
    return jsonify({'error': 'Пользователь не найден'}), 404

@app.route('/api/update-subscription', methods=['POST'])
def update_subscription():
    """Обновление подписки пользователя"""
    session_token = request.headers.get('Authorization', '').replace('Bearer ', '')
    
    if not session_token:
        return jsonify({'error': 'Токен сессии не предоставлен'}), 401
    
    user_id = validate_session(session_token)
    if not user_id:
        return jsonify({'error': 'Недействительная сессия'}), 401
    
    data = request.get_json()
    subscription = data.get('subscription')
    
    if not subscription:
        return jsonify({'error': 'Тип подписки не указан'}), 400
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    daily_proposals = 999 if subscription == 'premium' else 3
    daily_remaining = daily_proposals
    
    cursor.execute('''
        UPDATE users 
        SET subscription = ?, daily_proposals = ?, daily_remaining = ?
        WHERE id = ?
    ''', (subscription, daily_proposals, daily_remaining, user_id))
    
    conn.commit()
    conn.close()
    
    return jsonify({
        'success': True,
        'message': 'Подписка обновлена',
        'subscription': subscription,
        'daily_remaining': daily_remaining
    }), 200

if __name__ == '__main__':
    init_db()
    print("База данных инициализирована")
    
    # Получаем порт из переменных окружения (для облачных платформ)
    port = int(os.environ.get('PORT', 5000))
    
    print(f"Сервер аутентификации запущен на порту {port}")
    app.run(host='0.0.0.0', port=port, debug=False) 