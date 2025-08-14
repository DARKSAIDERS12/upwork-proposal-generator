#!/bin/bash
echo "🔄 ПРИНУДИТЕЛЬНОЕ ОБНОВЛЕНИЕ GITHUB PAGES..."

# Добавляем изменения
git add .

# Коммитим с указанием времени
git commit -m "🔄 ПРИНУДИТЕЛЬНОЕ ОБНОВЛЕНИЕ - исправления лимитов и входа

- Добавлена метка времени для принудительного обновления
- Версионирование app.js для обхода кэша браузера
- Исправления должны теперь корректно загрузиться

Время обновления: $(date '+%Y-%m-%d %H:%M:%S')"

# Отправляем в main
git push origin main

# Принудительно обновляем GitHub Pages
echo "📤 Обновление GitHub Pages..."
git checkout gh-pages
git reset --hard main
git push --force-with-lease origin gh-pages
git checkout main

echo "✅ ПРИНУДИТЕЛЬНОЕ ОБНОВЛЕНИЕ ЗАВЕРШЕНО!"
echo "🌍 Проверьте сайт через 2-3 минуты: https://darksaiders12.github.io/upwork-proposal-generator/"
echo "🔄 Рекомендуется очистить кэш браузера или открыть в режиме инкогнито"
