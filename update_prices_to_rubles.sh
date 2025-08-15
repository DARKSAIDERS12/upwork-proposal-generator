#!/bin/bash
echo "💰 ОБНОВЛЕНИЕ ЦЕН НА РУБЛИ..."

# Добавляем изменения
git add .

# Коммитим
git commit -m "💰 Обновлены цены на рубли в модальном окне

✅ Изменения:
- $0 → 0 ₽ (бесплатная версия)
- $9.99/мес → 699 ₽/мес (Premium)
- Синхронизирована цена в app.js: 1,500 ₽ → 699 ₽
- Обновлена версия для принудительного обновления кэша

📱 Теперь пользователи видят цены в российских рублях"

# Отправляем в репозиторий
git push origin main

# Принудительно обновляем GitHub Pages
echo "🚀 Обновление GitHub Pages..."
git checkout gh-pages
git reset --hard main
git push --force-with-lease origin gh-pages
git checkout main

echo "✅ ЦЕНЫ ОБНОВЛЕНЫ НА РУБЛИ!"
echo "🌍 Проверьте через 2-3 минуты: https://darksaiders12.github.io/upwork-proposal-generator/"
echo "💰 Теперь Premium стоит 699 ₽/мес вместо $9.99/мес"

