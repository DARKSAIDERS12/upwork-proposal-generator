// Глобальные переменные
let currentUser = null;
let stripe = null;

// Инициализация Stripe
function initStripe() {
    const publishableKey = 'pk_test_your_stripe_publishable_key'; // Замените на ваш ключ
    if (publishableKey !== 'pk_test_your_stripe_publishable_key') {
        stripe = Stripe(publishableKey);
    }
}

// Инициализация приложения
document.addEventListener('DOMContentLoaded', function() {
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
    
    // Инициализируем русскую премиум систему
    initializeRussianPremiumAI();
}

// Проверка и сброс ежедневных лимитов
function checkAndResetDailyLimits() {
    const users = JSON.parse(localStorage.getItem('users') || '[]');
    const today = new Date().toDateString();
    
    users.forEach(user => {
        if (user.lastResetDate !== today) {
            user.dailyRemaining = user.subscription === 'free' ? 3 : 999;
            user.lastResetDate = today;
        }
    });
    
    localStorage.setItem('users', JSON.stringify(users));
    
    // Обновляем текущего пользователя если он залогинен
    if (currentUser) {
        const updatedUser = users.find(u => u.email === currentUser.email);
        if (updatedUser) {
            currentUser = updatedUser;
            localStorage.setItem('user', JSON.stringify(currentUser));
            updateSubscriptionStatus();
        }
    }
}

// Проверка статуса аутентификации
function checkAuthStatus() {
    const user = JSON.parse(localStorage.getItem('user'));
    if (user) {
        currentUser = user;
        showMainApp();
        updateSubscriptionStatus();
    } else {
        showAuthForms();
    }
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
        // Получаем существующих пользователей
        const users = JSON.parse(localStorage.getItem('users') || '[]');
        
        // Проверяем, не существует ли уже пользователь с таким email
        if (users.find(u => u.email === email)) {
            showNotification('Пользователь с таким email уже существует', 'error');
            return;
        }
        
        // Создаем нового пользователя
        const user = {
            id: Date.now(),
            email: email,
            password: password, // В реальном приложении пароль должен быть захеширован
            subscription: 'free',
            dailyProposals: 3,
            dailyRemaining: 3,
            lastResetDate: new Date().toDateString(),
            createdAt: new Date().toISOString()
        };
        
        // Добавляем пользователя в список
        users.push(user);
        localStorage.setItem('users', JSON.stringify(users));
        
        // Устанавливаем текущего пользователя
        currentUser = user;
        localStorage.setItem('user', JSON.stringify(user));
        
        showMainApp();
        updateSubscriptionStatus();
        showNotification('Регистрация успешна!', 'success');
        
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
        // Получаем пользователей
        const users = JSON.parse(localStorage.getItem('users') || '[]');
        const user = users.find(u => u.email === email && u.password === password);
        
        if (user) {
            currentUser = user;
            localStorage.setItem('user', JSON.stringify(user));
            showMainApp();
            updateSubscriptionStatus();
            showNotification('Вход выполнен успешно!', 'success');
        } else {
            showNotification('Неверный email или пароль', 'error');
        }
        
    } catch (error) {
        showNotification('Ошибка входа: ' + error.message, 'error');
    }
}

// Выход пользователя
function logout() {
    currentUser = null;
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
    
    if (currentUser.subscription === 'premium') {
        subscriptionType.textContent = 'Premium';
        dailyRemaining.textContent = 'Неограниченно';
        upgradeBtn.textContent = 'Управлять подпиской';
        upgradeBtn.onclick = manageSubscription;
    } else {
        subscriptionType.textContent = 'Бесплатная';
        dailyRemaining.textContent = `Осталось: ${currentUser.dailyRemaining} предложений`;
        upgradeBtn.textContent = 'Обновить до Premium';
        upgradeBtn.onclick = showUpgradeModal;
    }
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
        // Для демо-версии обновляем статус вручную
        currentUser.subscription = 'premium';
        currentUser.dailyRemaining = 999; // Неограниченно для premium
        
        // Обновляем пользователя в списке
        const users = JSON.parse(localStorage.getItem('users') || '[]');
        const userIndex = users.findIndex(u => u.email === currentUser.email);
        if (userIndex !== -1) {
            users[userIndex] = currentUser;
            localStorage.setItem('users', JSON.stringify(users));
        }
        
        localStorage.setItem('user', JSON.stringify(currentUser));
        updateSubscriptionStatus();
        closeUpgradeModal();
        
        showNotification('Подписка Premium активирована! Теперь у вас неограниченный доступ.', 'success');
        
    } catch (error) {
        showNotification('Ошибка создания подписки: ' + error.message, 'error');
    }
}

// Управление подпиской
function manageSubscription() {
    if (currentUser && currentUser.subscription === 'premium') {
        const message = `Ваша Premium подписка активна!\n\nПреимущества:\n✅ Неограниченные предложения\n✅ Продвинутый AI\n✅ Приоритетная поддержка\n✅ Экспорт предложений`;
        showNotification('Premium подписка активна!', 'success');
        
        // Показываем модальное окно с информацией о подписке
        showSubscriptionInfoModal();
    } else {
        showNotification('У вас нет активной Premium подписки', 'info');
    }
}

// Показать модальное окно с информацией о подписке
function showSubscriptionInfoModal() {
    const modal = document.createElement('div');
    modal.className = 'modal';
    modal.style.display = 'flex';
    modal.innerHTML = `
        <div class="modal-content">
            <span class="close" onclick="this.parentElement.parentElement.remove()">&times;</span>
            <h2>Ваша Premium подписка</h2>
            <div class="subscription-info">
                <h3>✅ Активна</h3>
                <p>Ваша Premium подписка активна и предоставляет все преимущества:</p>
                <ul>
                    <li>🚀 Неограниченные предложения</li>
                    <li>🤖 Продвинутый AI (Yandex GPT/GigaChat)</li>
                    <li>⚡ Приоритетная поддержка</li>
                    <li>📤 Экспорт предложений</li>
                    <li>📊 Расширенная аналитика</li>
                </ul>
                <button onclick="this.parentElement.parentElement.remove()" class="btn-primary">Понятно</button>
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

// ===============================
// РУССКАЯ ПРЕМИУМ AI СИСТЕМА
// ===============================

// Инициализация русской премиум AI системы
function initializeRussianPremiumAI() {
    console.log('🇷🇺 Инициализация русской премиум AI системы...');
    
    // Проверяем, настроен ли Yandex GPT API
    checkYandexGPTSetup();
    
    // Обновляем интерфейс в зависимости от подписки
    updatePremiumInterface();
}

// Проверка настройки Yandex GPT
function checkYandexGPTSetup() {
    const yandexApiKey = localStorage.getItem('yandex_api_key');
    const setupStatus = localStorage.getItem('yandex_setup_status');
    
    if (!yandexApiKey || yandexApiKey === 'your-yandex-api-key-here') {
        console.log('⚠️ Yandex GPT не настроен');
        showYandexSetupNotification();
    } else {
        console.log('✅ Yandex GPT настроен');
    }
}

// Показать уведомление о настройке Yandex GPT
function showYandexSetupNotification() {
    const notification = document.createElement('div');
    notification.className = 'premium-notification';
    notification.innerHTML = `
        <div style="background: linear-gradient(135deg, #3498db, #2980b9); 
                    color: white; padding: 15px; border-radius: 10px; 
                    margin: 10px; position: fixed; top: 20px; right: 20px; 
                    z-index: 1000; box-shadow: 0 5px 15px rgba(0,0,0,0.2);">
            <h4 style="margin: 0 0 10px 0;">🇷🇺 Настройте Yandex GPT для премиум функций!</h4>
            <p style="margin: 0 0 10px 0;">Получите доступ к высококачественной генерации предложений</p>
            <button onclick="openSubscriptionManager()" 
                    style="background: white; color: #3498db; border: none; 
                           padding: 8px 16px; border-radius: 5px; cursor: pointer; 
                           font-weight: bold;">
                Настроить сейчас
            </button>
            <button onclick="this.parentElement.parentElement.remove()" 
                    style="background: transparent; color: white; border: 1px solid white; 
                           padding: 8px 16px; border-radius: 5px; cursor: pointer; 
                           margin-left: 10px;">
                Позже
            </button>
        </div>
    `;
    
    document.body.appendChild(notification);
    
    // Автоматически скрываем через 10 секунд
    setTimeout(() => {
        if (notification.parentElement) {
            notification.remove();
        }
    }, 10000);
}

// Открыть менеджер подписок
function openSubscriptionManager() {
    window.open('subscription_manager.html', '_blank');
}

// Обновление премиум интерфейса
function updatePremiumInterface() {
    if (!currentUser) return;
    
    const subscriptionType = currentUser.subscription || 'free';
    const isFreeTier = subscriptionType === 'free';
    
    // Обновляем статус подписки в интерфейсе
    updateSubscriptionStatusInUI(subscriptionType);
    
    // Показываем премиум функции для платных пользователей
    showPremiumFeatures(!isFreeTier);
}

// Обновление статуса подписки в UI
function updateSubscriptionStatusInUI(subscriptionType) {
    const subscriptionInfo = document.getElementById('subscriptionInfo');
    if (subscriptionInfo) {
        const subscriptionNames = {
            'free': 'Бесплатный',
            'premium': 'Премиум (Yandex GPT)',
            'pro': 'Профессиональный',
            'enterprise': 'Корпоративный'
        };
        
        const aiProviders = {
            'free': 'Демо',
            'premium': 'Yandex GPT',
            'pro': 'Yandex GPT + GigaChat',
            'enterprise': 'Все AI провайдеры'
        };
        
        subscriptionInfo.innerHTML = `
            <div style="padding: 10px; background: #f8f9fa; border-radius: 5px; margin: 10px 0;">
                <strong>План:</strong> ${subscriptionNames[subscriptionType] || subscriptionType}
                <br>
                <strong>AI:</strong> ${aiProviders[subscriptionType] || 'Демо'}
                <br>
                <strong>Остается сегодня:</strong> ${currentUser.dailyRemaining || 0}
                ${subscriptionType === 'free' ? 
                    '<br><button onclick="openSubscriptionManager()" style="margin-top: 5px; background: #3498db; color: white; border: none; padding: 5px 10px; border-radius: 3px; cursor: pointer;">Улучшить план</button>' 
                    : ''}
            </div>
        `;
    }
}

// Показать премиум функции
function showPremiumFeatures(isPremium) {
    const premiumElements = document.querySelectorAll('.premium-feature');
    premiumElements.forEach(element => {
        element.style.display = isPremium ? 'block' : 'none';
    });
    
    // Добавляем индикаторы премиум функций
    if (isPremium) {
        addPremiumIndicators();
    }
}

// Добавить индикаторы премиум функций
function addPremiumIndicators() {
    const generateBtn = document.querySelector('#generateBtn');
    if (generateBtn && !generateBtn.querySelector('.premium-badge')) {
        const badge = document.createElement('span');
        badge.className = 'premium-badge';
        badge.innerHTML = '🚀 Yandex GPT';
        badge.style.cssText = `
            background: #27ae60; 
            color: white; 
            font-size: 0.7em; 
            padding: 2px 6px; 
            border-radius: 10px; 
            margin-left: 5px;
        `;
        generateBtn.appendChild(badge);
    }
}

// Генерация предложения с русской премиум AI
async function generateProposalWithRussianAI(projectData) {
    const subscriptionType = currentUser?.subscription || 'free';
    
    // Проверяем лимиты
    if (!canGenerateProposal()) {
        showUpgradeModal();
        return null;
    }
    
    // Показываем индикатор загрузки
    showLoadingIndicator(subscriptionType);
    
    try {
        // Для бесплатного плана используем демо-генерацию
        if (subscriptionType === 'free') {
            return await generateDemoProposal(projectData);
        }
        
        // Для премиум планов пытаемся использовать Yandex GPT
        const yandexApiKey = localStorage.getItem('yandex_api_key');
        if (yandexApiKey && yandexApiKey !== 'your-yandex-api-key-here') {
            return await generateYandexGPTProposal(projectData, yandexApiKey);
        } else {
            // Fallback к демо если API ключ не настроен
            showNotification('⚠️ Yandex GPT не настроен. Используется демо-режим.', 'warning');
            return await generateDemoProposal(projectData);
        }
        
    } catch (error) {
        console.error('Ошибка генерации:', error);
        showNotification('❌ Ошибка генерации предложения', 'error');
        return null;
    } finally {
        hideLoadingIndicator();
    }
}

// Показать индикатор загрузки с информацией о AI
function showLoadingIndicator(subscriptionType) {
    const aiProviders = {
        'free': 'Демо-генерация',
        'premium': 'Yandex GPT генерирует предложение...',
        'pro': 'Yandex GPT генерирует предложение...',
        'enterprise': 'AI генерирует предложение...'
    };
    
    const loadingText = aiProviders[subscriptionType] || 'Генерация предложения...';
    
    const existingLoader = document.querySelector('.loading-indicator');
    if (existingLoader) {
        existingLoader.querySelector('.loading-text').textContent = loadingText;
    } else {
        const loader = document.createElement('div');
        loader.className = 'loading-indicator';
        loader.innerHTML = `
            <div style="position: fixed; top: 50%; left: 50%; transform: translate(-50%, -50%);
                        background: white; padding: 30px; border-radius: 10px; 
                        box-shadow: 0 10px 30px rgba(0,0,0,0.3); z-index: 2000;
                        text-align: center;">
                <div class="spinner" style="width: 40px; height: 40px; border: 4px solid #f3f3f3;
                                          border-top: 4px solid #3498db; border-radius: 50%;
                                          animation: spin 1s linear infinite; margin: 0 auto 15px;"></div>
                <div class="loading-text">${loadingText}</div>
            </div>
            <style>
                @keyframes spin { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }
            </style>
        `;
        document.body.appendChild(loader);
    }
}

// Скрыть индикатор загрузки
function hideLoadingIndicator() {
    const loader = document.querySelector('.loading-indicator');
    if (loader) {
        loader.remove();
    }
}

// Генерация с помощью Yandex GPT
async function generateYandexGPTProposal(projectData, apiKey) {
    // Создаем промпт для Yandex GPT
    const prompt = createYandexGPTPrompt(projectData);
    
    // Симуляция запроса к Yandex GPT (в реальности это будет запрос к backend)
    await new Promise(resolve => setTimeout(resolve, 2000)); // Имитация задержки
    
    // Возвращаем сгенерированное предложение
    return `[🚀 Сгенерировано с помощью Yandex GPT]

Здравствуйте!

Меня заинтересовал ваш проект "${projectData.title}". 

Как опытный специалист в области ${projectData.specialization.toLowerCase()}, я готов реализовать высококачественное решение в рамках вашего бюджета ${projectData.budget}.

Основываясь на описании: "${projectData.description}", я предлагаю следующий подход:

1. Детальный анализ требований и технических особенностей
2. Разработка архитектуры решения с учетом современных стандартов
3. Поэтапная реализация с регулярной обратной связью
4. Тестирование и оптимизация производительности
5. Передача готового проекта с документацией

Мой опыт включает работу с современными технологиями и успешную реализацию аналогичных проектов. Готов предоставить портфолио и обсудить детали в удобное для вас время.

Предлагаю начать с детального обсуждения технических требований. Уверен, что смогу превзойти ваши ожидания!

С уважением,
[Ваше имя]

P.S. Готов предоставить дополнительные примеры работ и рекомендации от предыдущих клиентов.`;
}

// Создание промпта для Yandex GPT
function createYandexGPTPrompt(projectData) {
    return `Создай профессиональное предложение для фриланс-проекта на Upwork.

Данные проекта:
- Название: ${projectData.title}
- Описание: ${projectData.description}  
- Бюджет: ${projectData.budget}
- Специализация: ${projectData.specialization}
- Тон: ${projectData.tone}

Требования к предложению:
- Профессиональный тон общения
- Демонстрация экспертизы в области
- Конкретный план работы
- Упоминание опыта и портфолио
- Призыв к действию
- Длина: 200-300 слов

Предложение должно быть написано на русском языке и адаптировано для российского рынка фриланса.`;
}

// Настройка Yandex GPT API ключа
function setupYandexGPTAPI() {
    const apiKey = prompt('Введите ваш Yandex GPT API ключ:');
    if (apiKey && apiKey.trim() !== '') {
        localStorage.setItem('yandex_api_key', apiKey.trim());
        localStorage.setItem('yandex_setup_status', 'configured');
        
        showNotification('✅ Yandex GPT успешно настроен!', 'success');
        updatePremiumInterface();
        
        // Скрываем уведомления о настройке
        const notifications = document.querySelectorAll('.premium-notification');
        notifications.forEach(n => n.remove());
    }
}

// Проверка возможности генерации с учетом русской системы
function canGenerateProposalRussian() {
    if (!currentUser) return false;
    
    const subscriptionType = currentUser.subscription || 'free';
    const dailyLimits = {
        'free': 3,
        'premium': 50,
        'pro': 200,
        'enterprise': -1 // Unlimited
    };
    
    const dailyLimit = dailyLimits[subscriptionType] || 3;
    const remaining = currentUser.dailyRemaining || 0;
    
    if (dailyLimit === -1) return true; // Unlimited
    return remaining > 0;
} 