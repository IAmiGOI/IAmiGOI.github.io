---
title: Sync, backup & updates
group: Interface & data
desc: Export your configuration, sync between devices, update the extension and manage backgrounds.
order: 19
needs: Optional cloud account
where: Settings screen
---
Four cards on the **settings screen** keep your setup safe and current.

<div class="cards" markdown="1">

<div class="mini" markdown="1">
**Preset**
Exports and imports the engine's whole configuration — handy for backups and sharing a setup.
</div>

<div class="mini" markdown="1">
**Sync**
Keeps settings and chats in step between your devices — through the cloud or GitHub.
</div>

<div class="mini" markdown="1">
**Updates**
Checks for and installs new versions of the extension.
</div>

<div class="mini" markdown="1">
**Backgrounds**
Manages chat backgrounds.
</div>

</div>

## Cloud sync — your account, nothing in between

Optional. Sign in with **your own Google Drive or Dropbox account** and the engine keeps the SillyTavern data you choose (for example characters, chats, lorebooks, backgrounds) in step on all your devices.

- It runs entirely **in your browser** and talks to your cloud account directly. Nothing is sent to the author.
- With Google, it requests only the `drive.file` permission: it can see and change **only the files and the folder it created itself** ("ST Module Engine Sync") — not the rest of your Drive.
- Disconnect any time in the extension; revoke access at myaccount.google.com/permissions.

Read the full [Privacy policy](../privacy.html).

<div class="note warn" markdown="1">
**Keep your own backups.** Sync copies files between devices; it is not a substitute for a backup. Export a **Preset** before big changes.
</div>

## Updating

Open the **Updates** card and install. The engine updates itself and shows an update overlay while it does. Your settings are stored separately and are kept.
