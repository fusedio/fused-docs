---
description: Check a Workbench doc page's workflow against the live UI, file a 3-section drift ticket with a GIF, and refresh its screenshot only if docs and live match.
argument-hint: <page> — a single doc page slug (e.g. "profile", "integrations/s3"), not a section
---

# Refresh workbench screenshot

Primary tool: **Claude for Chrome** (`mcp__Claude_in_Chrome__*`) driving the user's real,
logged-in browser. Target page: **$ARGUMENTS**.

Setup (check once; install if missing): `git`, `ffmpeg`, `curl`, and the Fused CLI
(`fused whoami` must succeed). Find the repo with `git rev-parse --show-toplevel`; doc
images live under `<repo>/static`.

## Steps
1. **Resolve & read all media.** Resolve `$ARGUMENTS` to a **single** `.mdx` under
   `docs/workbench/` — match the filename **or** the page's `id:`/URL slug (they often
   differ, e.g. `udf-explorer` → `udf-catalog.mdx`); grep frontmatter `id:` when the
   filename doesn't match. If it is ambiguous, names a section with several pages (e.g.
   `integrations`), or you can't confidently pin the file, **ask the user which exact
   page** instead of guessing. List the page's media (`![]` images, `<LazyReactPlayer>`
   `.mp4`). Read the prose and every image. For a video: `curl -s -o v.mp4 <url>` then
   `ffmpeg -i v.mp4 -vf fps=2 f_%04d.png` and read the frames. A doc's own media can
   contradict its prose — note that.
2. **Explore live.** Follow the documented steps on the live workbench. If an option
   isn't where the doc says, look elsewhere (sidebar, in-canvas avatar menu, tabs);
   record where it actually is, or that it's absent.
3. **Compare.** Table: aspect → docs say → live shows → verdict.
4. **Decide.** Mismatch/missing → do **not** refresh; file the ticket (below). Full match
   → refresh **every** referenced screenshot that's now stale (below). Never silently
   edit docs or capture a stale state.

## Refresh screenshots
The extension's `screenshot save_to_disk` doesn't produce a usable file, but its GIF
export does. **Repeat for each stale image the page references** (pages often have
several): reach its UI state, then `gif_creator` start_recording → screenshot → export
`download:true` (GIF lands in the browser's Downloads). Extract frames
`ffmpeg -y -i <downloads>/<file>.gif f_%04d.png` and take the last. Write it to the
destination **derived from that image's own reference**: take the `/img/...` path in its
MDX `![](...)` tag and write to `<repo>/static` + that exact path. Do **not** assume
`/img/workbench/` — pages use other prefixes too. If a target path or prefix is unclear,
ask the user for the appropriate destination. Then `git status` the path; don't
commit unless asked. (Backup, optional: a local Playwright tool attached to a debug
Chrome over CDP gives pixel-precise stills — only if set up.)

## File the drift ticket — Notion, exactly 3 sections
1. **Page targeted** — doc page + its media.
2. **Docs vs Live UI** — the comparison table.
3. **What to resolve** — concrete fixes, open questions, whether a screenshot needs refresh.

Create it in your team's `Engineering Tasks` data source (find via Notion search); set
`BUG`. Attach a **GIF** of the workflow as evidence — record with `gif_creator`, then
store it durably in Fused and reference the stable path (don't embed signed URLs, they
expire):
`fused files upload <gif> "fd://<handle>/claude/<name>.gif"`
Put that `fd://` path in the ticket with the read-back command
`fused files download "fd://<handle>/claude/<name>.gif" .` — get `<handle>` from
`fused whoami`.
