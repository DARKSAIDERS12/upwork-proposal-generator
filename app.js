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
});

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
        // В реальном приложении здесь был бы запрос к API
        const user = {
            id: Date.now(),
            email: email,
            subscription: 'free',
            dailyProposals: 3,
            dailyRemaining: 3
        };
        
        localStorage.setItem('user', JSON.stringify(user));
        currentUser = user;
        
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
        // В реальном приложении здесь был бы запрос к API
        const user = {
            id: Date.now(),
            email: email,
            subscription: 'free',
            dailyProposals: 3,
            dailyRemaining: 3
        };
        
        localStorage.setItem('user', JSON.stringify(user));
        currentUser = user;
        
        showMainApp();
        updateSubscriptionStatus();
        showNotification('Вход выполнен успешно!', 'success');
        
    } catch (error) {
        showNotification('Ошибка входа: ' + error.message, 'error');
    }
}

// Выход пользователя
function logout() {
    localStorage.removeItem('user');
    currentUser = null;
    showAuthForms();
    showNotification('Вы вышли из системы', 'success');
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
    if (!stripe) {
        showNotification('Stripe не настроен. Обратитесь к администратору.', 'error');
        return;
    }
    
    try {
        // В реальном приложении здесь был бы запрос к backend для создания сессии
        showNotification('Функция оплаты в разработке. Для тестирования обновите статус вручную.', 'success');
        
        // Для демо-версии обновляем статус вручную
        currentUser.subscription = 'premium';
        localStorage.setItem('user', JSON.stringify(currentUser));
        updateSubscriptionStatus();
        closeUpgradeModal();
        
    } catch (error) {
        showNotification('Ошибка создания подписки: ' + error.message, 'error');
    }
}

// Управление подпиской
function manageSubscription() {
    showNotification('Функция управления подпиской в разработке', 'info');
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