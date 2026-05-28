# fused-docs — contributing guide

See @README.md for project overview and @package.json for available npm scripts.

## Docs structure

Each section has a distinct purpose and writing voice. Put content in the right section and write it in that section's style.

| Section | Path | Purpose | Writing style |
|---|---|---|---|
| **Guide** | `docs/guide/` | Explore all aspects of Fused — concepts, setup, workflows | Concept-first. Explain the why, then the how. Link to API Reference for method details. |
| **Examples** | `docs/examples/` | Hands-on, concrete things you can build | Task-first. Show the code, explain what it does. Link back to Guide for concepts, API Reference for method signatures. |
| **Python SDK** | `docs/python-sdk/` | Exhaustive reference for the `fused` Python API | Generated — do not hand-edit. Every method, every parameter. No prose beyond what the docstring provides. |
| **Widget API** | `docs/widget-api/` | Reference for all available Fused widgets and their configuration | Schema-driven. Exhaustive props list, show minimal and full examples. |
| **Workbench Manual** | `docs/workbench/` | Reference for the Workbench UI | UI-first. Screenshot-heavy. Describe what each element does, not how to build with it. |

Before adding a page, ask: is this a concept (Guide), a recipe (Examples), a reference entry (Python SDK / Widget API), or a UI element (Workbench)? Put it in the right section and write in that section's voice.

## Core rules

- **Test before documenting**: Before changing any code reference or code block, run the code and confirm it works. See [Testing code](#testing-code) below.
- **Write for humans and agents**: Humans can click — link to the UI, to other pages, to live examples. Agents use the CLI — include the exact commands to run. A good doc serves both.
- **Use absolute links**: `[page](/python-sdk/quickstart)` not `[page](../quickstart)`. Relative links break when pages move.
- **Check before writing**: Search `docs/` for existing content on the topic before writing new sections. Don't duplicate.

## Testing code

Every code block must be runnable. How to test depends on what you're documenting:

**UDF code** — run with the fused CLI:
```bash
# Remote (default) — runs on Fused servers, results printed locally
fused run "" udf.py

# Local — runs in your environment, no network call
fused run "" udf.py --engine local
```
The `CANVAS` argument is required; `""` works for local files. Make sure `fused` is installed and on your PATH (`pip install fused`).

**SDK/API code** — run as a plain Python script in an environment with `fused` and its dependencies installed:
```bash
python script.py
# or
uv run script.py
```

**Configuration or CLI snippets** — run the exact command shown and confirm the output matches what the doc claims.

For code that requires credentials or external services, note this in the doc with a `:::note` admonition so readers know what they need before running it.

## Do not

- Hand-edit any file under `docs/python-sdk/api-reference/` or `docs/python-sdk/top-level-functions.mdx` — these are generated from fused-py source. Edit the generator (`utils/generate_reference_docs.py`) instead.
- Use `npm run serve` to validate — dev mode hides MDX rendering errors that only surface in the SSG production build. Always use `npm run build`.
- Document code you haven't run yourself.
- Use relative links between pages.

## Reference docs

Detailed references for common tasks are in `.claude/commands/` — readable directly as Markdown, and available as slash commands in Claude Code:

| File / Command | When to use |
|---|---|
| `mdx-components.md` / `/mdx-components` | Before adding or editing any MDX — every custom component, admonition type, and when to use each |
| `api-reference.md` / `/api-reference` | Before touching `docs/python-sdk/` or `utils/` — generation pipeline, design decisions, automation |

## Build & CI

```bash
npm run build        # full SSG build — required before any PR
uv run utils/test_api_reference_coverage.py   # API reference coverage gate
```

Before pushing any branch touching `docs/python-sdk/` or `utils/generate_reference_docs.py`, run both. Check that CI passes on the PR before calling it done.

## For AI agents — when compacting

Preserve across `/compact`: files modified this session, test commands run and their results, open PR numbers with branch names.
