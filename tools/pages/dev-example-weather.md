---
title: Example 3 · Scene Weather (advanced)
group: Development
desc: Ask a model after every reply, publish the answer as a {{macro}}, cancel stale work and surface errors.
order: 52
needs: A model connection
id: community.sceneWeather
---
**Level: advanced.** After each reply it asks a model for **one line about the weather and mood of the scene** and publishes it as the macro `{{scene_weather}}`, so any prompt, lorebook entry or character card can use it. It brings together everything from the other two examples and adds **calling a model**, **publishing a macro**, **cancelling stale work**, a **busy guard** and **error handling you can see**.

## What you will learn

- `model.generate` — prompts, system prompt, limits, `requestId`
- Publishing and clearing a macro with `macros.setValue` / `macros.clearValue`
- **Cancelling** an in-flight request when the chat changes
- Guarding against **overlapping** work
- Keeping pure helpers separate and testable
- Showing the last error instead of swallowing it

## The whole module

```js
/*@module
id: community.sceneWeather
title: Scene Weather
description: After each reply asks a model for one line of weather and mood, and publishes it as a macro.
version: 1.0.0
engine: ^0.2
rights: chatHistory.messages, model.generate, model.generate.cancel,
macros.setValue, macros.clearValue, storage.settings.get, storage.settings.set
*/
import { h } from 'stme:ui/tree';
import { signal, computed } from 'stme:ui/reactive';
import { Button, Field, Row, Section, Slider, TextArea, Toggle } from 'stme:widgets';
import { request } from 'stme:request';

const NAMESPACE = 'community.sceneWeather';
const MACRO = 'scene_weather';
const DEFAULT_INSTRUCTION = 'Read the roleplay excerpt and describe the weather and the mood of the scene '
    + 'in ONE short line, at most 15 words. Answer with that line only.';

/** Pure: whatever the model returned, as a clean single line. */
export function cleanLine(value) {
    const text = typeof value === 'string' ? value : value?.text ?? '';
    return text.replace(/\s+/g, ' ').replace(/^["'\s]+|["'\s]+$/g, '').slice(0, 160);
}

/** Pure: the user prompt, built from the last few messages. */
export function buildPrompt(messages) {
    return messages.map(message => `${message.name || (message.isUser ? 'User' : 'Character')}: ${message.text}`).join('\n\n');
}

export default function create(host) {
    const ask = (contract, params) => request(host.cores, contract, { params });

    const enabled = signal(true);
    const instruction = signal(DEFAULT_INSTRUCTION);
    const depth = signal(4);
    const current = signal('');       // the line published right now
    const lastError = signal('');
    const busy = signal(false);
    let activeRequestId = null;       // the in-flight model request, if any

    async function loadSettings() {
        const saved = await ask('storage.settings.get', { namespace: NAMESPACE, key: 'settings', fallback: null });
        if (!saved.ok || !saved.value) return;
        enabled.set(saved.value.enabled !== false);
        instruction.set(String(saved.value.instruction || DEFAULT_INSTRUCTION));
        depth.set(Number(saved.value.depth) || 4);
    }

    async function saveSettings() {
        await ask('storage.settings.set', {
            namespace: NAMESPACE, key: 'settings',
            value: { enabled: enabled.peek(), instruction: instruction.peek(), depth: depth.peek() },
        });
    }

    async function publish(line) {
        current.set(line);
        if (line) await ask('macros.setValue', { name: MACRO, value: line });
        else await ask('macros.clearValue', { name: MACRO });
    }

    async function refresh() {
        if (busy.peek()) return;                          // one request at a time
        busy.set(true);
        lastError.set('');
        const requestId = `scene-weather-${Date.now()}`;
        activeRequestId = requestId;
        try {
            const chat = await ask('chatHistory.messages', { limit: depth.peek() });
            if (!chat.ok || !chat.value?.length) return;
            const reply = await ask('model.generate', {
                requestId,
                systemPrompt: instruction.peek(),
                prompt: buildPrompt(chat.value),
                maxTokens: 60, temperature: 0.7, stream: false, reasoningMode: 'disabled',
            });
            if (activeRequestId !== requestId) return;    // cancelled or superseded: drop the answer
            if (!reply.ok) { lastError.set(reply.error.message); return; }
            await publish(cleanLine(reply.value));
        } finally {
            if (activeRequestId === requestId) activeRequestId = null;
            busy.set(false);
        }
    }

    async function onChatChanged() {
        if (activeRequestId) {
            const stale = activeRequestId;
            activeRequestId = null;                       // mark first, so the late answer is ignored
            await ask('model.generate.cancel', { requestId: stale });
        }
        await publish('');                                // the old chat's weather must not leak into the new one
    }

    const unsubscribers = [
        host.events.subscribe('generation.completed', () => { if (enabled.peek()) void refresh(); }),
        host.events.subscribe('st.chatChanged', () => { void onChatChanged(); }),
    ];

    return {
        async load() { await loadSettings(); },
        tree: () => Section('Scene Weather', {},
            Toggle('Update after every reply', enabled, { hint: 'Publishes the macro {{scene_weather}}.' }),
            Slider('Messages to read', depth, { min: 1, max: 12, step: 1 }),
            Field('Instruction', TextArea(instruction, { rows: 4 })),
            Row(Button('Refresh now', () => { void refresh(); }), Button('Save', () => { void saveSettings(); })),
            h('div', {}, computed(() => (busy() ? 'Asking the model…' : current() ? `Now: ${current()}` : 'No line yet.'))),
            computed(() => (lastError() ? h('small', { class: 'stme-module-hint' }, `Last error: ${lastError()}`) : null)),
        ),
        stop() {
            for (const off of unsubscribers) off();
            void ask('macros.clearValue', { name: MACRO });
        },
    };
}
```

## What is new

<ol class="steps">
<li markdown="1">
### Calling a model
`model.generate` takes a `systemPrompt` (your standing instruction) and a `prompt` (the data). `maxTokens`, `temperature`, `stream`, `reasoningMode` shape the answer; leave `workerId` out and the engine picks any working connection, or pin one. The envelope's `value` is the text. `cleanLine` is defensive about its shape and trims quotes and whitespace — and, being pure, can be unit tested without any engine.
</li>
<li markdown="1">
### Publishing a macro
`macros.setValue({ name, value })` makes `{{scene_weather}}` resolve to the line anywhere SillyTavern parses macros. `macros.clearValue({ name })` removes it. The engine caches the value, because SillyTavern resolves macros **synchronously** and cannot wait for a round trip.
</li>
<li markdown="1">
### Stale work
Every request gets a `requestId`. When the chat changes, the module marks the request as dead (`activeRequestId = null`) **before** cancelling, so a late answer is dropped by the `!== requestId` check instead of publishing the previous chat's weather. `model.generate.cancel` aborts the call itself.
</li>
<li markdown="1">
### The busy guard
`if (busy.peek()) return;` — a model call takes seconds and replies can arrive faster. The `finally` block always clears `busy`, even on the early returns.
</li>
<li markdown="1">
### Errors you can see
A failed envelope goes into a `lastError` signal and is shown on the card. A module's bug or a model failure should be **visible locally**, not a global toast and not silence.
</li>
<li markdown="1">
### Clean exit
`stop()` unsubscribes **both** handlers and clears the macro, so switching the module off leaves nothing behind.
</li>
</ol>

## Using the macro

Anywhere a prompt is parsed — a character card, a lorebook entry, a [Prompt Manager](prompt-manager.html) block:

> The scene right now: {{scene_weather}}. Let it colour your description.

<div class="note warn" markdown="1">
**Mind the cache.** A value that changes every message breaks the provider's prompt cache from the place it appears. Put the macro near the **end** of the request.
</div>

## Try it

Install and switch on (you need a [model connection](models.html)). Chat; after each reply the card shows the new line. Switch chats — the line clears.

## Where to go next

- Hold the generation until the line is ready by adding a **pipeline stage** (`pipeline.stages.add`) instead of reacting after the reply.
- Feed the line to the Prompt Manager with `promptManager.contribute`, so it is placed where the user chose.
- Keep one line **per chat** with `storage.settings` and a chat id as the key.
- Add a `// @ts-check` and the [typedefs](dev-typing.html) to catch shape mismatches early.
- Write a [scenario test](dev-testing.html) with a fake model that answers with a canned line.
