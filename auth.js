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
        
        // Создаем клиент с дополнительными опциями для решения CORS
        supabase = window.supabase.createClient(supabaseUrl, supabaseKey, {
            auth: {
                autoRefreshToken: true,
                persistSession: true,
                detectSessionInUrl: true
            },
            global: {
                headers: {
                    'X-Client-Info': 'upwork-proposal-generator'
                }
            }
        });
        
        isInitialized = true;
        console.log('✅ Supabase успешно инициализирован с дополнительными опциями');
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
    console.log('🔄 Начинаем GitHub вход...');
    
    const { data, error } = await supabase.auth.signInWithOAuth({
      provider: 'github',
      options: {
        redirectTo: window.location.origin
      }
    });
    
    if (error) {
      console.error('❌ Ошибка GitHub входа:', error);
      throw error;
    }
    
    console.log('✅ GitHub OAuth инициирован:', data);
    
    // Если пользователь успешно вошел, сохраняем профиль
    if (data.user) {
      try {
        await saveUserProfile(data.user, "github");
        console.log('✅ Профиль GitHub пользователя сохранен');
      } catch (profileError) {
        console.error('⚠️ Ошибка сохранения профиля GitHub, но вход прошел:', profileError);
        // Не прерываем вход, если профиль не сохранился
      }
    }
    
    return data.user;
  } catch (error) {
    console.error("❌ Ошибка GitHub входа:", error);
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
    console.log('🆕 Начинаем регистрацию пользователя:', email);
    
    const { data, error } = await supabase.auth.signUp({
      email: email,
      password: password,
      options: {
        data: {
          full_name: fullName || email
        }
      }
    });
    
    if (error) {
      console.error('❌ Ошибка регистрации:', error);
      
      // Специальная обработка CORS ошибок
      if (error.message.includes('NetworkError') || error.message.includes('fetch')) {
        console.error('🌐 CORS/Network ошибка - проверьте настройки Supabase');
        throw new Error('Ошибка сети. Проверьте подключение к интернету и настройки CORS.');
      }
      
      throw error;
    }
    
    console.log('✅ Регистрация успешна:', data.user);
    
    // Если регистрация успешна, сохраняем профиль
    if (data.user) {
      try {
        await saveUserProfile(data.user, "email");
        console.log('✅ Профиль пользователя сохранен');
      } catch (profileError) {
        console.error('⚠️ Ошибка сохранения профиля, но регистрация прошла:', profileError);
        // Не прерываем регистрацию, если профиль не сохранился
      }
    }
    
    return data.user;
  } catch (error) {
    console.error("❌ Ошибка регистрации:", error);
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
    console.log('🔄 Начинаем вход пользователя:', email);
    
    const { data, error } = await supabase.auth.signInWithPassword({
      email: email,
      password: password
    });
    
    if (error) {
      console.error('❌ Ошибка входа:', error);
      
      // Специальная обработка CORS ошибок
      if (error.message.includes('NetworkError') || error.message.includes('fetch')) {
        console.error('🌐 CORS/Network ошибка - проверьте настройки Supabase');
        throw new Error('Ошибка сети. Проверьте подключение к интернету и настройки CORS.');
      }
      
      // Если email не подтвержден, показываем понятное сообщение
      if (error.message.includes('Email not confirmed')) {
        throw new Error('Email не подтвержден. Проверьте почту и перейдите по ссылке для подтверждения.');
      }
      
      throw error;
    }
    
    console.log('✅ Вход выполнен успешно:', data.user);
    
    // При успешном входе обновляем профиль
    if (data.user) {
      try {
        await saveUserProfile(data.user, "email");
        console.log('✅ Профиль пользователя обновлен при входе');
      } catch (profileError) {
        console.error('⚠️ Ошибка обновления профиля при входе, но вход прошел:', profileError);
        // Не прерываем вход, если профиль не обновился
      }
    }
    
    return data.user;
  } catch (error) {
    console.error("❌ Ошибка входа:", error);
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

// Сохранение профиля пользователя в Supabase
async function saveUserProfile(user, provider) {
  if (!isInitialized) {
    if (!initSupabase()) {
      throw new Error('Supabase не инициализирован');
    }
  }
  
  try {
    console.log('💾 Сохранение профиля пользователя:', user.email);
    
    // Проверяем, что пользователь аутентифицирован
    const { data: { session } } = await supabase.auth.getSession();
    if (!session) {
      console.warn('⚠️ Пользователь не аутентифицирован, пропускаем сохранение профиля');
      return false;
    }
    
    // Проверяем, существует ли уже профиль
    const { data: existingProfile, error: selectError } = await supabase
      .from("user_profiles")
      .select("id")
      .eq("id", user.id)
      .single();
    
    if (selectError && selectError.code !== 'PGRST116') {
      console.error('❌ Ошибка проверки существующего профиля:', selectError);
      throw selectError;
    }
    
    if (existingProfile) {
      console.log('✅ Профиль уже существует, обновляем...');
      // Обновляем существующий профиль
      const { error } = await supabase
        .from("user_profiles")
        .update({
          email: user.email,
          full_name: user.user_metadata?.full_name || user.email,
          avatar_url: user.user_metadata?.avatar_url || null,
          provider: provider,
          updated_at: new Date()
        })
        .eq("id", user.id);
      
      if (error) {
        console.error('❌ Ошибка обновления профиля:', error);
        throw error;
      }
      console.log('✅ Профиль обновлен');
    } else {
      console.log('🆕 Создаем новый профиль...');
      // Создаем новый профиль
      const { error } = await supabase
        .from("user_profiles")
        .insert({
          id: user.id,
          email: user.email,
          full_name: user.user_metadata?.full_name || user.email,
          avatar_url: user.user_metadata?.avatar_url || null,
          provider: provider,
          created_at: new Date(),
          updated_at: new Date()
        });
      
      if (error) {
        console.error('❌ Ошибка создания профиля:', error);
        
        // Если ошибка RLS, пробуем альтернативный способ
        if (error.code === '42501') {
          console.warn('⚠️ RLS политика заблокировала создание, пробуем через auth.users...');
          // Профиль может быть создан автоматически через триггеры
          return true;
        }
        
        throw error;
      }
      console.log('✅ Новый профиль создан');
    }
    
    return true;
  } catch (error) {
    console.error('❌ Ошибка сохранения профиля:', error);
    
    // Если это ошибка RLS, не прерываем процесс
    if (error.code === '42501') {
      console.warn('⚠️ RLS политика заблокировала операцию, но это не критично');
      return false;
    }
    
    throw error;
  }
}

// Проверка состояния подключения к Supabase
async function checkSupabaseConnection() {
  if (!isInitialized) {
    console.error('❌ Supabase не инициализирован');
    return false;
  }
  
  try {
    console.log('🔍 Проверяем подключение к Supabase...');
    
    // Пробуем простой запрос для проверки подключения
    const { data, error } = await supabase
      .from('user_profiles')
      .select('count')
      .limit(1);
    
    if (error) {
      if (error.code === '42501') {
        console.warn('⚠️ RLS политика заблокировала запрос, но подключение работает');
        return true;
      }
      console.error('❌ Ошибка подключения к Supabase:', error);
      return false;
    }
    
    console.log('✅ Подключение к Supabase работает');
    return true;
  } catch (error) {
    console.error('❌ Ошибка проверки подключения:', error);
    return false;
  }
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
                console.log('🔄 Обнаружена активная сессия:', session.user.email);
                callback(session.user);
            } else {
                console.log('🔓 Активная сессия не найдена');
                callback(null);
            }
        });
        
        // Слушаем изменения аутентификации
        const { data: { subscription } } = supabase.auth.onAuthStateChange(async (event, session) => {
            console.log('🔄 Событие аутентификации:', event);
            
            if (event === 'SIGNED_IN' && session) {
                console.log('✅ Пользователь вошел в систему:', session.user.email);
                
                // Автоматически сохраняем/обновляем профиль
                try {
                    const provider = session.user.app_metadata?.provider || 'email';
                    await saveUserProfile(session.user, provider);
                    console.log('✅ Профиль автоматически сохранен при входе');
                } catch (profileError) {
                    console.error('⚠️ Ошибка автоматического сохранения профиля:', profileError);
                    // Не прерываем процесс входа
                }
                
                callback(session.user);
            } else if (event === 'SIGNED_OUT') {
                console.log('🔓 Пользователь вышел из системы');
                callback(null);
            } else if (event === 'TOKEN_REFRESHED' && session) {
                console.log('🔄 Токен обновлен для пользователя:', session.user.email);
                callback(session.user);
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
window.checkSupabaseConnection = checkSupabaseConnection;

// Функция для проверки готовности auth.js
window.isAuthReady = function() {
    return typeof window.signInWithGitHub !== 'undefined' &&
           typeof window.registerUser !== 'undefined' &&
           typeof window.loginUser !== 'undefined' &&
           typeof window.logoutUser !== 'undefined' &&
           typeof window.onAuthStateChange !== 'undefined' &&
           typeof window.getCurrentUser !== 'undefined' &&
           typeof window.getUserProfile !== 'undefined' &&
           typeof window.updateUserLimits !== 'undefined' &&
           typeof window.saveProposal !== 'undefined' &&
           typeof window.getProposalsHistory !== 'undefined' &&
           typeof window.checkSupabaseConnection !== 'undefined';
};

// Функция для ожидания готовности auth.js
window.waitForAuthReady = function() {
    return new Promise((resolve) => {
        if (window.isAuthReady()) {
            resolve();
            return;
        }
        
        const checkInterval = setInterval(() => {
            if (window.isAuthReady()) {
                clearInterval(checkInterval);
                resolve();
            }
        }, 100);
        
        // Таймаут на случай, если что-то пошло не так
        setTimeout(() => {
            clearInterval(checkInterval);
            console.warn('⚠️ Таймаут ожидания готовности auth.js');
            resolve();
        }, 30000);
    });
};

// Автоматическая инициализация
console.log('🚀 auth.js загружен, начинаем инициализацию...');

// Инициализируем Supabase сразу
if (typeof window.supabase !== 'undefined') {
    console.log('✅ Supabase SDK уже доступен, инициализируем...');
    initSupabase();
} else {
    console.log('⏳ Supabase SDK еще не загружен, ждем...');
    // Ждем загрузки Supabase SDK
    const checkSupabase = setInterval(() => {
        if (typeof window.supabase !== 'undefined') {
            clearInterval(checkSupabase);
            console.log('✅ Supabase SDK загружен, инициализируем...');
            initSupabase();
        }
    }, 100);
    
    // Таймаут для Supabase SDK
    setTimeout(() => {
        clearInterval(checkSupabase);
        console.error('❌ Таймаут загрузки Supabase SDK');
    }, 10000);
}

// Уведомляем, что auth.js готов
console.log('✅ auth.js полностью загружен и готов к использованию');

if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initAuth);
} else {
    initAuth();
}
