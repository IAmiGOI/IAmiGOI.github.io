#!/usr/bin/env python3
"""Generates the static site: index.html, install.html, docs/*.html, search-index.json.
Docs come from the engine's own guide articles (Client/Release/guide/knowledge/*.md).
Usage: python3 tools/build.py [path/to/guide/knowledge]"""
import html, json, re, sys, pathlib
import markdown

ROOT = pathlib.Path(__file__).resolve().parent.parent
KB = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else "/home/amigo/Module Engine/Client/Release/guide/knowledge")
REPO = "https://github.com/IAmiGOI/Module-Engine"

GROUPS = ["Start here", "Setup", "Modules", "Memory & prompts", "Interface & data", "Help"]
GROUP_BLURB = {
    "Start here": "New to Module Engine? Begin here.",
    "Setup": "Connect the models the engine works with.",
    "Modules": "Every feature, step by step.",
    "Memory & prompts": "Long-term memory and full control of the request.",
    "Interface & data": "The look of the engine, and keeping your data safe.",
    "Help": "When something is unclear or broken.",
}

def slug(s):
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")

ICON_CP = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="9" y="9" width="12" height="12" rx="2"/><path d="M5 15H4a1 1 0 01-1-1V4a1 1 0 011-1h10a1 1 0 011 1v1"/></svg>'
def cpbtn(cls, label):
    return f'<button type="button" class="btn {cls} copy-repo" data-copy="{REPO}">{ICON_CP} <span>{label}</span></button>'
ICON_DL = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 3v12m0 0l-4.5-4.5M12 15l4.5-4.5M4 20h16"/></svg>'
ICON_GH = '<svg viewBox="0 0 24 24" fill="currentColor"><path d="M12 .5a11.5 11.5 0 00-3.64 22.41c.58.1.79-.25.79-.56v-2c-3.2.7-3.88-1.37-3.88-1.37-.52-1.33-1.28-1.69-1.28-1.69-1.04-.71.08-.7.08-.7 1.15.08 1.76 1.19 1.76 1.19 1.03 1.76 2.69 1.25 3.35.96.1-.75.4-1.25.73-1.54-2.55-.29-5.24-1.28-5.24-5.69 0-1.26.45-2.28 1.19-3.09-.12-.29-.52-1.46.11-3.05 0 0 .97-.31 3.17 1.18a11 11 0 015.78 0c2.2-1.49 3.17-1.18 3.17-1.18.63 1.59.23 2.76.11 3.05.74.81 1.19 1.83 1.19 3.09 0 4.42-2.7 5.4-5.27 5.68.41.36.78 1.06.78 2.14v3.17c0 .31.21.67.8.56A11.5 11.5 0 0012 .5z"/></svg>'

def head(title, desc, base, extra=""):
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(title)}</title>
<meta name="description" content="{html.escape(desc)}">
<meta name="theme-color" content="#0d0e12">
<meta property="og:title" content="{html.escape(title)}">
<meta property="og:description" content="{html.escape(desc)}">
<meta property="og:type" content="website">
<meta name="twitter:card" content="summary">
<link rel="icon" href="{base}assets/me-logo.webp" type="image/webp">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Noto+Sans:wght@300;400;500;600&display=swap">
<script>document.documentElement.classList.add("js")</script>
<link rel="stylesheet" href="{base}assets/site.css">
{extra}
</head>
<body>
<div class="glows"></div>
"""

def nav(base, cur):
    def a(href, label, key):
        return f'<a class="l{" on" if cur == key else ""}" href="{base}{href}">{label}</a>'
    return f"""<header class="nav">
  <a class="brand" href="{base}index.html"><img src="{base}assets/me-logo.webp" alt="" width="30" height="27">Module Engine <small>for SillyTavern</small></a>
  <button class="burger" aria-label="Menu">☰</button>
  <nav class="links" style="display:contents">
    {a("index.html#features", "Features", "home")}
    {a("install.html", "Install", "install")}
    {a("docs/index.html", "Docs", "docs")}
    <a class="l" href="{REPO}">GitHub</a>
  </nav>
  {cpbtn("primary sm dl", "Copy install link")}
</header>
"""

def foot(base):
    return f"""<footer>
  <div>© 2026 IAmiGOI · All rights reserved. Source is viewable on GitHub (<a href="{REPO}/blob/main/LICENSE">license</a>). Not affiliated with SillyTavern.</div>
  <nav><a href="{base}docs/index.html">Docs</a><a href="{base}install.html">Install</a><a href="{base}privacy.html">Privacy policy</a><a href="{base}terms.html">Terms</a><a href="{REPO}/issues">Issues</a><a href="{REPO}">GitHub</a></nav>
</footer>
<script src="{base}assets/site.js"></script>
</body>
</html>
"""

# ---------------------------------------------------------------- landing
GRAPH_SVG = """<svg viewBox="0 0 320 210" class="graph" aria-hidden="true">
<g stroke="currentColor" stroke-opacity=".35" stroke-width="1.5" fill="none">
<path d="M160 105 L70 50 M160 105 L250 45 M160 105 L60 150 M160 105 L255 160 M70 50 L25 95 M250 45 L295 90 M60 150 L110 190 M255 160 L200 195"/></g>
<g fill="var(--surface)" stroke-width="2">
<circle cx="160" cy="105" r="22" stroke="#8da8ff"/><circle cx="70" cy="50" r="14" stroke="#ff7b6e"/><circle cx="250" cy="45" r="14" stroke="#5bb8ff"/>
<circle cx="60" cy="150" r="14" stroke="#c86bff"/><circle cx="255" cy="160" r="14" stroke="#8da8ff"/>
<circle cx="25" cy="95" r="8" stroke="#ff7b6e"/><circle cx="295" cy="90" r="8" stroke="#5bb8ff"/><circle cx="110" cy="190" r="8" stroke="#c86bff"/><circle cx="200" cy="195" r="8" stroke="#8da8ff"/></g>
<g fill="#dfe3ea" font-size="10" font-family="Noto Sans, sans-serif" text-anchor="middle">
<text x="160" y="109">Mira</text><text x="70" y="54">Tavern</text><text x="250" y="49">Harbour</text><text x="60" y="154">Key</text><text x="255" y="164">Guild</text></g></svg>"""

def landing():
    return head("ST Module Engine — modules, pipeline and memory for SillyTavern",
                "ST Module Engine is a SillyTavern extension: trackers, long-term memory, a prompt manager, scene pictures, music and more — as modules you switch on.", "") + nav("", "") + f"""
<main>
  <div class="hero">
    <div class="marks"><img class="st" src="assets/st-logo.png" alt="SillyTavern"><span>×</span><img class="me" src="assets/me-logo.webp" alt="Module Engine"></div>
    <h1>Your model writes the story.<br><span class="grad">Module Engine does the rest.</span></h1>
    <p class="lead">It keeps track of health, time and places, remembers what happened, polishes every reply, paints the scene and plays the music — each job done by a small module you switch on only when you want it.</p>
    <div class="cta">
      {cpbtn("primary big", "Copy install link")}
      <a class="btn big" href="install.html">Install guide</a>
    </div>
    <div class="meta">Paste it in SillyTavern → Extensions → Install extension</div>
    <div class="loadbar"></div>

    <div class="preview rv">
      <div class="chat">
        <div class="bubble u">I push the tavern door open and step out into the rain.</div>
        <div class="bubble"><b>Mira</b> pulls her hood up and follows you into the alley. "You really mean to go to the harbour tonight?"<br><span class="badge">🕒 Day 3 · 21:40</span></div>
        <div class="bubble u">We don't have a choice.</div>
      </div>
      <div class="float"><div class="h"><span>Tracker</span><span>✕</span></div><div class="b"><span>❤ <i>health</i> 82</span><span>📍 <i>location</i> Harbour alley</span><span>🎭 <i>mood</i> Tense</span></div></div>
      <div class="float two"><div class="h"><span>RP Time</span><span>✕</span></div><div class="b"><span>Day 3 · 21:40</span><span><i>raining</i></span></div></div>
      <div class="dock"><i>▦</i><i>♪</i><i>🎨</i><i>🗺</i></div>
    </div>
  </div>

  <section id="see">
    <div class="eyebrow">The real thing</div>
    <h2 class="sec">This is what it looks like</h2>
    <p class="lead">Screenshots from the engine itself, running inside SillyTavern.</p>
    <div class="gallery rv">
      <figure class="shot wide"><img src="assets/shots/modules.webp" alt="The Modules screen" loading="lazy"><figcaption>Modules — every feature has its own switch and its own settings.</figcaption></figure>
      <figure class="shot"><img src="assets/shots/tracker-form.webp" alt="Tracker settings" loading="lazy"><figcaption>Tracker — name the values you care about.</figcaption></figure>
      <figure class="shot"><img src="assets/shots/pass-form.webp" alt="Post-Turn pass" loading="lazy"><figcaption>Post-Turn Processor — a pass is just an instruction and a model.</figcaption></figure>
      <figure class="shot wide"><img src="assets/shots/summary.webp" alt="Chat Summary settings" loading="lazy"><figcaption>Chat Summary — a pyramid of summaries with a protected window.</figcaption></figure>
    </div>
  </section>

  <section id="how">
    <div class="eyebrow">How it works</div>
    <h2 class="sec">A helper team around every message</h2>
    <p class="lead">Your favourite model still writes the reply. Around it, small cheap models do the bookkeeping — before, after and in the background.</p>
    <div class="timeline rv">
      <div class="tl"><i>1</i><b>You send</b><span>a message as usual</span></div>
      <div class="tl pre"><i>2</i><b>Before</b><span>Trackers can hold the reply until values are fresh · the Prompt Manager assembles the request</span></div>
      <div class="tl main"><i>3</i><b>Your model writes</b><span>the roleplay reply</span></div>
      <div class="tl post"><i>4</i><b>After</b><span>Post-Turn passes polish the text</span></div>
      <div class="tl bg"><i>5</i><b>In the background</b><span>values, time, summaries and memory update · a picture and music follow the scene</span></div>
    </div>
  </section>

  <section class="show rv" id="tracker">
    <div class="txt">
      <div class="eyebrow">Tracker · RP Time</div>
      <h2 class="sec">Know the state of the story at a glance</h2>
      <p>Health, mood, location, money — any value you name. A cheap model keeps it current after every reply and shows it in a small window you can drag anywhere.</p>
      <ul class="ticks"><li>Use values in prompts as macros</li><li>Saved per message — rerolls show the right value</li><li>An in-world clock that knows it is already midnight</li></ul>
      <a class="more" href="docs/tracker.html">Tracker guide →</a>
    </div>
    <div class="vis">
      <div class="float st"><div class="h"><span>Tracker · status</span><span>✕</span></div><div class="b"><span>❤ <i>health</i> 82</span><span>💰 <i>gold</i> 140</span><span>📍 <i>location</i> Harbour alley</span><span>🎭 <i>mood</i> Tense</span></div></div>
      <div class="float st t2"><div class="h"><span>RP Time</span><span>✕</span></div><div class="b"><span>Day 3 · 21:40</span><span><i>night · raining</i></span></div></div>
      <div class="macro"><code>{{{{tracker_health}}}}</code> → <b>82</b></div>
    </div>
  </section>

  <section class="show rev rv" id="memory">
    <div class="txt">
      <div class="eyebrow">Chat Summary · Memory graph</div>
      <h2 class="sec">Long chats that still fit the context</h2>
      <p>Old messages fold into summaries, level by level — originals are hidden from the prompt, never deleted. A memory graph keeps who is connected to what, and pulls the right memories in by meaning.</p>
      <ul class="ticks"><li>Three levels of summaries, with a protected recent window</li><li>A mind-map of people, places and facts</li><li>Can start from your lorebook</li></ul>
      <a class="more" href="docs/summary.html">Memory guide →</a>
    </div>
    <div class="vis">
      <div class="levels sm"><div class="lv"><b>Newest messages</b><span>as they are</span></div><div class="lv l1"><b>Level 1</b><span>summary</span></div><div class="lv l2"><b>Level 2</b><span>summary of summaries</span></div></div>
      {GRAPH_SVG}
    </div>
  </section>

  <section class="show rv" id="polish">
    <div class="txt">
      <div class="eyebrow">Post-Turn Processor</div>
      <h2 class="sec">Every reply, polished</h2>
      <p>Chain independent rewrite passes — cut clichés, fix style, check continuity — each with its own prompt and its own model. The final text replaces the reply.</p>
      <ul class="ticks"><li>Passes run in order; each sees the previous result</li><li>Auto-run after each reply, or by hand</li><li>You say what must stay unchanged</li></ul>
      <a class="more" href="docs/postprocess.html">Post-Turn guide →</a>
    </div>
    <div class="vis">
      <div class="diff"><small>Before</small><p>Her eyes <s>sparkled like stars</s> as <s>a shiver ran down her spine</s>. She <s>let out a breath she didn't know she was holding</s>.</p></div>
      <div class="diff after"><small>After</small><p>Mira's hand found the doorframe. Rain hissed on the slates; she counted three breaths before she spoke.</p></div>
      <span class="eg">Illustrative example</span>
    </div>
  </section>

  <section class="show rev rv" id="prompt">
    <div class="txt">
      <div class="eyebrow">Prompt Manager</div>
      <h2 class="sec">Decide exactly what the model sees</h2>
      <p>Reorder prompt blocks by dragging, send a block only when a condition is true, preview the real request and watch how much of it the provider can cache.</p>
      <ul class="ticks"><li>Conditions: keywords, tracker values, chance, cooldown…</li><li>Guided chain-of-thought steps with their own models</li><li>Text rules that change only what is sent</li></ul>
      <a class="more" href="docs/prompt-manager.html">Prompt Manager guide →</a>
    </div>
    <div class="vis">
      <div class="pm">
        <div class="row"><u>⠿</u><em>☑</em>Main prompt</div>
        <div class="row"><u>⠿</u><em>☑</em>World Info</div>
        <div class="row cond"><u>⠿</u><em>☑</em>Injury rules <span class="chip">only when health &lt; 30</span></div>
        <div class="row mod"><u>⠿</u><em>☑</em>Memory graph <span class="chip">module</span></div>
        <div class="row"><u>⠿</u><em>☑</em>Chat history</div>
        <div class="cache"><small>Cache: shared start of the request</small><div class="bar"><i style="width:82%"></i></div><small>82% reused from the previous request</small></div>
      </div>
    </div>
  </section>

  <section class="show rv" id="atmosphere">
    <div class="txt">
      <div class="eyebrow">Scene Painter · Music</div>
      <h2 class="sec">See it. Hear it.</h2>
      <p>A text model turns the last messages into an image prompt and your backend draws it — with character avatars as reference photos. Music is picked by the meaning of the scene, locally, from your own tracks.</p>
      <ul class="ticks"><li>Pollinations (free), OpenAI-compatible, Automatic1111</li><li>🎨 button under every reply, or paint automatically</li><li>Your files or direct audio links</li></ul>
      <a class="more" href="docs/scene-painter.html">Scene Painter guide →</a>
    </div>
    <div class="vis">
      <div class="frame"><div class="art"></div><small>Harbour alley, rain</small></div>
      <div class="player"><b>♪</b><div><span>Rain on the Docks</span><div class="bar"><i style="width:38%"></i></div></div></div>
    </div>
  </section>

  <section id="more">
    <div class="eyebrow">And more</div>
    <h2 class="sec">Small modules for particular needs</h2>
    <div class="chips rv">
      <a href="docs/notebook-secrets.html"><b>Notebook &amp; Secrets</b><span>The AI's own memory, and facts only some characters know</span></a>
      <a href="docs/speaker-colors.html"><b>Speaker Colors</b><span>Every character's dialogue in their own colour</span></a>
      <a href="docs/map.html"><b>Map</b><span>A world map with distances and travel time</span></a>
      <a href="docs/lorebook-macros.html"><b>Lorebook &amp; Macros</b><span>Edit World Info; use live values anywhere</span></a>
      <a href="docs/chat-viewport.html"><b>Chat Viewport</b><span>An experimental chat view and a desktop home</span></a>
      <a href="docs/sync-backup-updates.html"><b>Sync &amp; backups</b><span>Between devices, via your own cloud account</span></a>
      <a href="docs/models.html"><b>Any model</b><span>OpenAI-compatible, Anthropic, Gemini — or SillyTavern's own</span></a>
      <a href="docs/introduction.html"><b>Mea, the guide</b><span>Lives inside the engine and walks you through the first start</span></a>
    </div>
  </section>

  <section id="safe">
    <div class="eyebrow">Built with care</div>
    <h2 class="sec">Your story is safe</h2>
    <div class="trio rv">
      <div><b>Nothing is deleted</b><p>Summaries hide old messages, they never remove them. Text rules change only what is sent. If prompt assembly ever fails, the original request goes through.</p></div>
      <div><b>Modules stay in their lane</b><p>A module can only reach what its rights allow, through gates — it cannot touch the network or SillyTavern directly.</p></div>
      <div><b>Your data stays yours</b><p>Everything runs in your browser. Optional sync goes straight to your own Google Drive, Dropbox or GitHub.</p></div>
    </div>
  </section>

  <section id="sync">
    <div class="eyebrow">Cloud sync &amp; Google sign-in</div>
    <h2 class="sec">About the optional sync</h2>
    <div class="card rv"><div class="card-body">
      <p>ST Module Engine is an extension for <a href="https://github.com/SillyTavern/SillyTavern">SillyTavern</a>. It adds modules, a generation pipeline, a memory graph and, optionally, synchronization of your SillyTavern files between your own devices.</p>
      <p>The optional cloud synchronization lets you sign in with your own Google Drive or Dropbox account so that your files can be kept in step on all your devices. Nothing is sent to the author of the extension: the extension runs entirely inside your browser and talks to your cloud account directly.</p>
      <p><a href="privacy.html">Privacy policy</a> · <a href="terms.html">Terms of service</a> · <a href="https://github.com/IAmiGOI/Module-Engine">Source code and issue tracker</a></p>
    </div></div>
  </section>

  <div class="final rv">
    <h2>Add it to SillyTavern in thirty seconds</h2>
    <p class="lead" style="margin:0 auto 22px">Copy the link, then Extensions → Install extension → paste → Install.</p>
    <div class="cta">{cpbtn("primary big", "Copy install link")}<a class="btn big" href="docs/quick-start.html">Quick start guide</a></div>
  </div>
</main>
""" + foot("")

# ---------------------------------------------------------------- install
def install():
    def copy(t): return f'<div class="copy"><span>{t}</span><button class="btn sm" type="button">Copy</button></div>'
    return head("Install — ST Module Engine", "How to install ST Module Engine into SillyTavern: by pasting the repository link into the in-app installer.", "") + nav("", "install") + f"""
<main>
  <div class="legal" style="max-width:860px">
    <div class="eyebrow">Install</div>
    <h1>Install ST Module Engine</h1>
    <p class="lead">It takes thirty seconds, and the engine updates itself afterwards.</p>

    <div class="note"><b>You need:</b> a working <a href="https://github.com/SillyTavern/SillyTavern">SillyTavern</a> (a recent release) and a browser. A model connection is needed for most features — the setup guide inside the engine helps with that on first launch.</div>

    <h2>Install from inside SillyTavern</h2>
    <ol class="steps">
      <li><h3>Open the installer</h3><p>In SillyTavern click the <b>Extensions</b> icon (stacked cubes) → <b>Install extension</b>.</p></li>
      <li><h3>Paste the repository link</h3><p>{cpbtn('primary sm', 'Copy link')}</p>{copy(REPO)}<p>Leave the branch empty and press <b>Install for all users</b> (or <b>Install just for me</b>).</p></li>
      <li><h3>Reload the page</h3><p>The loading screen now shows <b>ST × ME</b>. The engine's dock appears on the right edge of the screen — hover it to open the panel.</p></li>
    </ol>

    <h2>First launch</h2>
    <ol class="steps">
      <li><h3>Meet Mea</h3><p>On the very first start the built-in guide opens by itself and walks you through a short checklist.</p></li>
      <li><h3>Connect a model</h3><p>Choose <b>Use SillyTavern's current connection</b> for the quickest start, or enter your own API key and endpoint. See <a href="docs/models.html">Model connections</a>.</p></li>
      <li><h3>Turn modules on</h3><p>Open <a href="docs/modules.html">Modules</a> and switch on what you want — Tracker and RP Time are good first picks.</p></li>
    </ol>

    <h2>Updating</h2>
    <p>The engine checks for new versions itself: open the <b>Updates</b> card on the settings screen and press install. You can also use SillyTavern's own extension manager.</p>
    <h2>Uninstalling</h2>
    <p>Open <b>Extensions → Manage extensions</b>, find <b>ST Module Engine</b> and remove it. Your chats and characters are never touched.</p>

    <h2>Something went wrong?</h2>
    <ul>
      <li><b>No dock after reload</b> — reload the page and check that the extension is enabled in <b>Extensions → Manage extensions</b>.</li>
      <li><b>Features do nothing</b> — a model connection is missing or down. See <a href="docs/troubleshooting.html">Troubleshooting</a>.</li>
      <li>Still stuck? Open an <a href="{REPO}/issues">issue on GitHub</a>.</li>
    </ul>
  </div>
</main>
""" + foot("")

# ---------------------------------------------------------------- docs
def read_page(path):
    raw = path.read_text(encoding="utf-8")
    m = re.match(r"---\n(.*?)\n---\n(.*)", raw, re.S)
    meta = dict(l.split(": ", 1) for l in m.group(1).splitlines() if ": " in l)
    return meta, m.group(2)

def render_md(md, text):
    # <a class="mini"> cards: python-markdown only reads block elements, so go through a div and swap back
    text = re.sub(r'<a class="mini" href="([^"]+)" markdown="1">(.*?)</a>', r'<div class="mini" data-href="\1" markdown="1">\2</div>', text, flags=re.S)
    # <ol class="steps"><li> -> divs (li is not a block python-markdown reads into)
    text = text.replace('<ol class="steps">', '<div class="steps" markdown="1">').replace('</ol>', '</div>')
    text = text.replace('<li markdown="1">', '<div class="step" markdown="1">').replace('</li>', '</div>')
    md.reset()
    out = md.convert(text)
    out = re.sub(r'<div class="mini" data-href="([^"]+)">(.*?)</div>', r'<a class="mini" href="\1">\2</a>', out, flags=re.S)
    return out

def docs():
    md = markdown.Markdown(extensions=["tables", "fenced_code", "sane_lists", "md_in_html"])
    pages = []
    for f in sorted((ROOT / "tools" / "pages").glob("*.md")):
        meta, text = read_page(f)
        body = render_md(md, text)
        heads = []
        def addid(m):
            t = re.sub(r"<[^>]+>", "", m.group(1)); i = slug(t)
            heads.append((i, html.unescape(t)))
            return f'<h2 id="{i}">{m.group(1)}</h2>'
        body = re.sub(r"<h2>(.*?)</h2>", addid, body)
        pages.append(dict(meta, slug=f.stem, body=body, heads=heads, order=int(meta.get("order", 99))))
    pages.sort(key=lambda p: p["order"])
    index = []
    outdir = ROOT / "docs"; outdir.mkdir(exist_ok=True)

    def sidebar(cur):
        groups = {}
        for q in pages: groups.setdefault(q["group"], []).append(q)
        h = f'<a class="{"on" if cur == "index" else ""}" href="index.html">Documentation home</a>'
        for g in GROUPS:
            h += f"<h4>{g}</h4>" + "".join(f'<a class="{"on" if q["slug"] == cur else ""}" href="{q["slug"]}.html">{html.escape(q["title"])}</a>' for q in groups.get(g, []))
        return h

    def shell(title, desc, cur, inner, toc=""):
        return head(f"{title} — ST Module Engine docs", desc, "../") + nav("../", "docs") + f"""
<main class="docs">
  <aside class="side">
    <input class="search" data-base="" type="search" placeholder="Search docs  ( / )" aria-label="Search docs">
    <div class="results"></div>
    <div class="side-nav">{sidebar(cur)}</div>
  </aside>
  <article class="article">{inner}</article>
  <aside class="toc">{toc}</aside>
</main>
""" + foot("../")

    for n, p in enumerate(pages):
        glance = ""
        if p.get("needs") or p.get("where") or p.get("id"):
            items = [("Needs", p.get("needs")), ("Find it", p.get("where")), ("Module id", p.get("id"))]
            glance = '<div class="glance">' + "".join(f"<div><small>{k}</small><span>{v if k != 'Module id' else '<code>' + html.escape(v) + '</code>'}</span></div>" for k, v in items if v) + "</div>"
        # first paragraph is the lead
        body = re.sub(r"<p>", '<p class="lead">', p["body"], count=1)
        prev_ = pages[n - 1] if n else None
        next_ = pages[n + 1] if n + 1 < len(pages) else None
        pager = '<div class="pager">' + (f'<a href="{prev_["slug"]}.html"><small>← Previous</small>{html.escape(prev_["title"])}</a>' if prev_ else "<span></span>") + \
                (f'<a class="nx" href="{next_["slug"]}.html"><small>Next →</small>{html.escape(next_["title"])}</a>' if next_ else "") + "</div>"
        inner = f'<div class="eyebrow">{p["group"]}</div><h1>{html.escape(p["title"])}</h1>{glance}{body}{pager}'
        toc = ("<b>On this page</b>" + "".join(f'<a href="#{i}">{html.escape(t)}</a>' for i, t in p["heads"])) if p["heads"] else ""
        (outdir / f'{p["slug"]}.html').write_text(shell(p["title"], p["desc"], p["slug"], inner, toc), encoding="utf-8")
        index.append(dict(title=p["title"], url=f'{p["slug"]}.html', text=re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", html.unescape(p["body"])))))

    # docs home
    bycat = {}
    for q in pages: bycat.setdefault(q["group"], []).append(q)
    start = [q for q in pages if q["slug"] in ("quick-start", "concepts", "models")]
    big = "".join(f'<a class="mini big" href="{q["slug"]}.html"><b>{html.escape(q["title"])}</b><p>{html.escape(q["desc"])}</p></a>' for q in start)
    tasks = [("Track health, mood and location", "tracker"), ("Make a long chat fit the context", "summary"), ("Clean up the writing of replies", "postprocess"),
             ("Illustrate a scene", "scene-painter"), ("Control the prompt precisely", "prompt-manager"), ("Fix an error", "troubleshooting")]
    tk = "".join(f'<a class="task" href="{u}.html">{html.escape(t)} <span>→</span></a>' for t, u in tasks)
    topics = ""
    for g in GROUPS:
        qs = bycat.get(g, [])
        if not qs or g == "Start here": continue
        topics += f'<h2 class="sec-h">{g}<small>{GROUP_BLURB[g]}</small></h2><div class="cards">' + "".join(f'<a class="mini" href="{q["slug"]}.html"><b>{html.escape(q["title"])}</b><p>{html.escape(q["desc"])}</p></a>' for q in qs) + "</div>"
    inner = f"""<div class="eyebrow">Documentation</div><h1>Learn Module Engine</h1>
<p class="lead">Everything you need to install, set up and get the most out of the engine — written around what you want to do, not around the settings screen.</p>
<h2 class="sec-h">Start here<small>{GROUP_BLURB["Start here"]}</small></h2><div class="cards big3">{big}</div>
<h2 class="sec-h">I want to…</h2><div class="tasks">{tk}</div>{topics}"""
    (outdir / "index.html").write_text(shell("Documentation", "Install, set up and use ST Module Engine: guides for every module, memory, prompts and troubleshooting.", "index", inner), encoding="utf-8")
    (outdir / "search-index.json").write_text(json.dumps(index, ensure_ascii=False), encoding="utf-8")
    # drop pages of the previous doc layout
    keep = {f'{p["slug"]}.html' for p in pages} | {"index.html"}
    for old in outdir.glob("*.html"):
        if old.name not in keep: old.unlink()

# ---------------------------------------------------------------- legal pages (text untouched, restyled)
def restyle_legal(name, cur_title):
    """Text of the legal pages is never touched: only the shell (head/nav/footer) is regenerated around it."""
    src = ROOT / name
    raw = src.read_text(encoding="utf-8")
    t = re.search(r"<title>(.*?)</title>", raw, re.S).group(1)
    if 'class="legal"' in raw:  # already wrapped: take the inner text back out
        inner = re.search(r'<div class="legal">(.*?)</div></main>', raw, re.S).group(1)
    else:
        inner = re.search(r"<body>(.*?)</body>", raw, re.S).group(1).replace("<h1>", '<div class="eyebrow">Legal</div><h1>', 1)
    page = head(t, f"{cur_title} for the ST Module Engine extension.", "") + nav("", "") + f'<main><div class="legal">{inner}</div></main>' + foot("")
    src.write_text(page, encoding="utf-8")

if __name__ == "__main__":
    (ROOT / "index.html").write_text(landing(), encoding="utf-8")
    (ROOT / "install.html").write_text(install(), encoding="utf-8")
    docs()
    restyle_legal("privacy.html", "Privacy policy")
    restyle_legal("terms.html", "Terms of service")
    print("built")
