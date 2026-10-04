---
title: Prompt Manager
group: Memory & prompts
desc: Build the request that goes to the model — order, conditions, cache, chain-of-thought and text rules.
order: 17
needs: Chat Completion presets
where: SillyTavern's Prompt Manager button
---
The **Prompt Manager (PM)** builds the request that goes to the model **instead of SillyTavern's own prompt manager**. It opens with SillyTavern's **Prompt Manager button** (the native window is hidden while PM is on).

<div class="note" markdown="1">
**Scope.** PM works with **Chat Completion** and single chats. In group chats and Text Completion it steps aside and the ordinary SillyTavern prompt is used. If PM ever fails while assembling, the original request is sent — PM never blocks a generation (except after a second failed CoT step).
</div>

## First start

All your SillyTavern Chat Completion presets are **copied** into PM automatically — the ST files are never changed. The preset selected in ST becomes the active one. Import and export also work with ST files; passwords and keys are removed on export.

## The six tabs

<div class="cards" markdown="1">

<div class="mini" markdown="1">
**Order**
The preset's prompts as a tree. Drag to reorder, tick to send or not, edit a row.
</div>

<div class="mini" markdown="1">
**Preview**
What would be sent right now, tokens per block, what was trimmed, warnings.
</div>

<div class="mini" markdown="1">
**Log & cache**
Last requests and how much of each matches the previous one.
</div>

<div class="mini" markdown="1">
**CoT**
Guided chain-of-thought: hidden thinking steps before the answer.
</div>

<div class="mini" markdown="1">
**Text rules**
Replace, remove or regex text in what is sent — never in your chat.
</div>

<div class="mini" markdown="1">
**Settings**
Sampler, trimming, per-model overrides, plugins, versions.
</div>

</div>

## Order

The prompts of the preset as a tree: **drag** to reorder, **tick** to send or not. Groups can wrap their content in tags (`<info> … </info>`) and stay silent when empty. Click a row to edit it:

| Field | Meaning |
|---|---|
| Name, role, text | The block itself |
| **Position** | In order, or *N messages from the end* of the chat |
| **Trim priority** | Which blocks are cut first when the context is too full |
| **Send only when…** | A plain-words condition builder (below) |

**Module rows** (memory graph, Notebook, Summary…) can be placed wherever you want; a button returns one to the place the module suggested.

### "Send only when…" conditions

Build a condition from:

- keywords in the last messages
- message length
- a **tracker value**
- a variable
- a chance
- every N-th message
- a cooldown
- **Jev answers a question** (below)

### Dividers

**+ Divider** adds two coloured strips. Everything between the top and bottom strip is one region; the strips send nothing themselves. The **top strip carries the condition** — while it is false, every block between the strips is left out. Regions can nest (each pair gets its own colour). A pair that lost one strip does nothing, and the Preview says so. Removing one strip removes both; the blocks stay.

### Jev — a yes/no classifier

*Jev answers a question* gives the **chance (0–100%) that a statement you write is true**, for example *"The player is in danger in `player_message`"*. The condition is true when that chance is at least the percentage you set. The statement may use `player_message` (your newest message), `latest_turn` (the newest reply) and `history` (the older ones). The connection is set in **Model connections**, in the **Classifiers** category.

## Preview

Shows what would be sent for the current chat: tokens per block, what was trimmed, and warnings about random or unknown macros.

## Log & cache

Providers cache only the **start** of a request that is identical to the previous one. This tab shows the last requests and how much of each is shared with the one before. Anything that changes early (a memory block above long stable rules) **costs you the cache**; the tab names the block that changed and which stable blocks stand after it.

<div class="note tip" markdown="1">
A block that appears and disappears changes the request from that place on. Put such regions **near the end** of the request.
</div>

## CoT — guided chain-of-thought

Hidden thinking steps before the answer. **Off by default.**

- Each step is a **separate request**, sent as a user message after the whole prompt. Steps see the previous answers and reasoning; a **different model can be chosen per step**.
- The result is added to the final prompt and stored under the message as a **collapsed block** (it never goes into later history).
- A failed step is **retried once**; a second failure cancels the generation.

## Text rules

Replace or remove a phrase, cut everything between two marks, or use regex; choose roles and how far from the end. Rules change **only what is sent**, never your saved chat. You can import ST regex scripts.

## Settings

Sampler and other generation values of the preset, trimming headroom, **overrides per model, character or chat** (off by default), plugins, and **versions with rollback**.

## Good to know

| Topic | Behaviour |
|---|---|
| **Character prompts** | The card's system prompt fills the preset's `main` block, post-history text fills `jailbreak` (a block set to forbid overrides is left alone; `{{original}}` inserts the block's own text), the depth prompt goes in at the depth and role the card names. Turn off *Prefer Char. Prompt/Jailbreak* in ST to ignore them. |
| **Trimming** | Cuts the oldest history first and a little extra at once, so the start of the history does not move every turn (that would break the cache). |
| **Random macros** | Break the cache. **Freeze random** keeps one value per chat. |
| **Streaming** | The preset's streaming is applied by switching ST's own setting for the generation and back afterwards. |
