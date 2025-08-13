#!/bin/bash

echo "🚀 Запуск сервера аутентификации..."

# Активируем виртуальное окружение
if [ -d "venv" ]; then
    echo "📦 Активация виртуального окружения..."
    source venv/bin/activate
else
    echo "📦 Создание виртуального окружения..."
    python3 -m venv venv
    source venv/bin/activate
    
    echo "📦 Установка зависимостей..."
    pip install -r requirements.txt
fi

# Проверяем, что порт 5000 свободен
if lsof -Pi :5000 -sTCP:LISTEN -t >/dev/null ; then
    echo "⚠️  Порт 5000 уже занят. Останавливаем процесс..."
    lsof -ti:5000 | xargs kill -9
    sleep 2
fi

echo "🌐 Запуск сервера на http://localhost:5000"
echo "📱 Теперь вы можете входить в аккаунт с любого устройства!"
echo ""
echo "Для остановки сервера нажмите Ctrl+C"
echo ""

# Запускаем сервер
python auth_server.py 