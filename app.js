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