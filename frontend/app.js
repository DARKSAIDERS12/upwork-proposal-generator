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

// API functions
async function apiRequest(endpoint, options = {}) {
    const url = `${API_BASE}${endpoint}`;
    const config = {
        headers: {
            'Content-Type': 'application/json',
            ...options.headers
        },
        ...options
    };
    
    if (authToken) {
        config.headers.Authorization = `Bearer ${authToken}`;
    }
    
    try {
        const response = await fetch(url, config);
        const data = await response.json();
        
        if (!response.ok) {
            throw new Error(data.detail || 'Произошла ошибка');
        }
        
        return data;
    } catch (error) {
        console.error('API Error:', error);
        throw error;
    }
}

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
    
    try {
        await login(email, password);
        const user = await getCurrentUser();
        updateUserInfo(user);
        showSection('dashboard');
        showNotification('Вход выполнен успешно');
    } catch (error) {
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