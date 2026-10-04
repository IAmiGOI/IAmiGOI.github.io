---
title: Lorebook & Macros
group: Memory & prompts
desc: See and edit the World Info the engine uses, and use live values anywhere with {{macros}}.
order: 16
needs: Nothing extra
where: Engine panel → Lorebook / Macros
---
Two cards that connect the engine to the way you already write prompts in SillyTavern.

## Lorebook

The **Lorebook** card shows the World Info entries the engine sees — **global, character, chat and persona books** — and lets modules read and edit them. The guide Mea can also open a book, search it by meaning ("where is the mill described") and change or delete an entry for you.

## Macros

The **Macros** card lists every value the engine publishes — from the [Tracker](tracker.html), [RP Time](rp-time.html) and others — each usable in **any SillyTavern prompt** as `{{name}}`.

| Where you can write a macro | Example |
|---|---|
| Character card (description, system prompt) | `{{char}} is currently feeling {{tracker_mood}}.` |
| Lorebook entry | `It is {{rp_time}}; the market is closed.` |
| A [Prompt Manager](prompt-manager.html) block | `Current health: {{tracker_health}}` |

<div class="note warn" markdown="1">
**Macro names depend on your setup.** The names above are examples. The tracker's name and its fields decide the exact macro — open the **Macros** card to copy the real ones.
</div>

## Using macros well

- A value that changes every message **breaks the provider's prompt cache** from the place it appears. Put changing values near the end of the request — the Prompt Manager's *Log & cache* tab shows what changed.
- Random macros (like dice rolls) break the cache too; the Prompt Manager has **Freeze random** to keep one value per chat.
