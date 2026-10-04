---
title: Widget reference
group: Development
desc: The widget library — every ready-made building block available to module interfaces.
order: 45
---
Widgets are **pure functions**: data in, tree out. They live in `libraries/shared/widgets.js` and an external module imports them from `stme:widgets`. Controls take **signals** and write back into them.

```js
import { Section, Field, Row, TextInput, Select, Toggle, Slider, Button } from 'stme:widgets';
```

## Layout

| Widget | Signature | What it is |
|---|---|---|
| `Section` | `Section(title, options, ...children)` | A flat collapsible section — the standard container |
| `Card` | `Card(title, options, ...children)` | A top-level framed card (accent title, gradient header) |
| `Row` | `Row(...children)` | Children side by side |
| `Field` | `Field(label, control, { hint })` | A label, a control and optional hint text |
| `TwoColumn` | `TwoColumn({ left, right })` | A two-column layout |
| `Details` | `Details(summary, ...children)` | A native collapsible block |
| `EdgeDrawer` | `EdgeDrawer(open, { onToggle, title, side }, ...children)` | A drawer attached to a screen edge |
| `Overlay` | `Overlay(visibleSignal, { title, description, children })` | A modal overlay |

## Inputs

| Widget | Signature | Notes |
|---|---|---|
| `Button` | `Button(label, onClick, { variant, disabled })` | `variant`: `'default'` or `'danger'` (a red frame) |
| `IconButton` | `IconButton(icon, onClick, { active, title, disabled })` | An icon-only button |
| `HoldButton` | `HoldButton(label, onConfirm, { holdMs, variant, disabled })` | Must be held to confirm — for destructive actions |
| `TextInput` | `TextInput(signal, { placeholder, type, onInput })` | A one-line field |
| `TextArea` | `TextArea(signal, { placeholder, rows })` | A multi-line field |
| `NumberInput` | `NumberInput(signal, { min, max, step })` | A number field |
| `Slider` | `Slider(label, signal, { min, max, step })` | A slider with the live value beside its label |
| `Toggle` | `Toggle(label, checkedSignal, { hint, onChange })` | A switch for **state** |
| `Select` | `Select(signal, options, { onChange })` | `options` is `[{ value, label }]` (can be a signal) |
| `ColorPicker` | `ColorPicker(signal, { onChange })` | A colour field |

## Display

| Widget | Signature | What it is |
|---|---|---|
| `Badge` | `Badge(text, { tone })` | A small status label |
| `Chip` | `Chip(label, { title, onClick })` | A small clickable tag |
| `StatBlock` | `StatBlock(label, valueSignal, { icon, onClick, title, showLabel, showValue })` | A labelled live value |
| `ProgressBar` | `ProgressBar(percent, label)` | A progress bar |
| `Spinner` | `Spinner({ size })` | A loading indicator |
| `EmptyState` | `EmptyState(text)` | A friendly "nothing here" line |
| `Banner` | `Banner(textSignal, { tone, icon, action, actionLabel, busy, detail, onDismiss })` | A notice with an optional action |
| `Toast` | `Toast(text, { tone, onDismiss, key })` | One toast; `tone`: `ok`, `error`, `muted`… |
| `Avatar` | `Avatar(url, { width, height, name, onError })` | A picture with a fallback |
| `Timestamp` | `Timestamp(text, { title })` | A formatted time |

## Lists

| Widget | Signature | What it is |
|---|---|---|
| `List` | `List(itemsSignal, renderItem)` | Renders a signal of items; give each item a stable `key` |
| `EditableList` | `EditableList({ items, renderItem, onAdd, addLabel, empty, actions })` | A list with an add button and an empty state |

## Floating UI

| Widget | Signature | What it is |
|---|---|---|
| `FloatingPanel` | `FloatingPanel(title, { … })` | A draggable always-on-screen window (the tracker's state window is one) |
| `FloatingStack` | `FloatingStack(itemsSignal, { corner, renderItem })` | A stack of floating items in a screen corner |
| `DockButton` | `DockButton(icon, { position, drag, title })` | A draggable round button |

## Chat-specific

`MessageHeader`, `MessageActionsRow`, `ReasoningBlock`, `GenStripe` and `StatBlock` build the pieces of the engine's own chat view. They are meant for cores and the Chat Viewport rather than ordinary modules.

## A form in one screen

```js
tree: () => Section('My module', {},
    Field('Name', TextInput(name, { placeholder: 'Who?' })),
    Field('Mode', Select(mode, [{ value: 'fast', label: 'Fast' }, { value: 'deep', label: 'Deep' }])),
    Toggle('Enabled', enabled, { hint: 'Turn the whole module on or off.' }),
    Slider('Strength', strength, { min: 0, max: 1, step: 0.05 }),
    Row(Button('Save', save), Button('Reset', reset, { variant: 'danger' })),
)
```

<div class="note tip" markdown="1">
Need something new? A reusable element is written into the widget library at once, not "for now" in a module — a consumer holds only the wiring, never its own markup.
</div>
