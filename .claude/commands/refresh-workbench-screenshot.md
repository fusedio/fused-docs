---
description: Check a Workbench doc page's workflow against the live UI, file a 3-section drift ticket with a GIF, and refresh its screenshot only if docs and live match.
argument-hint: <page> (e.g. "profile", "integrations")
---

# Refresh workbench screenshot

Primary tool: **Claude for Chrome** (`mcp__Claude_in_Chrome__*`) driving the user's real,
logged-in browser. Target page: **$ARGUMENTS**.

Setup (check once; install if missing): `git`, `ffmpeg`, `curl`, and the Fused CLI
(`fused whoami` must succeed). Find the repo with `git rev-parse --show-toplevel`; doc
images live under `<repo>/static`.

## Steps
1. **Resolve & read all media.** Map `$ARGUMENTS` to a page in `docs/workbench/` (plus any
   linked guide holding the real steps). List its media (`![]` images, `<LazyReactPlayer>`
   `.mp4`). Read the prose and every image. For a video: `curl -s -o v.mp4 <url>` then
   `ffmpeg -i v.mp4 -vf fps=2 f_%02d.png` and read the frames. A doc's own media can
   contradict its prose — note that.
2. **Explore live.** Follow the documented steps on the live workbench. If an option
   isn't where the doc says, look elsewhere (sidebar, in-canvas avatar menu, tabs);
   record where it actually is, or that it's absent.
3. **Compare.** Table: aspect → docs say → live shows → verdict.
4. **Decide.** Mismatch/missing → do **not** refresh; file the ticket (below). Full match
   → refresh the screenshot (below). Never silently edit docs or capture a stale state.

## Refresh a screenshot
The extension's `screenshot save_to_disk` doesn't produce a usable file, but its GIF
export does. So: reach the UI state, then `gif_creator` start_recording → screenshot →
export `download:true` (GIF lands in the browser's Downloads). Extract the final frame:
`ffmpeg -y -i <downloads>/<file>.gif f_%03d.png` and copy the last frame to the repo path
`<repo>/static/img/workbench/.../<name>.png`. Then `git status` the path; don't commit
unless asked. (Backup, optional: a local Playwright tool attached to a debug Chrome over
CDP gives pixel-precise stills — only if set up.)

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
