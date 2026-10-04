/* Mea — the Module Engine guide, as a chat on the site. Talks to the mea-worker (Cloudflare Worker + Workers AI).
   Hidden unless window.MEA.api is set (or ?mea=http://localhost:PORT is used while developing). */
(function () {
  'use strict';
  var cfg = window.MEA || {};
  var api = cfg.api || '';
  try { // local development override — localhost only, so a crafted link cannot point the chat elsewhere
    var q = new URLSearchParams(location.search).get('mea');
    if (q && /^https?:\/\/(localhost|127\.0\.0\.1)(:\d+)?$/.test(q)) { api = q; sessionStorage.setItem('mea.api', q); }
    else if (!api && /^https?:\/\/(localhost|127\.0\.0\.1)(:\d+)?$/.test(sessionStorage.getItem('mea.api') || '')) api = sessionStorage.getItem('mea.api');
  } catch (e) {}
  if (!api) return;

  var script = document.currentScript || document.querySelector('script[src$="assets/mea.js"]');
  var root = script ? new URL('../', script.src).href : location.origin + '/';
  var POSES = { idle: 'happy', thinking: 'side', limited: 'laying', error: 'angry' };
  var SUGGESTIONS = ['What is Module Engine?', 'How do I install it?', 'Which modules are there?', 'How do I write my own module?'];
  var MAX_CHARS = 600, KEY = 'mea.chat';
  var reduced = window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches;

  var state = { open: false, busy: false, messages: [], remaining: null, retryTimer: null };
  try { var saved = JSON.parse(sessionStorage.getItem(KEY) || 'null'); if (saved && Array.isArray(saved.messages)) { state.messages = saved.messages.slice(-20); state.remaining = saved.remaining; } } catch (e) {}
  function persist() { try { sessionStorage.setItem(KEY, JSON.stringify({ messages: state.messages.slice(-20), remaining: state.remaining })); } catch (e) {} }

  function el(tag, cls, text) { var n = document.createElement(tag); if (cls) n.className = cls; if (text != null) n.textContent = text; return n; }
  function pose(name) { return root + 'assets/mea/' + POSES[name] + '.webp'; }

  // ---- markdown-lite: escape first, then allow **bold**, `code`, ``` blocks, lists and safe links
  function esc(s) { return s.replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); }
  function safeHref(u) {
    if (/^https?:\/\//i.test(u)) return { href: u, ext: true };
    if (/^[\w./#-]+$/.test(u) && u.indexOf('..') < 0) return { href: new URL(u.replace(/^\//, ''), root).href, ext: false };
    return null;
  }
  function inline(s) {
    return s.replace(/`([^`]+)`/g, '<code>$1</code>').replace(/\*\*([^*]+)\*\*/g, '<strong>$1</strong>')
      .replace(/\[([^\]]+)\]\(([^)\s]+)\)/g, function (m, t, u) { var l = safeHref(u); return l ? '<a href="' + l.href + '"' + (l.ext ? ' target="_blank" rel="noopener"' : '') + '>' + t + '</a>' : t; });
  }
  function render(text) {
    var parts = esc(text).split('```'), out = '';
    parts.forEach(function (part, i) {
      if (i % 2) { out += '<pre><code>' + part.replace(/^[a-z]*\n/, '') + '</code></pre>'; return; }
      var list = false;
      part.split('\n').forEach(function (line) {
        var item = /^\s*(?:[-*]|\d+[.)])\s+(.*)$/.exec(line);
        if (item) { if (!list) { out += '<ul>'; list = true; } out += '<li>' + inline(item[1]) + '</li>'; return; }
        if (list) { out += '</ul>'; list = false; }
        if (line.trim()) out += '<p>' + inline(line) + '</p>';
      });
      if (list) out += '</ul>';
    });
    return out;
  }

  // ---- DOM
  var launcher = el('button', 'mea-launcher'); launcher.type = 'button'; launcher.setAttribute('aria-label', 'Ask Mea about Module Engine');
  var launchImg = el('img'); launchImg.alt = ''; launchImg.src = pose('idle'); launcher.appendChild(launchImg);
  var tip = el('span', 'mea-tip', 'Ask Mea'); launcher.appendChild(tip);

  var panel = el('section', 'mea-panel'); panel.setAttribute('role', 'dialog'); panel.setAttribute('aria-label', 'Mea, the Module Engine guide'); panel.hidden = true;
  var head = el('div', 'mea-head');
  var avatar = el('img', 'mea-avatar'); avatar.alt = '';
  var who = el('div', 'mea-who'); who.appendChild(el('strong', null, 'Mea')); var sub = el('small', null, 'Guide of Module Engine · AI'); who.appendChild(sub);
  var btnReset = el('button', 'mea-icon', '⟲'); btnReset.type = 'button'; btnReset.title = 'Start over'; btnReset.setAttribute('aria-label', 'Start a new conversation');
  var btnClose = el('button', 'mea-icon', '✕'); btnClose.type = 'button'; btnClose.title = 'Close'; btnClose.setAttribute('aria-label', 'Close');
  head.append(avatar, who, btnReset, btnClose);
  var log = el('div', 'mea-log'); log.setAttribute('aria-live', 'polite');
  var chips = el('div', 'mea-chips');
  var form = el('form', 'mea-form');
  var input = el('textarea', 'mea-input'); input.rows = 1; input.maxLength = MAX_CHARS; input.placeholder = 'Ask about Module Engine…'; input.setAttribute('aria-label', 'Your question');
  var send = el('button', 'mea-send', '➤'); send.type = 'submit'; send.setAttribute('aria-label', 'Send');
  form.append(input, send);
  var note = el('div', 'mea-note');
  panel.append(head, log, chips, form, note);
  document.body.append(launcher, panel);

  function setPose(name) { avatar.src = pose(name); launchImg.src = pose(name === 'thinking' ? 'thinking' : name === 'idle' ? 'idle' : name); }
  function setNote() {
    note.textContent = (state.remaining != null && state.remaining >= 0 ? state.remaining + ' question' + (state.remaining === 1 ? '' : 's') + ' left today · ' : '')
      + 'AI answers can be wrong. Your question is sent to an AI service to be answered; nothing is stored.';
  }
  function scroll() { log.scrollTop = log.scrollHeight; }

  function addMessage(role, text, sources, animate) {
    var row = el('div', 'mea-msg ' + role);
    var bubble = el('div', 'mea-bubble'); row.appendChild(bubble); log.appendChild(row);
    if (role === 'user') bubble.textContent = text;
    else if (animate && !reduced) {
      var i = 0, step = Math.max(2, Math.ceil(text.length / 90));
      (function tick() { i = Math.min(text.length, i + step); bubble.innerHTML = render(text.slice(0, i)); scroll(); if (i < text.length) setTimeout(tick, 16); else addSources(row, sources); })();
    } else { bubble.innerHTML = render(text); addSources(row, sources); }
    scroll(); return bubble;
  }
  function addSources(row, sources) {
    if (!sources || !sources.length) return;
    var s = el('div', 'mea-sources'); s.appendChild(el('small', null, 'Read more:'));
    sources.forEach(function (src) { var l = safeHref(src.url); if (!l) return; var a = el('a', null, src.title); a.href = l.href; s.appendChild(a); });
    row.appendChild(s); scroll();
  }
  function welcome() {
    addMessage('assistant', 'Hi, I\'m **Mea** — I live inside Module Engine. Ask me anything about it: installing, the modules, memory, prompts, or writing your own module.', null, false);
  }
  function paint() {
    log.textContent = ''; welcome();
    state.messages.forEach(function (m) { addMessage(m.role, m.content, m.sources, false); });
    chips.hidden = state.messages.length > 0; setNote(); setPose('idle');
  }
  SUGGESTIONS.forEach(function (text) { var c = el('button', 'mea-chip', text); c.type = 'button'; c.addEventListener('click', function () { ask(text); }); chips.appendChild(c); });

  function lock(on) { state.busy = on; input.disabled = on; send.disabled = on; panel.classList.toggle('busy', on); }
  function say(role, text) { addMessage(role, text, null, role === 'assistant'); }

  function ask(text) {
    text = (text || '').trim().slice(0, MAX_CHARS);
    if (!text || state.busy) return;
    chips.hidden = true; input.value = ''; grow();
    state.messages.push({ role: 'user', content: text }); persist(); addMessage('user', text);
    var typing = el('div', 'mea-msg assistant'); var tb = el('div', 'mea-bubble mea-typing'); tb.innerHTML = '<i></i><i></i><i></i>'; typing.appendChild(tb); log.appendChild(typing); scroll();
    lock(true); setPose('thinking');
    var payload = state.messages.slice(-8).map(function (m) { return { role: m.role, content: m.content }; });
    fetch(api.replace(/\/$/, '') + '/chat', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ messages: payload }) })
      .then(function (r) { return r.json().catch(function () { return {}; }).then(function (d) { return { status: r.status, data: d }; }); })
      .then(function (res) {
        typing.remove(); lock(false);
        if (res.status === 200 && res.data.reply) {
          state.remaining = res.data.remainingToday; state.messages.push({ role: 'assistant', content: res.data.reply, sources: res.data.sources || [] }); persist();
          addMessage('assistant', res.data.reply, res.data.sources, true); setPose('idle'); setNote();
        } else if (res.status === 429) {
          state.messages.pop(); persist(); setPose('limited');
          var d = res.data, wait = d.retryAfter || 30;
          var msg = d.scope === 'minute' ? 'Give me a moment — I can answer again in about ' + wait + ' seconds.'
            : d.scope === 'day' ? 'That\'s all my questions for you today. The docs are always open: [documentation](docs/index.html). I\'ll be back tomorrow!'
            : 'I\'ve used up my free energy for today. Please try again tomorrow, or browse the [documentation](docs/index.html).';
          say('assistant', msg); input.disabled = d.scope !== 'minute'; send.disabled = input.disabled;
          if (d.scope === 'minute') { lock(true); clearTimeout(state.retryTimer); state.retryTimer = setTimeout(function () { lock(false); setPose('idle'); input.focus(); }, wait * 1000); }
          else { remainingZero(); }
        } else {
          state.messages.pop(); persist(); setPose('error');
          say('assistant', res.status === 403 ? 'I can\'t be reached from this address.' : (res.data && res.data.message) || 'Something went wrong on my side. Try again in a moment.');
        }
      })
      .catch(function () { typing.remove(); lock(false); state.messages.pop(); persist(); setPose('error'); say('assistant', 'I can\'t reach my brain right now. Check your connection, or browse the [documentation](docs/index.html).'); });
  }
  function remainingZero() { state.remaining = 0; setNote(); input.placeholder = 'Out of questions for today'; }

  function grow() { input.style.height = 'auto'; input.style.height = Math.min(110, input.scrollHeight) + 'px'; }
  input.addEventListener('input', grow);
  input.addEventListener('keydown', function (e) { if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); ask(input.value); } });
  form.addEventListener('submit', function (e) { e.preventDefault(); ask(input.value); });

  function open(on) {
    state.open = on; panel.hidden = !on; launcher.classList.toggle('open', on); tip.hidden = true;
    if (on) { if (!log.childNodes.length) paint(); setTimeout(function () { input.focus(); }, 30); }
  }
  launcher.addEventListener('click', function () { open(!state.open); });
  btnClose.addEventListener('click', function () { open(false); launcher.focus(); });
  btnReset.addEventListener('click', function () { clearTimeout(state.retryTimer); state.messages = []; state.remaining = null; persist(); lock(false); input.placeholder = 'Ask about Module Engine…'; paint(); });
  document.addEventListener('keydown', function (e) { if (e.key === 'Escape' && state.open) open(false); });

  // a quiet nudge once per session
  try { if (!sessionStorage.getItem('mea.seen')) { sessionStorage.setItem('mea.seen', '1'); setTimeout(function () { if (!state.open) { tip.hidden = false; setTimeout(function () { tip.hidden = true; }, 6000); } }, 4000); } else tip.hidden = true; } catch (e) {}
  tip.hidden = true; setPose('idle');
  window.MeaChat = { open: function () { open(true); }, ask: function (t) { open(true); ask(t); } };
})();
