# Mea — the Module Engine guide on the website

A tiny Cloudflare Worker that answers questions about Module Engine. It uses **Workers AI** (no API key, free daily allowance), looks the answer up in the docs first (BM25 retrieval over `src/knowledge.json`), and limits requests **per IP and per site**.

```
browser (assets/mea.js)  →  Worker /chat  →  limits (Durable Object)  →  retrieval  →  Workers AI  →  reply + sources
```

## What it does

- **Answers only from the docs.** The prompt carries the retrieved doc sections; Mea is told never to invent features and to say when she is not sure.
- **Per-IP limits:** `BURST_PER_MIN` per minute and `DAILY_PER_IP` per UTC day. **Site-wide cap:** `GLOBAL_DAILY` per UTC day, to stay inside the free AI allowance. Counters live in a Durable Object keyed by a *hash* of the IP + a secret salt — raw IPs are not stored.
- **Only your site can call it:** CORS and an Origin check against `ALLOWED_ORIGINS`.
- **Input is sanitised:** only `user`/`assistant` turns, capped length and count, control characters removed.
- **Non-English questions** are translated to English search keywords first (one short extra call), because the docs are English.
- Nothing is logged or stored besides the counters.

## Deploy

You need a free Cloudflare account and Node 20+.

```bash
cd mea-worker
npx wrangler login                    # opens a browser — log in to Cloudflare
npx wrangler secret put IP_SALT       # type any long random string
npx wrangler deploy                   # prints https://mea-worker.<your-subdomain>.workers.dev
```

Then put that URL into `assets/mea-config.js` of the site and push:

```js
window.MEA = { api: 'https://mea-worker.<your-subdomain>.workers.dev' };
```

Until `api` is set the widget stays hidden and the site is unchanged.

## Limits and cost

Defaults (`wrangler.toml`): 4 questions/minute and 15/day per IP, 120/day for the whole site. The free Workers AI allowance is counted in "neurons" per day; a short answer with ~2k tokens of context costs on the order of tens of neurons, so ~120 questions/day is a conservative fit for the free tier — **check the numbers on your Cloudflare dashboard** and raise `GLOBAL_DAILY` if you have headroom or a paid plan. The model is set by `MODEL` (default `@cf/meta/llama-3.1-8b-instruct`); any Workers AI text model works.

## Keep the knowledge fresh

The docs are the source of truth. After changing `tools/pages/*.md`:

```bash
python3 tools/build_knowledge.py       # rewrites mea-worker/src/knowledge.json
cd mea-worker && npm test && npx wrangler deploy
```

## Develop and test without Cloudflare

```bash
cd mea-worker
npm test                  # 29 tests: retrieval, limits, sanitising, the whole handler with a fake AI
node dev-server.mjs       # the real handler with a fake AI on http://localhost:8787
```

Open the site locally with `?mea=http://localhost:8787` (accepted for localhost only) to talk to the dev server.

## Privacy note for the site

Questions typed into the chat are sent to this Worker and to Cloudflare Workers AI to be answered. The widget says so under the input. The extension's own privacy policy is unchanged: it covers the extension, not this chat.
