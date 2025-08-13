#!/bin/bash

echo "🚀 Быстрый запуск системы аутентификации"
echo "=========================================="

# Переходим в папку backend
cd backend

# Делаем скрипты исполняемыми
chmod +x start_auth_server.sh
chmod +x migrate_users.py

echo "📦 Проверяем зависимости..."

# Проверяем Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 не найден. Установите Python3 и попробуйте снова."
    exit 1
fi

# Проверяем pip
if ! command -v pip3 &> /dev/null; then
    echo "❌ pip3 не найден. Установите pip3 и попробуйте снова."
    exit 1
fi

echo "✅ Python3 и pip3 найдены"

# Создаем виртуальное окружение если его нет
if [ ! -d "venv" ]; then
    echo "📦 Создаем виртуальное окружение..."
    python3 -m venv venv
fi

# Активируем виртуальное окружение
echo "📦 Активируем виртуальное окружение..."
source venv/bin/activate

# Устанавливаем зависимости
echo "📦 Устанавливаем зависимости..."
pip install -r requirements.txt

echo "✅ Зависимости установлены"

# Запускаем миграцию
echo "🔄 Запускаем миграцию пользователей..."
python3 migrate_users.py

echo ""
echo "🌐 Запускаем сервер аутентификации..."
echo "📱 Теперь вы можете входить в аккаунт с любого устройства!"
echo ""
echo "Для остановки сервера нажмите Ctrl+C"
echo ""

# Запускаем сервер
python3 auth_server.py 