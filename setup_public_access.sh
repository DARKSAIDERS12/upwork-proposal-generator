#!/bin/bash

echo "🚀 НАСТРОЙКА ПУБЛИЧНОГО ДОСТУПА ЧЕРЕЗ GITHUB PAGES"
echo "=================================================="

# Проверяем, что мы в правильной ветке
if [ "$(git branch --show-current)" != "gh-pages" ]; then
    echo "❌ Переключитесь на ветку gh-pages: git checkout gh-pages"
    exit 1
fi

# Проверяем наличие необходимых файлов
if [ ! -f "index.html" ]; then
    echo "❌ Файл index.html не найден!"
    exit 1
fi

if [ ! -f "app.js" ]; then
    echo "❌ Файл app.js не найден!"
    exit 1
fi

if [ ! -f "styles.css" ]; then
    echo "❌ Файл styles.css не найден!"
    exit 1
fi

echo "✅ Все необходимые файлы найдены"

# Добавляем все изменения
git add .

# Коммитим изменения
git commit -m "Обновление файлов для GitHub Pages"

echo ""
echo "📋 ИНСТРУКЦИИ ДЛЯ НАСТРОЙКИ GITHUB PAGES:"
echo "=========================================="
echo ""
echo "1. Откройте ваш репозиторий на GitHub"
echo "2. Перейдите в Settings → Pages"
echo "3. В Source выберите 'Deploy from a branch'"
echo "4. В Branch выберите 'gh-pages'"
echo "5. Нажмите Save"
echo ""
echo "🌐 После настройки сайт будет доступен по адресу:"
echo "   https://[ваш-username].github.io/upwork-proposal-generator/"
echo ""
echo "⏱️  Время ожидания: 2-5 минут"
echo ""

# Пытаемся отправить изменения
echo "📤 Отправка изменений на GitHub..."
if git push origin gh-pages; then
    echo "✅ Изменения отправлены успешно!"
else
    echo "⚠️  Не удалось отправить изменения автоматически"
    echo "   Создайте репозиторий вручную на GitHub и выполните:"
    echo "   git remote add origin https://github.com/[username]/upwork-proposal-generator.git"
    echo "   git push -u origin gh-pages"
fi

echo ""
echo "🎉 Настройка завершена!"
