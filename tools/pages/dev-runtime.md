---
title: Runtime (the Runner)
group: Development
desc: How the Runner discovers, checks, orders, loads and isolates modules — trust levels, scanning, quarantine, the catalog.
order: 42
---
The **Runner** is the engine's entry point. It starts everything in a fixed order — **Services → Libraries → Cores → Modules** — and it owns the answers to "which modules exist", "in what order do they load", "with what rights" and "why did one not load".

The Runner does not switch modules on by itself: that is the user's choice, saved by the registry and restored at the next start. An unknown id in the saved list is skipped silently — the build may have changed between launches, and failing at start because a module is gone would be the worst possible behaviour.

## Where modules come from

| Origin | How it is read | Rights |
|---|---|---|
| **Built-in** (`modules/*`) | Source read as text only for the header; code is imported normally | The header's `rights` list, as a *community*-level caller — a built-in module takes the same path as a third-party one |
| **Installed** (from a repository) | Source text stored with the module, so launching needs no network | By trust level, from the scan result |

A failure in one module — a bad header, a failed scan, a missing dependency — never stops the others. It lands in the **Could not load** list with a reason.

## The header, in detail

```
/*@module
id: community.dice
title: Dice
description: Rolls dice on request.
version: 1.2.0
engine: ^0.2
requires: module.tracker@^1.0, core.map@>=0.3
rights: tracking.poll, ui.notify
network: false
*/
```

- `id` and `version` are required; `engine`, `requires`, `rights` and `network` default to empty / `false`.
- For built-in modules `rights` is the requested set. For external ones it is only a **request** — the final rights depend on the trust level.
- The hash and the scan are computed over the same text that is later executed.

## Loading order and dependencies

`requires` lists modules and cores with semver ranges (`module.tracker@^1.0`; without `@` any version). The Runner sorts modules so that dependencies load first, checks the ranges, and refuses a module whose dependency is missing or too old. Version ranges follow semver, and a module's `engine` field is checked against the engine's own version.

## Trust levels

Every caller — module or core — is registered with a **trust tier**. The same mechanism serves both layers; first-party cores rarely need anything but the top tier.

| Tier | Meaning | Rights |
|---|---|---|
| `official` | Shipped by the engine | Effectively unrestricted |
| `community` | Reviewed and approved | An explicit allowed list |
| `scanned-safe` | Unreviewed; the scan found nothing dangerous | Everything not explicitly denied |
| `scanned-unsafe` | Unreviewed; the scan found risky patterns | Same, but more restricted |

Signed keys for the reviewed tier are deferred: for now external modules receive only the two scanned tiers.

For the scanned tiers the policy is **default-allow**: whatever the scan does not forbid is permitted. The scan decides the *tier*; the real boundary is the rights check at the gate.

## The scan

A static scan over the module's text — the code is never run. It is "the best possible", not a sandbox: it catches the obvious, and a determined author could evade it, which is why it only decides the trust level while the **gate** enforces rights.

| Finding | Severity | Effect |
|---|---|---|
| `eval`, `new Function`, `import()`, `importScripts` | block | The module does not load |
| Computed access to the global object, `constructor.constructor` | block | The module does not load |
| Any import other than `stme:<path>` | block | The module does not load |
| `fetch`, `XMLHttpRequest`, `WebSocket`, `EventSource`, `sendBeacon`, `RTCPeerConnection` | unsafe | Loads as *scanned-unsafe* |
| `localStorage`, `sessionStorage`, `indexedDB`, `document.cookie` | unsafe | Loads as *scanned-unsafe* |
| `window.parent`/`top`/`opener`, `document.write` | unsafe | Loads as *scanned-unsafe* |
| Direct SillyTavern access (`getContext(`, the word *SillyTavern*) | unsafe | Loads as *scanned-unsafe* |

False positives are acceptable (a worse tier, not a refusal). A miss is not, so the rules are deliberately coarse and run over the raw text.

## Network access

Network access is a **separate binary right**, not part of the trust level. It is physically a separate bus (`host.network`), not another gate on the services bus, so the check cannot be bypassed. A header's `network: true` is only a request; the user interface does not yet grant it to external modules.

## Quarantine

An external module is registered with *quarantine on violation*: any refusal by the gate — a contract outside its rights, an `http.request` without the network right — puts it in quarantine.

- It is recorded as `{ id, hash, contract, at }` and survives restarts.
- Quarantine is tied to the **id**, not the hash: a fixed version under the same name does not lift it, otherwise an author could change one byte to escape. Only the user can lift it — **Allow again** on the module's card.
- While quarantined a module is not loaded at start, is refused in the preview, and appears under **Could not load**.
- Built-in modules are never quarantined: they sometimes probe contracts they do not hold, and a silent refusal is the old behaviour.
- The user is not notified proactively. The violation shows on that module's card only.

The current response is not interrupted: the engine carries on, and generation is never aborted by a module's mistake.

## Installing from a repository

- **Preview installs nothing.** It downloads the text, parses the header, scans, computes SHA-256, and shows the trust level, requested rights, requested network, findings, and "replaces version X".
- The module is stored **with its source**, and re-parsed and re-scanned with the same analysis **on every start**.
- The user switches it on separately.
- **Limits:** source up to 512 KB; the id must start with `community.`.

The catalog repository holds confirmed modules (`modules/<name>/index.js`, one file each) and a `third-party.txt` with one link per line (`#` for comments). A link can be `owner/repo`, a repository URL, `…/tree/<ref>/<dir>` (takes `<dir>/index.js`) or `…/blob/<ref>/<file>.js`.

## An honest limit

There is **no sandbox**: an external module's JavaScript lives in the same page as SillyTavern. Protection is rights through the gate, the hash, the scan and quarantine — not isolation. Review what you install.
