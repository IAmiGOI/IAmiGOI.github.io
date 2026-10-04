import knowledge from './knowledge.json' with { type: 'json' };
import { buildIndex, search } from './retrieval.js';
import { buildMessages, sanitizeMessages, sourcesOf } from './prompt.js';

const index = buildIndex(knowledge);
const core = knowledge.filter(chunk => chunk.core);

const num = (value, fallback) => (Number.isFinite(Number(value)) && String(value).trim() !== '' ? Number(value) : fallback);

function corsHeaders(request, env) {
    const origin = request.headers.get('Origin') ?? '';
    const allowed = String(env.ALLOWED_ORIGINS ?? 'https://iamigoi.github.io').split(',').map(item => item.trim()).filter(Boolean);
    const ok = allowed.includes(origin) || (String(env.ALLOW_LOCALHOST ?? '') === '1' && /^https?:\/\/(localhost|127\.0\.0\.1)(:\d+)?$/.test(origin));
    return ok ? { 'Access-Control-Allow-Origin': origin, 'Vary': 'Origin', 'Access-Control-Allow-Methods': 'POST, GET, OPTIONS', 'Access-Control-Allow-Headers': 'Content-Type', 'Access-Control-Max-Age': '86400' } : null;
}

const json = (body, status, headers) => new Response(JSON.stringify(body), { status, headers: { 'Content-Type': 'application/json; charset=utf-8', 'Cache-Control': 'no-store', ...headers } });

async function sha256(text) {
    const bytes = await crypto.subtle.digest('SHA-256', new TextEncoder().encode(text));
    return [...new Uint8Array(bytes)].map(b => b.toString(16).padStart(2, '0')).join('');
}

/** one limiter instance by name; returns the decision */
async function check(env, name, limits) {
    const stub = env.LIMITER.get(env.LIMITER.idFromName(name));
    return stub.check(limits);
}

/** text from any of the shapes Workers AI models return */
export function textOf(output) {
    return String(output?.response ?? output?.result?.response ?? output?.choices?.[0]?.message?.content ?? '').trim();
}

/** Non-Latin questions are matched against English docs: ask the model for English search keywords first (cheap, short). */
async function searchQuery(env, text) {
    if (!/[^\u0000-\u007F]/.test(text)) return text;
    try {
        const out = await env.AI.run(env.MODEL, {
            messages: [{ role: 'system', content: 'Translate the user\'s question into English search keywords. Output only the keywords.' }, { role: 'user', content: text }],
            max_tokens: 40, temperature: 0,
        });
        return textOf(out) || text;
    } catch { return text; }
}

export async function handle(request, env) {
    const url = new URL(request.url);
    const cors = corsHeaders(request, env);

    if (request.method === 'OPTIONS') return cors ? new Response(null, { status: 204, headers: cors }) : new Response(null, { status: 403 });
    if (url.pathname === '/health') return json({ ok: true, chunks: knowledge.length }, 200, cors ?? {});
    if (url.pathname !== '/chat' || request.method !== 'POST') return json({ error: 'not_found' }, 404, cors ?? {});
    if (!cors) return json({ error: 'forbidden_origin' }, 403, {});

    let body;
    try { body = await request.json(); } catch { return json({ error: 'bad_json', message: 'Send JSON: { "messages": [...] }.' }, 400, cors); }
    const history = sanitizeMessages(body?.messages);
    if (!history) return json({ error: 'bad_messages', message: 'The last message must be a non-empty user message.' }, 400, cors);

    // limits: per IP (burst + daily), then the whole site (daily) — the site-wide cap protects the free AI allowance
    const ip = request.headers.get('CF-Connecting-IP') ?? 'unknown';
    const ipId = (await sha256(`${env.IP_SALT ?? 'mea'}:${ip}`)).slice(0, 32);
    const mine = await check(env, `ip:${ipId}`, { burst: num(env.BURST_PER_MIN, 4), windowMs: 60_000, daily: num(env.DAILY_PER_IP, 15) });
    if (!mine.allowed) return json({ error: 'rate_limited', scope: mine.scope, retryAfter: mine.retryAfter, message: mine.scope === 'minute' ? 'Slow down a little.' : 'You have used all of today\'s questions.' }, 429, { ...cors, 'Retry-After': String(mine.retryAfter) });
    const site = await check(env, 'site', { burst: 0, windowMs: 60_000, daily: num(env.GLOBAL_DAILY, 120) });
    if (!site.allowed) return json({ error: 'rate_limited', scope: 'global', retryAfter: site.retryAfter, message: 'I have used up the free allowance for today.' }, 429, { ...cors, 'Retry-After': String(site.retryAfter) });

    // retrieval: the last question, plus the one before it so follow-ups ("and how do I turn it on?") still find the topic
    const users = history.filter(message => message.role === 'user');
    const question = users[users.length - 1].content;
    const query = await searchQuery(env, [users.length > 1 ? users[users.length - 2].content : '', question].join(' ').trim());
    const hits = search(index, query, 5).map(hit => knowledge[hit.i]);
    const chunks = [...hits, ...core.filter(chunk => !hits.includes(chunk)).slice(0, 1)];   // always keep the "what is ME" fact within reach

    try {
        const output = await env.AI.run(env.MODEL ?? '@cf/meta/llama-3.1-8b-instruct', { messages: buildMessages(history, chunks), max_tokens: num(env.MAX_TOKENS, 380), temperature: 0.4 });
        const reply = textOf(output);
        if (!reply) return json({ error: 'empty', message: 'I could not come up with an answer.' }, 502, cors);
        return json({ reply, sources: sourcesOf(hits), remainingToday: mine.remainingToday }, 200, cors);
    } catch (error) {
        return json({ error: 'ai_failed', message: 'My brain is unavailable for a moment.' }, 502, cors);
    }
}
