# fused-docs — Claude instructions

## Core rules

- **Test before documenting**: Before changing any doc reference or code block, run the code yourself. Spin up a small UDF with the fused CLI and confirm it works. Don't document something you haven't verified.
- **Write for humans and agents**: Humans can click — link to the UI, to other pages, to live examples. Agents use the CLI — include the exact commands to run. A good doc serves both.
- **No hand-editing generated files**: Everything under `docs/python-sdk/api-reference/` and `docs/python-sdk/top-level-functions.mdx` is generated. Edit the generator, not the output.

## Slash commands (`.claude/commands/`)

| Command | When to use |
|---|---|
| `/mdx-components` | Before adding or editing any MDX — lists every custom component, admonition, and when to use each |
| `/api-reference` | Before touching anything in `docs/python-sdk/` or `utils/` — covers the generation pipeline, test gate, and design rules |

## Build & test

```bash
npm run build        # full SSG build — use this, not npm run serve
npm run serve        # dev mode only — hides MDX errors that break production
uv run utils/test_api_reference_coverage.py   # API reference coverage gate
```

Before pushing any branch touching `docs/python-sdk/` or `utils/generate_reference_docs.py`, run the coverage test and `npm run build` in parallel. Check CI after pushing.
