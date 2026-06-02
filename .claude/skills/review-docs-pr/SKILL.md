---
name: review-docs-pr
description: >
  Review a fused-docs pull request. Classifies the PR by what changed,
  runs deterministic SDK introspection on the API-reference portion via the
  deployed Fused UDF, and reasons about prose / examples / guides directly.
  Always emits the same 4-bucket report (blocks_merge, app_repo_fix,
  nice_to_have, unknown). Use when the user asks to review or check a
  fused-docs PR (e.g. "/review-docs-pr 1124" or "check PR 1130").
---

# Review fused-docs PR

This skill reviews a pull request against `fusedio/fused-docs`. The goal is
to flag anything that would mislead a reader, not to gatekeep style.

## Inputs

A PR number (e.g. `1124`) or a full PR URL. Optional repo override; defaults
to `fusedio/fused-docs`.

## Output

A single markdown report with **four buckets**:

- 🔴 **blocks_merge** — fix in this PR before merging. SDK conflict, broken
  link, example that can't possibly work.
- 🟡 **app_repo_fix** — upstream docstring / code fix needed in
  `fusedlabs/application` before regenerating docs.
- 🔵 **nice_to_have** — quality regression that won't break users (lost
  example, dropped parameter note).
- 🟣 **unknown** — change touches something that needs the live product to
  verify (Workbench UI flow, screenshot freshness, whether a workflow still
  matches reality). **Say "I don't know" explicitly — don't guess.**

Each finding is one line: `<file>:<lineish> — <what's wrong> — <why it matters>`.

## Steps

### 1. Fetch PR metadata

```bash
gh pr view <N> --repo fusedio/fused-docs --json title,body,headRefName,baseRefName,files
gh api repos/fusedio/fused-docs/pulls/<N>/files --paginate --jq '.[].filename'
```

### 2. Classify the PR by changed files

Bucket files into one of these groups (a PR can span multiple — handle each
subset with the matching checks):

| File pattern | Group | Checks |
|---|---|---|
| Branch `api-docs/**` AND only `docs/python-sdk/**.mdx` | `api_ref` | L1 mechanical UDF (step 3) |
| `blog/**` | `blog` | L3 prose (step 5) + L2 link/image existence |
| New `.mdx` under `docs/use-cases/`, `docs/examples/`, canvas dirs | `example` | L2 code-blocks + L3 prose |
| Edits to existing prose `docs/**.mdx` (not python-sdk, not blog) | `guide_revision` | L3 prose, lean on `unknown` for workflow changes |
| `sidebars.js`, `docusaurus.config.ts`, `package.json` | `nav` | Check internal references resolve |
| `scripts/**`, `.github/**`, `tools/**`, `_*.fused` | `plumbing` | Skip — emit one line: "no docs review needed" |
| Everything else | `other` | Flag into `unknown` |

If `headRefName` matches `api-docs/**`, treat the whole PR as `api_ref` even
if other files snuck in.

### 3. L1 — Run the SDK introspection UDF (only for `api_ref` files)

Call the deployed mechanical reviewer. **Always pass `engine="realtime"`** so
the introspection runs against the live cloud SDK, never against whatever
`fused` happens to be installed locally:

```bash
uv run --with fused --with pandas --with requests python <<'PY'
import fused, json
udf = fused.load("aman@fused.io/review_pr", collection_name="docs_pr_reviewer")
df = fused.run(
    udf,
    pr_number="<N>",
    repo="fusedio/fused-docs",
    output="table",
    engine="realtime",   # required: ensures cloud-side SDK is used
)
print(df.to_json(orient="records"))
PY
```

The local `fused` install is only a thin RPC client here — the UDF executes
on Fused's realtime infrastructure and introspects whatever SDK version is
deployed there. That's the version users actually run.

Parse the JSON. Each row already has a `bucket`, `file`, `finding`, `detail`
— pass them through to the report as-is.

If the UDF errors (e.g. installed `fused` version doesn't match the release),
note that as a single `unknown` row and continue.

### 4. L2 — Code-block static check (only for `example`, `blog` with code)

For each changed `.mdx`, extract \`\`\`python code blocks. For each block:

- Parse with `ast.parse`. Syntax error → `blocks_merge`.
- Find every `fused.X.Y(...)` call. For each: `uv run --with fused python -c
  "import fused; getattr(<resolve>, ...)"` — if missing → `blocks_merge`.
- Look for `fd://`, `s3://`, `https://` URLs that are clearly placeholders
  (`fd://my-bucket/...`, `s3://fused-users/...`) and flag those as
  `nice_to_have` so writers replace with realistic examples.

### 5. L3 — Prose review (everything that isn't `api_ref` or `plumbing`)

Read the changed file at `head`. For prose changes:

- **Internal links** — for each `[text](/path)` or `[text](path.mdx)`, check
  the target exists in the worktree (or in the PR head). Broken → `blocks_merge`.
- **External links** — flag `http(s)://` links that look stale (e.g.
  `localhost`, `staging.`, `127.0.0.1`) → `blocks_merge`.
- **Image references** — `![](./img/foo.png)`: file must exist in PR head.
- **Workflow claims** — when prose describes a Workbench flow ("click X,
  then Y appears"), you almost never know if that's still true. **Default
  to `unknown`** and quote the specific sentence.
- **Screenshot freshness** — referenced PNG/JPG in `static/img/**`: if
  introduced more than 6 months before the PR's base commit, flag as
  `unknown` ("screenshot may be stale, verify in current Workbench").

### 6. Emit the report

Use this exact structure so the output is consistent across PR types:

```markdown
# PR #<N> review — <title>

**Type:** <api_ref | blog | example | guide_revision | nav | mixed>
**Files changed:** <count>
**fused SDK version (UDF run):** <version or "n/a">

## 🔴 Blocks merge (<count>)
- `<file>` — <finding> — *<detail>*

## 🟡 Needs application repo fix (<count>)
- ...

## 🔵 Nice to have (<count>)
- ...

## 🟣 Needs human review (<count>)
- `<file>` — <what you couldn't verify> — *<what to check in Workbench / live site>*

## Summary
<one-paragraph synthesis: merge with fixes? merge as-is? block?>
```

If a bucket is empty, write `_None_` under the heading — don't drop the heading.

## Behavioural rules

- **Never guess workflow correctness.** If a doc says "the canvas now opens
  in side panel mode", you don't know that. Put it in `unknown`.
- **Don't repeat the same finding** across L1/L2/L3 — pick the bucket that
  best describes the fix, not all of them.
- **No emojis in the report** other than the bucket headers above.
- **Quote file paths verbatim** so the user can click through.
- **Don't suggest stylistic edits** — only flag things that mislead readers.

## Examples of judgment calls

- Docstring example says `fused.api.upload("file.json", "s3://...")` but the
  current convention is `fd://`. → `nice_to_have` ("update example to fd://").
  Not `blocks_merge` because the call still works.
- Page describes a 3-step workflow with screenshots from Workbench. → All
  three steps go to `unknown` with a note "verify in current Workbench".
- New blog post claims "Fused is 10× faster than X". → `unknown` ("benchmark
  claim, verify with author").
- Sidebar entry points at a renamed file. → `blocks_merge`.

## When NOT to use this skill

- Reviewing a PR in any repo other than `fusedio/fused-docs` (or a fork).
- Reviewing application-repo PRs — those have their own review tooling.
- General code review of `.py` UDF files outside `docs/`.
