#!/usr/bin/env python3
"""Generates the static site: index.html, install.html, docs/*.html, search-index.json.
Docs come from the engine's own guide articles (Client/Release/guide/knowledge/*.md).
Usage: python3 tools/build.py [path/to/guide/knowledge]"""
import html, json, re, sys, pathlib
import markdown

ROOT = pathlib.Path(__file__).resolve().parent.parent
KB = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else "/home/amigo/Module Engine/Client/Release/guide/knowledge")
REPO = "https://github.com/IAmiGOI/Module-Engine"

DOCS = [  # (group, slug, source file, title override, one-line description)
    ("Getting started", "overview", "engine-overview.md", "Overview", "What Module Engine is and how its parts fit together."),
    ("Getting started", "models", "models.md", "Model connections", "Connect the models the engine uses for its own calls."),
    ("Getting started", "modules", "modules.md", "Modules", "Turn features on and off."),
    ("Modules", "tracker", "tracker.md", "Tracker", "Values that update themselves: health, mood, location…"),
    ("Modules", "rp-time", "rp-time.md", "RP Time", "An in-world clock worked out from the chat."),
    ("Modules", "notebook-secrets", "notebook-secrets.md", "Notebook & Secrets", "Working memory and who-knows-what."),
    ("Modules", "postprocess", "postprocess.md", "Post-Turn Processor", "Rewrite every reply through a chain of passes."),
    ("Modules", "music", "music.md", "Music", "Background music that follows the scene."),
    ("Modules", "scene-painter", "scene-painter.md", "Scene Painter", "Paint the current scene into a picture."),
    ("Modules", "speaker-colors-map", "speaker-colors-map.md", "Speaker Colors & Map", "Coloured dialogue and a world map."),
    ("Memory & prompts", "summary-memory", "summary-memory.md", "Chat Summary & memory graph", "Long chats that still fit the context."),
    ("Memory & prompts", "lorebook-macros", "lorebook-macros.md", "Lorebook & Macros", "World Info and the values you can use in prompts."),
    ("Memory & prompts", "prompt-manager", "prompt-manager.md", "Prompt Manager", "Build the request the way you want it."),
    ("Interface & data", "chat-viewport-home", "chat-viewport-home.md", "Chat Viewport & desktop", "The engine's own chat view and home screen."),
    ("Interface & data", "preset-sync-updates", "preset-sync-updates.md", "Preset, sync, updates", "Back up, sync between devices, update."),
    ("Help", "troubleshooting", "troubleshooting.md", "Troubleshooting", "When something does not work."),
]

# the guide articles are written for an in-app assistant too; keep only what a reader needs
DROP_PAR = re.compile(r"for the user yourself|Write them as full briefs|do not pin one at random|You can read and explain|never mention them", re.I)
DROP_SENT = re.compile(r"\s*When you add passes for someone, check auto-run and offer to turn it on\.")

def clean(md):
    md = re.sub(r"\A---.*?---\s*", "", md, flags=re.S)                       # front matter
    md = re.sub(r"\[([^\]]+)\]\(stme:[^)]+\)", r"**\1**", md)               # in-app links -> bold
    md = md.replace("(know this before you build or advise)", "")
    md = md.replace("## How it really works ", "## How it works")
    md = re.sub(r"(module id:? )(module\.\w+)", r"\1`\2`", md, flags=re.I)
    md = DROP_SENT.sub("", md)
    md = md.replace(" (the state below tells you which)", "").replace(" — still say it in your own words if it matters", "")
    out = []
    for block in re.split(r"\n(?=- |\n)", md):
        if DROP_PAR.search(block):
            continue
        out.append(block)
    md = "\n".join(out)
    md = re.sub(r"(?m)^([^\s\-].*[^\n])\n(- )", r"\1\n\n\2", md)  # markdown needs a blank line before a list
    md = re.sub(r"\n{3,}", "\n\n", md)
    # first paragraph before any heading becomes the intro; keep as-is
    return md.strip()

MODULES_PAGE = """Modules are switched on and off in the **Modules** card; each module's own settings appear there once it is on. Most modules need a working [model connection](models.html).

Good first modules: **Tracker** (watch values like health or mood update by themselves) and **RP Time** (an in-world clock).

## All modules

| Module | What it does | Id |
|---|---|---|
| [Tracker](tracker.html) | Keeps named values up to date and publishes them as macros | `module.tracker` |
| [RP Time](rp-time.html) | Works out the in-world time from the chat | `module.time` |
| [Notebook](notebook-secrets.html) | Private working memory the AI writes to | `module.notebook` |
| [Secrets](notebook-secrets.html) | Hidden facts tagged with who knows them | `module.secrets` |
| [Post-Turn Processor](postprocess.html) | Rewrites each reply through a chain of passes | `module.postprocess` |
| [Music](music.html) | Background music that follows the scene | `module.music` |
| [Scene Painter](scene-painter.html) | Paints the current scene into a picture | `module.scenePainter` |
| [Speaker Colors](speaker-colors-map.html) | Colours dialogue by speaker | `module.speakerColors` |
| [Map](speaker-colors-map.html) | A floating world map with distances | `module.map` |
"""

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
    {a("docs/overview.html", "Docs", "docs")}
    <a class="l" href="{REPO}">GitHub</a>
  </nav>
  {cpbtn("primary sm dl", "Copy install link")}
</header>
"""

def foot(base):
    return f"""<footer>
  <div>© AmiGO · Free, open-source. Not affiliated with SillyTavern.</div>
  <nav><a href="{base}docs/overview.html">Docs</a><a href="{base}install.html">Install</a><a href="{base}privacy.html">Privacy policy</a><a href="{base}terms.html">Terms</a><a href="{REPO}/issues">Issues</a><a href="{REPO}">GitHub</a></nav>
</footer>
<script src="{base}assets/site.js"></script>
</body>
</html>
"""

# ---------------------------------------------------------------- landing
FEATURES = [
    ("Generation pipeline", "Takes over generation", "The engine sits in SillyTavern's generation path. It can hold a reply until a tracker has answered, rewrite it afterwards, or cancel it."),
    ("Model connections", "Bring any model", "OpenAI-compatible, Anthropic, Google Gemini — or just reuse the model SillyTavern is already connected to. Parallel requests, health checks, automatic failover."),
    ("Tracker", "Values that update themselves", "Health, mood, location — anything. A cheap model keeps them current and publishes them as macros like <code>{{tracker_health}}</code>."),
    ("RP Time", "An in-world clock", "Works out the story's time from the chat, shows a badge under replies and keeps the model aware of it."),
    ("Post-Turn Processor", "Polish every reply", "A chain of independent rewrite passes — clean clichés, fix style, check continuity — each with its own prompt and model."),
    ("Chat Summary & memory graph", "Long chats that fit", "Old messages fold into leveled summaries (never deleted). A memory graph tracks people, places and facts."),
    ("Prompt Manager", "Own the request", "Reorder prompts, send blocks only when conditions are true, inspect tokens and cache hits, add Guided CoT steps and text rules."),
    ("Scene Painter", "Paint the scene", "A text model writes the image prompt, a backend draws it — Pollinations, OpenAI-compatible or Automatic1111/Forge. Avatars can be used as references."),
    ("Music", "Soundtrack that follows", "Tracks are matched to the scene by meaning, locally. Your own files or direct audio links."),
    ("Notebook & Secrets", "Working memory", "A private notebook the AI writes to, and hidden facts tagged with who knows them."),
    ("Speaker Colors & Map", "Colour and place", "Dialogue coloured per character, and a full-screen world map with distances and travel time."),
    ("Lorebook & Macros", "Your world, editable", "See and edit World Info the engine sees; every tracker value becomes a macro for any prompt."),
    ("Sync & backups", "Your data, your devices", "Sync settings and chats between devices through your own Google Drive, Dropbox or GitHub. Nothing passes through a server of ours."),
    ("Mea, the built-in guide", "Ask, don't search", "A guide living inside the engine knows every setting and walks you through the first start."),
]

def landing():
    cards = "\n".join(
        f'<div class="card rv"><div class="card-head"><strong>{t}</strong><small>{s}</small></div><div class="card-body"><p>{b}</p></div></div>'
        for t, s, b in FEATURES)
    return head("ST Module Engine — modules, pipeline and memory for SillyTavern",
                "ST Module Engine is a SillyTavern extension: a modular engine with trackers, memory graph, prompt manager, scene painter, music and more.", "") + nav("", "") + f"""
<main>
  <div class="hero">
    <div class="marks"><img class="st" src="assets/st-logo.png" alt="SillyTavern"><span>×</span><img class="me" src="assets/me-logo.webp" alt="Module Engine"></div>
    <h1>Turn SillyTavern into a<br><span class="grad">modular roleplay engine</span></h1>
    <p class="lead">ST Module Engine is an extension that adds a generation pipeline, trackers, long-term memory, a prompt manager, pictures, music and more — as small modules you switch on when you want them.</p>
    <div class="cta">
      {cpbtn("primary big", "Copy install link")}
      <a class="btn big" href="install.html">Install guide</a>
    </div>
    <div class="meta">Paste it in SillyTavern → Extensions → Install extension · free &amp; open source</div>
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

  <section id="features">
    <div class="eyebrow">Features</div>
    <h2 class="sec">Everything is a module. Switch on what you need.</h2>
    <p class="lead">Most features make their own model calls on the side, separate from the roleplay reply — so a cheap fast model can do the bookkeeping while your favourite model writes the story.</p>
    <div class="grid">{cards}</div>
  </section>

  <section id="architecture">
    <div class="eyebrow">Architecture</div>
    <h2 class="sec">Built like a small operating system</h2>
    <p class="lead">Every layer only talks to the next one through gates and rights, so a module can never touch the network or SillyTavern directly — and a SillyTavern update only ever breaks one layer.</p>
    <div class="layers rv">
      <div class="layer"><div class="n">1</div><div><strong>Runner</strong><p>The entry point. Starts everything in order and remembers which modules you switched on.</p></div></div>
      <div class="layer"><div class="n">2</div><div><strong>Services</strong><p>The only layer that touches SillyTavern, the DOM, the network and timers. All ST-specific code lives here.</p></div></div>
      <div class="layer"><div class="n">3</div><div><strong>Libraries</strong><p>Shared building blocks: buses, queues, stores, UI primitives.</p></div></div>
      <div class="layer"><div class="n">4</div><div><strong>Cores</strong><p>The engine's own parts: model connections, memory, summaries, lorebook, sync, prompt pipeline, UI.</p></div></div>
      <div class="layer"><div class="n">5</div><div><strong>Modules</strong><p>The features you toggle: Tracker, RP Time, Notebook, Music, Scene Painter, Map…</p></div></div>
    </div>
  </section>

  <section id="sync">
    <div class="eyebrow">Cloud sync &amp; Google sign-in</div>
    <h2 class="sec">Your files stay yours</h2>
    <div class="card rv"><div class="card-body">
      <p>ST Module Engine is an extension for <a href="https://github.com/SillyTavern/SillyTavern">SillyTavern</a>. It adds modules, a generation pipeline, a memory graph and, optionally, synchronization of your SillyTavern files between your own devices.</p>
      <p>The optional cloud synchronization lets you sign in with your own Google Drive or Dropbox account so that your files can be kept in step on all your devices. Nothing is sent to the author of the extension: the extension runs entirely inside your browser and talks to your cloud account directly.</p>
      <p><a href="privacy.html">Privacy policy</a> · <a href="terms.html">Terms of service</a> · <a href="https://github.com/IAmiGOI/Module-Engine">Source code and issue tracker</a></p>
    </div></div>
  </section>

  <section id="start">
    <div class="eyebrow">Get started</div>
    <h2 class="sec">Up and running in three steps</h2>
    <ol class="steps rv">
      <li><h3>Install</h3><p>In SillyTavern open <b>Extensions → Install extension</b> and paste the repository link and press Install.</p><p><a href="install.html">Full installation guide →</a></p></li>
      <li><h3>Connect a model</h3><p>The quickest start: reuse SillyTavern's current connection with one click. Add a cheaper separate model later if you like.</p><p><a href="docs/models.html">Model connections →</a></p></li>
      <li><h3>Switch on modules</h3><p>Open the engine from the dock on the right edge of the screen. Good first picks: Tracker and RP Time. Mea, the built-in guide, helps on the first launch.</p><p><a href="docs/modules.html">Modules →</a></p></li>
    </ol>
  </section>

  <div class="final rv">
    <h2>Ready to try it?</h2>
    <p class="lead" style="margin:0 auto 22px">Free, open source and runs entirely in your browser.</p>
    <div class="cta">{cpbtn("primary big", "Copy install link")}<a class="btn big" href="{REPO}">{ICON_GH} View on GitHub</a></div>
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
def docs():
    md = markdown.Markdown(extensions=["tables", "fenced_code", "sane_lists"])
    pages, index = [], []
    for group, sl, src, title, desc in DOCS:
        md.reset()
        text = MODULES_PAGE if sl == "modules" else clean((KB / src).read_text(encoding="utf-8"))
        body = md.convert(text)
        # ids on h2 for the in-page nav
        heads = []
        def addid(m):
            t = re.sub(r"<[^>]+>", "", m.group(1)); i = slug(t)
            heads.append((i, html.unescape(t)))
            return f'<h2 id="{i}">{m.group(1)}</h2>'
        body = re.sub(r"<h2>(.*?)</h2>", addid, body)
        # the first paragraph (before any heading) is the module's own summary
        pages.append(dict(group=group, slug=sl, title=title, desc=desc, body=body, heads=heads))
        index.append(dict(title=title, url=f"docs/{sl}.html", text=re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", html.unescape(body)))))

    (ROOT / "docs").mkdir(exist_ok=True)
    for n, p in enumerate(pages):
        groups = {}
        for q in pages: groups.setdefault(q["group"], []).append(q)
        side = "".join(
            f'<h4>{g}</h4>' + "".join(f'<a class="{"on" if q["slug"] == p["slug"] else ""}" href="{q["slug"]}.html">{html.escape(q["title"])}</a>' for q in qs)
            for g, qs in groups.items())
        toc = "".join(f'<a href="#{i}">{html.escape(t)}</a>' for i, t in p["heads"])
        prev_ = pages[n - 1] if n else None
        next_ = pages[n + 1] if n + 1 < len(pages) else None
        pager = '<div class="pager">' + (f'<a href="{prev_["slug"]}.html"><small>← Previous</small>{html.escape(prev_["title"])}</a>' if prev_ else "<span></span>") + \
                (f'<a class="nx" href="{next_["slug"]}.html"><small>Next →</small>{html.escape(next_["title"])}</a>' if next_ else "") + "</div>"
        page = head(f'{p["title"]} — ST Module Engine docs', p["desc"], "../") + nav("../", "docs") + f"""
<main class="docs">
  <aside class="side">
    <input class="search" data-base="" type="search" placeholder="Search docs  ( / )" aria-label="Search docs">
    <div class="results"></div>
    <div class="side-nav">{side}</div>
  </aside>
  <article class="article">
    <div class="eyebrow">{p["group"]}</div>
    <h1>{html.escape(p["title"])}</h1>
    {p["body"]}
    {pager}
  </article>
  <aside class="toc">{"<b>On this page</b>" + toc if toc else ""}</aside>
</main>
""" + foot("../")
        (ROOT / "docs" / f'{p["slug"]}.html').write_text(page, encoding="utf-8")
    # search index lives next to the docs so data-base="" resolves
    (ROOT / "docs" / "search-index.json").write_text(json.dumps([dict(i, url=i["url"].split("/")[-1]) for i in index], ensure_ascii=False), encoding="utf-8")

# ---------------------------------------------------------------- legal pages (text untouched, restyled)
def restyle_legal(name, cur_title):
    src = ROOT / name
    raw = src.read_text(encoding="utf-8")
    if "assets/site.css" in raw:  # already restyled — extract original body
        return
    m = re.search(r"<body>(.*?)</body>", raw, re.S)
    t = re.search(r"<title>(.*?)</title>", raw, re.S).group(1)
    inner = m.group(1).replace("<h1>", '<div class="eyebrow">Legal</div><h1>', 1)
    page = head(t, f"{cur_title} for the ST Module Engine extension.", "") + nav("", "") + f'<main><div class="legal">{inner}</div></main>' + foot("")
    src.write_text(page, encoding="utf-8")

if __name__ == "__main__":
    (ROOT / "index.html").write_text(landing(), encoding="utf-8")
    (ROOT / "install.html").write_text(install(), encoding="utf-8")
    docs()
    restyle_legal("privacy.html", "Privacy policy")
    restyle_legal("terms.html", "Terms of service")
    print("built")
