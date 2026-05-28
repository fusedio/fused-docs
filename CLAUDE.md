# fused-docs — Claude instructions

See @README.md for project overview and @package.json for available npm scripts.

## Core rules

- **Test before documenting**: Before changing any doc reference or code block, run the code yourself. Spin up a small UDF with the fused CLI and confirm it works.
- **Write for humans and agents**: Humans can click — link to the UI, to other pages, to live examples. Agents use the CLI — include the exact commands to run.
- **Use absolute links**: `[page](/python-sdk/quickstart)` not `[page](../quickstart)`. Relative links break when pages move.

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
