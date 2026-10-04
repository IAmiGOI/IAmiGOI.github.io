---
title: Modules at a glance
group: Modules
desc: Every module on one page, with what it is for and where to read more.
order: 5
needs: Most modules need a model connection
where: Engine panel → Modules
---
Switch modules on and off in the **Modules** card. Each module's own settings appear there once it is on. Most modules need a working [model connection](models.html).

<div class="note tip" markdown="1">
**Good first modules:** [Tracker](tracker.html) — watch values like health or mood update by themselves — and [RP Time](rp-time.html) — an in-world clock.
</div>

## Story awareness

<div class="cards" markdown="1">

<a class="mini" href="tracker.html" markdown="1">
**Tracker** · `module.tracker`
Named values that a model keeps up to date and publishes as macros.
</a>

<a class="mini" href="rp-time.html" markdown="1">
**RP Time** · `module.time`
Works out the story's time from the chat and shows a badge.
</a>

<a class="mini" href="notebook-secrets.html" markdown="1">
**Notebook** · `module.notebook`
Private working memory the AI writes to and reads back.
</a>

<a class="mini" href="notebook-secrets.html" markdown="1">
**Secrets** · `module.secrets`
Hidden facts tagged with who knows them.
</a>

</div>

## Writing quality

<div class="cards" markdown="1">

<a class="mini" href="postprocess.html" markdown="1">
**Post-Turn Processor** · `module.postprocess`
Rewrites every fresh reply through a chain of passes.
</a>

<a class="mini" href="speaker-colors.html" markdown="1">
**Speaker Colors** · `module.speakerColors`
Colours each character's dialogue by who speaks.
</a>

</div>

## Atmosphere

<div class="cards" markdown="1">

<a class="mini" href="scene-painter.html" markdown="1">
**Scene Painter** · `module.scenePainter`
Paints the current scene into a picture.
</a>

<a class="mini" href="music.html" markdown="1">
**Music** · `module.music`
Plays background music that matches the scene.
</a>

<a class="mini" href="map.html" markdown="1">
**Map** · `module.map`
A floating world map with distances and travel time.
</a>

</div>

<div class="note" markdown="1">
The `module.*` ids are the names the engine uses internally (for example in the guide's actions). You never need to type them.
</div>
