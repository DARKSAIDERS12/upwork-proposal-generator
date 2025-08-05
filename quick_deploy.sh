#!/bin/bash

echo "🚀 БЫСТРЫЙ ДЕПЛОЙ НА GITHUB"
echo "================================"

# Проверяем статус Git
if [ ! -d ".git" ]; then
    echo "❌ Git репозиторий не инициализирован"
    exit 1
fi

# Добавляем все файлы
echo "📁 Добавление файлов..."
git add .

# Создаем коммит
echo "💾 Создание коммита..."
git commit -m "Update: $(date)"

# Проверяем, есть ли удаленный репозиторий
if ! git remote get-url origin > /dev/null 2>&1; then
    echo "🔗 Настройка удаленного репозитория..."
    echo "📋 Создайте репозиторий на GitHub:"
    echo "   1. Перейдите на https://github.com/new"
    echo "   2. Название: upwork-proposal-generator"
    echo "   3. Выберите Public"
    echo "   4. НЕ ставьте галочки"
    echo "   5. Нажмите Create repository"
    echo ""
    read -p "Введите ваше имя пользователя GitHub: " username
    git remote add origin "https://github.com/$username/upwork-proposal-generator.git"
    git branch -M main
fi

# Отправляем на GitHub
echo "🌐 Отправка на GitHub..."
git push origin main

echo ""
echo "✅ ДЕПЛОЙ ЗАВЕРШЕН!"
echo "================================"
echo "🌐 Сайт будет доступен на:"
echo "   https://[YOUR_USERNAME].github.io/upwork-proposal-generator/"
echo ""
echo "📋 Для настройки GitHub Pages:"
echo "   1. Перейдите в Settings репозитория"
echo "   2. Найдите Pages в левом меню"
echo "   3. Source: Deploy from a branch"
echo "   4. Branch: gh-pages, folder: / (root)"
echo "   5. Save"
echo ""
echo "💡 Замените [YOUR_USERNAME] на ваше имя пользователя" 