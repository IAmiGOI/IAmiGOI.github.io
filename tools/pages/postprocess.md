---
title: Post-Turn Processor
group: Modules
desc: Rewrite every fresh reply through a chain of independent passes — grammar, clichés, style, continuity.
order: 8
needs: A model connection
where: Modules → Post-Turn Processor
id: module.postprocess
---
The Post-Turn Processor takes each fresh reply and runs it through a **chain of rewrite passes**. Each pass is its own prompt and its own model; the final result **replaces the reply** in the chat.

<div class="flow" markdown="0"><span>Fresh reply</span><b>→</b><span>Pass 1<br><small>remove clichés</small></span><b>→</b><span>Pass 2<br><small>fix style</small></span><b>→</b><span class="ok">Final reply</span></div>

## When to use it

- Strip the repetitive phrases and "AI-isms" a model keeps producing.
- Enforce a style (concrete sensory detail, varied rhythm, a specific voice).
- Check continuity against recent chat.

<div class="note warn" markdown="1">
**A pass changes the story for good.** If it returns something shorter, longer or different, that is what stays in the chat — and a reroll is processed again. Always say **what must stay unchanged** (events, dialogue, length) in the instruction.
</div>

## How a pass works

- A pass receives **only the text produced by the previous step** (the first one gets the fresh reply). Your message and the rest of the chat are *not* sent unless **Include recent chat context** is on.
- The pass **Instruction** is sent as the system prompt; the text to rewrite arrives as the user message.
- The engine itself appends *"Return ONLY the rewritten text — no explanation, no markdown code fences, no commentary"* to every instruction.
- A pass with no connection chosen is spread over any available one.

## Set it up

<ol class="steps">
<li markdown="1">
### Switch the module on
Modules card → **Post-Turn Processor**.
</li>
<li markdown="1">
### Add a pass
Write an **Instruction** — a proper brief, not a one-liner — and optionally pick a **Model connection** for it. Add more passes for more steps; ↑ / ↓ change the order.
</li>
<li markdown="1">
### Turn on auto-run
Nothing runs unless the module is **Enabled**, at least one pass is on with a non-empty instruction, and **Auto-run after each reply** is on. Otherwise only **Process last reply now** works.
</li>
<li markdown="1">
### Save
**Save** stores the chain.
</li>
</ol>

## Example passes

| Pass | Instruction idea |
|---|---|
| **Cleanup** | Remove clichés and filler phrases. Keep all events, dialogue and the original length. |
| **Style** | Replace vague descriptions with concrete sensory detail and vary sentence rhythm. Do not add events. |
| **Continuity** *(with chat context on)* | Fix details that contradict the recent messages. Change nothing else. |

Pass 2 sees the result of pass 1, so **order matters**.

## Settings

| Setting | What it does |
|---|---|
| **Passes** | The chain, run in order after each reply. Each has its own **Instruction** and **Model connection**. |
| **Include recent chat context** | Off by default. On: a pass also gets the last few messages — useful for consistency edits. |
| **Messages of context** | How many recent messages (shown only when the toggle is on). |
| **Auto-run after each reply** | Process every fresh reply by itself. Off = by hand only. |
| **Process last reply now** | Runs the chain once on the latest reply; safe to press twice — an already processed reply is skipped. |
| **Enabled** | The whole module on or off. |

## Tips for reasoning models

Reasoning models spend the token limit on thinking. For rewrite passes **disable reasoning**, or the answer gets cut off. Set max tokens to at least **2× the usual reply length** — roleplay replies are commonly 300–1200 tokens, so 2000–4000 is safe.
