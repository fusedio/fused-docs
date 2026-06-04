# Fused Shorts — publish skill

`/shorts` is a separate Docusaurus blog instance at `shorts/` in the repo root (never `blog/`). Posts are 300–600 words, personal, numbered, part of the **Road to Zero Coding** series.

Style reference: [`/blog/notes-from-eo-summit`](https://docs.fused.io/blog/notes-from-eo-summit) — short, numbered sections, links out, personal tone.

## 1 — Get the content

**From a Notion URL:** use the Notion MCP tool — WebFetch cannot read authenticated pages.

```
mcp__claude_ai_Notion__notion-fetch({ id: "<notion url>" })
```

**From Markdown / pasted text:** use as-is.

## 2 — Next number

```bash
ls shorts/ | sort
```

Increment the highest `zero-coding-NNN`. Zero-pad to 3 digits.

## 3 — File structure

```
shorts/YYYY-MM-DD-zero-coding-NNN/
  index.mdx
  image-name.png    ← only if post has images
```

## 4 — Frontmatter

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

`authors` are defined in `shorts/authors.yml` — currently only `max`.

## 5 — Post structure

```mdx
import ShortsFooter from '@site/src/components/ShortsFooter';
import imgFoo from './image-name.png';   ← only if images are used

# Title (same as frontmatter title)

Opening paragraph — 2–3 sentences of context.

{/* truncate */}

### 1. First section

### 2. Second section

### 3. Third section

---

_This is short #N in the Road to Zero Coding series — short posts on getting towards building Fused 100% without writing a single line of code ourselves._

<ShortsFooter />
```

`{/* truncate */}` controls the excerpt in the index. `<ShortsFooter />` is required — it has feature-flag-controlled newsletter and agent-connect sections (toggle via `SHOW_NEWSLETTER` / `SHOW_CONNECT_AGENT` in `src/components/ShortsFooter/index.tsx`).

## 6 — Images

Place image files next to `index.mdx`. Import at the top.

- Wide screenshots (landscape): `style={{width: '70%', borderRadius: '8px', margin: '1.5rem auto', display: 'block'}}`
- Compact/square: `style={{maxWidth: '480px', width: '100%', borderRadius: '8px', margin: '1.5rem auto', display: 'block'}}`

Follow each image with an italics caption: `_Caption text._`

## 7 — Verify, commit, push

```bash
npm run build:docs 2>&1 | grep -E "ERROR|error TS|\[SUCCESS\]"
```

Must output `[SUCCESS]` before committing. The dev server hot-reload is not sufficient — it can show "compiled successfully" even when a runtime crash exists.

```bash
git add shorts/YYYY-MM-DD-zero-coding-NNN/
git commit -m "feat: add short #NNN — <title>"
git push
```

Target `main` for the PR.

## Key files

| File | Purpose |
|---|---|
| `shorts/authors.yml` | Author definitions |
| `src/components/ShortsFooter/index.tsx` | Footer with feature flags |
| `src/theme/BlogListPage/index.tsx` | Detects `/shorts` route, renders title-only list |
| `docusaurus.config.ts` | Plugin: `id: "shorts"`, `routeBasePath: "shorts"`, `path: "./shorts"` |
