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
| **CLI Reference** | `docs/cli/` | One page per `fused` CLI command — flags, subcommands, examples | Reference-style. One page per top-level command. Flags table + examples, no prose beyond what's needed to understand the flag. |
| **Workbench Manual** | `docs/workbench/` | Reference for the Workbench UI | UI-first. Screenshot-heavy. Describe what each element does, not how to build with it. |

Before adding a page, ask: is this a concept (Guide), a recipe (Examples), a reference entry (Python SDK / Widget API / CLI), or a UI element (Workbench)? Put it in the right section and write in that section's voice.

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
npm run build                              # full SSG build — required before any PR
uv run utils/test_api_reference_coverage.py   # API reference coverage gate
uv run utils/test_doc_snippets.py          # syntax-check all Python blocks in docs
```

Before pushing any branch touching `docs/python-sdk/` or `utils/generate_reference_docs.py`, run both the build and the coverage gate. Run `test_doc_snippets.py` after adding or editing any Python code block.

## Python code block conventions

Every `python` fence in the docs is syntax-checked automatically (pre-commit hook + CI). Keep code blocks valid Python:

- **Shell commands** (`pip install`, `fused run`, etc.) must use a `bash` fence, not `python`.
- **Pseudocode blocks** (REPL output, type stubs, emoji annotations, partial signatures, HTML embedded in a python block, bare URLs or other non-Python illustrative content) must start with `# doctest: skip` as their first line. This suppresses both the syntax check and Tier 2 execution without hiding the block from readers.
- **Generated files** (`docs/python-sdk/api-reference/` and `docs/python-sdk/top-level-functions.mdx`) are excluded from the check automatically — never add skip markers there.

### Installing the pre-commit hook

```bash
pip install pre-commit
pre-commit install
```

After this, every `git commit` that touches a `.mdx` or `.md` file runs two hooks on the changed files only: the **Tier 1** syntax check and the **Tier 2** execution check.

### Tier 2 — execution (local pre-commit hook)

Tier 2 (`doc-snippet-execution`) executes the runnable Python blocks in the docs you changed via pytest-markdown-docs. It does **not** run in CI — executing the blocks calls Fused servers, which needs an authenticated session that isn't available headlessly. It runs as a pre-commit hook instead, scoped to your changed files, using your local `fused login`.

It requires an active fused session: if `~/.fused/credentials` is missing, the hook fails fast and tells you to run `fused login` (it never opens a browser popup mid-commit). Log in once:

```bash
fused login
```

Run it manually against the whole tree, or just the changed files:

```bash
uv run utils/run_doc_execution.py                 # full docs/ tree
uv run utils/run_doc_execution.py docs/guide/foo.mdx   # specific files
```

To bypass it for a single commit (e.g. WIP): `SKIP=doc-snippet-execution git commit ...`.

## For AI agents — when compacting

Preserve across `/compact`: files modified this session, test commands run and their results, open PR numbers with branch names.
