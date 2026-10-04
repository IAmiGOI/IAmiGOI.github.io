---
title: UI primitives
group: Development
desc: Signals, the abstract tree, and how a module's interface is rendered without touching the DOM.
order: 44
---
A module never touches the DOM. It returns a **tree** — plain data describing the interface — and the engine's final-UI core applies it to the real page, with every DOM call passing through the same rights check as any other request. The result: widgets and whole modules can be tested without a browser, as data.

```
UI core (primitives)       reactive.js · tree.js · diff.js — signals, h(), diffing
        ↓
Widget library             libraries/shared/widgets.js — pure functions: data → tree
        ↓
Consumers                  the engine panel, your module
        ↓
Final UI core              the only thing that touches the DOM — and only through a gate
```

## Signals

A **signal** is a reactive value. Reads are tracked; writes re-run every dependent, **synchronously** — there is no batching or scheduler.

```js
import { signal, computed, effect } from 'stme:ui/reactive';

const count = signal(0);
count();                 // read (tracked if called inside computed/effect)
count.peek();            // read without tracking
count.set(5);            // write
count.update(n => n + 1) // write from the previous value

const doubled = computed(() => count() * 2);   // re-evaluates only when count changes

const dispose = effect(() => console.log(count()));  // runs now and on every change
dispose();                                            // after this it never runs again
```

| Function | Behaviour |
|---|---|
| `signal(initial)` | A reactive value. `set` with an identical value (`Object.is`) does nothing |
| `computed(fn)` | A signal derived from the signals `fn` read last time |
| `effect(fn)` | Runs `fn` now and again when anything it read changes; returns a dispose function |

<div class="note warn" markdown="1">
**Never create a signal inside a render function.** A signal made inside `renderItem` lives shorter than the node that reads it; on the next render the node stays subscribed to the old one. Keep a map `id → signal` with a **stable key** and create each signal once. This bit the engine twice.
</div>

## `h()` — the tree

```js
import { h } from 'stme:ui/tree';

h('div', { class: 'row', key: item.id },
    h('span', {}, item.name),
    h('button', { 'on:click': () => remove(item.id) }, 'Remove'),
);
```

`h(tag, props, ...children)` returns `{ tag, props, children }`. Children are flattened; `null`, `undefined` and `false` are dropped.

| Props | Meaning |
|---|---|
| `class`, `style`, attributes | Plain properties |
| `key` | A **stable** identity for list items — an id, not an array position |
| `on:<event>` | A DOM handler — `'on:click'`, `'on:input'`, `'on:pointerdown'` …; the event type is inferred from the name |

A **prop value or a child may itself be a signal**. The renderer resolves it and updates only that spot when it changes:

```js
h('p', {}, computed(() => `Clicked ${count()} times`))
h('ul', {}, computed(() => items().map(item => h('li', { key: item.id }, item.name))))
```

## Rendering

`render(node, onPatch)` (in `diff.js`) turns a tree into a stream of patches that the final UI core applies, diffing against the previous tree so only what changed is touched. You do not call it in a module: you return a tree from `tree()` and the engine mounts it.

## The rules behind the interface

Almost every rule here is a conclusion from a concrete mistake that was already made.

**Layers.** No core and no module touches the DOM. A widget is a pure function: no state, no bus access, no right to save anything. If a widget needs memory (is it collapsed?) it is *given* a signal and a callback.

**Hierarchy by fill, not borders.** Only the top level — a `Card` — draws a border. Everything inside is a flat `Section`. Nesting is shown by **depth of fill** (`--stme-level-1..3`, deeper = darker), taken from real DOM nesting, never set by hand. Inputs are lighter than their surface, otherwise a dark field on a dark background stops reading as a field.

**Colour.** One accent, `--stme-accent`, taken from the SillyTavern theme (`--SmartThemeQuoteColor`). Accent only on section titles; titles inside are plain and bright, because two blues on one screen compete.

**Buttons.** Meaning is carried by the **outline**, with live white or accent text. Danger is a red frame with white text. No fill on hover — the outline brightens and softly pulses (the pulse is removed for `prefers-reduced-motion`).

**State vs action.** State is a `Toggle`; an action is a `Button`. A button "Enable" makes you guess whether the label is the current state or the effect of a click. A number with clear limits is a `Slider` with the live value next to its label.

**Collapsing.** Everything collapses — section → module → its records — using native `<details>`/`<summary>`, **collapsed by default**, with the state remembered per consumer. Each collapsible has a **stable key** (the record id), or the state moves to a neighbour when you add an item. Buttons inside a `<summary>` must stop click propagation, or "Remove" also collapses the card.

**Style tokens.** Styles live in `styles/` as tokens on `:root` (accent, radii `14 / 9 / 7`, danger `#f5232f`, ok `#3f9e72`), not as scattered rules. Override SillyTavern by **specificity**, repeating the shape of its selector, never with `!important`.
