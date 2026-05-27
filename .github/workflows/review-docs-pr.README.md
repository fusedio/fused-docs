# Auto-review on PR open

Posts two comments on every PR opened against `main`:

1. **📄 Mechanical SDK review** — link to a live Fused UDF that introspects the
   cloud SDK against documented signatures. Refreshes on every click.
2. **🤖 Claude review** — qualitative review of prose, examples, internal links,
   and workflow claims. Posted as a 4-bucket markdown report
   (`blocks_merge` / `app_repo_fix` / `nice_to_have` / `unknown`).

Both comments use hidden markers (`<!-- review-docs-pr:mechanical -->` and
`<!-- review-docs-pr:claude -->`) so re-pushing the PR updates them in place
instead of stacking new comments.

## One-time setup

### 1. GitHub secrets

Two repository secrets must exist on `fusedio/fused-docs`:

| Secret | Value | How to get it |
|---|---|---|
| `ANTHROPIC_API_KEY` | Anthropic API key | https://console.anthropic.com/settings/keys |
| `GITHUB_TOKEN` | (built-in) | Provided automatically by Actions, no setup needed |

Set via `gh secret set ANTHROPIC_API_KEY --repo fusedio/fused-docs` or in the
repo Settings → Secrets and variables → Actions.

### 2. The mechanical UDF must stay public

The workflow points at this public Fused share token:

- Widget URL: `https://www.fused.io/share/fc_z8RQeHReLxcEWyB2nmGJz/widget_dashboard`
- Raw UDF: `https://udf.ai/fc_z8RQeHReLxcEWyB2nmGJz/review_pr.html`

Both are public read by design — no auth, anyone with the link can re-run.
If the share token is rotated, update the URLs in `review-docs-pr.yml`.

The UDF source lives at `tools/docs_pr_reviewer/review_pr.py`. To redeploy
after edits, `cd tools/docs_pr_reviewer && fused canvas push .`

### 3. The Claude skill must be committed

The workflow expects the skill at `.claude/skills/review-docs-pr/SKILL.md`.
The Claude Code action looks there automatically.

## What gets reviewed

| File pattern | Reviewed by | Bucket priority |
|---|---|---|
| `docs/python-sdk/**.mdx` | UDF (mechanical) + Claude | `blocks_merge`, `app_repo_fix` |
| `blog/**` | Claude only | `unknown` for claim verification |
| `docs/**` prose | Claude only | `unknown` for Workbench UI claims |
| `scripts/**`, `.github/**` | Skipped — "no docs review needed" | — |

## Disabling for a PR

Add the label `skip-review` (or just ignore the comments — they're advisory,
not gating). The workflow does not block merges; it only posts comments.

## Cost

- UDF: billed per call, ~$0.001 per click
- Claude: ~$0.05–0.20 per PR for typical docs PRs (a few changed files)

Negligible for the volume on `fusedio/fused-docs`.
