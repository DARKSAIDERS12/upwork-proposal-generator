#!/bin/bash

echo "🔧 Настройка сетевого доступа к серверу аутентификации..."

# Получаем IP адрес текущего устройства
LOCAL_IP=$(hostname -I | awk '{print $1}')
echo "📍 Ваш локальный IP адрес: $LOCAL_IP"

# Проверяем, запущен ли сервер
if pgrep -f "auth_server.py" > /dev/null; then
    echo "✅ Сервер аутентификации уже запущен"
else
    echo "🚀 Запускаем сервер аутентификации..."
    cd "$(dirname "$0")"
    nohup python3 auth_server.py > server.log 2>&1 &
    sleep 2
fi

# Проверяем статус сервера
echo "🔍 Проверяем статус сервера..."
if curl -s "http://localhost:5000/api/health" > /dev/null; then
    echo "✅ Сервер работает на localhost:5000"
else
    echo "❌ Сервер не отвечает на localhost:5000"
    exit 1
fi

# Проверяем доступность по сети
echo "🌐 Проверяем доступность по сети..."
if curl -s "http://$LOCAL_IP:5000/api/health" > /dev/null; then
    echo "✅ Сервер доступен по сети: http://$LOCAL_IP:5000"
else
    echo "❌ Сервер недоступен по сети"
    echo "🔧 Возможно, нужно настроить firewall..."
fi

echo ""
echo "📋 ИНСТРУКЦИЯ ДЛЯ ДОСТУПА С ДРУГИХ УСТРОЙСТВ:"
echo "1. Убедитесь, что устройства находятся в одной сети"
echo "2. На других устройствах используйте URL: http://$LOCAL_IP:5000"
echo "3. В файле app.js измените API_BASE_URL на: http://$LOCAL_IP:5000/api"
echo ""
echo "🔗 Для тестирования откройте: http://$LOCAL_IP:5000/api/health"
echo "👥 Для отладки пользователей: http://$LOCAL_IP:5000/api/user-info/demo@example.com"
echo "🔑 Для просмотра сессий: http://$LOCAL_IP:5000/api/debug/sessions" 