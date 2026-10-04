---
title: Development overview
group: Development
desc: How Module Engine is built, where the code lives and what you can build on top of it.
order: 40
---
Module Engine is built like a small operating system, and you can extend it: **modules** are small plugins that add features, and they run on the same engine as the built-in ones — Tracker, RP Time, Music and the rest are all modules.

This section is for people who want to write a module, or understand how the engine works inside. It is written from the engine's own design documents and its source.

<div class="cards" markdown="1">

<a class="mini" href="dev-first-module.html" markdown="1">
**Write a module**
The anatomy of a module: header, factory, lifecycle, rights.
</a>

<a class="mini" href="dev-runtime.html" markdown="1">
**Runtime**
How the Runner finds, checks, loads and isolates modules.
</a>

<a class="mini" href="dev-contracts.html" markdown="1">
**Contracts & buses**
How a module asks the engine for things, safely.
</a>

<a class="mini" href="dev-ui.html" markdown="1">
**UI primitives**
Signals, the tree, and how rendering works.
</a>

<a class="mini" href="dev-widgets.html" markdown="1">
**Widgets**
Ready-made building blocks for module interfaces.
</a>

<a class="mini" href="dev-typing.html" markdown="1">
**Typing**
Type checking with JSDoc — no TypeScript, no build step.
</a>

<a class="mini" href="dev-testing.html" markdown="1">
**Testing**
Unit tests and whole-engine scenario tests.
</a>

<a class="mini" href="dev-example-dice.html" markdown="1">
**Three example modules**
Dice, Reply Meter and Scene Weather — from easy to advanced.
</a>

</div>

## The five layers

<div class="layers" markdown="0">
<div class="layer"><div class="n">1</div><div><strong>Runner</strong><p>The entry point. Starts everything in order — Services, Libraries, Cores, Modules — and remembers which modules you switched on.</p></div></div>
<div class="layer"><div class="n">2</div><div><strong>Services</strong><p>The only layer that touches SillyTavern, the DOM, the network and timers. Each service is a separate file with its own version.</p></div></div>
<div class="layer"><div class="n">3</div><div><strong>Libraries</strong><p>Pure helpers with no state and no outside world: parsing, queues, widgets.</p></div></div>
<div class="layer"><div class="n">4</div><div><strong>Cores</strong><p>The engine's real logic: models, memory, summaries, lorebook, tracking, sync, UI. They never touch SillyTavern directly, and never each other directly — only through a bus.</p></div></div>
<div class="layer"><div class="n">5</div><div><strong>Modules</strong><p>The features a user switches on. Almost all infrastructure — waiting for conditions, picking a provider, reconciling — lives below and is invisible to a module.</p></div></div>
</div>

**Core or module?** One test: *a user installs a module; the engine does not work without a core.* The engine's own interface is a core; Notebook, Music and your Dice are modules — the engine runs fine if nobody installed them.

## Design priorities

When two decisions conflict, these win, in this order:

1. **Simple to write a module** — an author writes the minimum of infrastructure code.
2. **Full customisation** — any layer can be replaced or extended without touching the rest.
3. **Simple, dynamic connections with hot-swap**, handled by the core — a module never writes its own subscription or reconciliation code.
4. **Almost any modules can connect** to each other, with no artificial walls.
5. **Safe against SillyTavern changes** — everything SillyTavern-specific is isolated in one layer (Services).
6. **Plug and play** — the top priority.

## Where things live

```
modules/<name>/index.js     modules (one folder each)
cores/<domain>/index.js     cores
services/<name>.js          services
libraries/{core,module,shared}/<name>.js
styles/                     CSS, split by area
tests/                      unit and scenario tests
```

The documents behind this section ship with the engine: `ARCHITECTURE.md`, `RUNTIME.md`, `CONVENTIONS.md`, `UI.md`, `TYPING.md`, `TESTING.md`, `LIBRARIES.md`, `CORES.md`.

The three example modules in this section are real code: each was run against the engine's own widget library and request helper with a fake host, and passes the same header parser and scanner that the Runner uses (all three come out as *scanned-safe*).

## Set up a place to experiment

Run a separate test SillyTavern on its own port, install the engine there, and keep your personal instance untouched. Modules you write can be dropped in as a single `index.js` and installed from a repository link, so the loop is: edit, install, enable, look at the Modules card.

<div class="note tip" markdown="1">
**Naming.** Contract names are `<domain>.<capability>` in camelCase — `model.generate`, `storage.settings.get`. A domain is the *capability*, never the name of a particular provider, so any core can serve a contract. See [Contracts & buses](dev-contracts.html).
</div>
