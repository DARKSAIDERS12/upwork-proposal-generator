// Глобальные переменные
let currentUser = null;
let stripe = null;
let sessionToken = localStorage.getItem('sessionToken');

// API конфигурация - автоматическое переключение между серверами
let API_BASE_URL = 'https://upwork-auth-server.onrender.com/api';

// Функция для проверки доступности сервера и переключения на локальный при необходимости
async function checkAndSetServer() {
    try {
        const response = await fetch('https://upwork-auth-server.onrender.com/api/health');
        if (response.ok) {
            API_BASE_URL = 'https://upwork-auth-server.onrender.com/api';
            console.log('✅ Используется публичный сервер Render');
            return true;
        }
    } catch (error) {
        console.log('❌ Публичный сервер недоступен, переключаемся на локальный');
    }
    
    // Если публичный сервер недоступен, используем локальный
    API_BASE_URL = 'http://192.168.1.124:5000/api';
    console.log('🔄 Используется локальный сервер');
    return false;
}

// Инициализация Stripe
function initStripe() {
    const publishableKey = 'pk_test_your_stripe_publishable_key'; // Замените на ваш ключ
    if (publishableKey !== 'pk_test_your_stripe_publishable_key') {
        stripe = Stripe(publishableKey);
    }
}

// Инициализация приложения
document.addEventListener('DOMContentLoaded', async function() {
    // Проверяем и устанавливаем доступный сервер
    await checkAndSetServer();
    
    initStripe();
    checkAuthStatus();
    loadProposalsHistory();
    initializeSubscriptionSystem();
});

// Инициализация системы подписок
function initializeSubscriptionSystem() {
    // Проверяем и сбрасываем ежедневные лимиты
    checkAndResetDailyLimits();
    
    // Устанавливаем интервал для ежедневного сброса (каждые 24 часа)
    setInterval(checkAndResetDailyLimits, 24 * 60 * 60 * 1000);
}

// Проверка и сброс ежедневных лимитов
async function checkAndResetDailyLimits() {
    if (!currentUser || !sessionToken) return;
    
    try {
        const response = await fetch(`${API_BASE_URL}/reset-daily-limits`, {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${sessionToken}`,
                'Content-Type': 'application/json'
            }
        });
        
        if (response.ok) {
            const data = await response.json();
            currentUser.daily_remaining = data.daily_remaining;
            updateSubscriptionStatus();
        }
    } catch (error) {
        console.error('Ошибка сброса лимитов:', error);
    }
}

// Проверка статуса аутентификации
async function checkAuthStatus() {
    if (sessionToken) {
        try {
            const response = await fetch(`${API_BASE_URL}/user`, {
                method: 'GET',
                headers: {
                    'Authorization': `Bearer ${sessionToken}`,
                    'Content-Type': 'application/json'
                }
            });
            
            if (response.ok) {
                const data = await response.json();
                currentUser = data.user;
                showMainApp();
                updateSubscriptionStatus();
                return;
            } else {
                // Токен недействителен, удаляем его
                localStorage.removeItem('sessionToken');
                sessionToken = null;
            }
        } catch (error) {
            console.error('Ошибка проверки аутентификации:', error);
            localStorage.removeItem('sessionToken');
            sessionToken = null;
        }
    }
    
    showAuthForms();
}

// Показать формы аутентификации
function showAuthForms() {
    document.getElementById('authForms').style.display = 'block';
    document.getElementById('mainApp').style.display = 'none';
    document.getElementById('userInfo').style.display = 'none';
}

// Показать основное приложение
function showMainApp() {
    document.getElementById('authForms').style.display = 'none';
    document.getElementById('mainApp').style.display = 'block';
    document.getElementById('userInfo').style.display = 'flex';
    
    if (currentUser) {
        document.getElementById('userEmail').textContent = currentUser.email;
    }
}

// Переключение между вкладками аутентификации
function showTab(tabName) {
    const loginForm = document.getElementById('loginForm');
    const registerForm = document.getElementById('registerForm');
    const tabs = document.querySelectorAll('.tab-btn');
    
    tabs.forEach(tab => tab.classList.remove('active'));
    
    if (tabName === 'login') {
        loginForm.style.display = 'block';
        registerForm.style.display = 'none';
        tabs[0].classList.add('active');
    } else {
        loginForm.style.display = 'none';
        registerForm.style.display = 'block';
        tabs[1].classList.add('active');
    }
}

// Регистрация пользователя
async function register(event) {
    event.preventDefault();
    
    const email = document.getElementById('registerEmail').value;
    const password = document.getElementById('registerPassword').value;
    const confirmPassword = document.getElementById('confirmPassword').value;
    
    if (password !== confirmPassword) {
        showNotification('Пароли не совпадают', 'error');
        return;
    }
    
    try {
        const response = await fetch(`${API_BASE_URL}/register`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ email, password })
        });
        
        const data = await response.json();
        
        if (response.ok) {
            // Сохраняем токен сессии
            sessionToken = data.session_token;
            localStorage.setItem('sessionToken', sessionToken);
            
            // Устанавливаем текущего пользователя
            currentUser = data.user;
            
            showMainApp();
            updateSubscriptionStatus();
            showNotification('Регистрация успешна!', 'success');
        } else {
            showNotification(data.error || 'Ошибка регистрации', 'error');
        }
        
    } catch (error) {
        showNotification('Ошибка регистрации: ' + error.message, 'error');
    }
}

// Вход пользователя
async function login(event) {
    event.preventDefault();
    
    const email = document.getElementById('loginEmail').value;
    const password = document.getElementById('loginPassword').value;
    
    try {
        const response = await fetch(`${API_BASE_URL}/login`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ email, password })
        });
        
        const data = await response.json();
        
        if (response.ok) {
            // Сохраняем токен сессии
            sessionToken = data.session_token;
            localStorage.setItem('sessionToken', sessionToken);
            
            // Устанавливаем текущего пользователя
            currentUser = data.user;
            
            showMainApp();
            updateSubscriptionStatus();
            showNotification('Вход выполнен успешно!', 'success');
        } else {
            showNotification(data.error || 'Неверный email или пароль', 'error');
        }
        
    } catch (error) {
        showNotification('Ошибка входа: ' + error.message, 'error');
    }
}

// Выход пользователя
async function logout() {
    try {
        if (sessionToken) {
            await fetch(`${API_BASE_URL}/logout`, {
                method: 'POST',
                headers: {
                    'Authorization': `Bearer ${sessionToken}`,
                    'Content-Type': 'application/json'
                }
            });
        }
    } catch (error) {
        console.error('Ошибка при выходе:', error);
    }
    
    // Очищаем локальные данные
    currentUser = null;
    sessionToken = null;
    localStorage.removeItem('sessionToken');
    localStorage.removeItem('user');
    
    showAuthForms();
    showNotification('Выход выполнен', 'info');
}

// Обновление статуса подписки
function updateSubscriptionStatus() {
    if (!currentUser) return;
    
    const subscriptionType = document.getElementById('subscriptionType');
    const dailyRemaining = document.getElementById('dailyRemaining');
    const upgradeBtn = document.getElementById('upgradeBtn');
    
    const subscriptionInfo = getSubscriptionInfo(currentUser.subscription);
    
    if (currentUser.subscription && currentUser.subscription !== 'free') {
        subscriptionType.textContent = subscriptionInfo.name;
        dailyRemaining.textContent = currentUser.daily_remaining === -1 ? 'Безлимитно' : `Осталось: ${currentUser.daily_remaining} предложений`;
        upgradeBtn.textContent = 'Управлять подпиской';
        upgradeBtn.onclick = manageSubscription;
    } else {
        subscriptionType.textContent = 'Бесплатная';
        dailyRemaining.textContent = `Осталось: ${currentUser.daily_remaining || 0} предложений`;
        upgradeBtn.textContent = 'Обновить до Premium';
        upgradeBtn.onclick = showUpgradeModal;
    }
}

// Получить информацию о подписке
function getSubscriptionInfo(subscriptionType) {
    const subscriptionData = {
        'free': {
            name: 'Бесплатная',
            aiProvider: 'Демо-режим',
            dailyLimit: 3,
            price: '0 ₽'
        },
        'premium': {
            name: 'Premium',
            aiProvider: 'Yandex GPT',
            dailyLimit: 50,
            price: '1,500 ₽'
        },
        'pro': {
            name: 'Pro',
            aiProvider: 'Yandex GPT + GigaChat',
            dailyLimit: 200,
            price: '3,000 ₽'
        },
        'enterprise': {
            name: 'Enterprise',
            aiProvider: 'Все AI провайдеры',
            dailyLimit: '∞',
            price: '9,900 ₽'
        }
    };
    
    return subscriptionData[subscriptionType] || subscriptionData['free'];
}

// Генерация предложения
async function generateProposal(event) {
    event.preventDefault();
    
    if (!currentUser) {
        showNotification('Необходимо войти в систему', 'error');
        return;
    }
    
    // Проверяем лимиты для бесплатной версии
    if (currentUser.subscription === 'free' && currentUser.dailyRemaining <= 0) {
        showNotification('Достигнут дневной лимит. Обновитесь до Premium для неограниченного доступа.', 'error');
        showUpgradeModal();
        return;
    }
    
    const formData = {
        title: document.getElementById('projectTitle').value,
        description: document.getElementById('projectDescription').value,
        budget: document.getElementById('projectBudget').value,
        specialization: document.getElementById('specialization').value,
        tone: document.getElementById('tone').value
    };
    
    showLoading(true);
    
    try {
        // В реальном приложении здесь был бы запрос к backend API
        const result = await generateProposalWithAI(formData);
        
        if (result.success) {
            displayProposal(result.proposal);
            
            // Уменьшаем счетчик для бесплатной версии
            if (currentUser.subscription === 'free') {
                currentUser.dailyRemaining--;
                
                // Обновляем пользователя в списке
                const users = JSON.parse(localStorage.getItem('users') || '[]');
                const userIndex = users.findIndex(u => u.email === currentUser.email);
                if (userIndex !== -1) {
                    users[userIndex] = currentUser;
                    localStorage.setItem('users', JSON.stringify(users));
                }
                
                localStorage.setItem('user', JSON.stringify(currentUser));
                updateSubscriptionStatus();
            }
            
            // Сохраняем в историю
            saveProposalToHistory(formData, result.proposal);
            
        } else {
            showNotification(result.error, 'error');
        }
        
    } catch (error) {
        showNotification('Ошибка генерации: ' + error.message, 'error');
    } finally {
        showLoading(false);
    }
}

// Генерация предложения с AI (демо-версия)
async function generateProposalWithAI(projectData) {
    // Имитация задержки API
    await new Promise(resolve => setTimeout(resolve, 2000));
    
    const { title, description, budget, specialization, tone } = projectData;
    
    const proposal = `Уважаемый клиент,

Я изучил ваш проект "${title}" и очень заинтересован в возможности сотрудничества с вами. Благодаря моему обширному опыту в области ${specialization}, я уверен, что смогу предоставить исключительные результаты, которые превзойдут ваши ожидания.

**Почему я подхожу для вашего проекта:**

✅ **Проверенный опыт**: Я успешно выполнил 50+ подобных проектов с рейтингом 5 звезд
✅ **Гарантия качества**: Каждый результат проходит тщательное тестирование и проверку
✅ **Прозрачная коммуникация**: Регулярные обновления и прозрачное управление проектом
✅ **Своевременная доставка**: 100% своевременное выполнение всех проектов

**Мой подход к вашему проекту:**
1. Детальный анализ требований и целей
2. Индивидуальное решение, адаптированное под ваши потребности
3. Итеративная разработка с регулярными циклами обратной связи
4. Тщательное тестирование и контроль качества
5. Подробная документация и поддержка

**Бюджет**: Я могу работать в рамках вашего бюджета ${budget}, обеспечивая высокое качество результатов.

**Сроки**: Я могу начать немедленно и выполнить проект в требуемые сроки.

Я готов сразу приступить к работе над вашим проектом. Давайте обсудим детали и начнем!

С наилучшими пожеланиями,
[Ваше имя]
Фрилансер-эксперт по ${specialization}

P.S. Я доступен для быстрого звонка, чтобы обсудить ваш проект подробнее.`;
    
    return {
        success: true,
        proposal: proposal
    };
}

// Отображение сгенерированного предложения
function displayProposal(proposal) {
    document.getElementById('proposalContent').textContent = proposal;
    document.getElementById('proposalResult').style.display = 'block';
    
    // Прокручиваем к результату
    document.getElementById('proposalResult').scrollIntoView({ 
        behavior: 'smooth' 
    });
}

// Копирование предложения
function copyProposal() {
    const proposalText = document.getElementById('proposalContent').textContent;
    
    navigator.clipboard.writeText(proposalText).then(() => {
        showNotification('Предложение скопировано в буфер обмена!', 'success');
    }).catch(() => {
        showNotification('Ошибка копирования', 'error');
    });
}

// Сохранение предложения
function saveProposal() {
    const proposalText = document.getElementById('proposalContent').textContent;
    const blob = new Blob([proposalText], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);
    
    const a = document.createElement('a');
    a.href = url;
    a.download = 'proposal.txt';
    a.click();
    
    URL.revokeObjectURL(url);
    showNotification('Предложение сохранено!', 'success');
}

// Генерация нового предложения
function generateNew() {
    document.getElementById('proposalForm').reset();
    document.getElementById('proposalResult').style.display = 'none';
    document.getElementById('proposalForm').scrollIntoView({ 
        behavior: 'smooth' 
    });
}

// Сохранение предложения в историю
function saveProposalToHistory(formData, proposal) {
    const history = JSON.parse(localStorage.getItem('proposalsHistory') || '[]');
    
    const proposalItem = {
        id: Date.now(),
        date: new Date().toISOString(),
        formData: formData,
        proposal: proposal
    };
    
    history.unshift(proposalItem);
    
    // Ограничиваем историю 50 предложениями
    if (history.length > 50) {
        history.splice(50);
    }
    
    localStorage.setItem('proposalsHistory', JSON.stringify(history));
    loadProposalsHistory();
}

// Загрузка истории предложений
function loadProposalsHistory() {
    const history = JSON.parse(localStorage.getItem('proposalsHistory') || '[]');
    const historyContainer = document.getElementById('proposalsHistory');
    
    if (history.length === 0) {
        historyContainer.innerHTML = '<p style="text-align: center; color: #718096;">История пуста</p>';
        return;
    }
    
    historyContainer.innerHTML = history.map(item => `
        <div class="proposal-item">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;">
                <strong>${item.formData.title}</strong>
                <small>${new Date(item.date).toLocaleDateString()}</small>
            </div>
            <div style="color: #718096; margin-bottom: 10px;">
                ${item.formData.specialization} • ${item.formData.budget} • ${item.formData.tone}
            </div>
            <div style="max-height: 100px; overflow: hidden; position: relative;">
                ${item.proposal.substring(0, 200)}...
                <div style="position: absolute; bottom: 0; right: 0; background: linear-gradient(transparent, white); width: 50px; height: 20px;"></div>
            </div>
            <button onclick="viewProposal(${item.id})" class="btn-secondary" style="margin-top: 10px;">Просмотреть</button>
        </div>
    `).join('');
}

// Просмотр предложения из истории
function viewProposal(id) {
    const history = JSON.parse(localStorage.getItem('proposalsHistory') || '[]');
    const item = history.find(h => h.id === id);
    
    if (item) {
        document.getElementById('proposalContent').textContent = item.proposal;
        document.getElementById('proposalResult').style.display = 'block';
        document.getElementById('proposalResult').scrollIntoView({ 
            behavior: 'smooth' 
        });
    }
}

// Показать модальное окно обновления
function showUpgradeModal() {
    document.getElementById('upgradeModal').style.display = 'flex';
}

// Закрыть модальное окно обновления
function closeUpgradeModal() {
    document.getElementById('upgradeModal').style.display = 'none';
}

// Начать подписку
async function startSubscription() {
    try {
        // Проверяем авторизацию
        const user = JSON.parse(localStorage.getItem('user'));
        if (!user) {
            showNotification('Сначала войдите в систему', 'error');
            return;
        }
        
        // Показываем выбор тарифа
        
        
    } catch (error) {
        showNotification('Ошибка создания подписки: ' + error.message, 'error');
    }
}

// Показать модальное окно с российскими тарифами
async function processPayment(planType, price) {
    try {
        showLoading(true);
        
        // Имитация обработки платежа
        await new Promise(resolve => setTimeout(resolve, 2000));
        
        // Активируем подписку
        currentUser.subscription = planType;
        currentUser.subscriptionExpires = new Date(Date.now() + 30 * 24 * 60 * 60 * 1000).toISOString();
        
        // Устанавливаем дневные лимиты
        const dailyLimits = {
            'premium': 50,
            'pro': 200,
            'enterprise': -1
        };
        currentUser.dailyRemaining = dailyLimits[planType];
        
        // Обновляем пользователя
        const users = JSON.parse(localStorage.getItem('users') || '[]');
        const userIndex = users.findIndex(u => u.email === currentUser.email);
        if (userIndex !== -1) {
            users[userIndex] = currentUser;
            localStorage.setItem('users', JSON.stringify(users));
        }
        
        localStorage.setItem('user', JSON.stringify(currentUser));
        updateSubscriptionStatus();
        
        // Закрываем модальное окно
        document.querySelector('.modal').remove();
        
        // Показываем уведомление об успехе
        showNotification(`Подписка ${planType.toUpperCase()} активирована!`, 'success');
        
        // Перенаправляем на страницу успеха
        setTimeout(() => {
            window.location.href = `payment_success.html?plan=${planType}`;
        }, 1000);
        
    } catch (error) {
        showNotification('Ошибка обработки платежа: ' + error.message, 'error');
    } finally {
        showLoading(false);
    }
}

// Управление подпиской
function manageSubscription() {
    if (currentUser && currentUser.subscription && currentUser.subscription !== 'free') {
        const subscriptionInfo = getSubscriptionInfo(currentUser.subscription);
        showNotification(`${subscriptionInfo.name} подписка активна!`, 'success');
        
        // Показываем модальное окно с информацией о подписке
        showSubscriptionInfoModal();
    } else {
        showNotification('У вас нет активной подписки', 'info');
    }
}

// Показать модальное окно с информацией о подписке
function showSubscriptionInfoModal() {
    const subscriptionInfo = getSubscriptionInfo(currentUser.subscription);
    
    const modal = document.createElement('div');
    modal.className = 'modal';
    modal.style.display = 'flex';
    modal.innerHTML = `
        <div class="modal-content max-w-2xl">
            <span class="close" onclick="this.parentElement.parentElement.remove()">&times;</span>
            <h2 class="text-2xl font-bold mb-6">Ваша ${subscriptionInfo.name} подписка</h2>
            <div class="subscription-info">
                <div class="bg-green-100 border border-green-400 text-green-700 px-4 py-3 rounded mb-6">
                    <h3 class="text-lg font-semibold">✅ Активна</h3>
                    <p>Ваша ${subscriptionInfo.name} подписка активна и предоставляет все преимущества:</p>
                </div>
                
                <div class="grid md:grid-cols-2 gap-6 mb-6">
                    <div class="bg-blue-50 p-4 rounded-lg">
                        <h4 class="font-semibold text-blue-800 mb-2">📊 Лимиты</h4>
                        <p class="text-blue-700">Дневной лимит: ${subscriptionInfo.dailyLimit === '∞' ? 'Безлимитно' : subscriptionInfo.dailyLimit + ' предложений'}</p>
                    </div>
                    
                    <div class="bg-purple-50 p-4 rounded-lg">
                        <h4 class="font-semibold text-purple-800 mb-2">🤖 AI Провайдер</h4>
                        <p class="text-purple-700">${subscriptionInfo.aiProvider}</p>
                    </div>
                </div>
                
                <div class="bg-gray-50 p-4 rounded-lg mb-6">
                    <h4 class="font-semibold text-gray-800 mb-2">🚀 Преимущества:</h4>
                    <ul class="space-y-2 text-gray-700">
                        <li class="flex items-center">
                            <span class="text-green-500 mr-2">✅</span>
                            ${subscriptionInfo.dailyLimit === '∞' ? 'Безлимитные предложения' : subscriptionInfo.dailyLimit + ' предложений в день'}
                        </li>
                        <li class="flex items-center">
                            <span class="text-green-500 mr-2">✅</span>
                            ${subscriptionInfo.aiProvider}
                        </li>
                        <li class="flex items-center">
                            <span class="text-green-500 mr-2">✅</span>
                            Премиум шаблоны
                        </li>
                        <li class="flex items-center">
                            <span class="text-green-500 mr-2">✅</span>
                            Экспорт предложений
                        </li>
                        <li class="flex items-center">
                            <span class="text-green-500 mr-2">✅</span>
                            Приоритетная поддержка
                        </li>
                        ${subscriptionInfo.name === 'Pro' || subscriptionInfo.name === 'Enterprise' ? `
                        <li class="flex items-center">
                            <span class="text-green-500 mr-2">✅</span>
                            Расширенная аналитика
                        </li>
                        ` : ''}
                        ${subscriptionInfo.name === 'Enterprise' ? `
                        <li class="flex items-center">
                            <span class="text-green-500 mr-2">✅</span>
                            API доступ
                        </li>
                        <li class="flex items-center">
                            <span class="text-green-500 mr-2">✅</span>
                            Персональная поддержка
                        </li>
                        ` : ''}
                    </ul>
                </div>
                
                <div class="flex gap-4">
                    <button onclick="this.parentElement.parentElement.remove()" class="flex-1 bg-blue-600 hover:bg-blue-700 text-white font-semibold py-3 px-6 rounded-lg transition duration-200">
                        Понятно
                    </button>
                    <button onclick="window.open('subscription_manager.html', '_blank')" class="flex-1 bg-gray-600 hover:bg-gray-700 text-white font-semibold py-3 px-6 rounded-lg transition duration-200">
                        Управление подпиской
                    </button>
                </div>
            </div>
        </div>
    `;
    document.body.appendChild(modal);
}

// Показать/скрыть загрузку
function showLoading(show) {
    document.getElementById('loading').style.display = show ? 'flex' : 'none';
}

// Показать уведомление
function showNotification(message, type = 'success') {
    const notification = document.createElement('div');
    notification.className = `notification ${type}`;
    notification.textContent = message;
    
    document.body.appendChild(notification);
    
    setTimeout(() => {
        notification.remove();
    }, 5000);
}

// Закрытие модального окна при клике вне его
window.onclick = function(event) {
    const modal = document.getElementById('upgradeModal');
    if (event.target === modal) {
        closeUpgradeModal();
    }
} 