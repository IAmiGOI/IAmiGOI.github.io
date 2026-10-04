---
title: Typing
group: Development
desc: Type checking without TypeScript — JSDoc comments inside plain .js files, checked on demand.
order: 46
---
Types live in **JSDoc comments inside the existing `.js` files**. There are no `.ts` files, no build step and no new runtime dependency: the code that ships is exactly the code that is written. The TypeScript compiler is used only as a **checker** — a linter that understands JSDoc — run on demand and never imported by the engine.

## Why

The engine is made of buses, contracts and many small modules that talk through plain objects. The bugs that cost the most time were **shape mismatches that tests did not exercise**: a wrong field on an envelope, a value that can be `null` on one path, an inherited property treated as a lookup key. A checker finds that class of bug at the keyboard instead of in the browser.

It paid off on the first pass:

- `stme:constructor` resolved through `Object.prototype` and turned into a bogus module URL — fixed, with a regression test.
- A "home domain" type that was too narrow was rejected by existing tests, which showed services can register callers too.
- Places where a value could be `null` but was dereferenced (`meta`, `pending`, `hudUi`) were made explicit.

## How it works

1. **Opt in per file** with `// @ts-check` as the very first line. A file without it is not checked.
2. **Strict mode, no exceptions.** `jsconfig.json` sets `strict: true`. A file that opts in must pass with zero errors: no "allow implicit any" escape hatch and no `// @ts-ignore`. If a type is hard to express, fix the design or use a narrow, commented cast.
3. **Gradual.** `checkJs` is `false` globally, so unchecked files cannot break the check. The ratchet only goes one way: once a file is opted in it stays at zero errors.

```bash
npm run typecheck            # checks every opted-in file; non-zero exit on any error
npm run typecheck:progress   # how many files opted in, where the remaining errors are
```

Both fetch the compiler with `npx` the first time (network needed once); nothing is added to the dependencies. Editors that understand JSDoc (VS Code, WebStorm) read `jsconfig.json` and show the same errors and hover types as you type.

## Where the types are

Types are `@typedef`s in **code-free `.js` files** next to the code that owns them, imported with `import()` types:

| File | Defines |
|---|---|
| `libraries/shared/bus-types.js` | `Envelope`, `Host`, `Engine`, buses, gates, `RightsConfig`, `RightsCore`, `Domain` |
| `cores/ui/ui-types.js` | `Signal`, `UiNode`, `UiProps` (typed `on:*` handlers), `UiChild` |
| `libraries/core/module-types.js` | Module header/meta, `Analysis`, runner/installer/registry shapes |

```js
// @ts-check
/** @typedef {import('../shared/bus-types.js').Host} Host */
/** @template [T=any] @typedef {import('../../cores/ui/ui-types.js').Signal<T>} Signal */
```

A types file ends with `export {};` so it is a module, holds no logic, and is never run for its own sake.

## Writing annotations

- **One block per function.** The description and the `@param`/`@returns` tags must be a single `/** … */` directly above the function, or editors show only the nearest block. Put `@typedef`s at the top of the file.
- **Prefer precise unions over `any`.** `Envelope<T>` is `{ ok: true, value: T } | { ok: false, error }`; narrow with `if (!result.ok) return …` instead of casting.
- **`any` is deliberate and rare.** Today it appears only for contract `params` and envelope values, because there is no per-contract type map yet — a documented gap, not a style.
- **Data from outside is `unknown`.** Parsed JSON, storage values and GitHub responses are checked, never assumed.
- **A cast is a last resort and must say why:** `/** @type {X} */ (value)` with a short comment. Prefer a type guard or restructuring.
- **Do not widen a type to silence an error.** Ask first whether the error is a real bug — it often is.
- **If an options object has required fields, do not give the parameter a `= {}` default.**

```js
/** @type {Map<string, Entry>} */                 // empty collections need an explicit type
const byId = new Map();

/**
 * @template T
 * @param {() => T[]} items
 * @param {(item: T) => UiNode} renderItem
 * @returns {Signal<UiNode[]>}
 */

/** @type {GateAccessor['subscribe']} */          // reuse a member type instead of repeating it
function subscribe(contract, options, callback) { /* … */ }
```

## Adding a file to the checked set

1. Run `npm run typecheck:progress`, pick a file with few errors — ideally one the typed code already imports.
2. Put `// @ts-check` on the first line and run `npm run typecheck`.
3. Fix from the inside out: shared typedefs, then function signatures, then locals the checker cannot infer (empty arrays/maps, `let x = null`).
4. Run that area's tests, and check UI or engine changes in the test SillyTavern.
5. If the checker found a real bug, fix it **and add a regression test** — and confirm the test fails on the old code.

## Status and known gaps

Checked today under `strict` with zero errors: the module runtime, the connectivity layer (event bus, contract bus, `request`, gate, network gate, engine, rights core), the module kit, the UI primitives, all widgets and the Modules card and installer panel.

- **Contracts are untyped.** The bus does not know the shape of each contract. A contract map (name → params/result) would give typed `request()` calls; it is the most valuable next step, introduced contract by contract rather than all ~280 at once.
- **Tests are not type-checked** — they intentionally pass partial stubs.
- **Catalog modules** are plain JavaScript the engine cannot check; an author can opt in with `// @ts-check` and the typedefs above.
