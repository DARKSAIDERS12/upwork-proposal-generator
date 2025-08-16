// ========================================
// AUTH.JS - НОВАЯ ВЕРСИЯ БЕЗ ПРОБЛЕМ
// ========================================
// Версия: 5.0 - Полностью переписана
// Дата: 16.08.2025

// Константы
const SITE_SOURCE = 'upwork-proposal-generator';

// Глобальные переменные
let supabase = null;
let isInitialized = false;

// Инициализация Supabase
function initSupabase() {
    if (isInitialized && supabase) {
        return true;
    }

    try {
        // Проверяем, загружен ли Supabase SDK
        if (typeof window.supabase === 'undefined') {
            console.error('❌ Supabase SDK не загружен');
            return false;
        }

        // Создаем клиент
        const supabaseUrl = 'https://xykhpnksatwipwcmxwyn.supabase.co';
        const supabaseKey = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Inh5a2hwbmtzYXR3aXB3Y214d3luIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTUyNTAyNjIsImV4cCI6MjA3MDgyNjI2Mn0.PSARsuv14dI7xq35xvgVoxwjptb4cm8Ywb3bYZhY0KM';
        
        supabase = window.supabase.createClient(supabaseUrl, supabaseKey);
        isInitialized = true;
        
        console.log('✅ Supabase инициализирован');
        return true;
    } catch (error) {
        console.error('❌ Ошибка инициализации Supabase:', error);
        return false;
    }
}

// Регистрация пользователя
async function registerUser(email, password, fullName) {
    if (!isInitialized) {
        if (!initSupabase()) {
            throw new Error('Supabase не инициализирован');
        }
    }

    try {
        console.log('🔄 Регистрируем пользователя:', email);
        
        const { data, error } = await supabase.auth.signUp({
            email: email,
            password: password,
            options: {
                data: {
                    full_name: fullName
                }
            }
        });

        if (error) {
            console.error('❌ Ошибка регистрации:', error);
            throw error;
        }

        console.log('✅ Пользователь зарегистрирован:', data.user);
        
        // НЕ сохраняем профиль - функция отключена
        console.log('ℹ️ Профиль пользователя не сохраняется (функция отключена)');
        
        return data.user;
    } catch (error) {
        console.error("Ошибка регистрации:", error);
        throw error;
    }
}

// Вход пользователя
async function loginUser(email, password) {
    if (!isInitialized) {
        if (!initSupabase()) {
            throw new Error('Supabase не инициализирован');
        }
    }

    try {
        console.log('🔄 Входим в систему:', email);
        
        const { data, error } = await supabase.auth.signInWithPassword({
            email: email,
            password: password
        });

        if (error) {
            console.error('❌ Ошибка входа:', error);
            
            // Если email не подтвержден, показываем понятное сообщение
            if (error.message.includes('Email not confirmed')) {
                throw new Error('Email не подтвержден. Проверьте почту и перейдите по ссылке для подтверждения.');
            }
            
            throw error;
        }

        console.log('✅ Вход выполнен успешно:', data.user);
        return data.user;
    } catch (error) {
        console.error("Ошибка входа:", error);
        throw error;
    }
}

// Выход пользователя
async function logoutUser() {
    if (!isInitialized) {
        if (!initSupabase()) {
            throw new Error('Supabase не инициализирован');
        }
    }

    try {
        const { error } = await supabase.auth.signOut();
        if (error) throw error;
        
        console.log('✅ Пользователь успешно вышел из системы');
        return true;
    } catch (error) {
        console.error("Ошибка выхода:", error);
        throw error;
    }
}

// Получение текущего пользователя
async function getCurrentUser() {
    if (!isInitialized) {
        if (!initSupabase()) {
            console.error('Supabase не инициализирован для getCurrentUser');
            return null;
        }
    }

    try {
        const { data: { user }, error } = await supabase.auth.getUser();
        if (error) throw error;
        return user;
    } catch (error) {
        console.error("Ошибка получения текущего пользователя:", error);
        return null;
    }
}

// Слушатель состояния аутентификации
function onAuthStateChange(callback) {
    if (!isInitialized) {
        if (!initSupabase()) {
            console.error('Supabase не инициализирован для onAuthStateChange');
            return;
        }
    }

    try {
        const { data: { subscription } } = supabase.auth.onAuthStateChange((event, session) => {
            console.log('🔄 Изменение состояния аутентификации:', event);
            if (callback) callback(event, session);
        });
        
        return subscription;
    } catch (error) {
        console.error("Ошибка настройки слушателя аутентификации:", error);
    }
}

// GitHub аутентификация
async function signInWithGitHub() {
    if (!isInitialized) {
        if (!initSupabase()) {
            throw new Error('Supabase не инициализирован');
        }
    }

    try {
        const { data, error } = await supabase.auth.signInWithOAuth({
            provider: 'github',
            options: {
                redirectTo: window.location.origin
            }
        });

        if (error) throw error;
        return data;
    } catch (error) {
        console.error("Ошибка GitHub входа:", error);
        throw error;
    }
}

// Заглушки для совместимости (временно отключены)
async function saveUserProfile(user, provider) {
    console.warn('⚠️ Функция saveUserProfile временно отключена');
    return true;
}

async function getUserProfile(userId) {
    console.warn('⚠️ Функция getUserProfile временно отключена');
    return null;
}

async function updateUserLimits(userId, newDailyRemaining) {
    console.warn('⚠️ Функция updateUserLimits временно отключена');
    return true;
}

async function saveProposal(userId, formData, generatedProposal) {
    console.warn('⚠️ Функция saveProposal временно отключена');
    return true;
}

async function getProposalsHistory(userId) {
    console.warn('⚠️ Функция getProposalsHistory временно отключена');
    return [];
}

// Автоматическая инициализация при загрузке DOM
document.addEventListener('DOMContentLoaded', () => {
    console.log('🔄 DOM загружен, инициализируем Supabase...');
    
    // Пытаемся инициализировать Supabase
    if (initSupabase()) {
        console.log('✅ Supabase инициализирован при загрузке DOM');
    } else {
        console.log('⚠️ Supabase не удалось инициализировать при загрузке DOM');
    }
});

// Принудительная инициализация через 3 секунды
setTimeout(() => {
    if (!isInitialized) {
        console.log('🔄 Принудительная инициализация Supabase...');
        initSupabase();
    }
}, 3000);

console.log('✅ auth_new.js загружен');
