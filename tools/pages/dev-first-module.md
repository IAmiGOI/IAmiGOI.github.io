---
title: Writing a module
group: Development
desc: The anatomy of a module — header, factory, lifecycle, imports, rights and how it is installed.
order: 41
---
A module is **one JavaScript file**, `index.js`. It has a header comment that describes it, and a default-exported factory that gives the engine the module's behaviour.

## The smallest module

```js
/*@module
id: community.hello
title: Hello (example)
description: A tiny example module. Safe to remove.
version: 1.0.0
engine: ^0.2
rights: ui.notify
*/
import { h } from 'stme:ui/tree';
import { signal } from 'stme:ui/reactive';
import { Button } from 'stme:widgets';
import { request } from 'stme:request';

export default function create(host) {
    const clicks = signal(0);

    async function sayHello() {
        clicks.set(clicks.peek() + 1);
        await request(host.cores, 'ui.notify', { params: { tone: 'ok', text: `Hello! (${clicks.peek()})` } });
    }

    return {
        async load() {},
        tree: () => h('div', {}, Button('Say hello', sayHello)),
        stop() {},
    };
}
```

This is the real example module in the catalog repository. Everything a module is made of is in it.

## 1. The header

The very first thing in the file is a `/*@module … */` block of `key: value` lines. It is read **as text, without running anything**, so a stranger's module can be inspected safely.

| Key | Meaning | Required |
|---|---|---|
| `id` | Unique id. External modules **must** start with `community.`; `module.*` belongs to built-ins | yes |
| `version` | Semver, e.g. `1.2.0` | yes |
| `title`, `description` | Shown on the module's card | no |
| `engine` | Range of engine versions it works with, e.g. `^0.2` | no |
| `requires` | Other modules or cores it needs, e.g. `module.tracker@^1.0, core.map@>=0.3` | no |
| `rights` | Contracts it asks permission to use — a comma-separated list | no |
| `network` | `true` if it needs the network (only *requested*, never granted automatically) | no |

A line may end in a comma to continue on the next one, and lines starting with `#` are comments — useful to explain why each right is needed.

## 2. The factory

`export default function create(host)` is called once. It receives the **host** — everything the module may use to reach the rest of the engine — and returns an object:

| Member | When it runs |
|---|---|
| `load()` | When the user switches the module on. Restore saved state, subscribe, do first work |
| `tree()` | Returns the module's settings UI, shown on its card (see [UI primitives](dev-ui.html)) |
| `stop()` | When it is switched off. **Unsubscribe from everything you subscribed to** |

Whatever else you return (`id`, `title`, …) is optional for external modules; the header already says it.

## 3. The host

`host` is how a module reaches the world:

| Part | Use |
|---|---|
| `host.cores` | Ask a core for something — `request(host.cores, 'model.generate', { params })` |
| `host.services` | Ask a service — DOM, chat, SillyTavern events (needs matching rights) |
| `host.network` | The only path to the internet (needs the network right) |
| `host.events` | The event bus: `subscribe(name, callback)` returns an unsubscribe function, `emit(name, payload)` |
| `host.own` | The module's home bus |

A module **never** touches SillyTavern, the DOM or the network directly. Every request goes through a bus and is checked against the module's rights. See [Contracts & buses](dev-contracts.html).

## 4. Imports

An external module may import only these four paths, written as `stme:<path>`:

| Import | Gives you |
|---|---|
| `stme:ui/tree` | `h()` — builds UI nodes |
| `stme:ui/reactive` | `signal`, `computed`, `effect` |
| `stme:widgets` | The widget library — Button, Toggle, Select, Section… |
| `stme:request` | `request(bus, contract, options)` |

Any other import — a URL, `data:`, a relative path — is a violation and the module does not load. The engine replaces `stme:` paths with real addresses when it prepares the source, and runs exactly the text that was hashed and scanned.

## 5. Rights

`rights:` lists every contract the module will call. Check the list against your code: a call outside it is refused, and for an external module it **quarantines** the module (see [Runtime](dev-runtime.html)).

<div class="note warn" markdown="1">
**What the scanner rejects.** The text is scanned before it runs. `eval`, `new Function`, `import()`, computed global access like `window["x"]`, and `constructor.constructor` stop the module from loading. `fetch`, `XMLHttpRequest`, `WebSocket`, `localStorage`/`indexedDB`, `getContext()` and even the word *SillyTavern* in your source make it *scanned-unsafe*. Keep those words out of comments and strings too.
</div>

## 6. Conventions

- **Reactive state in signals, created once.** Never create a signal inside a render function: the next render subscribes to a stale one.
- **Persist through the storage contracts**, with a namespace equal to your module id.
- **Return failures, do not throw them across the bus.** Every `request()` resolves to an envelope `{ ok, value }` or `{ ok: false, error }` — check `ok`.
- **Clean up in `stop()`.**

## Install and run

1. Put the module file in a repository folder, for example `modules/dice/index.js`.
2. In the engine open **Modules → Install a module**, paste the repository link (or `owner/repo`, or a `…/tree/<ref>/<dir>` link).
3. **Preview** shows the header, requested rights, scan findings, the file's SHA-256 and the trust level — nothing is installed yet.
4. **Install**, then switch the module on. It is switched on separately.

The catalog repository is `IAmiGOI/Module-Engine-Modules`: confirmed modules live in `modules/<name>/index.js`, and a `third-party.txt` lists links to other people's modules.

**Next:** build the [Dice](dev-example-dice.html) module step by step.
