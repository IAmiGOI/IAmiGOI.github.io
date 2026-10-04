---
title: Map
group: Modules
desc: A floating full-screen world map with regions, distances and travel time.
order: 12
needs: No model
where: Its own draggable button
id: module.map
---
Map is a floating, full-screen **map window** with a settings drawer. It opens from its own draggable button. Locations, regions and sub-regions give you real distances and **travel time** between places.

## Set it up

<ol class="steps">
<li markdown="1">
### Switch it on
Engine panel → **Modules** → **Map**. A draggable button appears.
</li>
<li markdown="1">
### Set the scale
In the settings drawer enter the real-world **Map width / height (m)** the map stands for. Distances and travel time are computed from it.
</li>
<li markdown="1">
### Add locations
Add a location (name, description, colour, radius). Use **+ Sub-region** to nest a region inside another one.
</li>
</ol>

## Map settings

| Setting | What it does |
|---|---|
| **Map width / height (m)** | The real-world size the map stands for |
| **Walking speed (m/min)** + **Auto-calculate travel time** | Travel time between places is worked out from distance and this speed |
| **Auto-connect distance (m)** | Any two locations closer than this are connected even if their borders do not touch (blank = off) |
| **Minimum traversable rank** | Locations ranked below this are excluded from movement (blank = no ceiling) |
| **Nested-level scale coefficient** | Each nesting level without its own explicit size is this many times smaller than its parent |
| **Marker size** | Size of location markers |

## Per location

| Field | Meaning |
|---|---|
| **Name** / **Description** | What it is |
| **Rank** | Free-form abstraction level — lower = more abstract, blank = unranked |
| **Color** | Blank = theme colour |
| **Radius** | Size of the location |
| **+ Sub-region** | Nest a region inside this one |
| **Delete location** | Removes it |
