---
title: Music
group: Modules
desc: Background music chosen by the meaning of the scene — locally, with your own tracks.
order: 10
needs: Optional — only for describing tracks
where: Modules → Music
id: module.music
---
Music plays background tracks that **match the scene**. Tracks are chosen **locally by meaning** (embeddings) — picking a track makes no model calls. A model is only used, once, to *describe* tracks so that matching works even when file names say nothing.

The player is a floating window you toggle from the dock.

<figure class="shot player"><img src="../assets/shots/music-player.webp" alt="The Music player window" loading="lazy"><figcaption>The player: the track that matches the scene, with how well it matches.</figcaption></figure>


## Set it up

<ol class="steps">
<li markdown="1">
### Switch the module on
Engine panel → **Modules** → **Music**.
</li>
<li markdown="1">
### Add tracks
**Import audio files** from your computer, or **Add a direct audio link** to a file or stream (.mp3, .ogg, .m4a, .flac…). For links, only the *address* is stored — never the audio.
</li>
<li markdown="1">
### Describe them
Turn on **Describe new tracks with the model** (or press **Describe with the model**). A model writes a one-line mood description per track, in batches of 10. Edit any description yourself — hand-edited ones are never overwritten.
</li>
<li markdown="1">
### Let it follow the story
Switch on **Auto-switch with the scene** and open the player from the dock.
</li>
</ol>

## Settings

| Setting | What it does |
|---|---|
| **Auto-switch with the scene** | After each reply the module compares the scene with the tracks and may change the music. Off = only by hand |
| **Scene depth** | How many recent messages describe "the scene". More = steadier, fewer = reacts faster |
| **Min similarity** | How close a track must be to the scene to play at all. Higher = pickier (may stay silent); lower = always plays something |
| **Switch margin** | How much better a new track must fit than the current one before the music changes. Higher = fewer switches |
| **Describe new tracks with the model** | After import, a model writes a mood description for each track |
| **Mood description** *(per track)* | The text a track is matched by. Editing marks it as yours; a badge shows its source: *AI*, *Edited* or *Title only* |

<div class="note tip" markdown="1">
**Music keeps changing too much?** Raise **Switch margin** and **Scene depth**. **Silence?** Lower **Min similarity**.
</div>
