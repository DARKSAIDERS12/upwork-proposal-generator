#!/usr/bin/env python3
"""
Скрипт для запуска защищенного backend сервера
"""

import subprocess
import time
import os
import sys

def start_secure_backend():
    """Запускает защищенный backend сервер"""
    print("🔒 Запуск защищенного backend сервера...")
    
    backend_dir = os.path.join(os.path.dirname(__file__), "backend")
    os.chdir(backend_dir)
    
    # Активируем виртуальное окружение и запускаем сервер
    cmd = f"source venv/bin/activate && python run.py"
    
    try:
        process = subprocess.Popen(
            cmd,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        # Ждем немного для запуска
        time.sleep(3)
        
        if process.poll() is None:
            print("✅ Защищенный backend сервер запущен!")
            print("🔗 URL: http://192.168.0.124:8000")
            print("📚 API документация: http://192.168.0.124:8000/docs")
            print("🔒 Безопасность: Rate limiting, Security headers, CORS настроен")
            return process
        else:
            print("❌ Ошибка запуска backend сервера")
            return None
            
    except Exception as e:
        print(f"❌ Ошибка запуска backend: {e}")
        return None

if __name__ == "__main__":
    print("=" * 60)
    print("🔒 ЗАЩИЩЕННЫЙ BACKEND СЕРВЕР")
    print("=" * 60)
    
    process = start_secure_backend()
    
    if process:
        print("\n" + "=" * 60)
        print("🎉 Backend готов к работе!")
        print("=" * 60)
        print("💡 Для остановки нажмите Ctrl+C")
        print("=" * 60)
        
        try:
            process.wait()
        except KeyboardInterrupt:
            print("\n🛑 Остановка сервера...")
            process.terminate()
            process.wait()
            print("✅ Сервер остановлен")
    else:
        print("❌ Не удалось запустить сервер")
        sys.exit(1) 