from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import json
from datetime import datetime, timedelta
import secrets
import hashlib
from dotenv import load_dotenv

# Загружаем переменные окружения
load_dotenv()

app = Flask(__name__)
app.secret_key = secrets.token_hex(32)

# Улучшенные CORS настройки
CORS(app, 
     supports_credentials=True,
     origins=['*'],
     methods=['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'],
     allow_headers=['Content-Type', 'Authorization', 'X-Requested-With'])

# Определяем тип базы данных из переменных окружения
DATABASE_URL = os.environ.get('DATABASE_URL')
USE_POSTGRESQL = DATABASE_URL is not None

if USE_POSTGRESQL:
    import psycopg2
    from psycopg2.extras import RealDictCursor
    print("🐘 Используем PostgreSQL")
else:
    import sqlite3
    print("📁 Используем SQLite (fallback)")
    DB_PATH = os.path.join(os.path.dirname(__file__), 'users.db')

# Добавляем маршрут для корня
@app.route('/')
def root():
    """Корневой маршрут для проверки доступности сервера"""
    return jsonify({
        'status': 'running',
        'service': 'Upwork Proposal Generator Auth Server',
        'version': '2.0.0 (Railway)',
        'database': 'PostgreSQL' if USE_POSTGRESQL else 'SQLite',
        'timestamp': datetime.now().isoformat()
    }), 200

# Добавляем маршрут для health check
@app.route('/api/health')
def health_check():
    """Проверка состояния сервера"""
    try:
        if USE_POSTGRESQL:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute('SELECT COUNT(*) FROM users')
            user_count = cursor.fetchone()[0]
            conn.close()
        else:
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            cursor.execute('SELECT COUNT(*) FROM users')
            user_count = cursor.fetchone()[0]
            conn.close()
        
        return jsonify({
            'status': 'healthy',
            'database': 'connected',
            'database_type': 'PostgreSQL' if USE_POSTGRESQL else 'SQLite',
            'user_count': user_count,
            'timestamp': datetime.now().isoformat()
        }), 200
    except Exception as e:
        return jsonify({
            'status': 'unhealthy',
            'error': str(e),
            'timestamp': datetime.now().isoformat()
        }), 500

def get_db_connection():
    """Получение подключения к базе данных"""
    if USE_POSTGRESQL:
        conn = psycopg2.connect(DATABASE_URL, cursor_factory=RealDictCursor)
        return conn
    else:
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        return conn

def init_db():
    """Инициализация базы данных"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        if USE_POSTGRESQL:
            # PostgreSQL DDL
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id SERIAL PRIMARY KEY,
                    email VARCHAR(255) UNIQUE NOT NULL,
                    password_hash VARCHAR(255) NOT NULL,
                    subscription VARCHAR(50) DEFAULT 'free',
                    daily_proposals INTEGER DEFAULT 3,
                    daily_remaining INTEGER DEFAULT 3,
                    last_reset_date DATE,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    last_login TIMESTAMP
                )
            ''')
            
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS sessions (
                    id SERIAL PRIMARY KEY,
                    user_id INTEGER REFERENCES users(id),
                    session_token VARCHAR(255) UNIQUE NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    expires_at TIMESTAMP
                )
            ''')
        else:
            # SQLite DDL (fallback)
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
        print("✅ База данных инициализирована")
    except Exception as e:
        print(f"❌ Ошибка инициализации БД: {e}")

def hash_password(password):
    """Хеширование пароля"""
    return hashlib.sha256(password.encode()).hexdigest()

def create_session(user_id):
    """Создание сессии для пользователя"""
    session_token = secrets.token_hex(32)
    expires_at = datetime.now() + timedelta(days=30)
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    if USE_POSTGRESQL:
        cursor.execute('''
            INSERT INTO sessions (user_id, session_token, expires_at)
            VALUES (%s, %s, %s)
        ''', (user_id, session_token, expires_at))
    else:
        cursor.execute('''
            INSERT INTO sessions (user_id, session_token, created_at, expires_at)
            VALUES (?, ?, ?, ?)
        ''', (user_id, session_token, datetime.now().isoformat(), expires_at.isoformat()))
    
    conn.commit()
    conn.close()
    
    return session_token

def validate_session(session_token):
    """Проверка валидности сессии"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Сначала очищаем истекшие сессии
    if USE_POSTGRESQL:
        cursor.execute('DELETE FROM sessions WHERE expires_at <= %s', (datetime.now(),))
        cursor.execute('''
            SELECT user_id, expires_at FROM sessions 
            WHERE session_token = %s AND expires_at > %s
        ''', (session_token, datetime.now()))
    else:
        cursor.execute('DELETE FROM sessions WHERE expires_at <= ?', (datetime.now().isoformat(),))
        cursor.execute('''
            SELECT user_id, expires_at FROM sessions 
            WHERE session_token = ? AND expires_at > ?
        ''', (session_token, datetime.now().isoformat()))
    
    result = cursor.fetchone()
    conn.commit()
    conn.close()
    
    if result:
        return result[0] if not USE_POSTGRESQL else result['user_id']
    return None

def get_user_by_id(user_id):
    """Получение пользователя по ID"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    if USE_POSTGRESQL:
        cursor.execute('SELECT * FROM users WHERE id = %s', (user_id,))
    else:
        cursor.execute('SELECT * FROM users WHERE id = ?', (user_id,))
    
    user = cursor.fetchone()
    conn.close()
    
    if user:
        return {
            'id': user[0] if not USE_POSTGRESQL else user['id'],
            'email': user[1] if not USE_POSTGRESQL else user['email'],
            'subscription': user[3] if not USE_POSTGRESQL else user['subscription'],
            'daily_proposals': user[4] if not USE_POSTGRESQL else user['daily_proposals'],
            'daily_remaining': user[5] if not USE_POSTGRESQL else user['daily_remaining'],
            'last_reset_date': user[6] if not USE_POSTGRESQL else str(user['last_reset_date']),
            'created_at': user[7] if not USE_POSTGRESQL else str(user['created_at'])
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
        
        password_hash = hash_password(password)
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Проверяем, не существует ли уже пользователь
        if USE_POSTGRESQL:
            cursor.execute('SELECT id FROM users WHERE email = %s', (email,))
        else:
            cursor.execute('SELECT id FROM users WHERE email = ?', (email,))
        
        if cursor.fetchone():
            conn.close()
            return jsonify({'error': 'Пользователь с таким email уже существует'}), 409
        
        # Создаем пользователя
        today = datetime.now().date()
        if USE_POSTGRESQL:
            cursor.execute('''
                INSERT INTO users (email, password_hash, last_reset_date)
                VALUES (%s, %s, %s) RETURNING id
            ''', (email, password_hash, today))
            user_id = cursor.fetchone()[0]
        else:
            cursor.execute('''
                INSERT INTO users (email, password_hash, last_reset_date, created_at)
                VALUES (?, ?, ?, ?)
            ''', (email, password_hash, today.isoformat(), datetime.now().isoformat()))
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
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Ищем пользователя
        if USE_POSTGRESQL:
            cursor.execute('SELECT id FROM users WHERE email = %s AND password_hash = %s', 
                          (email, password_hash))
        else:
            cursor.execute('SELECT id FROM users WHERE email = ? AND password_hash = ?', 
                          (email, password_hash))
        
        user = cursor.fetchone()
        
        if not user:
            conn.close()
            return jsonify({'error': 'Неверный email или пароль'}), 401
        
        user_id = user[0] if not USE_POSTGRESQL else user['id']
        
        # Очищаем старые сессии пользователя
        if USE_POSTGRESQL:
            cursor.execute('DELETE FROM sessions WHERE user_id = %s', (user_id,))
            cursor.execute('UPDATE users SET last_login = %s WHERE id = %s', 
                          (datetime.now(), user_id))
        else:
            cursor.execute('DELETE FROM sessions WHERE user_id = ?', (user_id,))
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

@app.route('/api/update-limits', methods=['POST'])
def update_user_limits():
    """Обновление лимитов пользователя"""
    session_token = request.headers.get('Authorization', '').replace('Bearer ', '')
    
    if not session_token:
        return jsonify({'error': 'Токен сессии не предоставлен'}), 401
    
    user_id = validate_session(session_token)
    if not user_id:
        return jsonify({'error': 'Недействительная сессия'}), 401
    
    try:
        data = request.get_json()
        daily_remaining = data.get('daily_remaining')
        
        if daily_remaining is None:
            return jsonify({'error': 'Параметр daily_remaining обязателен'}), 400
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Обновляем лимиты пользователя
        if USE_POSTGRESQL:
            cursor.execute('''
                UPDATE users 
                SET daily_remaining = %s 
                WHERE id = %s
            ''', (daily_remaining, user_id))
        else:
            cursor.execute('''
                UPDATE users 
                SET daily_remaining = ? 
                WHERE id = ?
            ''', (daily_remaining, user_id))
        
        conn.commit()
        conn.close()
        
        return jsonify({
            'success': True,
            'message': 'Лимиты обновлены',
            'daily_remaining': daily_remaining
        }), 200
        
    except Exception as e:
        return jsonify({'error': f'Ошибка обновления лимитов: {str(e)}'}), 500

if __name__ == '__main__':
    init_db()
    print("База данных инициализирована")
    
    # Получаем порт из переменных окружения
    port = int(os.environ.get('PORT', 5000))
    
    print(f"🚀 Сервер аутентификации запущен на порту {port}")
    print(f"🗄️ Используется: {'PostgreSQL' if USE_POSTGRESQL else 'SQLite'}")
    
    app.run(host='0.0.0.0', port=port, debug=False)

