#!/bin/bash

echo "🚀 Обновление GitHub Pages..."

# Проверяем, что мы в ветке main
current_branch=$(git branch --show-current)
if [ "$current_branch" != "main" ]; then
    echo "❌ Ошибка: Вы должны быть в ветке main"
    echo "Текущая ветка: $current_branch"
    exit 1
fi

# Сохраняем текущие изменения
echo "💾 Сохранение изменений в main..."
git add .
git commit -m "Auto-update: $(date '+%Y-%m-%d %H:%M:%S')" || echo "Нет изменений для коммита"

# Отправляем изменения в main
echo "📤 Отправка изменений в main..."
git push origin main

# Переключаемся на gh-pages
echo "🔄 Переключение на ветку gh-pages..."
git checkout gh-pages

# Обновляем gh-pages из main
echo "📥 Обновление gh-pages из main..."
git merge main

# Отправляем обновленную gh-pages
echo "📤 Отправка обновленной gh-pages..."
git push origin gh-pages

# Возвращаемся на main
echo "🔄 Возврат на ветку main..."
git checkout main

echo ""
echo "✅ GitHub Pages обновлен!"
echo "🌍 Ваш сайт доступен по адресу: https://darksaiders12.github.io/upwork-proposal-generator/"
echo "⏰ Обновление займет несколько минут..."
echo ""
echo "🔐 Сервер аутентификации: https://upwork-auth-server.onrender.com"
echo "📱 Пользователи могут входить в личный кабинет с любого устройства!" 