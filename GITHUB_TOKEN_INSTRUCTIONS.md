# 🔑 СОЗДАНИЕ ТОКЕНА ДОСТУПА GITHUB

## 📋 Пошаговая инструкция:

### 1️⃣ **Создание Personal Access Token:**

1. **Перейдите на GitHub:**
   - Откройте https://github.com
   - Войдите в свой аккаунт DARKSAIDERS12

2. **Создайте токен:**
   - Нажмите на свой аватар (правый верхний угол)
   - Выберите "Settings"
   - В левом меню найдите "Developer settings"
   - Нажмите "Personal access tokens"
   - Выберите "Tokens (classic)"
   - Нажмите "Generate new token (classic)"

3. **Настройте токен:**
   - **Note:** `Upwork Proposal Generator`
   - **Expiration:** `No expiration` (или выберите дату)
   - **Scopes:** Отметьте следующие:
     - ✅ `repo` (полный доступ к репозиториям)
     - ✅ `workflow` (для GitHub Actions)
     - ✅ `write:packages` (для пакетов)

4. **Создайте токен:**
   - Нажмите "Generate token"
   - **Скопируйте токен** (он показывается только один раз!)

### 2️⃣ **Использование токена:**

При запросе пароля используйте:
- **Username:** `DARKSAIDERS12`
- **Password:** `ваш_токен_доступа` (не пароль от аккаунта!)

### 3️⃣ **Автоматическая настройка:**

```bash
# Настройте Git для использования токена
git config --global user.name "DARKSAIDERS12"
git config --global user.email "ваш_email@example.com"

# При push используйте токен как пароль
git push origin main
```

### 4️⃣ **Альтернативный способ (SSH):**

Если хотите использовать SSH ключи:

```bash
# Генерируйте SSH ключ
ssh-keygen -t ed25519 -C "ваш_email@example.com"

# Добавьте ключ в SSH агент
eval "$(ssh-agent -s)"
ssh-add ~/.ssh/id_ed25519

# Скопируйте публичный ключ
cat ~/.ssh/id_ed25519.pub

# Добавьте ключ в GitHub Settings → SSH and GPG keys
```

### 5️⃣ **Проверка подключения:**

```bash
# Проверьте подключение
ssh -T git@github.com

# Или для HTTPS
git ls-remote https://github.com/DARKSAIDERS12/upwork-proposal-generator.git
```

---

**💡 Важно:** Храните токен в безопасном месте и не делитесь им! 