#!/usr/bin/env python3
"""
Настройка GitHub с токеном доступа
"""

import subprocess
import os
import getpass

def print_banner():
    print("=" * 60)
    print("🔑 НАСТРОЙКА GITHUB ТОКЕНА")
    print("=" * 60)
    print("Автоматическая настройка доступа к GitHub")
    print("=" * 60)

def setup_git_config():
    """Настраивает Git конфигурацию"""
    print("🔧 Настройка Git конфигурации...")
    
    # Настройка пользователя
    subprocess.run(["git", "config", "--global", "user.name", "DARKSAIDERS12"])
    subprocess.run(["git", "config", "--global", "user.email", "darksaiders12@example.com"])
    
    # Настройка credential helper
    subprocess.run(["git", "config", "--global", "credential.helper", "store"])
    
    print("✅ Git конфигурация настроена!")

def setup_remote_repo():
    """Настраивает удаленный репозиторий"""
    print("🔗 Настройка удаленного репозитория...")
    
    # Удаляем существующий remote если есть
    subprocess.run(["git", "remote", "remove", "origin"], capture_output=True)
    
    # Добавляем новый remote
    repo_url = "https://github.com/DARKSAIDERS12/upwork-proposal-generator.git"
    subprocess.run(["git", "remote", "add", "origin", repo_url])
    
    print("✅ Удаленный репозиторий настроен!")

def create_token_instructions():
    """Создает инструкции для токена"""
    print("\n📋 ИНСТРУКЦИИ ДЛЯ СОЗДАНИЯ ТОКЕНА:")
    print("=" * 60)
    print("1. Перейдите на https://github.com/settings/tokens")
    print("2. Нажмите 'Generate new token (classic)'")
    print("3. Название: 'Upwork Proposal Generator'")
    print("4. Срок действия: 'No expiration'")
    print("5. Права доступа:")
    print("   ✅ repo (полный доступ к репозиториям)")
    print("   ✅ workflow (для GitHub Actions)")
    print("6. Нажмите 'Generate token'")
    print("7. СКОПИРУЙТЕ ТОКЕН (показывается только один раз!)")
    print("=" * 60)

def test_connection():
    """Тестирует подключение к GitHub"""
    print("\n🔍 Тестирование подключения к GitHub...")
    
    try:
        result = subprocess.run(
            ["git", "ls-remote", "https://github.com/DARKSAIDERS12/upwork-proposal-generator.git"],
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0:
            print("✅ Подключение к GitHub успешно!")
            return True
        else:
            print("❌ Ошибка подключения к GitHub")
            print(f"Ошибка: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        return False

def main():
    print_banner()
    
    print("🌐 Этот скрипт поможет настроить доступ к GitHub")
    print("📱 После настройки вы сможете загружать код на GitHub")
    print()
    
    # Настройка Git
    setup_git_config()
    
    # Настройка удаленного репозитория
    setup_remote_repo()
    
    # Показываем инструкции
    create_token_instructions()
    
    print("\n💡 После создания токена:")
    print("1. Выполните: git push origin main")
    print("2. При запросе пароля введите токен (не пароль от аккаунта)")
    print("3. Токен сохранится автоматически")
    
    print("\n" + "=" * 60)
    print("🎯 ГОТОВО К ДЕПЛОЮ!")
    print("=" * 60)
    print("📋 Следующие шаги:")
    print("   1. Создайте токен по инструкции выше")
    print("   2. Выполните: git push origin main")
    print("   3. Введите токен при запросе пароля")
    print("=" * 60)

if __name__ == "__main__":
    main() 