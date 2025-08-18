#!/bin/bash

# Скрипт для запуска публичного сайта Upwork Proposal Generator
# Автор: AI Assistant
# Дата: 16.08.2025

echo "🚀 Запуск публичного сайта Upwork Proposal Generator..."

# Переходим в директорию проекта
cd "$(dirname "$0")"

# Останавливаем все предыдущие серверы
echo "🛑 Останавливаем предыдущие серверы..."
pkill -f "python3 -m http.server" 2>/dev/null
sleep 2

# Проверяем наличие необходимых файлов
echo "📁 Проверяем файлы проекта..."
if [ ! -f "index.html" ]; then
    echo "❌ Ошибка: index.html не найден!"
    exit 1
fi

if [ ! -f "app.js" ]; then
    echo "❌ Ошибка: app.js не найден!"
    exit 1
fi

if [ ! -f "auth.js" ]; then
    echo "❌ Ошибка: auth.js не найден!"
    exit 1
fi

if [ ! -f "styles.css" ]; then
    echo "❌ Ошибка: styles.css не найден!"
    exit 1
fi

echo "✅ Все необходимые файлы найдены"

# Запускаем HTTP сервер
echo "🌐 Запускаем HTTP сервер на порту 8000..."
python3 -m http.server 8000 &

# Ждем запуска сервера
sleep 3

# Проверяем, что сервер работает
if curl -s -o /dev/null -w "%{http_code}" http://localhost:8000/ | grep -q "200"; then
    echo "✅ Сайт успешно запущен!"
    echo "🌍 Откройте в браузере: http://localhost:8000"
    echo "📱 Или: http://127.0.0.1:8000"
    echo ""
    echo "Для остановки сервера нажмите Ctrl+C или выполните: pkill -f 'python3 -m http.server'"
    echo ""
    echo "📊 Статус сервера:"
    ps aux | grep "python3 -m http.server" | grep -v grep
else
    echo "❌ Ошибка запуска сервера!"
    exit 1
fi

# Ждем сигнала остановки
trap 'echo ""; echo "🛑 Останавливаем сервер..."; pkill -f "python3 -m http.server"; echo "✅ Сервер остановлен"; exit 0' INT

# Держим скрипт активным
while true; do
    sleep 1
done
