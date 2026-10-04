---
title: Introduction
group: Start here
desc: What Module Engine is, what it adds to SillyTavern and who it is for.
order: 1
---
Module Engine (ME) is an extension for SillyTavern that adds a second layer on top of your roleplay: **small, switchable features that work alongside the model that writes your story**.

While your main model writes the reply, ME can quietly keep track of the hero's health, work out what time it is in the story, rewrite the reply to remove clichés, fold old messages into summaries, paint the scene, pick music — each job done by a model you choose, usually a cheaper and faster one.

## What it gives you

<div class="cards" markdown="1">

<a class="mini" href="tracker.html" markdown="1">
**Track the story**
Health, mood, location, relationships — values that update themselves after every reply.
</a>

<a class="mini" href="summary.html" markdown="1">
**Fit long chats**
Leveled summaries keep a long history inside the context.
</a>

<a class="mini" href="memory-graph.html" markdown="1">
**Map the world**
A mind-map of people, places and facts, with a Pathway view of what was recalled.
</a>

<a class="mini" href="postprocess.html" markdown="1">
**Polish replies**
Chains of rewrite passes that clean up style, grammar and continuity.
</a>

<a class="mini" href="prompt-manager.html" markdown="1">
**Control the prompt**
Reorder blocks, send them only when conditions are true, inspect tokens and cache.
</a>

<a class="mini" href="scene-painter.html" markdown="1">
**Pictures and music**
Paint the current scene and play a soundtrack that follows it.
</a>

<a class="mini" href="sync-backup-updates.html" markdown="1">
**Keep it safe**
Back up and sync your settings and chats between devices.
</a>

</div>

## How it feels to use

<figure class="shot"><img src="../assets/shots/desktop.webp" alt="The Module Engine desktop" loading="lazy"><figcaption>The desktop: recent chats, quick actions, the guide Mea — and the dock on the right edge.</figcaption></figure>

You keep using SillyTavern the way you always did. Module Engine adds:

- a **dock** on the right edge of the screen — hover it to slide it out and open the engine's panel;
- **floating windows** (tracker values, the in-world clock, the music player, pictures, the map) that you can drag around;
- small **badges and buttons under replies** (time, 🎨 Paint);
- a built-in guide, **Mea**, who knows every setting and can walk you through the first start.

Nothing is forced on you: every feature is a **module** that is off until you switch it on, and the engine never deletes your messages.

<figure class="shot "><img src="../assets/shots/hub.webp" alt="The engine panel: one tile per area — Models, Classifiers, Modules, Macros, Lorebook, Chat Summary." loading="lazy"><figcaption>The engine panel: one tile per area — Models, Classifiers, Modules, Macros, Lorebook, Chat Summary.</figcaption></figure>

## Good to know before you start

<div class="note tip" markdown="1">
**You need a model for the "side jobs".** Trackers, summaries, pictures and rewrite passes make their own model calls. The quickest start is to reuse the model SillyTavern is already connected to — one click, no key. Later you can add a cheaper separate model just for these jobs. See [Model connections](models.html).
</div>

- ME takes over part of the **generation pipeline**: it can hold a reply until a tracker has answered, rewrite it afterwards, or cancel it.
- Everything runs in your browser. Cloud sync is optional and goes straight to your own account.

**Next:** [Quick start →](quick-start.html)
