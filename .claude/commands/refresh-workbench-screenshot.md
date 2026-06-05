---
description: Check a Workbench doc page's workflow against the live UI, file a 3-section drift ticket with a GIF, and refresh its screenshots only if docs and live match.
argument-hint: <page> — a single doc page slug (e.g. "profile", "integrations/s3"), not a section
---

# Refresh workbench screenshot

Primary tool: **Claude for Chrome** (`mcp__Claude_in_Chrome__*`) on the user's real,
logged-in browser. Target: **$ARGUMENTS**. Setup (check once): `git`, `ffmpeg`, `curl`,
Fused CLI (`fused whoami`). Repo root: `git rev-parse --show-toplevel`; assets live under
`<repo>/static`.

## Steps
1. **Resolve & read.** Map `$ARGUMENTS` to one `.mdx` in `docs/workbench/` by filename
   **or** frontmatter `id:`/URL slug (they differ, e.g. `udf-explorer` → `udf-catalog.mdx`).
   If ambiguous, a section (e.g. `integrations`), or unresolvable, **ask the user**. Read
   the prose and **every media asset** — `![]`, `ClickZoomImage`, `<img src>`,
   `<LazyReactPlayer>`, `<video>/<source>`. Per video, download to a **unique** name and
   extract frames (`curl -s -o v1.mp4 <url>; ffmpeg -i v1.mp4 -vf fps=2 v1_%04d.png`), then
   read them. Note where a page's own media contradicts its prose.
2. **Explore live.** Follow the documented steps on the live workbench; if an option isn't
   where the doc says, look elsewhere (sidebar, avatar menu, tabs) — record where it
   actually is, or that it's absent.
3. **Compare.** Table: aspect → docs say → live shows → verdict. Also mark each
   referenced image **current or stale** by comparing it against its live state.
4. **Decide.** Mismatch/missing → don't refresh; file the ticket. Full match → refresh
   **every** stale asset. Never silently edit docs or capture a stale state.

## Refresh screenshots
(`screenshot save_to_disk` yields no usable file; the GIF export does.) For **each** stale
asset: reach its UI state → `gif_creator` start_recording → screenshot → export
`download:true` (lands in Downloads) → `ffmpeg -y -i <gif> f_%04d.png`, take the last
frame → write it to `<repo>/static` + the asset's own `/img/...` path (from its `![]`/`src`
tag — don't assume `/img/workbench/`). Ask the user if a path is unclear. `git status` the
paths; don't commit unless asked. (Backup: a local Playwright tool attached to a debug
Chrome over CDP for pixel-precise stills — only if set up.)

## Ticket — Notion, exactly 3 sections
1. **Page targeted** — page + its media.
2. **Docs vs Live UI** — the comparison table.
3. **What to resolve** — fixes, open questions, which assets need refreshing.

Create in your team's `Engineering Tasks` data source (find via search); set `BUG`. Attach
a workflow **GIF** as evidence: record with `gif_creator`, upload to Fused, reference the
stable path (don't embed signed URLs — they expire):
`fused files upload <gif> "fd://<handle>/claude/<name>.gif"` — put that `fd://` path in the
ticket with `fused files download "fd://<handle>/claude/<name>.gif" .` (`<handle>` from
`fused whoami`).
