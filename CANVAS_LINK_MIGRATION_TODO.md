# Canvas link migration: `unstable.fused.io` → `www.fused.io`

Tracking for ITEM-11720 — move all canvas demos from unstable to prod.

## Done (this PR)

| Canvas | Old (unstable) | New (prod) | File |
|---|---|---|---|
| Standardized text to image | `unstable.fused.io/canvas/fc_fused/Standardized_text_to_image` | `www.fused.io/canvas/fc_fused/Standardized_text_to_image` | `docs/examples/branded-text-to-image.mdx` |
| GDrive to infographic | `unstable.fused.io/canvas/fc_fused/gdrive_to_infographic` | `www.fused.io/canvas/fc_fused/gdrive_to_infographic` | `docs/examples/gdrive-to-slides-infographic.mdx` |
| ComfyUI generative AI | `unstable.fused.io/canvas/fc_fused/comfyui_generativeAI` | `www.fused.io/canvas/fc_fused/comfyui_generativeAI` | `docs/examples/comfyui-fused-workflows.mdx` |
| GDrive integration | `unstable.fused.io/canvas/fc_fused/gdrive_integration` | `www.fused.io/canvas/fc_fused/gdrive_integration` | `docs/workbench/integrations/gdrive.mdx` |
| Widgets docs guide | `unstable.fused.io/canvas/fc_fused/Widgets_Docs_Guide` | `www.fused.io/canvas/fc_fused/Widgets_Docs_Guide` | `docs/guide/data-input-outputs/import-connection/widgets.mdx` |
| Widget showcase | `unstable.fused.io/canvas/fc_fused/Widget_Showcase` | `www.fused.io/canvas/fc_fused/Widget_Showcase` | `docs/guide/data-input-outputs/import-connection/widgets.mdx` |
| Google Calendar routing | `unstable.fused.io/canvas/fc_70N994S9ZGgYAuDs6eHzXy` | `www.fused.io/canvas/fc_public/Google_Calendar_routing` | `docs/examples/google-calendar-meetings.mdx` |
| Debugging UDF example | `unstable.fused.io/canvas/fc_29NPh0rbEeqbLc39IxEYIg` | `www.fused.io/canvas/fc_fused/debugging_udf_example` | `docs/guide/working-with-udfs/udf-best-practices/debugging-playbook.mdx` |
| Overture MCP agent | `unstable.fused.io/canvas/fc_7OKlCRLA5FeqcwXkB5wvsq` | `www.fused.io/canvas/fc_fused/overture_fused_mcp` | `docs/examples/overture-maps-mcp-agent.mdx` |
| Overture building release comparison | `unstable.fused.io/canvas/fc_1OKBYKbEo1nab5A4aE2ezb` | `www.fused.io/canvas/fc_fused/Overture_building_release_comparison` | `docs/examples/overture-buildings-agents.mdx` |
| Messy data agents | `unstable.fused.io/canvas/fc_3NzqyeXDOMTNZ5pm1Sm1v8` | `www.fused.io/canvas/fc_fused/joining_messy_data_demo` | `docs/examples/messy-data-agents.mdx` |
| Read subset / ingestion | `unstable.fused.io/canvas/fc_17TeJLzhH83TLBJ9ZpvKoR` | `www.fused.io/canvas/fc_fused/get_chunks_metadata_example` | `docs/guide/data-input-outputs/read-write/geospatial/ingestion.mdx` |
| Sharing canvas dashboards (embed) | `unstable.fused.io/canvas/fc_4Dr6z6OuYHboSbs3VbpdEc?embed=true` | `www.fused.io/canvas/fc_fused/Minimal_live_dashboard?embed=true` | `docs/examples/sharing-canvas-dashboards.mdx` |

## Pending

All `/canvas/` links are migrated — none pending.

## Provided prod link with no current doc usage

- `www.fused.io/canvas/fc_public/airtable_integration` — no `airtable` canvas link currently exists in the docs; ready to use if an Airtable integration page is added.

## Out of scope (not `/canvas/` links, still on unstable)

Flagged for a follow-up — these are `/server/`, `/share/`, and `/workbench/` URLs, not canvas links:

- `docs/guide/data-input-outputs/import-connection/widgets.mdx` — `/share/fc_1bHh5W6D1Yk6smpCeUuWPy...` (lines 143, 328, 335)
- `docs/examples/overture-maps-mcp-agent.mdx` — `/share/fc_7OKlCRLA5FeqcwXkB5wvsq/overture_ai_chat_widget` (line 13)
- `docs/workbench/udf-builder/viz-styling.mdx` — `/server/v1/realtime-shared/UDF_Property_Based_Color/...` (lines 1215, 1221)
- `docs/guide/h3-analytics/converting.mdx` — `/server/v1/realtime-shared/fc_4RviGoMsnragXi4YvzqFQ4-...` (line 25)
- `docs/examples/poi-site-selection-dashboard.mdx` — `/workbench/max/Dashboard_Overture_Census_Isochrone` (lines 12, 14, 18, 489)

> Note: `static/llms-full.txt` is generated and also contains unstable canvas links; it will refresh from source on the next build.
