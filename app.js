<<<<<<< HEAD
<<<<<<<< HEAD:app.js
// API Configuration - используем локальное хранилище для демо
const USE_LOCAL_STORAGE = true;
const APP_VERSION = '1.2.0'; // Версия для обновления кэша
========
// API Configuration
const API_BASE = "http://localhost:8000/api/v1"; // Для работы нужно запустить локальный сервер


// Проверка подключения к API
async function checkApiConnection() {
    try {
        const response = await fetch(`${API_BASE.replace("/api/v1", "")}/health`);
        if (response.ok) {
            console.log("✅ API сервер доступен");
            return true;
        }
    } catch (error) {
        console.log("❌ API сервер недоступен");
        showApiError();
        return false;
    }
}

// Показать ошибку подключения к API
function showApiError() {
    const errorDiv = document.createElement("div");
    errorDiv.innerHTML = `
        <div style="background: #fee; border: 1px solid #fcc; padding: 20px; margin: 20px; border-radius: 8px; text-align: center;">
            <h3 style="color: #c33; margin: 0 0 15px 0;">🚫 Сервер недоступен</h3>
            <p style="margin: 0 0 15px 0;">Для работы сайта нужно запустить локальный сервер:</p>
            <div style="background: #f5f5f5; padding: 15px; border-radius: 5px; font-family: monospace; text-align: left;">
                <p style="margin: 5px 0;"><strong>1.</strong> Откройте терминал</p>
                <p style="margin: 5px 0;"><strong>2.</strong> Перейдите в папку проекта</p>
                <p style="margin: 5px 0;"><strong>3.</strong> Выполните: <code>python3 quick_start.py</code></p>
                <p style="margin: 5px 0;"><strong>4.</strong> Откройте: <a href="http://localhost:3000" target="_blank">http://localhost:3000</a></p>
            </div>
        </div>
    `;
    document.body.insertBefore(errorDiv, document.body.firstChild);
}
>>>>>>>> main:frontend/app.js

// State management
let currentUser = null;
let authToken = localStorage.getItem('authToken');

// DOM Elements
const elements = {
    // Sections
    hero: document.querySelector('.hero'),
    authSection: document.getElementById('authSection'),
    loginForm: document.getElementById('loginForm'),
    registerForm: document.getElementById('registerForm'),
    proposalSection: document.getElementById('proposalSection'),
    dashboardSection: document.getElementById('dashboardSection'),
    
    // Buttons
    loginBtn: document.getElementById('loginBtn'),
    registerBtn: document.getElementById('registerBtn'),
    startBtn: document.getElementById('startBtn'),
    logoutBtn: document.getElementById('logoutBtn'),
    generateNewBtn: document.getElementById('generateNewBtn'),
    viewHistoryBtn: document.getElementById('viewHistoryBtn'),
    copyBtn: document.getElementById('copyBtn'),
    newProposalBtn: document.getElementById('newProposalBtn'),
    
    // Forms
    loginFormElement: document.getElementById('loginFormElement'),
    registerFormElement: document.getElementById('registerFormElement'),
    proposalForm: document.getElementById('proposalForm'),
    
    // Results
    proposalResult: document.getElementById('proposalResult'),
    proposalText: document.getElementById('proposalText'),
    loading: document.getElementById('loading'),
    
    // User info
    userName: document.getElementById('userName'),
    userEmail: document.getElementById('userEmail'),
    userSpecialization: document.getElementById('userSpecialization')
};

// Utility functions
function showNotification(message, type = 'success') {
    const notifications = document.getElementById('notifications');
=======
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
    
    const proposal = `Dear Client,

I've reviewed your project "${title}" and I'm excited about the opportunity to work with you. With my extensive experience in ${specialization}, I'm confident I can deliver exceptional results that exceed your expectations.

**Why I'm the right fit for your project:**

✅ **Proven Expertise**: I have successfully completed 50+ similar projects with 5-star ratings
✅ **Quality Assurance**: Every deliverable goes through rigorous testing and review
✅ **Clear Communication**: Regular updates and transparent project management
✅ **On-time Delivery**: 100% on-time completion rate with all my clients

**My approach to your project:**
1. Detailed analysis of requirements and objectives
2. Custom solution design tailored to your specific needs
3. Iterative development with regular feedback cycles
4. Thorough testing and quality assurance
5. Comprehensive documentation and support

**Budget**: I can work within your ${budget} budget while ensuring top-quality results.

**Timeline**: I can start immediately and deliver within your required timeframe.

I'm ready to begin working on your project right away. Let's discuss the details and get started!

Best regards,
[Your Name]
Freelance ${specialization} Expert

P.S. I'm available for a quick call to discuss your project in detail.`;
    
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
>>>>>>> main
    const notification = document.createElement('div');
    notification.className = `notification ${type}`;
    notification.textContent = message;
    
<<<<<<< HEAD
    notifications.appendChild(notification);
=======
    document.body.appendChild(notification);
>>>>>>> main
    
    setTimeout(() => {
        notification.remove();
    }, 5000);
}

<<<<<<< HEAD
function showSection(section) {
    // Hide all sections
    elements.hero.style.display = 'none';
    elements.authSection.style.display = 'none';
    elements.proposalSection.style.display = 'none';
    elements.dashboardSection.style.display = 'none';
    
    // Show target section
    if (section === 'hero') {
        elements.hero.style.display = 'block';
    } else if (section === 'auth') {
        elements.authSection.style.display = 'block';
    } else if (section === 'proposal') {
        elements.proposalSection.style.display = 'block';
    } else if (section === 'dashboard') {
        elements.dashboardSection.style.display = 'block';
    }
}

function showAuthForm(form) {
    elements.loginForm.style.display = 'none';
    elements.registerForm.style.display = 'none';
    
    if (form === 'login') {
        elements.loginForm.style.display = 'block';
    } else if (form === 'register') {
        elements.registerForm.style.display = 'block';
    }
}

function updateUserInfo(user) {
    currentUser = user;
    elements.userName.textContent = `${user.first_name} ${user.last_name}`;
    elements.userEmail.textContent = user.email;
    elements.userSpecialization.textContent = user.specialization || 'Не указано';
}

// API functions - локальная версия для демонстрации
async function apiRequest(endpoint, options = {}) {
    if (USE_LOCAL_STORAGE) {
        // Имитируем API задержку
        await new Promise(resolve => setTimeout(resolve, 500));
        
        const url = endpoint;
        
        if (url === '/auth/register') {
            const userData = JSON.parse(options.body);
            
            // Проверяем, что пользователь не существует
            const users = JSON.parse(localStorage.getItem('users') || '[]');
            if (users.find(u => u.email === userData.email)) {
                throw new Error('Пользователь с таким email уже существует');
            }
            
            // Создаем нового пользователя
            const newUser = {
                id: Date.now(),
                ...userData,
                created_at: new Date().toISOString()
            };
            
            users.push(newUser);
            localStorage.setItem('users', JSON.stringify(users));
            
            return { message: 'Регистрация успешна' };
            
        } else if (url === '/auth/login-json') {
            const { email, password } = JSON.parse(options.body);
            
            // Проверяем пользователя
            const users = JSON.parse(localStorage.getItem('users') || '[]');
            const user = users.find(u => u.email === email && u.password === password);
            
            if (!user) {
                throw new Error('Неверный email или пароль');
            }
            
            // Создаем токен и сохраняем информацию о пользователе
            const token = 'demo_token_' + Date.now();
            localStorage.setItem('currentUser', JSON.stringify({ ...user, password: undefined }));
            
            return { 
                access_token: token,
                user: { ...user, password: undefined }
            };
            
        } else if (url === '/auth/me') {
            console.log('Getting current user...');
            console.log('Auth token:', authToken);
            
            if (!authToken) {
                console.error('No auth token found');
                throw new Error('Не авторизован');
            }
            
            // Сохраняем информацию о пользователе в токене
            const userInfo = localStorage.getItem('currentUser');
            console.log('User info from localStorage:', userInfo);
            
            if (!userInfo) {
                console.error('No currentUser found in localStorage');
                throw new Error('Пользователь не найден');
            }
            
            const user = JSON.parse(userInfo);
            console.log('Parsed user:', user);
            return { ...user, password: undefined };
            
        } else if (url === '/proposals/generate') {
            if (!authToken) {
                throw new Error('Не авторизован');
            }
            
            const proposalData = JSON.parse(options.body);
            
            // Генерируем демо предложение
            const demoProposal = generateDemoProposal(proposalData);
            
            // Сохраняем в историю
            const proposals = JSON.parse(localStorage.getItem('proposals') || '[]');
            proposals.push({
                id: Date.now(),
                user_id: parseInt(authToken.split('_')[2]),
                ...proposalData,
                content: demoProposal,
                created_at: new Date().toISOString()
            });
            localStorage.setItem('proposals', JSON.stringify(proposals));
            
            return { content: demoProposal };
        }
        
        throw new Error('Неизвестный endpoint');
    } else {
        // Оригинальный API код
        const url = `${API_BASE}${endpoint}`;
        const config = {
            headers: {
                'Content-Type': 'application/json',
                ...(authToken && { 'Authorization': `Bearer ${authToken}` })
            },
            ...options
        };
        
        const response = await fetch(url, config);
        
        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || 'API Error');
        }
        
        return await response.json();
    }
}

// Функция для генерации демо предложений
function generateDemoProposal(data) {
    const templates = {
        'профессиональный': `Уважаемый клиент!

Я внимательно изучил ваш проект "${data.project_description}" и готов предложить профессиональное решение.

**Мой опыт:**
- ${data.experience_level} опыта в ${data.specialization}
- Более 50 успешных проектов
- 100% положительных отзывов

**Мой подход к вашему проекту:**
1. Детальный анализ требований
2. Создание технического плана
3. Поэтапная разработка с регулярными обновлениями
4. Тестирование и оптимизация
5. Поддержка после запуска

**Почему выбирают меня:**
✅ Соблюдение сроков
✅ Качественный код
✅ Прозрачная коммуникация
✅ Гибкость в изменениях

Бюджет: ${data.budget_range}

Готов обсудить детали и начать работу немедленно!

С уважением,
[Ваше имя]`,

        'дружелюбный': `Привет! 👋

Очень заинтересовался твоим проектом "${data.project_description}"! 

**Что я могу предложить:**
🎯 ${data.experience_level} опыта в ${data.specialization}
🚀 Быстрая и качественная работа
💬 Постоянная связь и обновления
🎨 Современные технологии и подходы

**Мой план работы:**
1. Обсуждение деталей проекта
2. Создание макета/прототипа
3. Разработка с показом промежуточных результатов
4. Финальная доработка и тестирование

Бюджет: ${data.budget_range}

Давай обсудим детали! Буду рад ответить на все вопросы 😊

До связи!`,

        'креативный': `🌟 ВАУ! Отличный проект! 🌟

"${data.project_description}" - это именно то, что я люблю создавать!

**Мой креативный подход:**
✨ Уникальные решения для каждой задачи
🎨 Современный дизайн и UX
⚡ Быстрая и эффективная разработка
🎯 Фокус на результатах

**Что вы получите:**
- ${data.experience_level} опыта в ${data.specialization}
- Инновационные решения
- Полную поддержку
- Прозрачность процесса

**Мой процесс:**
1. 🧠 Мозговой штурм идей
2. 📝 Детальное планирование
3. 🚀 Быстрая реализация
4. 🎯 Тестирование и оптимизация

Бюджет: ${data.budget_range}

Готов создать что-то потрясающее! 🚀

Давайте начнем прямо сейчас! ✨`
    };
    
    const tone = data.tone || 'профессиональный';
    return templates[tone] || templates['профессиональный'];
}

// API функции
async function register(userData) {
    return await apiRequest('/auth/register', {
        method: 'POST',
        body: JSON.stringify(userData)
    });
}

async function login(email, password) {
    const data = await apiRequest('/auth/login-json', {
        method: 'POST',
        body: JSON.stringify({ email, password })
    });
    
    authToken = data.access_token;
    localStorage.setItem('authToken', authToken);
    return data;
}

async function getCurrentUser() {
    return await apiRequest('/auth/me');
}

async function generateProposal(proposalData) {
    return await apiRequest('/proposals/generate', {
        method: 'POST',
        body: JSON.stringify(proposalData)
    });
}

// Event handlers
elements.loginBtn.addEventListener('click', () => {
    showSection('auth');
    showAuthForm('login');
});

elements.registerBtn.addEventListener('click', () => {
    showSection('auth');
    showAuthForm('register');
});

elements.startBtn.addEventListener('click', () => {
    if (authToken) {
        showSection('proposal');
    } else {
        showSection('auth');
        showAuthForm('register');
    }
});

elements.logoutBtn.addEventListener('click', () => {
    authToken = null;
    currentUser = null;
    localStorage.removeItem('authToken');
    localStorage.removeItem('currentUser');
    showSection('hero');
    showNotification('Вы вышли из системы');
});

elements.generateNewBtn.addEventListener('click', () => {
    showSection('proposal');
});

elements.viewHistoryBtn.addEventListener('click', () => {
    showNotification('Функция истории предложений будет добавлена в следующей версии');
});

elements.copyBtn.addEventListener('click', () => {
    const text = elements.proposalText.textContent;
    navigator.clipboard.writeText(text).then(() => {
        showNotification('Предложение скопировано в буфер обмена');
    });
});

elements.newProposalBtn.addEventListener('click', () => {
    elements.proposalResult.style.display = 'none';
    elements.proposalForm.reset();
});

// Form submissions
elements.loginFormElement.addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const email = document.getElementById('loginEmail').value;
    const password = document.getElementById('loginPassword').value;
    
    console.log('Login attempt:', { email, password });
    console.log('App version:', APP_VERSION);
    
    try {
        console.log('Calling login function...');
        await login(email, password);
        console.log('Login successful, getting current user...');
        const user = await getCurrentUser();
        console.log('Current user retrieved:', user);
        updateUserInfo(user);
        showSection('dashboard');
        showNotification('Вход выполнен успешно');
    } catch (error) {
        console.error('Login error:', error);
        showNotification(error.message, 'error');
    }
});

elements.registerFormElement.addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const userData = {
        email: document.getElementById('registerEmail').value,
        password: document.getElementById('registerPassword').value,
        first_name: document.getElementById('firstName').value,
        last_name: document.getElementById('lastName').value,
        specialization: document.getElementById('specialization').value,
        experience_level: document.getElementById('experienceLevel').value
    };
    
    try {
        await register(userData);
        showNotification('Регистрация выполнена успешно! Теперь войдите в систему');
        showAuthForm('login');
    } catch (error) {
        showNotification(error.message, 'error');
    }
});

elements.proposalForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const proposalData = {
        project_description: document.getElementById('projectDescription').value,
        budget_range: document.getElementById('budgetRange').value,
        specialization: document.getElementById('proposalSpecialization').value,
        experience_level: currentUser?.experience_level || '3-5 лет',
        key_requirements: document.getElementById('keyRequirements').value,
        tone: document.getElementById('tone').value
    };
    
    try {
        elements.loading.style.display = 'block';
        elements.proposalResult.style.display = 'none';
        
        const result = await generateProposal(proposalData);
        
        elements.proposalText.textContent = result.content;
        elements.proposalResult.style.display = 'block';
        elements.loading.style.display = 'none';
        
        showNotification('Предложение сгенерировано успешно!');
    } catch (error) {
        elements.loading.style.display = 'none';
        showNotification(error.message, 'error');
    }
});

// Auth form switching
document.getElementById('showRegister').addEventListener('click', (e) => {
    e.preventDefault();
    showAuthForm('register');
});

document.getElementById('showLogin').addEventListener('click', (e) => {
    e.preventDefault();
    showAuthForm('login');
});

// Auto-fill user data in proposal form
function fillUserData() {
    if (currentUser) {
        document.getElementById('proposalSpecialization').value = currentUser.specialization || '';
    }
}

// Initialize app
async function initApp() {
    if (authToken) {
    // Проверяем подключение к API
    await checkApiConnection();

        try {
            const user = await getCurrentUser();
            updateUserInfo(user);
            showSection('dashboard');
        } catch (error) {
            // Token is invalid, remove it
            authToken = null;
            localStorage.removeItem('authToken');
            showSection('hero');
        }
    } else {
        showSection('hero');
    }
}

// Start the app
document.addEventListener('DOMContentLoaded', initApp);

// Add some demo data for testing
function addDemoData() {
    // Auto-fill demo data for testing
    if (window.location.search.includes('demo=true')) {
        document.getElementById('projectDescription').value = 'Нужен разработчик для создания интернет-магазина на WordPress с интеграцией платежных систем. Требуется современный дизайн и адаптивная верстка.';
        document.getElementById('budgetRange').value = '$1000-5000';
        document.getElementById('proposalSpecialization').value = 'Веб-разработка';
        document.getElementById('keyRequirements').value = 'WordPress, WooCommerce, PHP, JavaScript';
        document.getElementById('tone').value = 'профессиональный';
    }
}

// Add demo data if needed
addDemoData(); 
=======
// Закрытие модального окна при клике вне его
window.onclick = function(event) {
    const modal = document.getElementById('upgradeModal');
    if (event.target === modal) {
        closeUpgradeModal();
    }
} 
>>>>>>> main
