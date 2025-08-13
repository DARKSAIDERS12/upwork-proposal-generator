# 🌍 ПУБЛИЧНЫЙ САЙТ - ИНСТРУКЦИЯ

## ✅ Статус: РАБОТАЕТ

Ваш публичный сайт полностью настроен и работает!

## 🔗 Ссылки

- **🌍 Публичный сайт**: https://darksaiders12.github.io/upwork-proposal-generator/
- **🔐 Сервер аутентификации**: https://upwork-auth-server.onrender.com
- **📱 GitHub репозиторий**: https://github.com/DARKSAIDERS12/upwork-proposal-generator

## 🚀 Как обновить сайт

### Автоматическое обновление:
```bash
./update_github_pages.sh
```

### Ручное обновление:
```bash
# 1. Сохранить изменения в main
git add .
git commit -m "Описание изменений"
git push origin main

# 2. Обновить gh-pages
git checkout gh-pages
git merge main
git push origin gh-pages

# 3. Вернуться на main
git checkout main
```

## 🔧 Что настроено

### ✅ GitHub Pages
- Ветка `gh-pages` настроена для публикации
- Файл `.nojekyll` для правильной работы
- Автоматическое обновление при push в gh-pages

### ✅ Сервер аутентификации
- Публичный сервер на Render.com
- Автоматический запуск и перезапуск
- База данных пользователей синхронизирована

### ✅ Фронтенд
- Использует только публичный сервер
- Не зависит от локального IP
- Работает из любой точки мира

## 📱 Функции сайта

- **🔐 Регистрация и вход** в личный кабинет
- **🤖 Генерация предложений** с помощью AI
- **💰 Система подписок** (Premium, Pro)
- **⚙️ Управление подпиской** и настройками
- **📊 История предложений** и статистика

## 🛠️ Техническая поддержка

### Если сайт не работает:
1. Проверьте статус сервера: `curl https://upwork-auth-server.onrender.com/api/health`
2. Обновите GitHub Pages: `./update_github_pages.sh`
3. Проверьте логи на Render.com

### Если не работает аутентификация:
1. Проверьте подключение к интернету
2. Убедитесь, что сервер Render работает
3. Очистите кэш браузера

## 📞 Контакты

- **GitHub Issues**: https://github.com/DARKSAIDERS12/upwork-proposal-generator/issues
- **Статус сервера**: https://upwork-auth-server.onrender.com/api/health

---

**🎉 Ваш сайт готов к использованию! Пользователи могут регистрироваться и входить в личный кабинет с любого устройства.** 