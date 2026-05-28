# fused-docs — Claude instructions

See @README.md for project overview and @package.json for available npm scripts.

## Docs structure

Understanding where content belongs and how each section is written:

| Section | Purpose | Writing style |
|---|---|---|
| **Guide** (`docs/guide/`) | Explore all aspects of Fused — concepts, setup, workflows | Concept-first. Explain the why, then the how. Link to API Reference for method details. |
| **Examples** (`docs/examples/`) | Hands-on, concrete things you can build | Task-first. Show the code, explain what it does. Link back to Guide for concepts, API Reference for method signatures. |
| **API Reference** (`docs/python-sdk/`) | Exhaustive source of truth for the `fused` Python API and all available widgets | Generated — do not hand-edit. Every method, every parameter. No prose beyond what the docstring provides. |
| **Workbench Manual** (`docs/workbench/`) | Reference for the Workbench UI — same philosophy as API Reference but for the interface | UI-first. Screenshot-heavy. Describe what each element does, not how to build with it. |

Before adding a page, ask: is this a concept (Guide), a recipe (Examples), a reference entry (API Reference), or a UI element (Workbench Manual)? Put it in the right section and write it in that section's voice.

## Core rules

- **Test before documenting**: Before changing any doc reference or code block, verify the code runs. See [Testing code](#testing-code) below.
- **Write for humans and agents**: Humans can click — link to the UI, to other pages, to live examples. Agents use the CLI — include the exact commands to run.
- **Use absolute links**: `[page](/python-sdk/quickstart)` not `[page](../quickstart)`. Relative links break when pages move.

## Testing code

Every code block in the docs must be runnable. Before committing:

1. Write a minimal UDF that exercises the feature:
    ```python
    @fused.udf
    def udf():
        # your test code here
        return result
    ```
2. Run it with the fused CLI (`CANVAS` is required but `""` works for local files):
    ```bash
    fused run "" udf.py
    ```
    Or run it locally without hitting the remote server:
    ```bash
    fused run "" udf.py --engine local
    ```
3. Confirm the output matches what the docs claim. Only then update the doc.

For code that requires credentials or external services, note this explicitly in the doc with a `:::note` admonition.

## Do not

- Hand-edit any file under `docs/python-sdk/api-reference/` or `docs/python-sdk/top-level-functions.mdx` — these are generated. Edit the generator instead.
- Use `npm run serve` to validate — dev mode hides MDX errors that only surface in the SSG production build. Use `npm run build`.
- Document code you haven't run. Test it first.
- Duplicate prose that already exists — check `docs/` for existing content before writing new sections.

## Slash commands (`.claude/commands/`)

| Command | When to use |
|---|---|
| `/mdx-components` | Before adding or editing any MDX — lists every custom component, admonition, and when to use each |
| `/api-reference` | Before touching anything in `docs/python-sdk/` or `utils/` — covers the generation pipeline, test gate, and design rules |

## Build & test

```bash
npm run build        # full SSG build — required before any PR
uv run utils/test_api_reference_coverage.py   # API reference coverage gate
```

Before pushing any branch touching `docs/python-sdk/` or `utils/generate_reference_docs.py`, run both in parallel. Check CI after pushing.

## When compacting

Always preserve: the list of files modified in this session, any test commands that were run and their results, and open PR numbers with their branch names.
