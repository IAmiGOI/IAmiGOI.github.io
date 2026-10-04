---
title: Testing
group: Development
desc: Two levels of tests — small unit tests, and scenario tests that run the whole real engine.
order: 47
---
There are two levels of tests. They have different purposes and do not replace each other.

## Level 1 — unit tests

Test **one pure function, or one core or module, in isolation.** Almost everything around it is faked — buses, context — with the narrowest fake the test needs. Many small tests, each pinning one behaviour or one bug.

- **Name a test as a full sentence about behaviour.**
- **A new regression test must be proven to catch the bug.** Temporarily revert the fix, confirm the test fails with the expected message, restore the fix.

```bash
npm test          # node --test tests/**/*.test.js
```

## Level 2 — scenario tests

Bring up the **whole real engine**: the real Runner, buses, directors, gates, rights core, capability cores and modules. Only the **Services layer** is replaced — the one boundary that touches the outside world.

This works because of the strict layering: since a service is the only place that touches SillyTavern, the DOM or the network, there is a short, finite list of "leaf" functions to fake — the same set that is designed as an offline library for testing. No separate test framework is needed: the same Runner, with real cores and modules and fake services.

**An example scenario:** *the user sent a message → the tracking core polled the model → the value was published → a macro resolves it.* The whole path runs through real director → gate → director chains, the real rights system and real blocks — but the "model" at the end of the service answers with canned data instead of real HTTP.

| When | Which level |
|---|---|
| Every pure function, core and module, as it is written | Level 1 — fast feedback, many edge cases |
| Every significant end-to-end flow — what a user really does | Level 2 — proves the layers, assembled, behave as intended |

The first scenario test of the project was a skeleton: a fake module → core → service through the real chain, including a refusal on rights at each level and a trigger on a `when` event.

## Testing a module

- Put pure logic in functions you can call directly — counting words, building a prompt, parsing a reply.
- Fake `host` with an object whose `cores.subscribe` answers with envelopes, and whose `events.subscribe` collects handlers. Then call `create(host)`, run `load()`, fire an event, assert what it requested.
- For anything that crosses layers, write a scenario test against the real engine.

A sketch of a unit test with a fake host:

```js
import test from 'node:test';
import assert from 'node:assert/strict';
import create from '../modules/dice/index.js';

test('a roll is recorded in the history and a notification is requested', async () => {
    const calls = [];
    const host = {
        events: { subscribe: () => () => {} },
        cores: { subscribe: (contract, options, callback) => { calls.push({ contract, options }); callback({ ok: true, value: true }); return () => {}; } },
    };
    const module = create(host);
    await module.load();
    // …trigger a roll through the tree's button, then:
    assert.ok(calls.some(call => call.contract === 'ui.notify'));
});
```

Check UI and engine changes in the **test SillyTavern** on its own port, never your personal one.
