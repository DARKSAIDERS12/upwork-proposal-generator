import { serve } from "https://deno.land/std@0.177.0/http/server.ts";
import { createClient } from "https://esm.sh/@supabase/supabase-js@2";

function corsHeaders(origin: string | null) {
  return {
    "Access-Control-Allow-Origin": origin ?? "*",
    "Access-Control-Allow-Methods": "POST, OPTIONS",
    "Access-Control-Allow-Headers": "authorization, content-type",
    "Vary": "Origin",
    "Content-Type": "application/json; charset=utf-8",
  } as Record<string, string>;
}

serve(async (req) => {
  const origin = req.headers.get("origin");
  if (req.method === "OPTIONS") {
    return new Response("ok", { headers: corsHeaders(origin) });
  }

  try {
    if (req.method !== "POST") {
      return new Response(JSON.stringify({ error: "method_not_allowed" }), {
        status: 405,
        headers: corsHeaders(origin),
      });
    }

    const authHeader = req.headers.get("authorization");
    if (!authHeader || !authHeader.toLowerCase().startsWith("bearer ")) {
      return new Response(JSON.stringify({ error: "missing_bearer" }), {
        status: 401,
        headers: corsHeaders(origin),
      });
    }

    const accessToken = authHeader.slice(7);

    const SUPABASE_URL = Deno.env.get("SUPABASE_URL");
    const SERVICE_ROLE = Deno.env.get("SUPABASE_SERVICE_ROLE_KEY");

    if (!SUPABASE_URL || !SERVICE_ROLE) {
      return new Response(JSON.stringify({ error: "missing_service_env" }), {
        status: 500,
        headers: corsHeaders(origin),
      });
    }

    const admin = createClient(SUPABASE_URL, SERVICE_ROLE, {
      auth: { autoRefreshToken: false, persistSession: false },
      global: { headers: { "X-Client-Info": "delete-user-edge" } },
    });

    // Получаем пользователя из токена
    const { data: userData, error: userErr } = await admin.auth.getUser(accessToken);
    if (userErr || !userData?.user) {
      return new Response(JSON.stringify({ error: "unauthorized", details: userErr?.message }), {
        status: 401,
        headers: corsHeaders(origin),
      });
    }

    const userId = userData.user.id;

    // Удаляем связанные данные из публичных таблиц (адаптируйте под ваши таблицы)
    try {
      await admin.from("user_profiles").delete().eq("id", userId);
    } catch (_) {
      // игнорируем ошибки удаления профиля, продолжаем удаление auth-пользователя
    }

    // Удаляем auth-пользователя (требуется service_role)
    const { error: delErr } = await admin.auth.admin.deleteUser(userId);
    if (delErr) {
      return new Response(JSON.stringify({ success: false, error: delErr.message }), {
        status: 500,
        headers: corsHeaders(origin),
      });
    }

    return new Response(JSON.stringify({ success: true }), {
      status: 200,
      headers: corsHeaders(origin),
    });
  } catch (e) {
    return new Response(JSON.stringify({ error: "unexpected_error", details: `${e?.message ?? e}` }), {
      status: 500,
      headers: corsHeaders(req.headers.get("origin")),
    });
  }
});


