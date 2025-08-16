// Система аутентификации Supabase
// Версия 4.0 - ОБНОВЛЕНО 16.08.2025

// Глобальные переменные
let currentUser = null;
let userProfile = null;

// Функция переключения вкладок аутентификации - определяем сразу
function showTab(tabName) {
    console.log('Переключение на вкладку:', tabName);
    
    try {
        // Скрываем все формы
        const forms = document.querySelectorAll('.auth-form');
        forms.forEach(form => {
            form.style.display = 'none';
        });
        
        // Показываем нужную форму
        const targetForm = document.getElementById(tabName + 'Form');
        if (targetForm) {
            targetForm.style.display = 'block';
        }
        
        // Обновляем активную вкладку
        const buttons = document.querySelectorAll('.tab-btn');
        buttons.forEach(btn => {
            btn.classList.remove('active');
        });
        
        // Находим кнопку по тексту
        const targetBtn = Array.from(buttons).find(btn => {
            if (tabName === 'login') return btn.textContent.includes('Вход');
            if (tabName === 'register') return btn.textContent.includes('Регистрация');
            return false;
        });
        
        if (targetBtn) {
            targetBtn.classList.add('active');
        }
    } catch (error) {
        console.error('Ошибка в showTab:', error);
    }
}

// Делаем функцию доступной глобально
window.showTab = showTab;

// Инициализация приложения
document.addEventListener('DOMContentLoaded', function() {
    console.log('🚀 Приложение загружено');
    
    try {
        // Проверяем, что auth.js загружен
        if (typeof onAuthStateChange === 'undefined') {
            console.error('❌ onAuthStateChange не определен - auth.js не загружен');
            return;
        }
        
        // Слушатель состояния аутентификации
        onAuthStateChange((user) => {
            if (user) {
                console.log('✅ Пользователь вошел:', user.email);
                currentUser = user;
                showUserInterface(user);
                loadUserProfile(user.id);
            } else {
                console.log('👋 Пользователь вышел');
                currentUser = null;
                userProfile = null;
                showAuthInterface();
            }
        });
        
        console.log('✅ Слушатель аутентификации установлен');
    } catch (error) {
        console.error('❌ Ошибка инициализации приложения:', error);
    }
});

// Показать интерфейс пользователя
function showUserInterface(user) {
    try {
        document.getElementById('authForms').style.display = 'none';
        document.getElementById('mainApp').style.display = 'block';
        document.getElementById('userInfo').style.display = 'block';
        document.getElementById('userEmail').textContent = user.email;
        
        // Загрузить историю предложений
        loadProposalsHistory(user.id);
    } catch (error) {
        console.error('❌ Ошибка в showUserInterface:', error);
    }
}

// Показать интерфейс аутентификации
function showAuthInterface() {
    try {
        document.getElementById('authForms').style.display = 'block';
        document.getElementById('mainApp').style.display = 'none';
        document.getElementById('userInfo').style.display = 'none';
    } catch (error) {
        console.error('❌ Ошибка в showAuthInterface:', error);
    }
}

// Загрузка профиля пользователя
async function loadUserProfile(userId) {
    try {
        userProfile = await getUserProfile(userId);
        if (userProfile) {
            updateSubscriptionStatus(userProfile);
        }
    } catch (error) {
        console.error('Ошибка загрузки профиля:', error);
    }
}

// Обновление статуса подписки
function updateSubscriptionStatus(profile) {
    const subscriptionType = document.getElementById('subscriptionType');
    const dailyRemaining = document.getElementById('dailyRemaining');
    
    if (subscriptionType) subscriptionType.textContent = profile.subscription === 'free' ? 'Бесплатная (Демо)' : 'Premium';
    if (dailyRemaining) dailyRemaining.textContent = `Осталось: ${profile.daily_remaining} предложений`;
}

// GitHub вход
window.handleGitHubLogin = async () => {
    try {
        showNotification('Входим через GitHub...', 'info');
        await signInWithGitHub();
        showNotification('Успешный вход через GitHub!', 'success');
    } catch (error) {
        console.error('Ошибка GitHub входа:', error);
        showNotification('Ошибка входа через GitHub: ' + error.message, 'error');
    }
};

// Регистрация
window.handleRegister = async (event) => {
    event.preventDefault();
    
    const email = document.getElementById('registerEmail').value;
    const password = document.getElementById('registerPassword').value;
    const confirmPassword = document.getElementById('confirmPassword').value;
    
    if (password !== confirmPassword) {
        showNotification('Пароли не совпадают!', 'error');
        return;
    }
    
    try {
        showNotification('Регистрируем...', 'info');
        await registerUser(email, password, email);
        showNotification('Регистрация успешна!', 'success');
    } catch (error) {
        console.error('Ошибка регистрации:', error);
        showNotification('Ошибка регистрации: ' + error.message, 'error');
    }
};

// Вход
window.handleLogin = async (event) => {
    event.preventDefault();
    
    const email = document.getElementById('loginEmail').value;
    const password = document.getElementById('loginPassword').value;
    
    try {
        showNotification('Входим...', 'info');
        await loginUser(email, password);
        showNotification('Вход выполнен!', 'success');
    } catch (error) {
        console.error('Ошибка входа:', error);
        showNotification('Ошибка входа: ' + error.message, 'error');
    }
};

// Выход
window.handleLogout = async () => {
    try {
        await logoutUser();
        showNotification('Выход выполнен!', 'info');
    } catch (error) {
        console.error('Ошибка выхода:', error);
        showNotification('Ошибка выхода: ' + error.message, 'error');
    }
};

// Генерация предложения
window.generateProposal = async (event) => {
    event.preventDefault();
    
    if (!currentUser) {
        showNotification('Сначала войдите в систему!', 'error');
        return;
    }
    
    if (!userProfile || userProfile.daily_remaining <= 0) {
        showNotification('Достигнут лимит предложений на сегодня!', 'error');
        return;
    }
    
    const formData = {
        title: document.getElementById('projectTitle').value,
        description: document.getElementById('projectDescription').value
    };
    
    try {
        showNotification('Генерируем предложение...', 'info');
        
        // Демо-генерация (замените на реальный AI)
        const generatedProposal = generateDemoProposal(formData);
        
        // Сохраняем в Supabase
        await saveProposal(currentUser.id, formData, generatedProposal);
        
        // Обновляем лимиты
        await updateUserLimits(currentUser.id, userProfile.daily_remaining - 1);
        userProfile.daily_remaining -= 1;
        updateSubscriptionStatus(userProfile);
        
        // Показываем результат
        document.getElementById('proposalContent').innerHTML = generatedProposal;
        document.getElementById('proposalResult').style.display = 'block';
        
        showNotification('Предложение сгенерировано!', 'success');
        
        // Перезагружаем историю
        loadProposalsHistory(currentUser.id);
        
    } catch (error) {
        console.error('Ошибка генерации:', error);
        showNotification('Ошибка генерации: ' + error.message, 'error');
    }
};

// Демо-генерация предложения
function generateDemoProposal(data) {
    return `
        <div class="proposal-demo">
            <h4>Предложение для проекта: ${data.title}</h4>
            <p><strong>Описание:</strong> ${data.description}</p>
            <hr>
            <div class="proposal-text">
                <p>Здравствуйте!</p>
                <p>Я заинтересован в вашем проекте "${data.title}". Изучив описание, я понимаю, что вам нужен профессионал, который может качественно выполнить эту задачу.</p>
                <p>Вот что я предлагаю:</p>
                <ul>
                    <li>Детальный анализ требований проекта</li>
                    <li>Поэтапное выполнение с регулярными обновлениями</li>
                    <li>Качественный результат в установленные сроки</li>
                    <li>Поддержка после завершения проекта</li>
                </ul>
                <p>Готов обсудить детали и ответить на любые вопросы. Давайте работать вместе!</p>
                <p>С уважением,<br>Ваш исполнитель</p>
            </div>
        </div>
    `;
}

// Загрузка истории предложений
async function loadProposalsHistory(userId) {
    try {
        const proposals = await getProposalsHistory(userId);
        // Здесь можно добавить отображение истории
        console.log('История предложений загружена:', proposals);
    } catch (error) {
        console.error('Ошибка загрузки истории:', error);
    }
}

// Утилиты
// Система уведомлений
function showNotification(message, type = 'info') {
    const notifications = document.getElementById('notifications');
    const notification = document.createElement('div');
    notification.className = `notification ${type}`;
    notification.textContent = message;
    notifications.appendChild(notification);
    
    // Автоматическое удаление через 5 секунд
    setTimeout(() => {
        if (notification.parentNode) {
            notification.remove();
        }
    }, 5000);
}
