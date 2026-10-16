# API reference pipeline — fused-docs

`docs/python-sdk/top-level-functions.mdx`, the `api`, `options`, `jobpool`, `udf` and `h3` pages in `docs/python-sdk/api-reference/`, every page in `docs/cli/`, and the **Query parameters** table in `docs/rest-api/h3.mdx` are **generated**. Never edit these directly.

---

## How to regenerate

```bash
# Regenerate all API reference MDX against the latest published fused package
uv run --reinstall-package fused utils/generate_reference_docs.py

# Verify coverage (every allowlisted method exists in the package AND in the MDX)
uv run utils/test_api_reference_coverage.py
```

Regenerate the `GET /h3/query` parameter table from the deployed server's OpenAPI spec with `python3 utils/generate_rest_reference.py`.

---

## Files

| File | Purpose |
|---|---|
| `utils/generate_reference_docs.py` | Generator — parses fused-py with griffe, renders MDX via griffe2md |
| `utils/test_api_reference_coverage.py` | Coverage gate — red/green test for the generator output |
| `utils/generate_rest_reference.py` | Generator for the `GET /h3/query` parameter table in `docs/rest-api/h3.mdx`, from https://www.fused.io/server/openapi.json. Descriptions live in `ROWS`; it fails on a parameter or `format` value that has none |
| `update-api-docs.yaml` in `fusedlabs/application` | Automation: on every `fused-py-v*` tag, checks out fused-docs, runs both generators, and opens a PR on `api-docs/fused-py-v<version>` |
| `.github/workflows/update-api-reference.yml` | Manual fallback for the Python reference only |

---

## Design rules — don't change without understanding why

**Bare name headings**
`fused.api` functions render as `## access_token`, not `## fused.api.access_token`.
Controlled by `show_root_full_path = False` in the per-section griffe2md config.
Same for `fused.h3`. FusedAPI class methods are `### method_name` (level 3).

**Alphabetical ordering**
All function/method lists in the generator are sorted. This makes release diffs stable — new methods slot in without displacing existing ones.

**MDX brace escaping**
griffe2md can emit docstring template variables like `{source_dir}` as raw text. MDX 3 treats bare `{expr}` as JSX and fails the SSG production build. The `escape_mdx_braces()` post-processor rewrites these to `\{source_dir\}` — except inside fenced code blocks and inline backtick spans.

**`<code>` tag replacement**
griffe2md templates emit `<code>str</code>` HTML for parameter types. The `fix_code_tags()` post-processor converts these to backtick inline code for readability. Both post-processors run at every file write.

**Test script is a gate, not a wishlist**
Allowlists in `test_api_reference_coverage.py` must match what the generator actually produces. Method in package but not in the allowlist → warning (stale allowlist). Method in allowlist but missing from MDX → failure.

---

## Before pushing

Run both checks in parallel:

```bash
uv run utils/test_api_reference_coverage.py &
npm run build &
wait
```

Use `npm run build` (SSG), not `npm run serve` — dev mode hides MDX errors that only surface in production.

---

## Automation

Releases are handled by `update-api-docs.yaml` in `fusedlabs/application`, which runs on every `fused-py-v*` tag. Its REST step has `continue-on-error`, so a new parameter with no description in `ROWS` shows as a failed step in that run without blocking the Python reference PR.

Rerun it without a release:
```bash
gh workflow run update-api-docs.yaml -R fusedlabs/application
```

Regenerate only the Python reference from this repo:
```bash
gh workflow run update-api-reference.yml -f version=2.8.0
```
