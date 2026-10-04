---
title: Notebook & Secrets
group: Modules
desc: Working memory for plans and goals, and hidden facts that only some characters know.
order: 13
needs: A model connection
where: Modules → Notebook / Secrets
id: module.notebook · module.secrets
---
Two small modules that give the AI a memory of its own.

<div class="compare" markdown="1">

<div class="opt" markdown="1">
#### Notebook
A **private notebook** the AI writes to and reads back — working memory for plans, secrets and goals across the whole chat.

*Use it when* a character should remember intentions and long-term goals.
</div>

<div class="opt" markdown="1">
#### Secrets
A list of **hidden story facts**, each tagged with *who knows it*, so characters do not reveal what they should not know.

*Use it for* mysteries, betrayals and information asymmetry.
</div>

</div>

## Settings (the same for both)

| Setting | What it does |
|---|---|
| **Maximum notes / Maximum secrets** | How many entries are kept. When full, the oldest are cleared to make room |
| **Cleanup batch** | How many of the oldest entries are cleared at once (never more than the maximum), so cleaning does not run on every new entry |
| **Injection depth (@N)** | Where entries go in the prompt: N messages from the end. 0 = right at the end; larger = further back |
| **New note / New secret** + **+ Add** | Add an entry by hand; the model adds its own with its tool. A secret is tagged with who knows it |
| **Delete** | Removes one entry |
| **Save settings** | Stores the sliders |

<div class="note tip" markdown="1">
Entries are placed in the prompt at the **injection depth** you choose. Closer to the end = more influence on the next reply; further back = a quiet background reminder.
</div>
