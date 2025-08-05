#!/usr/bin/env python3
"""
Остановка серверов Upwork Proposal Generator
"""

import os
import subprocess
import time

def print_banner():
    print("=" * 60)
    print("🛑 ОСТАНОВКА UPWORK PROPOSAL GENERATOR")
    print("=" * 60)

def stop_servers():
    """Останавливает все серверы"""
    print("🛑 Остановка серверов...")
    
    # Останавливаем backend
    print("📡 Остановка backend сервера...")
    result1 = subprocess.run("pkill -f 'python.*run.py'", shell=True, capture_output=True)
    if result1.returncode == 0:
        print("✅ Backend сервер остановлен")
    else:
        print("ℹ️  Backend сервер уже остановлен")
    
    # Останавливаем frontend
    print("🎨 Остановка frontend сервера...")
    result2 = subprocess.run("pkill -f 'python.*server.py'", shell=True, capture_output=True)
    if result2.returncode == 0:
        print("✅ Frontend сервер остановлен")
    else:
        print("ℹ️  Frontend сервер уже остановлен")
    
    # Проверяем, что порты освобождены
    print("🔍 Проверка освобождения портов...")
    time.sleep(2)
    
    result3 = subprocess.run("ss -tlnp | grep -E '(8000|3000)'", shell=True, capture_output=True)
    if result3.returncode != 0:
        print("✅ Порта 8000 и 3000 освобождены")
    else:
        print("⚠️  Некоторые порты все еще заняты")

def main():
    print_banner()
    stop_servers()
    
    print("\n" + "=" * 60)
    print("👋 Серверы остановлены!")
    print("=" * 60)
    print("💡 Для запуска: ./quick_start.py")
    print("=" * 60)

if __name__ == "__main__":
    main() 