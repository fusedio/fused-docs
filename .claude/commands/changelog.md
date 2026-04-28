# Changelog entry generator

Generate a new changelog entry for `docs/python-sdk/changelog.mdx`.

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
| **Improvements** | Smaller enhancements, UI polish, new options, performance wins that users notice. |
| **Bug fixes** | Fixed regressions or broken behaviors. Start each bullet with "Fixed:". |

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
- **0–3 named feature sections** — bold heading (`**Feature name**`), followed by 1–2 sentences of plain English description. Add a screenshot or video embed if one exists.
- **Improvements** — flat unordered list, grouped by topic (all canvas items together, all AI items together, all home page items together, etc.). Do not list in PR order.
- **Bug fixes** — flat unordered list, each starting with `Fixed:`.

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

{Optional: screenshot or video embed — copy the JSX pattern from a nearby entry}

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

1. Create a branch named `changelog_{version_underscored}` (e.g. `changelog_2_6_0`)
2. Commit with message: `docs: add v{VERSION} changelog entry`
3. Open a draft PR with title `docs: add v{VERSION} changelog entry`
4. PR description should include: version, date, list of PRs included, and a note to add screenshots/videos before merging if they are missing

**Do not include Notion links in the PR description.**

## Reference: recent entry format

See `## v2.5.0` in `docs/python-sdk/changelog.mdx` for a complete example of the expected output format.
