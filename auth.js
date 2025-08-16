// Система аутентификации Supabase
// Версия 4.1 - ОБНОВЛЕНО 16.08.2025
// САЙТ 1 - использует общую базу данных

// Supabase клиент - инициализируем после загрузки SDK
let supabase = null;
let isInitialized = false;

// Функция инициализации Supabase
function initSupabase() {
    if (typeof window.supabase === 'undefined') {
        console.error('❌ Supabase SDK не загружен!');
        return false;
    }
    
    try {
        const supabaseUrl = 'https://xykhpnksatwipwcmxwyn.supabase.co';
        const supabaseKey = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Inh5a2hwbmtzYXR3aXB3Y214d3luIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTUyNTAyNjIsImV4cCI6MjA3MDgyNjI2Mn0.PSARsuv14dI7xq35xvgVoxwjptb4cm8Ywb3bYZhY0KM';
        supabase = window.supabase.createClient(supabaseUrl, supabaseKey);
        isInitialized = true;
        console.log('✅ Supabase успешно инициализирован');
        return true;
    } catch (error) {
        console.error('❌ Ошибка инициализации Supabase:', error);
        return false;
    }
}

// Автоматическая инициализация при загрузке
document.addEventListener('DOMContentLoaded', function() {
    console.log('🔄 Попытка инициализации Supabase...');
    if (typeof window.supabase !== 'undefined') {
        initSupabase();
    } else {
        console.log('⏳ Ожидание загрузки Supabase SDK...');
        const checkInterval = setInterval(() => {
            if (typeof window.supabase !== 'undefined') {
                clearInterval(checkInterval);
                initSupabase();
            }
        }, 100);
        
        // Таймаут на случай, если SDK не загрузится
        setTimeout(() => {
            clearInterval(checkInterval);
            console.error('❌ Таймаут загрузки Supabase SDK');
        }, 5000);
    }
});

// Константа для идентификации сайта
const SITE_SOURCE = "site1";

// GitHub вход через Supabase
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
    
    // Если пользователь успешно вошел, сохраняем профиль
    if (data.user) {
      await saveUserProfile(data.user, "github");
    }
    
    return data.user;
  } catch (error) {
    console.error("Ошибка GitHub входа:", error);
    throw error;
  }
}

// Email/Password регистрация через Supabase
async function registerUser(email, password, fullName) {
  if (!isInitialized) {
    if (!initSupabase()) {
      throw new Error('Supabase не инициализирован');
    }
  }
  
  try {
    const { data, error } = await supabase.auth.signUp({
      email: email,
      password: password,
      options: {
        data: {
          full_name: fullName || email
        }
      }
    });
    
    if (error) throw error;
    
    // Если регистрация успешна, сохраняем профиль
    if (data.user) {
      await saveUserProfile(data.user, "email");
    }
    
    return data.user;
  } catch (error) {
    console.error("Ошибка регистрации:", error);
    throw error;
  }
}

// Email/Password вход через Supabase
async function loginUser(email, password) {
  if (!isInitialized) {
    if (!initSupabase()) {
      throw new Error('Supabase не инициализирован');
    }
  }
  
  try {
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

// Выход через Supabase
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

// Сохранение профиля пользователя в Supabase (временно отключено)
async function saveUserProfile(user, provider) {
  console.warn('⚠️ Функция saveUserProfile временно отключена - проблемы с БД');
  return true; // Возвращаем true для совместимости
}

// Слушатель состояния аутентификации (удален дубликат)

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

// Получение профиля пользователя из Supabase
async function getUserProfile(userId) {
  if (!isInitialized) {
    if (!initSupabase()) {
      console.error('Supabase не инициализирован для getUserProfile');
      return null;
    }
  }
  
  try {
    const { data, error } = await supabase
      .from("user_profiles")
      .select("*")
      .eq("id", userId)
      .single();
    
    if (error) throw error;
    return data;
  } catch (error) {
    console.error("Ошибка получения профиля:", error);
    return null;
  }
}

// Обновление лимитов пользователя (временно отключено)
async function updateUserLimits(userId, newDailyRemaining) {
  console.warn('⚠️ Функция updateUserLimits временно отключена - колонка daily_remaining не существует в БД');
  return true; // Возвращаем true для совместимости
}

// Сохранение предложения
async function saveProposal(userId, formData, generatedProposal) {
  if (!isInitialized) {
    if (!initSupabase()) {
      throw new Error('Supabase не инициализирован');
    }
  }
  
  try {
    const { error } = await supabase
      .from("proposals")
      .insert({
        user_id: userId,
        project_title: formData.title,
        project_description: formData.description,
        generated_proposal: generatedProposal,
        site_source: SITE_SOURCE,
        created_at: new Date()
      });
    
    if (error) throw error;
    console.log("Предложение сохранено в Supabase");
  } catch (error) {
    console.error("Ошибка сохранения предложения:", error);
    throw error;
  }
}

// Получение истории предложений
async function getProposalsHistory(userId) {
  if (!isInitialized) {
    if (!initSupabase()) {
      console.error('Supabase не инициализирован для getProposalsHistory');
      return [];
    }
  }
  
  try {
    const { data, error } = await supabase
      .from("proposals")
      .select("*")
      .eq("user_id", userId)
      .eq("site_source", SITE_SOURCE)
      .order("created_at", { ascending: false });
    
    if (error) throw error;
    return data || [];
  } catch (error) {
    console.error("Ошибка получения истории:", error);
    return [];
  }
}

// Функция для отслеживания состояния аутентификации
function onAuthStateChange(callback) {
    if (!isInitialized) {
        if (!initSupabase()) {
            console.error('❌ Не удалось инициализировать Supabase для onAuthStateChange');
            return;
        }
    }
    
    try {
        // Получаем текущего пользователя
        supabase.auth.getSession().then(({ data: { session } }) => {
            if (session) {
                callback(session.user);
            } else {
                callback(null);
            }
        });
        
        // Слушаем изменения аутентификации
        const { data: { subscription } } = supabase.auth.onAuthStateChange((event, session) => {
            if (event === 'SIGNED_IN' && session) {
                callback(session.user);
            } else if (event === 'SIGNED_OUT') {
                callback(null);
            }
        });
        
        return subscription;
    } catch (error) {
        console.error('❌ Ошибка в onAuthStateChange:', error);
        callback(null);
    }
}

// Инициализация при загрузке страницы
function initAuth() {
    console.log('🔄 Инициализация аутентификации...');
    
    // Пытаемся инициализировать Supabase
    if (typeof createClient !== 'undefined') {
        console.log('✅ Supabase SDK найден, инициализируем...');
        initSupabase();
    } else {
        console.log('⏳ Supabase SDK еще не загружен, ждем...');
        // Если SDK еще не загружен, ждем
        setTimeout(initAuth, 100);
    }
}

// Делаем функции доступными глобально
window.signInWithGitHub = signInWithGitHub;
window.registerUser = registerUser;
window.loginUser = loginUser;
window.logoutUser = logoutUser;
window.onAuthStateChange = onAuthStateChange;
window.getCurrentUser = getCurrentUser;
window.getUserProfile = getUserProfile;
window.updateUserLimits = updateUserLimits;
window.saveProposal = saveProposal;
window.getProposalsHistory = getProposalsHistory;

// Автоматическая инициализация
console.log('🚀 auth.js загружен, начинаем инициализацию...');

// Принудительная инициализация через небольшую задержку
setTimeout(() => {
    if (typeof createClient !== 'undefined') {
        console.log('✅ Supabase SDK найден, инициализируем...');
        initSupabase();
    } else {
        console.log('⏳ Supabase SDK еще не загружен, ждем...');
        initAuth();
    }
}, 100);

if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initAuth);
} else {
    initAuth();
}
