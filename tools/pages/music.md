---
title: Music
group: Modules
desc: Ready-made background music from the Module Engine music library, chosen by the meaning of the scene.
order: 10
needs: Nothing for the library · a model only to describe your own tracks
where: Modules → Music
id: module.music
---
Music plays background tracks that **match the scene** — and you do not have to bring any. Pick a section of the **Music library**, the ready-made collection on the Module Engine music server, and tracks start on their own as the story changes.

<figure class="shot player"><img src="../assets/shots/music-player.webp" alt="The Music player window" loading="lazy"><figcaption>The player: the track that matches the scene, with how well it matches.</figcaption></figure>

The player is a floating window you toggle from the dock.

## How it works

1. After each reply the engine turns the recent scene into a numeric **vector** — a fingerprint of its meaning.
2. The music server receives that vector (not your chat text) together with what is playing now, and answers with one track, or "keep the current one".
3. If the server cannot be reached, nothing breaks: the current track simply keeps playing.

You never see or manage individual server tracks — you only choose the **section**.

## Set it up

<ol class="steps">
<li markdown="1">
### Switch the module on
Engine panel → **Modules** → **Music**.
</li>
<li markdown="1">
### Pick a section of the Music library
In the Music settings choose a section in **Music library**. *Off — only my own tracks* turns the server library off. Tracks start on their own to match the scene.
</li>
<li markdown="1">
### (Optional) Smart scene detection
Switch on **Smart scene detection (Jev)**. When the music is about to change, your Jev connection (**Models → Classifiers**) rates the scene so the track fits it better. Without a Jev connection it is simply skipped.
</li>
<li markdown="1">
### Let it follow the story
Keep **Auto-switch with the scene** on and open the player from the dock.
</li>
</ol>

## Settings

| Setting | What it does |
|---|---|
| **Music library** | The section of ready-made music to play from. *Off — only my own tracks* disables the server library |
| **Smart scene detection (Jev)** | Lets your Jev classifier rate the scene when the music is about to change. Skipped without a Jev connection |
| **Auto-switch with the scene** | After each reply the module compares the scene with the tracks and may change the music. Off = only by hand |
| **Scene depth** | How many recent messages describe "the scene". More = steadier, fewer = reacts faster |
| **Min similarity** | How close a track must be to the scene to play at all. Higher = pickier (may stay silent); lower = always plays something |
| **Switch margin** | How much better a new track must fit than the current one before the music changes. Higher = fewer switches |

## Your own music (optional)

The library is the main way to use Music. If you also want your own tracks, they play **side by side** with the library and are chosen by the same scene matching.

- **Import audio files**, or **Add a direct audio link** to a file or stream (.mp3, .ogg, .m4a, .flac…). For links only the *address* is stored, never the audio.
- **Describe new tracks with the model** — after importing, a text model writes a one-line mood description for each track (in batches of 10), so matching works even when file names say nothing. **Describe with the model** does it for tracks already added; descriptions you edited by hand are never overwritten.
- **Mood description** *(per track)* — the text a track is matched by. A badge shows where it came from: *AI*, *Edited* or *Title only*.

<div class="note tip" markdown="1">
**Music keeps changing too much?** Raise **Switch margin** and **Scene depth**. **Silence?** Lower **Min similarity**.
</div>
