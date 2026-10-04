// Runs the REAL request handler locally with a fake AI and an in-memory limiter — no Cloudflare account needed.
//   node dev-server.mjs            → http://localhost:8787
// Then open the site with  ?mea=http://localhost:8787  to talk to it. The fake AI just quotes the best-matching docs.
import http from 'node:http';
import { handle } from './src/handler.js';
import { decide } from './src/limits.js';

const states = new Map();
const env = {
    ALLOWED_ORIGINS: 'https://iamigoi.github.io', ALLOW_LOCALHOST: '1', MODEL: 'fake',
    BURST_PER_MIN: process.env.BURST_PER_MIN ?? '4', DAILY_PER_IP: process.env.DAILY_PER_IP ?? '15', GLOBAL_DAILY: '500',
    LIMITER: { idFromName: name => name, get: id => ({ async check(limits) { const r = decide(states.get(id), Date.now(), limits); states.set(id, r.state); return r; } }) },
    AI: {
        async run(_model, { messages }) {
            if (messages.length === 2 && /search keywords/.test(messages[0].content)) return { response: 'install extension' };
            const context = messages[0].content.split('CONTEXT:')[1] ?? '';
            const first = context.trim().split('\n\n')[0].replace(/^\[(.+?)\]\n/, '');
            const lines = first.split('\n').slice(0, 3).join('\n');
            return { response: `Here is what the docs say:\n\n**${(context.match(/^\s*\[(.+?)\]/) ?? [])[1] ?? 'Module Engine'}**\n${lines.slice(0, 420)}\n\n- the dock opens the engine\n- run \`npm test\` to check a module` };
        },
    },
};

http.createServer(async (req, res) => {
    const chunks = []; for await (const c of req) chunks.push(c);
    const request = new Request(`http://localhost:8787${req.url}`, { method: req.method, headers: req.headers, body: ['GET', 'HEAD', 'OPTIONS'].includes(req.method) ? undefined : Buffer.concat(chunks) });
    const response = await handle(request, env);
    res.writeHead(response.status, Object.fromEntries(response.headers));
    res.end(Buffer.from(await response.arrayBuffer()));
}).listen(8787, () => console.log('Mea dev server on http://localhost:8787'));
