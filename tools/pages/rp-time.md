---
title: RP Time
group: Modules
desc: An in-world clock worked out from the conversation, shown under replies.
order: 7
needs: A model connection
where: Modules → RP Time
id: module.time
---
RP Time works out **what time it is in the story** from the conversation. It shows a time badge under replies, keeps a floating clock, publishes the time as a macro, and can tell the model the current time before it writes — so the story stops forgetting that it is already midnight.

<div class="float demo" markdown="0"><div class="h"><span>RP Time</span><span>✕</span></div><div class="b"><span>Day 3 · 21:40</span><span><i>raining</i></span></div></div>

## Set it up

<ol class="steps">
<li markdown="1">
### Turn on RP Time
Engine panel → **Modules** → switch on **RP Time**.
</li>
<li markdown="1">
### Choose a connection
Pick which model works out the time. Any cheap one will do.
</li>
<li markdown="1">
### Set the starting time
Where the clock begins before anything has been worked out. The default is *Year 1, Month 1, Day 1, 08:00 (Morning)*.
</li>
<li markdown="1">
### (Optional) Start from a preset
Choose a **Preset** (the default is *Year · Month · Day · Time · Period*) and press **Apply preset** — it fills the instruction and sampler fields from a ready-made setup. Nothing changes until you press Apply.

<figure class="shot "><img src="../assets/shots/time-form.webp" alt="RP Time settings: preset, model connection, display template and the fields the model fills in." loading="lazy"><figcaption>RP Time settings: preset, model connection, display template and the fields the model fills in.</figcaption></figure>

</li>
</ol>

## Settings

| Setting | What it does |
|---|---|
| **Model connection** | Works out the time from the chat |
| **Preset** + **Apply preset** | Fills the neighbouring fields from a ready-made setup |
| **Starting time** | Where the clock starts |
| **Display template** | How the time is written in the badge and the floating window, e.g. `Year {year}, Month {month}, Day {day}, {time} ({period})`. Click a token — `{year}` `{month}` `{day}` `{time}` `{period}` — to append it |
| **Show in chat** | The badge under each reply. Off only hides the badge — tracking keeps running |
| **Floating time window** | A small always-on-screen clock. Closing it with ✕ hides it, it does not stop tracking; this switch brings it back |
| **Enabled** | The whole module on or off |

## Buttons

- **Advance now** — works the time out right now instead of waiting for the next reply.
- **Reset for this chat** — forgets this chat's time and starts again from the starting time.

<div class="note tip" markdown="1">
Because the time is a macro, you can use it in prompts and lorebook entries — for example an entry that only matters "at night". Check the **Macros** card for the exact name.
</div>
