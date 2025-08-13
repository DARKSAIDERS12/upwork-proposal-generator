#!/bin/bash

echo "🚀 Развертывание сервера аутентификации в облако"
echo "================================================"

# Переходим в папку backend
cd backend

echo ""
echo "📋 Выберите платформу для развертывания:"
echo "1. Render.com (рекомендуется, бесплатно)"
echo "2. Railway.app (бесплатно)"
echo "3. Heroku (бесплатно)"
echo "4. Локальный сервер (только для тестирования)"
echo ""

read -p "Введите номер (1-4): " choice

case $choice in
    1)
        echo "🌐 Развертывание на Render.com"
        echo ""
        echo "📋 Инструкция:"
        echo "1. Перейдите на https://render.com"
        echo "2. Создайте аккаунт и войдите"
        echo "3. Нажмите 'New +' → 'Web Service'"
        echo "4. Подключите ваш GitHub репозиторий"
        echo "5. Выберите ветку main"
        echo "6. В настройках:"
        echo "   - Name: upwork-auth-server"
        echo "   - Environment: Python"
        echo "   - Build Command: pip install -r requirements.txt"
        echo "   - Start Command: python auth_server.py"
        echo "7. Нажмите 'Create Web Service'"
        echo ""
        echo "✅ После развертывания скопируйте URL и обновите app.js"
        ;;
    2)
        echo "🚂 Развертывание на Railway.app"
        echo ""
        echo "📋 Инструкция:"
        echo "1. Перейдите на https://railway.app"
        echo "2. Создайте аккаунт и войдите"
        echo "3. Нажмите 'New Project' → 'Deploy from GitHub repo'"
        echo "4. Выберите ваш репозиторий"
        echo "5. Railway автоматически определит настройки"
        echo "6. Дождитесь развертывания"
        echo "7. Скопируйте URL и обновите app.js"
        ;;
    3)
        echo "⚡ Развертывание на Heroku"
        echo ""
        echo "📋 Инструкция:"
        echo "1. Установите Heroku CLI: https://devcenter.heroku.com/articles/heroku-cli"
        echo "2. Войдите: heroku login"
        echo "3. Создайте приложение: heroku create upwork-auth-server"
        echo "4. Разверните: git push heroku main"
        echo "5. Откройте: heroku open"
        echo "6. Скопируйте URL и обновите app.js"
        ;;
    4)
        echo "💻 Запуск локального сервера"
        echo ""
        echo "⚠️  ВНИМАНИЕ: Локальный сервер доступен только с вашего компьютера!"
        echo "Другие устройства не смогут подключиться."
        echo ""
        echo "Для публичного доступа выберите варианты 1-3"
        echo ""
        read -p "Продолжить с локальным сервером? (y/n): " local_choice
        if [[ $local_choice == "y" ]]; then
            echo "🚀 Запуск локального сервера..."
            source venv/bin/activate
            python3 auth_server.py
        else
            echo "❌ Отменено. Выберите облачную платформу."
        fi
        ;;
    *)
        echo "❌ Неверный выбор. Попробуйте снова."
        exit 1
        ;;
esac

echo ""
echo "🎯 После развертывания не забудьте:"
echo "1. Скопировать URL вашего сервера"
echo "2. Обновить API_BASE_URL в app.js"
echo "3. Загрузить обновленный код на GitHub Pages"
echo "4. Протестировать вход с разных устройств"
echo ""
echo "📚 Подробные инструкции в README_AUTH_FIX.md" 