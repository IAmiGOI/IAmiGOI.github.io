#!/usr/bin/env python3
"""Builds mea-worker/src/knowledge.json — the chunks Mea retrieves from — out of the docs sources.
Every chunk is one H2 section (or a page intro), capped in length, remembering the page it came from."""
import json, re, pathlib, html

ROOT = pathlib.Path(__file__).resolve().parent.parent
PAGES = ROOT / "tools" / "pages"
MAX = 1100
ROW_PAGES = {"glossary", "troubleshooting"}
ROW_HEADINGS = {"Where things live", "Reading connection states", "By symptom"}

def clean(md):
    md = re.sub(r"<[^>]+>", " ", md)                       # HTML shells (cards, figures, steps)
    md = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", md)      # links -> text
    md = re.sub(r"[*_`]{1,3}", "", md)
    md = re.sub(r"^\|?\s*[-:| ]{3,}\s*\|?\s*$", "", md, flags=re.M)   # table rules
    md = md.replace("|", " · ")
    md = re.sub(r"[ \t]+", " ", md)
    md = re.sub(r"\n{2,}", "\n", md)
    return html.unescape(md).strip()

def split(text):
    """Pack paragraphs into pieces of at most MAX characters."""
    out, cur = [], ""
    for para in [p.strip() for p in text.split("\n") if p.strip()]:
        while len(para) > MAX:
            cut = para.rfind(". ", 0, MAX) + 1 or MAX
            if cur: out.append(cur); cur = ""
            out.append(para[:cut].strip()); para = para[cut:].strip()
        if len(cur) + len(para) + 1 > MAX and cur:
            out.append(cur); cur = para
        else:
            cur = (cur + "\n" + para).strip()
    if cur: out.append(cur)
    return out

chunks = []
for f in sorted(PAGES.glob("*.md")):
    raw = f.read_text(encoding="utf-8")
    m = re.match(r"---\n(.*?)\n---\n(.*)", raw, re.S)
    meta = dict(l.split(": ", 1) for l in m.group(1).splitlines() if ": " in l)
    # code blocks are noise for retrieval, except in the example-module pages where they are the point
    body = re.sub(r"```.*?```", lambda c: c.group(0) if f.stem.startswith("dev-example") else "", m.group(2), flags=re.S)
    title, url = meta["title"], f"docs/{f.stem}.html"
    parts = re.split(r"(?m)^## (.+)$", body)
    sections = [("", parts[0])] + [(parts[i], parts[i + 1]) for i in range(1, len(parts) - 1, 2)]
    for heading, text in sections:
        # table-heavy sections (glossary, symptoms, "where things live") work best as one chunk per row
        if f.stem in ROW_PAGES or heading in ROW_HEADINGS:
            for line in text.splitlines():
                cells = [c.strip() for c in line.strip().strip("|").split("|")]
                if len(cells) >= 2 and not re.match(r"^[-: ]+$", cells[0]) and cells[0].lower() not in ("term", "symptom", "place", "state"):
                    label = re.sub(r"[*`]", "", cells[0])
                    body = clean(" — ".join(c for c in cells if c))
                    if len(body) > 25:
                        chunks.append({"title": f"{title} — {label}", "url": url, "text": body, "head": label, "page": title})
            continue
        text = clean(text)
        if len(text) < 30: continue
        anchor = re.sub(r"[^a-z0-9]+", "-", heading.lower()).strip("-") if heading else ""
        for piece in split(text):
            chunks.append({"title": title + (f" — {heading}" if heading else ""), "url": url + (f"#{anchor}" if anchor else ""),
                           "text": piece, "head": heading, "page": title})

# facts that live on the landing / install pages rather than in the docs
extra = [
    ("About Module Engine", "index.html", "ST Module Engine (ME) is an extension for SillyTavern. It adds a generation pipeline, trackers, long-term memory, a prompt manager, scene pictures, music and more, as small modules the user switches on. Your main model still writes the reply; around it, small cheap models do the bookkeeping — before, after and in the background. Nothing is deleted: summaries hide old messages, text rules change only what is sent. Everything runs in the browser; optional sync goes straight to the user's own cloud account.", True),
    ("Install", "install.html", "Install: in SillyTavern open Extensions, press Install extension, paste https://github.com/IAmiGOI/Module-Engine and install. Leave the branch empty. Reload the page — the loading screen shows ST × ME and the dock appears on the right edge of the screen. On the first launch the guide Mea opens by herself. Update later from the Updates tile. Remove from Extensions → Manage extensions; chats and characters are not touched.", False),
    ("Links", "index.html", "Source and issues: https://github.com/IAmiGOI/Module-Engine . Module catalog: https://github.com/IAmiGOI/Module-Engine-Modules . Site: https://iamigoi.github.io/ . The author is AmiGO.", False),
    ("License", "index.html", "The source code is viewable on GitHub under an All Rights Reserved license: you may view it, but copying, modification and redistribution need the author's permission.", False),
]
extra += [
    ("Cost and price", "docs/faq.html", "Is Module Engine free? The engine has no subscription of its own. Costs come from the model providers you connect (for example OpenAI or OpenRouter). Reusing SillyTavern's own connection, or a local model, adds no extra provider. Scene Painter can use the free Pollinations backend. The source code license is All Rights Reserved: viewable on GitHub, not freely copyable.", False),
    ("Remembering a long story", "docs/summary.html", "To make a very long chat fit the model's context, use Chat Summary: old messages fold into leveled summaries and are hidden from the prompt (never deleted); the newest messages stay untouched in a protected window. The Memory graph is a separate feature: a mind-map of people, places and facts with a Pathway view of what was recalled. The Notebook and Secrets tools are the AI's own working memory.", False),
    ("What is Jev", "docs/prompt-manager.html", "Jev is a small classifier. It gives the chance, 0 to 100 percent, that a statement you write is true, for example 'The player is in danger'. The Prompt Manager uses it in conditions ('Jev answers a question'), and Music can use it for Smart scene detection. Its connection is set in Models, in the Classifiers category.", False),
]
for title, url, text, core in extra:
    chunks.append({"title": title, "url": url, "text": text, "head": "", "page": title, "core": core, "boost": 0.6 if title == "Links" else 1.6})

out = ROOT / "mea-worker" / "src" / "knowledge.json"
out.write_text(json.dumps(chunks, ensure_ascii=False), encoding="utf-8")
print(len(chunks), "chunks,", out.stat().st_size // 1024, "KB; longest", max(len(c["text"]) for c in chunks))
