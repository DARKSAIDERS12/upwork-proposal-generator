# 🚀 Upwork Proposal Generator

AI-помощник для создания выигрышных предложений на Upwork

## 🌐 Живой сайт

**🌍 Публичный URL:** https://[YOUR_USERNAME].github.io/upwork-proposal-generator/

## 📋 Описание

Полнофункциональное SaaS-приложение, которое помогает фрилансерам создавать профессиональные предложения для проектов на Upwork с помощью искусственного интеллекта.

## 🏗 Архитектура

- **Frontend**: HTML/CSS/JavaScript (GitHub Pages)
- **Backend**: FastAPI + Python + SQLite
- **AI**: OpenAI GPT-3.5-turbo
- **База данных**: SQLite

## 🚀 Быстрый запуск

### Локальный запуск:
```bash
git clone https://github.com/[YOUR_USERNAME]/upwork-proposal-generator.git
cd upwork-proposal-generator
python3 quick_start.py
```

### Доступ к сайту:
- **Локально:** http://localhost:3000
- **GitHub Pages:** https://[YOUR_USERNAME].github.io/upwork-proposal-generator/

## 🌐 Деплой на GitHub Pages

### Автоматический деплой:
1. Создайте репозиторий на GitHub
2. Загрузите код в репозиторий
3. Включите GitHub Pages в настройках репозитория
4. Выберите ветку `gh-pages` как источник

### Ручной деплой:
```bash
# Добавьте файлы
git add .

# Создайте коммит
git commit -m "Initial commit"

# Добавьте удаленный репозиторий
git remote add origin https://github.com/[YOUR_USERNAME]/upwork-proposal-generator.git

# Отправьте код
git push -u origin main
```

## 🎯 Функции

- ✅ Регистрация и вход пользователей
- ✅ Генерация предложений с помощью AI
- ✅ Настройка параметров (бюджет, специализация, тон)
- ✅ Копирование сгенерированных предложений
- ✅ История созданных предложений
- ✅ Полное API с документацией

## 📁 Структура проекта

```
upwork-proposal-generator/
├── frontend/                 # Frontend (HTML/CSS/JS)
├── backend/                  # Backend API (FastAPI)
├── docs/                     # GitHub Pages (автогенерируется)
├── .github/workflows/        # GitHub Actions
├── quick_start.py           # Быстрый запуск
├── README_GITHUB.md         # Этот файл
└── README.md                # Основной README
```

## 🔧 API эндпоинты

- `POST /api/v1/auth/register` - Регистрация
- `POST /api/v1/auth/login-json` - Вход
- `GET /api/v1/auth/me` - Профиль пользователя
- `POST /api/v1/proposals/generate` - Генерация предложений
- `GET /api/v1/proposals/` - История предложений

## 📊 Статус проекта

- ✅ **Frontend:** 100% готов
- ✅ **Backend:** 100% готов
- ✅ **GitHub Pages:** Настроен
- ✅ **Автоматический деплой:** Настроен
- ⚠️ **AI интеграция:** Требует настройки OpenAI API ключа

## 🎯 Следующие шаги

1. Создайте репозиторий на GitHub
2. Замените `[YOUR_USERNAME]` на ваше имя пользователя
3. Загрузите код в репозиторий
4. Включите GitHub Pages
5. Настройте OpenAI API ключ для генерации предложений

## 📖 Подробная документация

См. файл `README.md` для подробной информации по установке, настройке и устранению неполадок.

---

**Создано с ❤️ для фрилансеров** 