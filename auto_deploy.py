#!/usr/bin/env python3
"""
Автоматическое развертывание на Render.com через GitHub
"""

import requests
import json
import time
import os
from datetime import datetime

def create_render_service():
    """Создание сервиса на Render.com"""
    
    print("🚀 Создание сервиса на Render.com...")
    
    # Данные для создания сервиса
    service_data = {
        "name": "upwork-auth-server",
        "type": "web_service",
        "env": "python",
        "buildCommand": "pip install -r requirements.txt",
        "startCommand": "python auth_server.py",
        "sourceDir": "backend",
        "autoDeploy": True,
        "healthCheckPath": "/api/user"
    }
    
    print("📋 Настройки сервиса:")
    for key, value in service_data.items():
        print(f"   {key}: {value}")
    
    print("\n⚠️  ВАЖНО: Этот скрипт не может автоматически создать сервис на Render.com")
    print("   Вам нужно сделать это вручную:")
    print("\n📋 Пошаговая инструкция:")
    print("1. Перейдите на https://render.com")
    print("2. Создайте аккаунт и войдите")
    print("3. Нажмите 'New +' → 'Web Service'")
    print("4. Подключите GitHub репозиторий:")
    print("   - Выберите: DARKSAIDERS12/upwork-proposal-generator")
    print("   - Ветка: main")
    print("5. Настройте сервис:")
    print("   - Name: upwork-auth-server")
    print("   - Environment: Python")
    print("   - Build Command: pip install -r requirements.txt")
    print("   - Start Command: python auth_server.py")
    print("   - Source Directory: backend")
    print("6. Нажмите 'Create Web Service'")
    print("7. Дождитесь развертывания (2-5 минут)")
    print("8. Скопируйте URL (например: https://upwork-auth-server.onrender.com)")
    
    return None

def update_frontend_with_url(render_url):
    """Обновление фронтенда с новым URL"""
    
    if not render_url:
        print("\n❌ URL не предоставлен. Пропускаем обновление фронтенда.")
        return False
    
    print(f"\n🔧 Обновление фронтенда с URL: {render_url}")
    
    # Читаем app.js
    app_js_path = "app.js"
    try:
        with open(app_js_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Заменяем URL
        old_url = "http://localhost:5000/api"
        new_url = f"{render_url}/api"
        
        if old_url in content:
            content = content.replace(old_url, new_url)
            
            # Записываем обновленный файл
            with open(app_js_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print(f"✅ URL обновлен: {old_url} → {new_url}")
            return True
        else:
            print("⚠️  Старый URL не найден в app.js")
            return False
            
    except Exception as e:
        print(f"❌ Ошибка обновления app.js: {e}")
        return False

def deploy_to_github_pages():
    """Загрузка обновленного кода на GitHub Pages"""
    
    print("\n📤 Загрузка на GitHub Pages...")
    
    try:
        # Добавляем изменения
        os.system("git add .")
        
        # Коммитим
        commit_msg = f"Update API URL for cloud deployment - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        os.system(f'git commit -m "{commit_msg}"')
        
        # Пушим
        os.system("git push origin main")
        
        print("✅ Код загружен на GitHub Pages")
        print("🔄 GitHub Pages автоматически обновится через несколько минут")
        return True
        
    except Exception as e:
        print(f"❌ Ошибка загрузки на GitHub: {e}")
        return False

def test_deployment(render_url):
    """Тестирование развернутого сервера"""
    
    if not render_url:
        print("\n❌ URL не предоставлен. Пропускаем тестирование.")
        return False
    
    print(f"\n🧪 Тестирование сервера: {render_url}")
    
    try:
        # Тест регистрации
        test_data = {
            "email": f"test_{int(time.time())}@example.com",
            "password": "test123"
        }
        
        response = requests.post(f"{render_url}/api/register", json=test_data, timeout=30)
        
        if response.status_code == 201:
            print("✅ Регистрация работает")
            
            # Тест входа
            login_response = requests.post(f"{render_url}/api/login", json=test_data, timeout=30)
            
            if login_response.status_code == 200:
                print("✅ Вход работает")
                
                # Получаем токен
                login_data = login_response.json()
                token = login_data.get('session_token')
                
                if token:
                    # Тест получения пользователя
                    headers = {"Authorization": f"Bearer {token}"}
                    user_response = requests.get(f"{render_url}/api/user", headers=headers, timeout=30)
                    
                    if user_response.status_code == 200:
                        print("✅ Получение пользователя работает")
                        print("🎉 Все тесты пройдены успешно!")
                        return True
                    else:
                        print(f"❌ Ошибка получения пользователя: {user_response.status_code}")
                else:
                    print("❌ Токен не получен")
            else:
                print(f"❌ Ошибка входа: {login_response.status_code}")
        else:
            print(f"❌ Ошибка регистрации: {response.status_code}")
            
    except requests.exceptions.Timeout:
        print("❌ Таймаут - сервер еще развертывается")
    except requests.exceptions.ConnectionError:
        print("❌ Ошибка подключения - сервер недоступен")
    except Exception as e:
        print(f"❌ Ошибка тестирования: {e}")
    
    return False

def main():
    """Основная функция"""
    
    print("🚀 АВТОМАТИЧЕСКОЕ РАЗВЕРТЫВАНИЕ СЕРВЕРА АУТЕНТИФИКАЦИИ")
    print("=" * 60)
    
    # Шаг 1: Создание сервиса на Render.com
    render_url = create_render_service()
    
    # Ждем ввода URL от пользователя
    print("\n" + "=" * 60)
    print("⏳ ОЖИДАНИЕ: Создайте сервис на Render.com по инструкции выше")
    print("После получения URL введите его ниже:")
    
    while True:
        user_input = input("\n🌐 Введите URL вашего сервера (или 'skip' для пропуска): ").strip()
        
        if user_input.lower() == 'skip':
            print("⏭️  Пропускаем обновление фронтенда")
            break
        elif user_input.startswith('http'):
            render_url = user_input.rstrip('/')  # Убираем trailing slash
            print(f"✅ URL получен: {render_url}")
            break
        else:
            print("❌ Неверный формат URL. Попробуйте снова или введите 'skip'")
    
    if render_url:
        # Шаг 2: Обновление фронтенда
        if update_frontend_with_url(render_url):
            # Шаг 3: Тестирование
            print("\n⏳ Ожидание 30 секунд для завершения развертывания...")
            time.sleep(30)
            
            test_deployment(render_url)
            
            # Шаг 4: Загрузка на GitHub Pages
            deploy_to_github_pages()
            
            print("\n🎉 РАЗВЕРТЫВАНИЕ ЗАВЕРШЕНО!")
            print(f"🌐 Ваш сервер: {render_url}")
            print("📱 Теперь вход с любого устройства будет работать!")
            
        else:
            print("\n❌ Не удалось обновить фронтенд")
    else:
        print("\n⚠️  URL не предоставлен. Развертывание не завершено.")

if __name__ == "__main__":
    main() 