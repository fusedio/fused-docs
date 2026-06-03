# Changelog entry generator

Generate a new changelog entry for `docs/python-sdk/changelog.mdx`.

## Automated mode (CI)

This command runs in two modes:

- **Interactive mode** — a human runs `/changelog` with no arguments. Follow Step 1 to gather inputs, and Step 5 to open the PR.
- **Automated mode (CI)** — invoked as `/changelog <version> <date>` (e.g. `/changelog 2.9.0 2026-06-15`) with a `release-notes.md` file present in the repo root. This is how the `changelog.yaml` workflow in `fusedlabs/application` calls it after a release.

When in **Automated mode**:
1. **Skip Step 1's prompts.** Take the version and date from the arguments, and read the merged-PR list from `release-notes.md` in the repo root (GitHub's auto-generated notes between the previous and current release tag).
2. Apply Steps 2–4 exactly as written to produce the entry and insert it at the top of `docs/python-sdk/changelog.mdx`.
3. **Do not add screenshot/GIF embeds or any `{/* TODO */}` placeholders** to `changelog.mdx` — the entry must read cleanly on its own. Instead, if the entry has any named feature sections, write a file `changelog-media-todo.md` in the repo root with one bullet per named feature (just the feature names). The workflow posts that list as a comment on the PR and then discards the file — it never becomes part of the changelog. If there are no named features, do not create the file.
4. **Skip Step 5 entirely.** Do not create a branch, commit, or open a PR — the workflow handles git and opens the PR via `peter-evans/create-pull-request`. Edit `changelog.mdx` (and optionally write `changelog-media-todo.md`) and stop.

## Step 1 — Gather the inputs

Ask the user for:
1. **Version number** (e.g. `v2.6.0`)
2. **Release date** (default to today's date if not provided)
3. **Source of changes** — one of:
   - A list of GitHub PR numbers or URLs
   - A Notion page / Linear ticket with the release summary
   - A raw list of bullet points describing what changed
   - "I'll paste the git log" — in which case, prompt them to paste it

If the user gives PR numbers, use `gh pr view <number> --json title,body` to fetch each one.

## Step 2 — Categorize the changes

Read through all the provided changes and sort them into three buckets:

| Bucket | What goes here |
|--------|----------------|
| **Named features** (0–3 items) | The most impactful, user-visible new capabilities. Each gets its own bold heading + 1–2 sentence description + optional screenshot/video embed. |
| **Improvements** (5–6 max) | Smaller enhancements, UI polish, new options, performance wins that users notice. Pick only the **5–6 most important, user-facing** ones — this is a highlight reel, not an exhaustive list. |
| **Bug fixes** (4–5 max) | Fixed regressions or broken behaviors users would actually notice. Pick only the **4–5 most important**. Start each bullet with "Fixed:". |

**Exclude entirely** (do not mention):
- Infrastructure upgrades (Amazon Linux, Kubernetes, DB versions)
- Internal refactors, state management changes, SQL query handling
- Caching optimizations invisible to users
- Admin-only endpoints or agent infrastructure fixes
- Anything that is purely internal and has no user-facing effect

## Step 3 — Apply the writing rules

### Feature naming conventions
- Widget builder → always write as **[Widgets](/guide/data-input-outputs/import-connection/widgets)**
- Canvas → [Canvas](/workbench/udf-builder/canvas)
- H3 analytics → [H3 analytics](/guide/h3-analytics/h3-overview)
- Shared tokens / API endpoints → [tokens & endpoints](/guide/data-input-outputs/export-api/tokens-endpoints)
- Slack integration → [Slack integration](/guide/data-input-outputs/export-api/slack)

Use Docusaurus-style relative paths for all internal links. Link to relevant docs pages wherever it makes sense.

### Section structure
- **0–3 named feature sections** — bold heading (`**Feature name**`), followed by 1–2 sentences of plain English description. Embed a screenshot/video only if you have a real asset URL; never insert a placeholder or TODO.
- **Improvements** — flat unordered list of the **5–6 most important** user-facing items, grouped by topic (all canvas items together, all AI items together, etc.). Do not list in PR order, and do not dump every change.
- **Bug fixes** — flat unordered list of the **4–5 most important** user-facing fixes, each starting with `Fixed:`.

### Tone
- Write for end users, not engineers. Avoid jargon.
- Be concise. One sentence per bullet.
- Don't repeat the section heading in the bullet text.

## Step 4 — Draft the entry

Insert the new entry at the top of `docs/python-sdk/changelog.mdx`, immediately after the frontmatter block and the `# Changelog` heading. Use this template:

```mdx
## v{VERSION} ({DATE})

**{Feature 1 heading}**

{1–2 sentence description.}

See the [{relevant docs page}]({path}) to get started.

**{Feature 2 heading}** *(if applicable)*

{1–2 sentence description.}

**Improvements**

- {bullet}
- {bullet}

**Bug fixes**

- Fixed: {bullet}
- Fixed: {bullet}
```

## Step 5 — Open a PR

> **Automated mode (CI):** skip this step. The `changelog.yaml` workflow opens the PR for you — just leave the edited `changelog.mdx` in the working tree.

1. Create a branch named `changelog_{version_underscored}` (e.g. `changelog_2_6_0`)
2. Commit with message: `docs: add v{VERSION} changelog entry`
3. Open a draft PR with title `docs: add v{VERSION} changelog entry`
4. PR description should include: version, date, list of PRs included, and a note to add screenshots/videos before merging if they are missing

**Do not include Notion links in the PR description.**

## Reference: recent entry format

See `## v2.5.0` in `docs/python-sdk/changelog.mdx` for a complete example of the expected output format.
