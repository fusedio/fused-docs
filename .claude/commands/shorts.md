# Fused Shorts — publish skill

End-to-end guide for publishing a new post to `docs.fused.io/shorts`. Read this fully before touching any file.

---

## What Shorts are

`/shorts` is a separate Docusaurus blog instance (distinct from `/blog`). It lives at `shorts/` in the repo root. Posts are short (300–600 words), personal, numbered, and part of the **Road to Zero Coding** series — about building Fused without writing code ourselves.

Style reference: [`/blog/notes-from-eo-summit`](https://docs.fused.io/blog/notes-from-eo-summit) — short, numbered sections, links out, personal tone.

---

## Step 1 — Get the content

**From a Notion URL:** Use the Notion MCP tool directly. Never use WebFetch for Notion — it can't read authenticated pages.

```
mcp__claude_ai_Notion__notion-fetch({ id: "<notion url>" })
```

**From Markdown / pasted text:** Use as-is.

---

## Step 2 — Determine the next number

```bash
ls shorts/ | sort
```

Take the highest `zero-coding-NNN` number and increment. Zero-pad to 3 digits: `001`, `002`, `003`…

---

## Step 3 — Create the file structure

```
shorts/
  YYYY-MM-DD-zero-coding-NNN/
    index.mdx
    image-name.png   ← only if post has images
```

Directory name: `YYYY-MM-DD-zero-coding-NNN` — use the intended publish date.

---

## Step 4 — Frontmatter template

```mdx
---
title: "Human readable title — no number prefix"
description: "1–2 sentence excerpt shown in the /shorts listing."
slug: zero-coding-NNN
date: YYYY-MM-DD
authors: [max]
tags: [relevant, tags]
---
```

- `title`: plain human title, no `#001 —` prefix
- `slug`: always `zero-coding-NNN` (zero-padded)
- `authors`: defined in `shorts/authors.yml` — currently only `max`

---

## Step 5 — Post structure

```mdx
import ShortsFooter from '@site/src/components/ShortsFooter';
import imgFoo from './image-name.png';   ← only if images are used

# Title (same as frontmatter title)

Opening paragraph — 2–3 sentences of context. What prompted this.

{/* truncate */}

### 1. First section

Content...

### 2. Second section

Content...

### 3. Third section

Content...

---

_This is short #N in the Road to Zero Coding series — short posts on getting towards building Fused 100% without writing a single line of code ourselves._

<ShortsFooter />
```

**Required elements:**
- `import ShortsFooter` at the top
- `{/* truncate */}` after the opening paragraph (controls the excerpt shown in the index)
- `<ShortsFooter />` as the last element
- Closing italics line with the correct `#N` number

---

## Step 6 — Images

Place image files in the post directory alongside `index.mdx`. Import at the top of the file.

**Sizing rules:**
- Wide screenshots (landscape, >800px wide): `style={{width: '70%', borderRadius: '8px', margin: '1.5rem auto', display: 'block'}}`
- Compact/square images: `style={{maxWidth: '480px', width: '100%', borderRadius: '8px', margin: '1.5rem auto', display: 'block'}}`

Always add a caption in italics below: `_Caption text._`

---

## Step 7 — Verify before committing

**Always run this synchronously — do not skip:**

```bash
npm run build:docs 2>&1 | grep -E "ERROR|error TS|\[SUCCESS\]"
```

This catches MDX syntax errors, broken imports, and TypeScript issues. If it outputs `[SUCCESS]` you're good. Fix any errors before proceeding.

**Do not** rely on the dev server hot-reload to catch errors — it can show "compiled successfully" even when a runtime crash exists. Always use the build.

---

## Step 8 — Commit and push

```bash
git add shorts/YYYY-MM-DD-zero-coding-NNN/
git commit -m "feat: add short #NNN — <title>"
git push
```

If opening a new PR, target `main`.

---

## Step 9 — Merge conflict on llms.txt

These files are auto-generated and will conflict whenever main has moved. Resolve with:

```bash
git checkout --theirs static/llms.txt static/llms-full.txt static/llms-python-sdk.txt
node scripts/generate-llms-txt.js
git add static/llms.txt static/llms-full.txt static/llms-python-sdk.txt
git commit -m "chore: resolve llms.txt conflicts, regenerate"
```

---

## Pitfalls — do not repeat these

**Wrong location.** Shorts go in `shorts/`, not `blog/`. The `/blog` and `/shorts` are separate plugin instances. Never add a short to `blog/`.

**Broken JSX comment nesting.** Never use `{/* ... */}` to comment out a block that itself contains `{/* ... */}` — the inner `*/` terminates the outer comment and causes a syntax error. Use boolean flags instead:
```tsx
const SHOW_SECTION = false;
// ...
{SHOW_SECTION && <div>...</div>}
```

**Polling the dev server.** Never use `until grep -q ...; do sleep N; done` inline. Use `Bash run_in_background: true` for a one-shot ready signal, or arm a `Monitor` for ongoing error streaming.

**WebFetch on Notion.** WebFetch cannot read authenticated Notion workspace pages. Always use `mcp__claude_ai_Notion__notion-fetch`.

**Committing without building.** Always run `npm run build:docs` and confirm `[SUCCESS]` before committing.

---

## Component reference

| Component | Import | Use |
|---|---|---|
| `ShortsFooter` | `@site/src/components/ShortsFooter` | Required footer on every short — has feature-flag-controlled newsletter and agent-connect sections |

To enable the newsletter or agent-connect section when they're ready: open `src/components/ShortsFooter/index.tsx` and set `SHOW_NEWSLETTER = true` or `SHOW_CONNECT_AGENT = true`.

---

## Key files

| File | Purpose |
|---|---|
| `shorts/authors.yml` | Author definitions for the shorts plugin |
| `src/components/ShortsFooter/index.tsx` | Footer component with feature flags |
| `src/theme/BlogListPage/index.tsx` | Custom list page — detects `/shorts` route and renders title-only list |
| `docusaurus.config.ts` | Plugin config: `id: "shorts"`, `routeBasePath: "shorts"`, `path: "./shorts"` |
