#!/usr/bin/env python3
"""
Скрипт для проверки и настройки GitHub Pages
"""

import requests
import time
import subprocess
import sys

def check_github_pages():
    """Проверяет доступность GitHub Pages"""
    url = "https://darksaiders12.github.io/upwork-proposal-generator/"
    
    print("🔍 Проверяем GitHub Pages...")
    print(f"URL: {url}")
    
    try:
        response = requests.get(url, timeout=10)
        print(f"Статус: {response.status_code}")
        
        if response.status_code == 200:
            print("✅ Сайт работает!")
            return True
        elif response.status_code == 404:
            print("❌ Сайт возвращает 404")
            return False
        else:
            print(f"⚠️ Неожиданный статус: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Ошибка при проверке: {e}")
        return False

def check_gh_pages_branch():
    """Проверяет ветку gh-pages"""
    print("\n🔍 Проверяем ветку gh-pages...")
    
    try:
        # Проверяем текущую ветку
        result = subprocess.run(['git', 'branch', '--show-current'], 
                              capture_output=True, text=True)
        current_branch = result.stdout.strip()
        print(f"Текущая ветка: {current_branch}")
        
        # Проверяем наличие gh-pages
        result = subprocess.run(['git', 'branch', '-a'], 
                              capture_output=True, text=True)
        branches = result.stdout
        print("Доступные ветки:")
        for line in branches.split('\n'):
            if 'gh-pages' in line:
                print(f"  {line.strip()}")
        
        return 'gh-pages' in branches
        
    except Exception as e:
        print(f"❌ Ошибка при проверке веток: {e}")
        return False

def check_files_in_gh_pages():
    """Проверяет файлы в ветке gh-pages"""
    print("\n🔍 Проверяем файлы в gh-pages...")
    
    try:
        # Переключаемся на gh-pages
        subprocess.run(['git', 'checkout', 'gh-pages'], check=True)
        
        # Проверяем файлы
        result = subprocess.run(['ls', '-la'], capture_output=True, text=True)
        files = result.stdout
        
        print("Файлы в ветке gh-pages:")
        for line in files.split('\n'):
            if any(keyword in line for keyword in ['index.html', 'styles.css', 'app.js']):
                print(f"  {line.strip()}")
        
        # Возвращаемся на main
        subprocess.run(['git', 'checkout', 'main'], check=True)
        
        return True
        
    except Exception as e:
        print(f"❌ Ошибка при проверке файлов: {e}")
        return False

def fix_github_pages():
    """Исправляет проблемы с GitHub Pages"""
    print("\n🔧 Исправляем GitHub Pages...")
    
    try:
        # Переключаемся на gh-pages
        subprocess.run(['git', 'checkout', 'gh-pages'], check=True)
        
        # Удаляем все файлы кроме нужных
        subprocess.run(['git', 'rm', '-r', '--cached', '.'], check=True)
        subprocess.run(['git', 'add', 'index.html', 'styles.css', 'app.js'], check=True)
        
        # Коммитим изменения
        subprocess.run(['git', 'commit', '-m', 'Clean gh-pages branch'], check=True)
        
        # Отправляем на GitHub
        subprocess.run(['git', 'push', 'origin', 'gh-pages'], check=True)
        
        # Возвращаемся на main
        subprocess.run(['git', 'checkout', 'main'], check=True)
        
        print("✅ GitHub Pages исправлен!")
        return True
        
    except Exception as e:
        print(f"❌ Ошибка при исправлении: {e}")
        return False

def main():
    print("🚀 Проверка и настройка GitHub Pages")
    print("=" * 50)
    
    # Проверяем текущее состояние
    pages_working = check_github_pages()
    gh_pages_exists = check_gh_pages_branch()
    files_ok = check_files_in_gh_pages()
    
    print("\n📊 Результаты проверки:")
    print(f"GitHub Pages работает: {'✅' if pages_working else '❌'}")
    print(f"Ветка gh-pages существует: {'✅' if gh_pages_exists else '❌'}")
    print(f"Файлы в порядке: {'✅' if files_ok else '❌'}")
    
    if not pages_working:
        print("\n🔧 Пытаемся исправить...")
        if fix_github_pages():
            print("\n⏳ Ждем 2 минуты для обновления GitHub Pages...")
            time.sleep(120)
            
            if check_github_pages():
                print("🎉 Проблема решена! Сайт работает!")
            else:
                print("❌ Проблема не решена. Проверьте настройки GitHub Pages вручную.")
        else:
            print("❌ Не удалось исправить автоматически.")
    
    print("\n📋 Рекомендации:")
    print("1. Проверьте настройки GitHub Pages: https://github.com/DARKSAIDERS12/upwork-proposal-generator/settings/pages")
    print("2. Убедитесь, что источник установлен на 'Deploy from a branch'")
    print("3. Ветка должна быть 'gh-pages'")
    print("4. Папка должна быть '/ (root)'")

if __name__ == "__main__":
    main() 