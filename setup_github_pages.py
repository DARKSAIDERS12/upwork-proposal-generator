#!/usr/bin/env python3
"""
Настройка GitHub Pages для публичного доступа к Upwork Proposal Generator
"""

import subprocess
import os
import sys
import time

def print_banner():
    print("=" * 60)
    print("🌐 НАСТРОЙКА GITHUB PAGES")
    print("=" * 60)
    print("Публичный доступ к Upwork Proposal Generator")
    print("📱 Доступен на всех устройствах | 🔒 HTTPS")
    print("=" * 60)

def create_gh_pages_branch():
    """Создает ветку gh-pages для GitHub Pages"""
    print("🌿 Создание ветки gh-pages...")
    
    # Создаем новую ветку
    subprocess.run(["git", "checkout", "-b", "gh-pages"])
    
    # Удаляем все файлы кроме frontend
    subprocess.run(["git", "rm", "-r", "backend"])
    subprocess.run(["git", "rm", "-r", "docs"])
    subprocess.run(["git", "rm", "*.py"])
    subprocess.run(["git", "rm", "*.md"])
    subprocess.run(["git", "rm", "*.sh"])
    subprocess.run(["git", "rm", "*.zip"])
    subprocess.run(["git", "rm", "ngrok"])
    subprocess.run(["git", "rm", ".gitignore"])
    
    # Перемещаем frontend файлы в корень
    subprocess.run(["mv", "frontend/*", "."])
    subprocess.run(["rmdir", "frontend"])
    
    # Создаем index.html если его нет
    if not os.path.exists("index.html"):
        create_index_html()
    
    # Добавляем и коммитим
    subprocess.run(["git", "add", "."])
    subprocess.run(["git", "commit", "-m", "Setup GitHub Pages"])
    
    print("✅ Ветка gh-pages создана!")

def create_index_html():
    """Создает index.html для GitHub Pages"""
    html_content = """<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Upwork Proposal Generator - AI помощник для фрилансеров</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            margin: 0;
            padding: 20px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            min-height: 100vh;
        }
        .container {
            max-width: 800px;
            margin: 0 auto;
            text-align: center;
        }
        h1 {
            font-size: 2.5em;
            margin-bottom: 20px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }
        .description {
            font-size: 1.2em;
            margin-bottom: 30px;
            line-height: 1.6;
        }
        .features {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin: 40px 0;
        }
        .feature {
            background: rgba(255,255,255,0.1);
            padding: 20px;
            border-radius: 10px;
            backdrop-filter: blur(10px);
        }
        .feature h3 {
            margin-top: 0;
            color: #ffd700;
        }
        .cta-button {
            display: inline-block;
            background: #ff6b6b;
            color: white;
            padding: 15px 30px;
            text-decoration: none;
            border-radius: 25px;
            font-size: 1.1em;
            font-weight: bold;
            transition: transform 0.3s ease;
            margin: 10px;
        }
        .cta-button:hover {
            transform: translateY(-2px);
            background: #ff5252;
        }
        .status {
            background: rgba(255,255,255,0.1);
            padding: 20px;
            border-radius: 10px;
            margin: 20px 0;
        }
        .github-link {
            color: #ffd700;
            text-decoration: none;
        }
        .github-link:hover {
            text-decoration: underline;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🚀 Upwork Proposal Generator</h1>
        <p class="description">
            AI-помощник для создания выигрышных предложений на Upwork.<br>
            Автоматизируйте процесс создания профессиональных предложений с помощью искусственного интеллекта.
        </p>
        
        <div class="features">
            <div class="feature">
                <h3>🤖 AI Генерация</h3>
                <p>Создавайте персонализированные предложения с помощью OpenAI GPT</p>
            </div>
            <div class="feature">
                <h3>⚡ Быстро</h3>
                <p>Генерируйте предложения за секунды вместо часов</p>
            </div>
            <div class="feature">
                <h3>🎯 Эффективно</h3>
                <p>Увеличьте шансы на получение проектов</p>
            </div>
        </div>
        
        <div class="status">
            <h3>📊 Статус проекта</h3>
            <p>✅ MVP готов к использованию</p>
            <p>✅ Backend API работает</p>
            <p>✅ Frontend интерфейс готов</p>
            <p>⚠️ Требуется настройка OpenAI API ключа</p>
        </div>
        
        <a href="https://github.com/DARKSAIDERS12/upwork-proposal-generator" class="cta-button">
            📁 Исходный код на GitHub
        </a>
        
        <a href="http://192.168.0.124:3000" class="cta-button">
            🚀 Запустить локально
        </a>
        
        <p style="margin-top: 40px; font-size: 0.9em; opacity: 0.8;">
            Создано с ❤️ для фрилансеров | 
            <a href="https://github.com/DARKSAIDERS12/upwork-proposal-generator" class="github-link">
                GitHub репозиторий
            </a>
        </p>
    </div>
</body>
</html>"""
    
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html_content)

def push_to_github():
    """Отправляет ветку gh-pages на GitHub"""
    print("📤 Отправка на GitHub...")
    
    subprocess.run(["git", "push", "origin", "gh-pages"])
    
    print("✅ Код отправлен на GitHub!")

def setup_github_pages():
    """Инструкции по настройке GitHub Pages"""
    print("\n📋 ИНСТРУКЦИИ ПО НАСТРОЙКЕ GITHUB PAGES:")
    print("=" * 60)
    print("1. Перейдите на https://github.com/DARKSAIDERS12/upwork-proposal-generator")
    print("2. Нажмите на вкладку 'Settings'")
    print("3. В левом меню найдите 'Pages'")
    print("4. В разделе 'Source' выберите 'Deploy from a branch'")
    print("5. В 'Branch' выберите 'gh-pages' и '/ (root)'")
    print("6. Нажмите 'Save'")
    print("7. Подождите 2-5 минут для деплоя")
    print("=" * 60)
    print("🌐 После настройки сайт будет доступен по адресу:")
    print("   https://darksaiders12.github.io/upwork-proposal-generator/")

def main():
    print_banner()
    
    # Создаем ветку gh-pages
    create_gh_pages_branch()
    
    # Отправляем на GitHub
    push_to_github()
    
    # Показываем инструкции
    setup_github_pages()
    
    print("\n🎉 НАСТРОЙКА ЗАВЕРШЕНА!")
    print("📱 После настройки GitHub Pages сайт будет доступен:")
    print("   - На всех устройствах")
    print("   - Из любой точки мира")
    print("   - По HTTPS (защищенное соединение)")
    print("   - Через любой браузер")

if __name__ == "__main__":
    main() 