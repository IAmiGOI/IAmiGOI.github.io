---
title: Chat Summary
group: Memory & prompts
desc: Fold old messages into leveled summaries so very long chats still fit the context.
order: 14
needs: A model connection
where: Engine panel → Chat Summary (tile)
---
Long chats outgrow the model's context. **Chat Summary** folds old messages into **summaries**, in levels, and **hides the originals from the prompt** — it never deletes them. A protected window of recent messages is never folded.

<div class="levels" markdown="0">
<div class="lv"><b>Newest messages</b><span>always sent as they are · <i>protected window</i></span></div>
<div class="lv l1"><b>Level 1</b><span>oldest raw messages folded into one summary</span></div>
<div class="lv l2"><b>Level 2</b><span>several level-1 summaries folded into one</span></div>
<div class="lv l3"><b>Level 3</b><span>several level-2 summaries folded into one</span></div>
</div>

The **Chat Summary** screen, with its defaults:

<figure class="shot "><img src="../assets/shots/summary.webp" alt="Protected window 20, level batches 10 / 5 / 5, an optional verify pass." loading="lazy"><figcaption>Protected window 20, level batches 10 / 5 / 5, an optional verify pass.</figcaption></figure>

## How it works

1. Once there are at least **protected window + level-1 batch** messages, the oldest raw messages are folded into one level-1 summary by a model.
2. When enough level-1 summaries pile up, they are folded into a level-2 summary — and level 2 into level 3.
3. An optional **verify** pass checks each summary.

## Settings

| Setting | What it does |
|---|---|
| **Protected window** | How many of the newest messages never get folded (20 by default) |
| **Worker** | Which connection writes summaries (*Default* = any working one) |
| **Level 1 / 2 / 3 batch size** | Level 1 folds this many of the **oldest raw messages** into one summary; level 2 folds this many level-1 summaries; level 3 does the same with level 2. Bigger batches = fewer, coarser summaries |
| **Verify level >1 summaries** | Off by default. When on, after folding a summary of summaries the model double-checks it against the original content one level further down — it catches drift higher up the pyramid |
| **Verify worker** | The connection that does the check (*Same as fold worker* by default) |
| **+ Add level** / **Remove** | Add or remove a level of the pyramid |
| **Save settings** | Stores the values |
| **Fold now** | Folds eligible messages immediately instead of waiting |

<div class="note tip" markdown="1">
**Starting point:** keep the protected window large enough that the current scene is never folded, and use a cheap, reliable model as the worker. Summaries work best alongside the [Memory graph](memory-graph.html), which keeps people, places and facts.
</div>
