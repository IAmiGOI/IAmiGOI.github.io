---
title: Example 2 · Reply Meter (medium)
group: Development
desc: Listen to engine events, read the chat, keep derived state and persist settings.
order: 51
needs: Nothing
id: community.replyMeter
---
**Level: medium.** After every reply it counts the words, keeps a running average and, if you ask it to, nudges you when a reply comes out much shorter than your target. It adds **events**, **reading the chat**, **derived state**, **saved settings** and **cleanup**.

## What you will learn

- Subscribing to an **event** and unsubscribing in `stop()`
- Reading messages with `chatHistory.messages`
- **Checking `ok`** on every envelope
- Persisting settings with `storage.settings.get/set`
- `computed` for derived values

## The whole module

```js
/*@module
id: community.replyMeter
title: Reply Meter
description: Counts the words in each reply and nudges you when replies run short.
version: 1.0.0
engine: ^0.2
rights: chatHistory.messages, storage.settings.get, storage.settings.set, ui.notify
*/
import { h } from 'stme:ui/tree';
import { signal, computed } from 'stme:ui/reactive';
import { Button, Field, Row, Section, Slider, Toggle } from 'stme:widgets';
import { request } from 'stme:request';

const NAMESPACE = 'community.replyMeter';

/** Pure: words are runs of non-space characters. */
export const countWords = text => (String(text ?? '').match(/\S+/g) ?? []).length;

export default function create(host) {
    const ask = (contract, params) => request(host.cores, contract, { params });

    const target = signal(250);     // words
    const nudge = signal(true);
    const replies = signal(0);
    const totalWords = signal(0);
    const lastWords = signal(0);
    const average = computed(() => (replies() ? Math.round(totalWords() / replies()) : 0));

    async function loadSettings() {
        const saved = await ask('storage.settings.get', { namespace: NAMESPACE, key: 'settings', fallback: null });
        if (!saved.ok || !saved.value) return;                 // first run, or the store failed: keep defaults
        target.set(Number(saved.value.target) || 250);
        nudge.set(saved.value.nudge !== false);
    }

    async function saveSettings() {
        const saved = await ask('storage.settings.set', {
            namespace: NAMESPACE, key: 'settings', value: { target: target.peek(), nudge: nudge.peek() },
        });
        await ask('ui.notify', { tone: saved.ok ? 'ok' : 'error', text: saved.ok ? 'Reply Meter saved.' : saved.error.message });
    }

    async function onReplyCompleted() {
        const result = await ask('chatHistory.messages', { limit: 1 });
        const last = result.ok ? result.value?.[0] : null;
        if (!last || last.isUser) return;                      // count only the AI's replies
        const words = countWords(last.text);
        lastWords.set(words);
        replies.update(n => n + 1);
        totalWords.update(n => n + words);
        if (nudge.peek() && words < target.peek() / 2) {
            await ask('ui.notify', { tone: 'muted', text: `Short reply: ${words} words (target ${target.peek()}).` });
        }
    }

    const stopListening = host.events.subscribe('generation.completed', () => { void onReplyCompleted(); });
    const resetSession = () => { replies.set(0); totalWords.set(0); lastWords.set(0); };

    return {
        async load() { await loadSettings(); },
        tree: () => Section('Reply Meter', {},
            Slider('Target length (words)', target, { min: 50, max: 1000, step: 10 }),
            Toggle('Nudge me when a reply is much shorter', nudge, { hint: 'Below half of the target.' }),
            Field('This session', h('div', {}, computed(() => `Last reply ${lastWords()} words · average ${average()} over ${replies()} replies`))),
            Row(Button('Save', () => { void saveSettings(); }), Button('Reset session', resetSession)),
        ),
        stop() { stopListening(); },
    };
}
```

## What is new

<ol class="steps">
<li markdown="1">
### Events
`host.events.subscribe('generation.completed', cb)` returns an **unsubscribe function**. Keep it, and call it in `stop()` — a module that forgets leaves a live handler behind after the user switches it off.
</li>
<li markdown="1">
### A small `ask` helper
All calls go to `host.cores` with the same shape, so one line wraps them. The contract and its params are the only things that change.
</li>
<li markdown="1">
### Always check `ok`
`const last = result.ok ? result.value?.[0] : null;` — if the chat could not be read, there is simply nothing to count. Settings loading does the same: a failed read leaves the defaults. Never assume `value` exists.
</li>
<li markdown="1">
### Persisting
`storage.settings.set` takes `{ namespace, key, value }`. The namespace is the module id, so two modules never collide. Reading back uses `fallback: null` to tell "never saved" from "saved".
</li>
<li markdown="1">
### Derived state
`average` is a `computed` of two signals; the status line is a computed string. Nothing recomputes by hand — change a signal and the screen follows.
</li>
</ol>

<div class="note tip" markdown="1">
**Your messages are filtered out.** `chatHistory.messages` returns messages with `isUser`, so the meter counts only the AI's side. If the last message were yours, there would be nothing to measure yet.
</div>

## Try it

Install, switch on, set a high target, and chat. A toast appears when a reply is under half the target. Switch the module off — the handler is removed.

## Make it yours

- Keep the numbers **per chat**: listen to `st.chatChanged` and reset the session there.
- Show the **longest** reply as well as the average.
- Turn the nudge into a *prompt contribution* so the model itself is reminded about length (see the pipeline stage contracts in [Contracts](dev-contracts.html)).

**Next:** [Scene Weather](dev-example-weather.html) — calling a model, publishing a macro and cancelling work.
