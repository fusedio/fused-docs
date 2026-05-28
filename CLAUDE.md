# fused-docs — Claude instructions

## General rules

- **Test before documenting**: Before changing any doc reference or code block, run the code yourself. Use `fused run` locally with a small UDF to confirm it works. Don't document something you haven't verified.
- **Write for humans and agents**: Humans can click — link to the UI, to pages, to examples. Agents use the CLI — include the exact commands to run. A good doc serves both.

---

## API reference PRs

Before pushing any branch that touches `docs/python-sdk/` or `utils/generate_reference_docs.py`, always run these two checks **in parallel**:

1. **Coverage test** — `uv run utils/test_api_reference_coverage.py`
2. **Full production build** — `npm run build`

Do not rely on `npm run serve` — dev mode hides MDX rendering errors that only surface in the SSG production build.

After pushing, check that CI passes on the PR before reporting it as done.

---

## API reference pipeline

The Python SDK API reference is **fully generated** from the fused-py package. Docs are never edited by hand.

**Run the generator:**
```bash
uv run --reinstall-package fused utils/generate_reference_docs.py
```

**Key design rules — don't change without understanding why:**

- **Bare name headings**: `fused.api` functions render as `## access_token`, not `## fused.api.access_token`. Controlled by `show_root_full_path = False` in the per-section config. Same for `fused.h3`.
- **Alphabetical ordering**: All function lists must be sorted so diffs are stable across releases.
- **MDX brace escaping**: griffe2md can render docstring variables like `{source_dir}` into text. MDX 3 evaluates bare `{expr}` as JSX and fails the SSG build. The `escape_mdx_braces()` post-processor in the generator escapes these — except inside fenced code blocks and inline backtick spans.
- **`<code>` tag replacement**: griffe2md templates emit `<code>str</code>` for parameter types. The `fix_code_tags()` post-processor converts these to backticks. Both post-processors run at every file write.
- **Test script is a gate, not a wishlist**: allowlists in `test_api_reference_coverage.py` must match what the generator actually produces. Method in package but not in allowlist → warning. Method in allowlist but missing from MDX → failure.
