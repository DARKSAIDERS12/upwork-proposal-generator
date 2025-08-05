#!/usr/bin/env python3
"""
Автоматический деплой Upwork Proposal Generator на GitHub
"""

import subprocess
import os
import sys
import time

def print_banner():
    print("=" * 60)
    print("🚀 ДЕПЛОЙ НА GITHUB PAGES")
    print("=" * 60)
    print("Автоматический деплой Upwork Proposal Generator")
    print("=" * 60)

def run_command(command, description):
    """Выполняет команду и выводит результат"""
    print(f"🔧 {description}...")
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ {description} - успешно!")
            return True
        else:
            print(f"❌ {description} - ошибка!")
            print(f"Ошибка: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ {description} - исключение: {e}")
        return False

def setup_git():
    """Настраивает Git репозиторий"""
    print("🔧 Настройка Git репозитория...")
    
    # Инициализация Git
    if not run_command("git init", "Инициализация Git"):
        return False
    
    # Добавление файлов
    if not run_command("git add .", "Добавление файлов"):
        return False
    
    # Первый коммит
    if not run_command('git commit -m "Initial commit: Upwork Proposal Generator"', "Создание коммита"):
        return False
    
    return True

def create_github_repo():
    """Создает репозиторий на GitHub"""
    print("🌐 Создание репозитория на GitHub...")
    print("📋 Инструкции:")
    print("1. Перейдите на https://github.com/new")
    print("2. Название репозитория: upwork-proposal-generator")
    print("3. Описание: AI-помощник для создания выигрышных предложений на Upwork")
    print("4. Выберите 'Public'")
    print("5. НЕ ставьте галочки на README, .gitignore, license")
    print("6. Нажмите 'Create repository'")
    
    input("Нажмите Enter после создания репозитория...")
    return True

def setup_remote_repo():
    """Настраивает удаленный репозиторий"""
    print("🔗 Настройка удаленного репозитория...")
    
    username = input("Введите ваше имя пользователя GitHub: ")
    repo_url = f"https://github.com/{username}/upwork-proposal-generator.git"
    
    # Добавление удаленного репозитория
    if not run_command(f"git remote add origin {repo_url}", "Добавление удаленного репозитория"):
        return False
    
    # Переименование ветки в main
    if not run_command("git branch -M main", "Переименование ветки в main"):
        return False
    
    # Отправка кода
    if not run_command("git push -u origin main", "Отправка кода на GitHub"):
        return False
    
    return True

def setup_github_pages():
    """Настраивает GitHub Pages"""
    print("📄 Настройка GitHub Pages...")
    print("📋 Инструкции:")
    print("1. Перейдите в настройки репозитория")
    print("2. Найдите раздел 'Pages' в левом меню")
    print("3. В 'Source' выберите 'Deploy from a branch'")
    print("4. В 'Branch' выберите 'gh-pages' и '/ (root)'")
    print("5. Нажмите 'Save'")
    print("6. Подождите несколько минут для деплоя")
    
    input("Нажмите Enter после настройки GitHub Pages...")
    return True

def create_deploy_script():
    """Создает скрипт для быстрого деплоя"""
    deploy_script = """#!/bin/bash
# Скрипт для быстрого деплоя на GitHub Pages

echo "🚀 Деплой на GitHub Pages..."

# Добавляем изменения
git add .

# Создаем коммит
git commit -m "Update: $(date)"

# Отправляем на GitHub
git push origin main

echo "✅ Деплой завершен!"
echo "🌐 Сайт будет доступен через несколько минут на:"
echo "   https://[YOUR_USERNAME].github.io/upwork-proposal-generator/"
"""
    
    with open("deploy.sh", "w") as f:
        f.write(deploy_script)
    
    # Делаем скрипт исполняемым
    os.chmod("deploy.sh", 0o755)
    print("✅ Скрипт deploy.sh создан!")

def main():
    print_banner()
    
    print("🌐 Этот скрипт поможет вам развернуть проект на GitHub Pages")
    print("📱 После деплоя сайт будет доступен из любой точки мира!")
    print()
    
    # Настройка Git
    if not setup_git():
        print("❌ Ошибка настройки Git")
        return
    
    # Создание репозитория
    if not create_github_repo():
        print("❌ Ошибка создания репозитория")
        return
    
    # Настройка удаленного репозитория
    if not setup_remote_repo():
        print("❌ Ошибка настройки удаленного репозитория")
        return
    
    # Настройка GitHub Pages
    if not setup_github_pages():
        print("❌ Ошибка настройки GitHub Pages")
        return
    
    # Создание скрипта деплоя
    create_deploy_script()
    
    print("\n" + "=" * 60)
    print("🎉 ДЕПЛОЙ ЗАВЕРШЕН!")
    print("=" * 60)
    print("🌐 Ваш сайт будет доступен на:")
    print("   https://[YOUR_USERNAME].github.io/upwork-proposal-generator/")
    print("=" * 60)
    print("📋 Для обновления сайта используйте:")
    print("   ./deploy.sh")
    print("=" * 60)
    print("💡 Замените [YOUR_USERNAME] на ваше имя пользователя GitHub")
    print("=" * 60)

if __name__ == "__main__":
    main() 