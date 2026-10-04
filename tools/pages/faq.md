---
title: FAQ
group: Help
desc: Short answers to the questions people ask first.
order: 21
---
## Do I need a second model?

No. You can reuse SillyTavern's connection for everything. A separate cheap, fast model for the side jobs is just cheaper and quicker. See [Model connections](models.html).

## Does it change or delete my chats?

No deleting. Summaries **hide** old messages from the prompt but keep them. The [Post-Turn Processor](postprocess.html) *does* replace a reply with the rewritten one — that is its job — so write passes that keep events unchanged. Text rules and macros only change what is **sent**.

## Does it work with Text Completion?

Model connections: yes, the *SillyTavern main connection* works with Chat Completion and Text Completion (not Kobold Horde or NovelAI). The [Prompt Manager](prompt-manager.html) is Chat Completion only and steps aside in group chats and Text Completion.

## Where is my data stored?

In your browser and SillyTavern's own settings. Cloud sync is optional and goes straight to *your* Google Drive, Dropbox or GitHub. See the [Privacy policy](../privacy.html).

## Can I use several modules together?

Yes — that is the point. A tracker value can feed a lorebook entry, a Prompt Manager condition, and a rewrite pass at once.

## How do I update?

Open the **Updates** card. See [Sync, backup & updates](sync-backup-updates.html).

## How do I remove it?

**Extensions → Manage extensions** → remove ST Module Engine. Your chats and characters are not touched.

## What is Mea?

The engine's built-in guide. She has a chat of her own — separate from your roleplay chats — and knows every setting. She opens by herself on the first launch, and from her widget on the desktop later.

## Is it affiliated with SillyTavern?

No. It is an independent extension for SillyTavern.
