---
title: Core concepts
group: Start here
desc: The handful of ideas that make every other page easy to understand.
order: 3
---
Five ideas explain almost everything in Module Engine.

## 1. Modules — the features you toggle

A **module** is one feature: Tracker, RP Time, Music, Scene Painter and so on. Each is switched on or off in the **Modules** card, and its settings appear only after it is on. Modules cannot reach the network or SillyTavern directly — they only get what their *rights* allow, through gates. That is why a misbehaving module cannot break your chats.

## 2. Cores — the engine's own parts

**Cores** are what modules stand on: model connections, chat memory, summaries, the lorebook, sync, the prompt pipeline, the interface. You rarely touch them directly — they appear as **cards** in the engine panel (Model connections, Chat Summary, Lorebook, Sync, Updates…).

<div class="layers-mini" markdown="1">
**Runner** starts everything → **Services** touch SillyTavern, the page and the network → **Libraries** share building blocks → **Cores** do the engine's work → **Modules** are the features you see.
</div>

## 3. Model connections — who does the side jobs

A **model connection** (internally a *worker*) is a model the engine may call: format, endpoint, key, model name. Features pick a connection, or leave it on *Default* and the engine uses any working one. Every connection is health-checked, and unstable ones automatically get fewer requests. [More →](models.html)

<div class="note tip" markdown="1">
**Rule of thumb.** Let your best model write the story in SillyTavern. Give the side jobs (trackers, summaries, clean-up passes) to a cheap, fast one.
</div>

## 4. Macros — values you can use anywhere

When a tracker or RP Time knows something, it publishes it as a **macro** — a placeholder such as `{{tracker_health}}` that you can write into any SillyTavern prompt, character card or lorebook entry. The text is replaced with the current value when the prompt is built. The **Macros** card lists every macro that exists right now. [More →](lorebook-macros.html)

## 5. Nothing is deleted

The engine is careful with your story:

- summaries **hide** old messages from the prompt, they never delete them;
- text rules change only **what is sent**, never your saved chat;
- tracker values are saved **per message**, so rerolling or going back shows the value of that moment;
- if the engine's prompt assembly ever fails, the original SillyTavern request is sent instead.

## Where things live

| Place | What is there |
|---|---|
| **Dock** (right edge, hover) | Opens the engine panel, the music player, the map and other windows |
| **Engine panel** | Cards: Modules, Model connections, Chat Summary, Memory graph, Lorebook, Macros, Chat Viewport… |
| **Settings screen** | Preset (export/import), Sync, Updates, Backgrounds |
| **Under replies** | Time badge and the 🎨 Paint button |
| **Floating windows** | Tracker values, clock, music player, picture, map |
| **Mea (the guide)** | A chat of her own — never mixed into your roleplay chats |
