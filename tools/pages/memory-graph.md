---
title: Memory graph
group: Memory & prompts
desc: A mind-map of people, places and facts built from your chat, in its own window.
order: 15
needs: A model connection
where: Engine panel → Memory graph
---
The **Memory graph** builds a **mind-map** from your chat: *nodes* with text (people, places, facts, events) connected by typed links, with one central node and a network around it. It runs alongside the Chat Summary and the Notebook — it complements them, it does not replace them.

It opens in its own window, where you can look at the graph, edit nodes and see which memories were pulled into the last prompt (the *pathway* overlay).

## Why a graph

A summary is a flat story. A graph keeps **who is connected to what**: that the innkeeper owes the hero a favour, that the key is in the harbour warehouse. The right memories are pulled in by meaning, not by position in the chat.

## How it keeps itself tidy

- **Regions** — related nodes are grouped; each region holds a limited number of nodes (23 by default).
- **Merging duplicates** — near-identical nodes are merged on insert, before a region overflows.
- **Reconsolidation** — if a region still overflows, a cluster of weak nodes is rewritten into a compact one (preferred).
- **Decay** — as a last resort the weakest node is removed. **Protected** nodes (such as a region's centre) are never evicted.
- Matching by meaning uses a **local embedding model** in your browser — picking memories does not call a remote model.

## Start it from your lorebook

The graph can **bootstrap from your Lorebook**: existing entries become the first nodes, so it starts with your world instead of empty. Use the **Bootstrap & graph** panel in the memory graph window.

<div class="note" markdown="1">
The graph window has side panels: **Bootstrap & graph**, **Map visuals** and **Edit node**. Node count is shown on the card subtitle in the engine panel.
</div>
