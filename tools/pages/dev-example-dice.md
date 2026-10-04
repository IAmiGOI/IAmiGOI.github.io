---
title: Example 1 · Dice (easy)
group: Development
desc: A first module in 40 lines — signals, widgets, one contract call. Build it step by step.
order: 50
needs: Nothing
id: community.dice
---
**Level: easy.** A die with a configurable number of sides, a **Roll** button, a short history and a toast with the result. It teaches the four things every module is made of: the header, a signal, a few widgets, and one call to the engine.

## What you will learn

- Writing the **header** and choosing **rights**
- Holding state in **signals**
- Building an interface with **widgets**
- Calling a **contract** and reading its envelope

## The whole module

```js
/*@module
id: community.dice
title: Dice
description: Rolls a die and keeps the last few results.
version: 1.0.0
engine: ^0.2
rights: ui.notify
*/
import { h } from 'stme:ui/tree';
import { signal, computed } from 'stme:ui/reactive';
import { Button, EmptyState, Field, NumberInput, Row, Section } from 'stme:widgets';
import { request } from 'stme:request';

/** Pure: a roll of an n-sided die. Kept outside the factory so it can be tested alone. */
export const rollDie = (sides, random = Math.random) => 1 + Math.floor(random() * sides);

export default function create(host) {
    const sides = signal(20);
    const history = signal([]);   // newest first: { id, sides, value }

    async function roll() {
        const n = Math.max(2, Math.floor(sides.peek()) || 20);
        const value = rollDie(n);
        history.update(list => [{ id: Date.now(), sides: n, value }, ...list].slice(0, 8));
        await request(host.cores, 'ui.notify', { params: { tone: 'ok', text: `d${n} → ${value}` } });
    }

    return {
        async load() {},
        tree: () => Section('Dice', {},
            Field('Sides', NumberInput(sides, { min: 2, max: 1000 })),
            Row(Button('Roll', () => { void roll(); })),
            computed(() => (history().length
                ? history().map(item => h('div', { key: item.id }, `d${item.sides} → ${item.value}`))
                : [EmptyState('No rolls yet.')])),
        ),
        stop() {},
    };
}
```

## Step by step

<ol class="steps">
<li markdown="1">
### The header
`id: community.dice` — external modules must start with `community.`. `rights: ui.notify` — the only contract this module calls. If you call something that is not in this list, the module is quarantined.
</li>
<li markdown="1">
### Pure logic first
`rollDie` takes the random source as a parameter, so a test can pass a fixed one. Keep logic like this **outside** the factory, in plain functions.
</li>
<li markdown="1">
### State in signals
`sides` and `history` are created **once**, in the factory — never inside `tree()`. `history.update(fn)` writes from the previous value. `sides.peek()` reads without subscribing, which is what you want inside an event handler.
</li>
<li markdown="1">
### The tree
`tree()` returns widgets: `Section` is the container, `Field` pairs a label with a control, `NumberInput` is bound to the `sides` signal (typing updates it), `Button` runs `roll`. The list is a `computed` — it re-renders when `history` changes, and each item has a stable `key`.
</li>
<li markdown="1">
### One contract call
`request(host.cores, 'ui.notify', { params: { tone: 'ok', text } })` shows a toast. It resolves to an envelope and never throws; here we ignore the result because a missed toast is harmless. The next examples check `ok`.
</li>
</ol>

## Try it

1. Put the file at `modules/dice/index.js` in a repository.
2. **Modules → Install a module**, paste the link, check the preview (it should say *scanned-safe* and show the one right), **Install**, switch it on.
3. Open its card, press **Roll**.

## Make it yours

- Replace `NumberInput` with a `Select` of common dice (`d4`, `d6`, `d20`, `d100`).
- Roll several dice at once and show the sum.
- Add a `Toggle('Announce rolls', announce)` and only call `ui.notify` when it is on.

**Next:** [Reply Meter](dev-example-meter.html) — events, saved settings and reading the chat.
