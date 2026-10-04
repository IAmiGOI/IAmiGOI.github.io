---
title: Troubleshooting
group: Help
desc: Find your symptom, get the fix.
order: 20
---
**Always start here:** open **Models** → **Model connections**. Most problems are a connection that is **down** or **rejected** — its last error is shown right under it.

## By symptom

| Symptom | Likely cause | Fix |
|---|---|---|
| **HTTP 401 / 403** | Wrong or expired API key | Re-enter the key in the connection |
| **HTTP 404** | Wrong endpoint or model name | Check the endpoint (OpenAI-compatible usually ends with `/v1`) and the exact model name |
| **HTTP 429** | Rate limit | Add another connection; it recovers on its own |
| **"Failed to fetch"** | Endpoint unreachable, or it blocks the browser (CORS) | Check the address; try another provider or a proxy |
| A feature does nothing | Module is off, or has no connection | Modules screen: switch it on and select a connection |
| Replies wait before generating | A tracker set to *before the reply* is polling, or a connection is slow | Change *Poll when* to *after every reply*; check connection latency |
| A tracker never updates | Not saved, not enabled, or vague field prompts | Press **Save**, check **Enabled**, rewrite field prompts, try **Poll now** |
| Post-Turn pass never runs | Auto-run is off, or the pass is empty | Enable **Auto-run after each reply** and write an instruction |
| Rewritten replies are cut off | A reasoning model used the token limit on thinking | Disable reasoning for the pass; raise max tokens to ≥ 2× the reply length |
| Music is silent | **Min similarity** too high, or tracks have no descriptions | Lower it; describe tracks with the model |
| Music switches constantly | **Switch margin** too low | Raise **Switch margin** and **Scene depth** |
| Picture ignores the characters | The backend has no reference-image support | Use a model that accepts image input (e.g. nano-banana, seedream, flux-kontext, gpt-image) |
| No dock after install | Extension disabled or page not reloaded | Reload; check **Extensions → Manage extensions** |

## Reading connection states

| State | Meaning |
|---|---|
| **Up** | Healthy |
| **Unstable** | Gets fewer requests automatically |
| **Down** | Only used when nothing else works |

## Still stuck?

Ask **Mea** — she sees the live state of your connections and modules. Or open an [issue on GitHub](https://github.com/IAmiGOI/Module-Engine/issues) with the connection's last error and what you expected.
