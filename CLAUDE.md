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

- Hand-edit any file under `docs/python-sdk/api-reference/`, `docs/python-sdk/top-level-functions.mdx`, or `docs/cli/` — these are generated from fused-py source (the CLI pages from the `fused` Click command tree). Edit the generator (`utils/generate_reference_docs.py`) or the CLI command definitions in fused-py instead.
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
npm run check-links                        # fast check for broken internal page/asset links
uv run utils/test_api_reference_coverage.py   # API reference coverage gate
uv run utils/test_doc_snippets.py          # syntax-check all Python blocks in docs
```

Before pushing any branch touching `docs/python-sdk/` or `utils/generate_reference_docs.py`, run both the build and the coverage gate. Run `test_doc_snippets.py` after adding or editing any Python code block.

## Broken links

Two complementary, **non-blocking** checks surface broken links — neither fails a PR:

- **Internal page & asset links** — `npm run check-links` (script: `scripts/check-doc-links.js`) resolves every internal link in `docs/` against the real Docusaurus URL space (slug/`id` rules, folder-index collapse, redirects, blog, generated `widget-api` pages, and `static/` assets) in ~1s with no network. A non-blocking pre-commit hook runs it automatically (`--warn` mode: prints the report, never blocks the commit). To use the hook, enable pre-commit once: `pip install pre-commit && pre-commit install`. Run `npm run check-links` directly for a one-off check (exits non-zero on findings).
- **Anchors (`#fragment`) & cross-page links** — the build (`onBrokenLinks: "throw"`, `onBrokenMarkdownLinks: "throw"` in `docusaurus.config.ts`) hard-fails on broken page links, while `onBrokenAnchors: "warn"` prints broken anchors as warnings without failing. Anchors can't be checked from source (many headings are emitted by MDX components), so the build is the only accurate anchor check — scan its output for `broken anchors` warnings.

## Python code block conventions

Every `python` fence in the docs is syntax-checked automatically (pre-commit hook + CI). Keep code blocks valid Python:

- **Shell commands** (`pip install`, `fused run`, etc.) must use a `bash` fence, not `python`.
- **Pseudocode blocks** (REPL output, type stubs, emoji annotations, partial signatures, HTML embedded in a python block, bare URLs or other non-Python illustrative content) must start with `# doctest: skip` as their first line. This suppresses both the syntax check and Tier 2 execution without hiding the block from readers.
- **Generated files** (`docs/python-sdk/api-reference/` and `docs/python-sdk/top-level-functions.mdx`) are excluded from the check automatically — never add skip markers there.

### Tier 2 — execution (CI)

Tier 2 (the `execution-check` job in `.github/workflows/test-doc-snippets.yml`) executes the runnable Python blocks in the docs via pytest-markdown-docs. It runs **in CI** on every PR — no local pre-commit setup needed.

Execution is **local-engine and fast** — `conftest.py` defaults `fused.run` (and direct UDF calls) to `engine="local"`, so UDFs run in-process with no authentication. Blocks that need external context (data files/URLs, cloud storage, a database, the network, or a live Fused catalog/account call) are **auto-skipped** by a pattern in `conftest.py`, so the full suite finishes in a few seconds and works headlessly.

Two ways to control a single block:
- `# doctest: skip` on its first line — exclude it (also skips Tier 1's syntax check).
- `{/* pmd-metadata: continuation */}` directly above its fence — run it with the previous block's code prepended (for narrative snippets that reuse earlier names).

Run it locally (e.g. before pushing) against the whole tree or specific files:

```bash
uv run utils/run_doc_execution.py                      # full docs/ tree
uv run utils/run_doc_execution.py docs/guide/foo.mdx   # specific files
```

(The Tier 1 syntax check still runs both in CI and as an optional pre-commit hook — `pip install pre-commit && pre-commit install`.)

## For AI agents — when compacting

Preserve across `/compact`: files modified this session, test commands run and their results, open PR numbers with branch names.
