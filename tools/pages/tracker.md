---
title: Tracker
group: Modules
desc: Keep named values — health, mood, location — up to date automatically and use them in prompts.
order: 6
needs: A model connection
where: Modules → Tracker
id: module.tracker
---
The Tracker keeps **named values** (health, mood, location, anything) up to date by asking a model after or before replies. The values appear in a small always-on-screen window and become **macros** you can use in prompts.

<div class="float demo" markdown="0"><div class="h"><span>Tracker · status</span><span>✕</span></div><div class="b"><span>❤ <i>health</i> 82</span><span>📍 <i>location</i> Harbour alley</span><span>🎭 <i>mood</i> Tense</span></div></div>

## What it is good for

- Show the hero's health, money, mood or location at a glance.
- Make the model *aware* of the state: put `{{tracker_health}}` in your prompt and the reply can react to it.
- Keep long-running facts (who is allied with whom, what day it is) from drifting.

Values are saved **per message**, so rerolling or going back to an older message shows the value of that moment.

## Set up your first tracker

<ol class="steps">
<li markdown="1">
### Switch the module on
Modules card → turn on **Tracker**.
</li>
<li markdown="1">
### Create a tracker
Add a tracker and give it a short, lowercase name without spaces, such as `status`. The name becomes part of its macros.
</li>
<li markdown="1">
### Pick a connection
Choose which model answers. A cheap fast one is fine — the answer is small JSON.
</li>
<li markdown="1">
### Add fields
Press **+ Add field**. Give each field a **name**, a short **prompt** that tells the model what to write, and a **starting value**. Clear prompts matter more than anything else here.
</li>
<li markdown="1">
### Choose when it updates and Save
Set **Poll when** (see below), then press **Save** — nothing takes effect until saved. Use **Poll now** to test.
</li>
</ol>

### Example fields

| Field | Prompt | Starting value |
|---|---|---|
| `health` | how hurt the hero is, 0–100 | 100 |
| `location` | where the scene currently takes place | Unknown |
| `mood` | the hero's dominant emotion, one or two words | Calm |

## When should it update?

| **Poll when…** | Use it for |
|---|---|
| after every reply | Most trackers — the value is fresh for the next turn |
| every N replies | Slow-changing values; saves cost |
| every N minutes | Real-time pacing |
| when I send a message | Reacting to your input |
| **before the reply is generated** | Values the reply must already know (see below) |
| only by hand | Tracker you update yourself with **Poll now** |

<div class="note warn" markdown="1">
**Hold the generation until this tracker answers.** Only available with *before the reply*. The reply waits so it already sees the fresh value — never a step behind, but slower. If replies pause before generating, a tracker set this way is probably polling.
</div>

## All settings

| Setting | What it does |
|---|---|
| **Name** | The tracker's id. Its values become macros — keep it short, lowercase, no spaces. |
| **Model connection** | Which connection answers the polls. |
| **Fields** | The values to keep: name, prompt, starting value. |
| **Poll prompt** | The full text sent to the model. Empty = the engine's default, which is right almost always. `{fields}` inserts the field list. |
| **Display template** | How the value looks in the small window, e.g. `❤ {health} · 📍 {location}`. Empty = a plain "name: value" list. Click a token to append it. |
| **Show the floating state window** | The small always-on-screen panel with current values. |
| **Sampler & reasoning** | Belong to this tracker, not the connection. Low temperature / *Precise* or *Deterministic* presets suit strict JSON. |
| **Enabled** | Off = stops polling but keeps its settings. |

### Buttons

| Button | Does |
|---|---|
| **Save** | Writes the configuration |
| **Poll now** | Runs one update right away using the saved settings |
| **Reset** | Puts this chat's values back to their starting values |
| **Remove** | Deletes the tracker |

## Use the values in prompts

Every field becomes a macro you can write into a character card, a lorebook entry or a Prompt Manager block. Open the **Macros** card to see the exact names currently available.

> The hero's current health is {{tracker_health}} out of 100. Describe injuries accordingly.

See [Lorebook & Macros](lorebook-macros.html). To send a block only when a value matters (for example health below 30), use a condition in the [Prompt Manager](prompt-manager.html).

## Troubleshooting

| Problem | Try |
|---|---|
| Value never changes | Is the module on, a connection chosen, and the tracker **Enabled** and **Saved**? |
| Values are garbage | Make field prompts more specific; use a *Precise* / *Deterministic* sampler preset |
| Reply waits | A *before the reply* tracker is polling — switch to *after every reply* |
| Wrong value after reroll | Expected: each message keeps its own value; **Reset** restores the start |
