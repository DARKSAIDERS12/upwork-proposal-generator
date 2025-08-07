// API Configuration - используем локальное хранилище для демо
const USE_LOCAL_STORAGE = true;
const APP_VERSION = '1.2.0'; // Версия для обновления кэша

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
    const notification = document.createElement('div');
    notification.className = `notification ${type}`;
    notification.textContent = message;
    
    notifications.appendChild(notification);
    
    setTimeout(() => {
        notification.remove();
    }, 5000);
}

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