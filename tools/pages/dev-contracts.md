---
title: Contracts, buses & events
group: Development
desc: How modules and cores talk — contracts, the four buses, the envelope, request(), events, blocks and errors.
order: 43
---
Nothing in the engine calls anything else directly. A caller asks for a **capability** by name over a **bus**; a provider registers to answer it. The bus finds the provider, applies the rights check, and delivers the answer — and the caller never needs to know who answered.

## Contracts

A **contract** is a pre-declared request/response shape, addressed by name.

- **Name:** `<domain>.<capability>[.<detail>]`, lowercase, camelCase inside a segment — `model.generate`, `storage.settings.get`, `worldInfo.entries`, `tracking.value`, `pipeline.run`.
- **The domain is the capability, not a provider.** `model.generate` can be served by the internal-models core, a local-host core or SillyTavern's own connection; the caller asks for the capability and never a particular core.
- **A contract name is finite and never changes at runtime.** Do not bake a dynamic id into a name (`tracker:field:<id>:<name>`). Use a fixed name — `tracking.value` — and pass the dynamic part as a parameter: `{ blockId, fieldName }`.

## The buses

| Bus | Carries | Reached through |
|---|---|---|
| **Events** | Broadcast pub/sub — a "dumb transport" | `host.events` |
| **Modules** | Module ↔ module | `host.modules` (cores) |
| **Cores** | Core ↔ core, and modules asking cores | `host.cores` |
| **Services** | The only path to SillyTavern, the DOM, timers | `host.services` |
| **Network** | The only path to the internet (`http.*` contracts) | `host.network` |

Each bus plays **director** for its own domain: it decides **who** answers (by the provider's declared load), **when** the answer is delivered (waiting on a condition or event), and **in what format** if a contract can be implemented in several ways.

A **gate** sits at each crossing between domains. The gate is where rights are really checked.

## The envelope

Every delivery has exactly one shape:

```
{ ok: true,  value: <result> }
{ ok: false, error: { message, code? } }
```

The bus never throws across its boundary: any exception inside a provider is caught and converted. One failing subscriber never disturbs the others. Always check `ok`:

```js
const result = await request(host.cores, 'chatHistory.messages', { params: { limit: 4 } });
if (!result.ok) return;          // result.error.message says why
const messages = result.value;
```

## `request()`

`request(bus, contract, options)` is sugar over `subscribe()`: subscribe once, resolve on the first delivery, unsubscribe automatically. It **never rejects**.

| Option | Meaning |
|---|---|
| `params` | The contract's input |
| `when` | A condition for delivery (below) |
| `timeoutMs` | For "completion"-type conditions only; on timeout resolves with an error envelope |
| `priority` | Handed to the provider next to the caller's identity (`'pipeline'` marks a call on the generation's critical path) |

### `when` conditions

| Field | Meaning |
|---|---|
| `event` | Deliver when this event happens |
| `every` | Every N-th event, or `{ event, count, ms }` — or on a timer |
| `debounceMs`, `throttleMs` | Rate-shape the delivery |
| `dedupe` | Skip repeats of the same value |
| `once` | Deliver once, then stop |

## Events

Events travel on the event bus. Native SillyTavern events are brought in by a thin service and arrive as `st.*`; the engine and modules add their own.

```js
const off = host.events.subscribe('generation.completed', payload => { /* … */ });
// later, in stop():
off();
```

Events you can rely on include: `st.chatChanged`, `st.messageSwiped`, `st.messageDeleted`, `generation.beforeSend`, `generation.completed`, `model.workers.changed`, `tracking.poll.completed`, `settings.changed`, `summary.folded`.

**Names** follow the thing they describe: a block `tracking.blocks` announces changes as `tracking.blocks.changed`. For operations that are slow, fallible or touch SillyTavern, a triple is used — `<contract>.started`, `.completed`, `.failed` — so an observer never has to guess a DOM timing.

## Blocks

A **block** is a category of entries inside a bus — "the tracker fields that can be inserted", "the published lorebook entries". When a block's content changes, its owner emits one `<block>.changed` event for the whole block; a consumer re-requests the content with an ordinary `request()`. The **taxonomy of block categories** belongs to the engine: a module registers its block under an official category name and any consumer of that category picks it up, with no change to anyone else's code. The pipeline's stage registry is a block: `pipeline.stages.add` writes to it, `pipeline.stagesChanged` announces it.

## Identity and rights

A caller **cannot know or forge its own rights**. Its own bus knows them from the moment it registered, and the gate checks them. Rights are *flat* — one set per module, not per contract.

## Contracts a module commonly uses

These are real contracts; each needs its name in the header's `rights:` list.

| Contract | Input → output |
|---|---|
| `ui.notify` | `{ tone, text, … }` → shows a toast (`tone`: `ok`, `error`, `muted`…) |
| `storage.settings.get` | `{ namespace, key, fallback }` → the stored value |
| `storage.settings.set` | `{ namespace, key, value }` → `true`. Publishes `settings.changed` |
| `chatHistory.messages` | `{ limit }` → messages `{ mesid, isUser, name, text, … }` |
| `chatHistory.replaceText`, `.annotate`, `.annotations` | Edit a message's text, attach and read per-message notes |
| `model.generate` | `{ prompt, systemPrompt, workerId, temperature, maxTokens, stream, … }` → the model's text. `model.generate.cancel` aborts by `requestId` |
| `macros.setValue`, `macros.clearValue` | `{ name, value }` / `{ name }` → publish or remove a `{{macro}}` |
| `tracking.poll`, `tracking.reset`, `tracking.trackers` | Drive the Tracker core |
| `pipeline.stages.add`, `pipeline.stages.remove` | Add or remove a stage in a generation pipeline |
| `promptManager.contribute` | Give the Prompt Manager a block |
| `ui.messageFooter.claim`, `.release` | Own a strip under a message |

<div class="note" markdown="1">
Contracts are **untyped** for now: the bus does not know that `storage.settings.get` takes `{ namespace, key, fallback }`. A contract map is the most valuable next step and will be introduced contract by contract. See [Typing](dev-typing.html).
</div>

## Errors

- A provider's exception becomes `{ ok: false, error }` — never a thrown error for the caller.
- A **rights violation** is quiet: the module is quarantined and the user sees a mark on its card only.
- An ordinary runtime error (a bug) is visible **locally on the module's card** as its last error — not as a global toast.
- Logging an error uses the same point as the audit log; it is not a separate system.

## Persistence

Settings and per-chat data go through the storage contracts, namespaced (`<module id>` is the convention). Do not use browser storage: the scanner flags it as *unsafe*, and the engine's storage cores also keep your data syncable between devices.
