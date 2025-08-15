#!/bin/bash

# 🚂 СКРИПТ ОБНОВЛЕНИЯ URL НА RAILWAY
# Этот скрипт обновит все ссылки с Render.com на Railway.app

echo "🚂 ОБНОВЛЕНИЕ ПУБЛИЧНОГО САЙТА НА RAILWAY..."

# Проверяем, что мы в правильной директории
if [ ! -f "app.js" ]; then
    echo "❌ Ошибка: файл app.js не найден. Убедитесь, что вы в корне проекта."
    exit 1
fi

# Просим пользователя ввести Railway URL
echo "📝 Введите URL вашего Railway приложения (например: https://upwork-auth-production.up.railway.app):"
read RAILWAY_URL

# Убираем trailing slash если есть
RAILWAY_URL=${RAILWAY_URL%/}

echo "🔄 Обновляем app.js..."
# Обновляем API_BASE_URL в app.js
sed -i.bak "s|const API_BASE_URL = 'https://upwork-auth-server.onrender.com/api';|const API_BASE_URL = '$RAILWAY_URL/api';|g" app.js

echo "🔄 Обновляем subscription_manager.html..."
# Обновляем URL в subscription_manager.html
sed -i.bak "s|https://upwork-auth-server.onrender.com/api/user|$RAILWAY_URL/api/user|g" subscription_manager.html

echo "🔄 Обновляем версию для обхода кэша..."
# Обновляем версию в index.html
NEW_VERSION=$(date +"%Y%m%d-%H%M")
sed -i.bak "s|app\.js?v=[^\"]*|app.js?v=$NEW_VERSION|g" index.html

echo "📤 Коммитим изменения..."
git add .
git commit -m "🚂 Миграция на Railway.app - обновление API URL"

echo "🚀 Деплоим на GitHub Pages..."
git push origin main

echo "📤 Обновляем gh-pages..."
git checkout gh-pages
git reset --hard main
git push --force-with-lease origin gh-pages
git checkout main

echo "✅ ОБНОВЛЕНИЕ ЗАВЕРШЕНО!"
echo ""
echo "🌍 Публичный сайт: https://darksaiders12.github.io/upwork-proposal-generator/"
echo "🚂 Railway backend: $RAILWAY_URL"
echo ""
echo "🔄 Рекомендуется:"
echo "   1. Очистить кэш браузера"
echo "   2. Проверить работу через 2-3 минуты"
echo "   3. Протестировать регистрацию и вход"

