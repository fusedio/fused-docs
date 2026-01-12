# Docs Structure v3 - Revised with Merged Data & Processing Sections

Building on v2, this version:
- Merges load/write into unified `data/` section (organized by source)
- Creates `processing/` section with H3 as subsection
- Moves `configuration/` to bottom (advanced/secondary content)
- Adds missing categories from legacy docs

---

## Full Structure

```
docs/
├── index.mdx                        # Landing page with persona selector
│
├── quickstart/                      # 🎯 PERSONA ENTRY POINTS
│   ├── index.mdx                    # "Choose your path" overview
│   ├── data-scientist.mdx           # Notebooks, ML, visualization
│   ├── data-engineer.mdx            # Ingestion, ETL, batch jobs, APIs
│   └── data-analyst.mdx             # Workbench UI, dashboards, no-code
│
├── guide/                           # 📖 GUIDES - "I'm learning"
│   ├── getting-started/
│   │   ├── index.mdx                # Overview of getting started journey
│   │   ├── your-first-udf.mdx       # Write & run your first UDF in Workbench
│   │   ├── understanding-udfs.mdx   # What UDFs are, how they work, why Fused
│   │   └── workbench-intro.mdx      # UI orientation, panels, navigation
│   │
│   ├── data/                        # 📦 All data operations by source
│   │   ├── index.mdx                # Overview + quick file formats table (Parquet/CSV/COG/Shapefile) with rule of thumb
│   │   ├── local-files.mdx          # Drag & drop, upload(), download as CSV/JSON
│   │   ├── cloud-storage.mdx        # S3/GCS/Azure: read, write, credentials
│   │   ├── databases.mdx            # Snowflake, BigQuery, Postgres
│   │   ├── stac.mdx                 # STAC catalogs: pystac, odc.stac
│   │   ├── gee.mdx                  # Google Earth Engine: auth, xarray
│   │   ├── planetary-computer.mdx   # 🔮 FUTURE: Microsoft Planetary Computer
│   │   └── ingestion/               # Large-scale vector tiling
│   │       ├── index.mdx            # Why ingest, when to use fused.ingest()
│   │       └── ingesting-datasets.mdx
│   │
│   │
│   ├── processing/                  # ⚙️ Execution, scaling & H3
│   │   ├── index.mdx                # Overview: realtime vs batch, scaling
│   │   ├── running-udfs.mdx         # fused.run(), local vs remote, engine
│   │   ├── realtime.mdx             # Interactive, tile-based, <120s jobs
│   │   ├── batch-jobs.mdx           # Large jobs, run_batch(), notifications
│   │   ├── parallel-processing.mdx  # fused.submit(), arg_list, patterns
│   │   ├── single-vs-tile.mdx       # Single vs Tile, bounds, fused.types.Bounds
│   │   ├── caching.mdx              # @fused.cache, cache_max_age
│   │   ├── performance-tips.mdx     # Profiling, optimization, bottlenecks
│   │   └── h3-analytics/            # H3 hexagon processing
│   │       ├── index.mdx            # Why H3, resolution guide
│   │       ├── converting-to-h3.mdx # Raster→H3, vector→H3
│   │       ├── aggregations.mdx     # Groupby hex, stats, temporal
│   │       ├── joining-datasets.mdx # Multi-resolution joins
│   │       ├── zonal-stats.mdx      # Raster stats per polygon/hex
│   │       └── visualization.mdx    # H3 styling, colors, 3D extrusion
│   │
│   ├── building-apps/               # 🚀 Share & deploy
│   │   ├── index.mdx                # Overview: ways to share your work
│   │   ├── standalone-maps.mdx      # Embeddable maps, pydeck, map URLs
│   │   ├── dashboards.mdx           # Canvas dashboards, fused.run(), components
│   │   ├── sharing-udfs.mdx         # Tokens, HTTPS endpoints, URL formats
│   │   ├── ai-assisted-building.mdx # AI chat, LLM prompting, generating UDFs
│   │   ├── integrations.mdx         # DeckGL, Felt, Kepler, Mapbox, QGIS
│   │   ├── mcp-servers.mdx          # MCP config, AI tools querying data
│   │   └── pmtiles.mdx              # 🔮 FUTURE: PM Tiles visualization
│   │
│   │
│   ├── use-cases/                   # 📚 End-to-end examples
│   │   ├── index.mdx                # Overview of examples
│   │   ├── climate-dashboard.mdx    # ERA5, temporal analysis
│   │   ├── dark-vessel-detection.mdx# AIS, parallel processing
│   │   ├── satellite-imagery.mdx    # Landsat/Sentinel, NDVI, COG
│   │   ├── competitor-analysis.mdx  # POI, spatial joins, BI
│   │   ├── pdf-scraping.mdx         # Document extraction
│   │   ├── web-scraping.mdx         # Structured data, batch scraping
│   │   ├── data-exploration.mdx     # Patterns, quick viz
│   │   ├── interactive-charts.mdx   # Plotly, charts in apps
│   │   ├── realtime-processing.mdx  # Live data feeds
│   │   └── canvas-examples.mdx      # Example Canvas workflows
│   │
│   ├── best-practices/              # ✨ Do it right
│   │   ├── index.mdx                # Overview
│   │   ├── udf-patterns.mdx         # Common patterns, anti-patterns
│   │   ├── workbench-workflow.mdx   # Efficient usage, QA, debugging
│   │   └── team-workflow.mdx        # 🔮 FUTURE: Team collaboration
│   │
│   └── configuration/               # ⚙️ Advanced setup
│       ├── index.mdx                # Overview of config options
│       ├── environment-variables.mdx# Env vars, fused.secrets
│       ├── file-system.mdx          # /mnt/cache, EFS, persistent storage
│       ├── git-integration.mdx      # GitHub sync, push/pull
│       ├── dependencies.mdx         # pip packages, custom modules
│       └── on-prem-setup.mdx        # Docker self-hosted, enterprise
│
│
├── reference/                       # 📚 REFERENCE - "I know what I want"
│   │
│   ├── python-sdk/
│   │   ├── index.mdx                # Installation, auth, quick reference
│   │   ├── fused-udf.mdx            # @fused.udf decorator, params, metadata
│   │   ├── fused-run.mdx            # fused.run() API, parameters
│   │   ├── fused-submit.mdx         # fused.submit() API, parallel
│   │   ├── fused-cache.mdx          # @fused.cache decorator
│   │   ├── fused-load.mdx           # fused.load() from GitHub/name
│   │   ├── fused-ingest.mdx         # fused.ingest() API, options
│   │   ├── fused-download.mdx       # fused.download() API
│   │   ├── types.mdx                # fused.types.Bounds, Tile, ViewportGDF
│   │   ├── job.mdx                  # Job object API, status
│   │   ├── jobpool.mdx              # JobPool API, batch management
│   │   └── changelog.mdx            # Version history
│   │
│   │
│   ├── data/                        # Data cheat sheet
│   │   ├── index.mdx                # Quick reference overview
│   │   ├── files.mdx                # Parquet, CSV, GeoJSON, Shapefile
│   │   ├── cloud.mdx                # S3, GCS, Azure, HTTP
│   │   ├── databases.mdx            # Snowflake, BigQuery, Postgres
│   │   └── specialized.mdx          # STAC, GEE, Overture
│   │
│   │
│   ├── udf-patterns/                # Pattern library
│   │   ├── index.mdx                # Pattern overview
│   │   ├── bounds-and-tiles.mdx     # bounds, tiles, mercantile
│   │   ├── caching.mdx              # Cache strategies, TTL
│   │   ├── async.mdx                # Async execution, sync=False
│   │   ├── http-endpoints.mdx       # URL structure, query params
│   │   ├── visualization.mdx        # vizConfig, layer styling
│   │   └── error-handling.mdx       # Try/catch, logging
│   │
│   │
│   ├── h3/                          # H3 quick reference
│   │   ├── index.mdx                # H3 overview, resolution table
│   │   ├── conversions.mdx          # latlng_to_cell, cell_to_boundary
│   │   └── operations.mdx           # Neighbors, rings, polyfill
│   │
│   └── workbench/                   # Product UI reference
│       │
│       ├── index.mdx                # Workbench overview
│       ├── udf-builder/
│       │   ├── code-editor.mdx      # Editor, shortcuts, autocomplete
│       │   ├── map.mdx              # Map controls, layers, basemaps
│       │   ├── results.mdx          # Results panel, profiler
│       │   ├── canvas.mdx           # Canvas UI, connecting UDFs
│       │   ├── navigation.mdx       # Layer panel, drag/drop
│       │   └── viz-styling.mdx      # Viz config, presets
|       |
│       ├── app-builder/
│       │   ├── overview.mdx         # App Builder intro
│       │   ├── add-a-map.mdx        # Maps in apps, pydeck
│       │   └── components.mdx       # Widgets, inputs, layout
│       │
│       ├── file-explorer.mdx        # File browser, upload
│       ├── udf-catalog.mdx          # Catalog, public UDFs, search
│       ├── token-management.mdx     # Token list, create/revoke
│       ├── ai-assistant.mdx         # AI chat, prompting
│       ├── preferences.mdx          # Settings, secrets
│       ├── account.mdx              # Account, billing, team
│       └── free-tier.mdx            # Limits, quotas, upgrade
│
└── faq.mdx                          # Common questions, troubleshooting
```

---

## Key Changes from v2

| Change | Reasoning |
|--------|-----------|
| Merged `loading-data/` + `writing-data/` → `data/` | Users think "I'm working with S3" not "I'm reading from S3" |
| Created `processing/` section | Unified place for execution, scaling, and H3 analytics |
| H3 as subsection of `processing/` | H3 is a processing/analysis pattern, not a standalone concept |
| Moved `configuration/` to bottom | Advanced setup - not needed for new users |
| Removed `authentication.mdx` from getting-started | Workbench-first approach, no setup needed. SDK auth in `reference/python-sdk/` |
| Added `ai-assistant.mdx` | Product feature documentation |
| Added `free-tier.mdx` | Users need to understand limits |

---

## New Pages Added in v3 (Final)

| New Page | Location | Source Content |
|----------|----------|----------------|
| `single-vs-tile.mdx` | `guide/processing/` | `filetile.mdx` - Single/Tile modes, bounds param |
| `mcp-servers.mdx` | `guide/building-apps/` | `let-anyone-talk-to-your-data.mdx` |
| `canvas-examples.mdx` | `guide/use-cases/` | `canvas_catalog.mdx` |
| `on-prem-setup.mdx` | `guide/configuration/` | `onprem.mdx` - Docker self-hosted |
| `stac.mdx` | `guide/data/` | STAC catalogs (separated from apis) |
| `web-scraping.mdx` | `guide/use-cases/` | `scraping.mdx` |
| `data-exploration.mdx` | `guide/use-cases/` | `discover_data.mdx` |
| `interactive-charts.mdx` | `guide/use-cases/` | `interactive-graphs-for-your-data.mdx` |

---

## Future Placeholders (🔮)

| Page | Location | Purpose |
|------|----------|---------|
| `planetary-computer.mdx` | `guide/data/` | Microsoft Planetary Computer integration |
| `pmtiles.mdx` | `guide/building-apps/` | PM Tiles visualization for large datasets |
| `team-workflow.mdx` | `guide/best-practices/` | Team collaboration, sharing conventions |

---

## Content Merges

| Merged Into | Source Content |
|-------------|----------------|
| `guide/data/index.mdx` | File formats table (Parquet/CSV/GeoJSON/COG comparison) |
| `guide/data/databases.mdx` | BigQuery content from `gee_bigquery.mdx` |
| `guide/data/local-files.mdx` | Drag & drop upload + download as CSV/Parquet/JSON |
| `guide/processing/running-udfs.mdx` | Realtime constraints (<120s, RAM limits) from `realtime-data-processing.mdx` |
| `guide/building-apps/dashboards.mdx` | Canvas workflows, fused.run() connections, component messaging |
| `guide/building-apps/sharing-udfs.mdx` | Token creation/management + sharing workflow (combined) |
| `guide/building-apps/integrations.mdx` | DeckGL, Felt, Kepler, Mapbox, QGIS from `other-integrations.mdx` |
| `guide/best-practices/udf-patterns.mdx` | Processing examples from `processing-statistics.mdx` |
| `guide/best-practices/workbench-workflow.mdx` | QA tips from `quality-assurance.mdx`, geo tips from `best-practices.mdx` |
| `faq.mdx` | Geo FAQ content from `geo-faq.mdx` |

---

## Content Scope Clarifications

### Sharing UDFs: One Comprehensive Guide
`guide/building-apps/sharing-udfs.mdx` covers **everything about sharing**:
- What are shared tokens, when to use them
- Creating tokens (Python: `udf.create_access_token()`, Workbench UI)
- Private vs shared tokens
- HTTPS endpoint URL formats (`/run/file`, `/run/tiles/{z}/{x}/{y}`)
- Query parameters (`format=`, custom params)
- Revoking and managing tokens
- Team sharing patterns

**Reference page:** `reference/workbench/token-management.mdx` covers the **UI** (token list, permissions)

### Local Files: Round-trip Workflow
`guide/data/local-files.mdx` covers **file transfer mechanics**:
- **In**: Drag & drop in Workbench, `fused.api.upload()`
- **Out**: `https://udf.ai/[token].csv`, Canvas UI download, `fused.download()`

### Dashboards: Goal-Oriented Canvas Guide
`guide/building-apps/dashboards.mdx` covers **building interactive apps**:
- Canvas basics for dashboards
- Connecting UDFs with `fused.run()`
- Component messaging patterns
- Streamlit-like widget usage

**Reference page:** `reference/workbench/udf-builder/canvas.mdx` covers **all Canvas features**

### Team Workflow: Best Practice (not Config)
`guide/best-practices/team-workflow.mdx` covers **collaboration patterns**:
- Team UDF naming conventions (`team/udf_name`)
- Sharing UDFs within team
- Git workflow for teams
- Code review patterns

---

## Ingestion Types (Clarification)

Fused has two distinct ingestion operations:

### 1. Vector Tiling Ingestion (`fused.ingest()`)
- Takes very large vector datasets (e.g., Overture Buildings ~500GB)
- Creates spatially-tiled version optimized for tile-based access
- Tiles based on **row count** (equal rows per tile), not spatial extent
- Lives in: `guide/data/ingestion/`

### 2. H3 Ingestion
- Converts raster or vector data into H3 hexagons
- Enables H3-based spatial analytics (aggregations, joins, zonal stats)
- Lives in: `guide/processing/h3-analytics/`

## User Navigation Flow

| Step | User Question | Section |
|------|---------------|---------|
| 1 | "How do I start?" | `getting-started/` |
| 2 | "How do I get my data in/out?" | `data/` |
| 3 | "How do I run and scale things?" | `processing/` |
| 4 | "How do I share my work?" | `building-apps/` |
| 5 | "Show me examples" | `use-cases/` |
| 6 | "How do I do it right?" | `best-practices/` |
| 7 | "Advanced setup stuff" | `configuration/` |

---

## Legacy Files Mapping

This section tracks where each legacy file goes in the new structure.

### From `_archived_docs/core-concepts/`

| Legacy File | New Location | Notes |
|-------------|--------------|-------|
| `why.mdx` | `guide/getting-started/understanding-udfs.mdx` | Merge with UDF explanation |
| `async.mdx` | `reference/udf-patterns/async.mdx` | |
| `cache.mdx` | `guide/processing/caching.mdx` + `reference/udf-patterns/caching.mdx` | Split guide vs reference |
| `write.mdx` | `guide/data/cloud-storage.mdx` | Merged into data section |
| `generic-data-ingestion.mdx` | `guide/data/ingestion/` | Vector tiling ingestion |
| `onprem.mdx` | `guide/configuration/on-prem-setup.mdx` | Docker self-hosted setup |
| `best-practices/*.mdx` | `guide/best-practices/` | |
| `content-management/environment-variables.mdx` | `guide/configuration/environment-variables.mdx` | |
| `content-management/file-system.mdx` | `guide/configuration/file-system.mdx` | |
| `content-management/git.mdx` | `guide/configuration/git-integration.mdx` | |
| `content-management/download.mdx` | `guide/data/local-files.mdx` | Part of download workflow |
| `run-udfs/dependencies.mdx` | `guide/configuration/dependencies.mdx` | |
| `run-udfs/run.mdx` | `guide/processing/running-udfs.mdx` + `guide/building-apps/sharing-udfs.mdx` | Split execution vs sharing |
| `run-udfs/large_jobs.mdx` | `guide/processing/batch-jobs.mdx` | |

### From `_archived_docs/python-sdk/`

| Legacy File | New Location | Notes |
|-------------|--------------|-------|
| `index.mdx` | `reference/python-sdk/index.mdx` | Includes auth snippets |
| `authentication.mdx` | `reference/python-sdk/index.mdx` | Merged into SDK index |
| `batch.mdx` | `guide/processing/batch-jobs.mdx` | |
| `top-level-functions.mdx` | Split across `reference/python-sdk/*.mdx` | |
| `changelog.mdx` | `reference/python-sdk/changelog.mdx` | |
| `api-reference/job.mdx` | `reference/python-sdk/job.mdx` | |
| `api-reference/jobpool.mdx` | `reference/python-sdk/jobpool.mdx` | |
| `api-reference/udf.mdx` | `reference/python-sdk/fused-udf.mdx` | |
| `api-reference/h3.mdx` | `reference/h3/` | |

### From `_archived_docs/tutorials/`

| Legacy File | New Location | Notes |
|-------------|--------------|-------|
| `two_min_with_fused.mdx` | `guide/getting-started/your-first-udf.mdx` | |
| `load_and_save_data.mdx` | `guide/data/` | Split by data source |
| `fused-advanced.mdx` | `guide/best-practices/udf-patterns.mdx` | |
| `Analytics & Dashboard/standalone-maps.mdx` | `guide/building-apps/standalone-maps.mdx` | |
| `Analytics & Dashboard/create-interactive-dashboards.mdx` | `guide/building-apps/dashboards.mdx` | |
| `Analytics & Dashboard/interactive-graphs-for-your-data.mdx` | `guide/use-cases/interactive-charts.mdx` | |
| `Analytics & Dashboard/realtime-data-processing.mdx` | `guide/processing/realtime.mdx` | |
| `Analytics & Dashboard/let-anyone-talk-to-your-data.mdx` | `guide/building-apps/mcp-servers.mdx` | |
| `Data Science & AI/competitor_analysis.mdx` | `guide/use-cases/competitor-analysis.mdx` | |
| `Data Science & AI/pdf_scraping.mdx` | `guide/use-cases/pdf-scraping.mdx` | |
| `Data Science & AI/scraping.mdx` | `guide/use-cases/web-scraping.mdx` | |
| `Data Science & AI/discover_data.mdx` | `guide/use-cases/data-exploration.mdx` | |
| `Engineering & ETL/turn-your-data-into-an-api.mdx` | `guide/building-apps/sharing-udfs.mdx` | Part of sharing workflow |
| `Engineering & ETL/handling-large-remote-files.mdx` | `guide/data/cloud-storage.mdx` or `guide/processing/performance-tips.mdx` | |
| `Geospatial with Fused/filetile.mdx` | `guide/processing/single-vs-tile.mdx` | Single/Tile modes |
| `Geospatial with Fused/canvas_catalog.mdx` | `guide/use-cases/canvas-examples.mdx` | |
| `Geospatial with Fused/other-integrations.mdx` | `guide/building-apps/integrations.mdx` | DeckGL, Felt, etc. |
| `Geospatial with Fused/processing-statistics.mdx` | `guide/best-practices/udf-patterns.mdx` | Merge |
| `Geospatial with Fused/quality-assurance.mdx` | `guide/best-practices/workbench-workflow.mdx` | Merge |
| `Geospatial with Fused/best-practices.mdx` | `guide/best-practices/workbench-workflow.mdx` | Merge |
| `Geospatial with Fused/geo-faq.mdx` | `faq.mdx` | Merge |
| `Geospatial with Fused/gee_bigquery.mdx` | `guide/data/gee.mdx` + `guide/data/databases.mdx` | Split |
| `Geospatial with Fused/h3-tiling/*` | `guide/processing/h3-analytics/` | H3 ingestion goes here |
| `Geospatial with Fused/use-cases/*` | `guide/use-cases/` | |
| `Geospatial with Fused/read-data.mdx` | `guide/data/` | Split by data source |
| `Geospatial with Fused/write-data.mdx` | `guide/data/` | Merged with read |
| `Geospatial with Fused/visualization.mdx` | `guide/processing/h3-analytics/visualization.mdx` + `reference/udf-patterns/visualization.mdx` | |
| `Geospatial with Fused/geospatial-data-ingestion/*` | `guide/data/ingestion/` | Vector tiling ingestion |

### From `_archived_docs/workbench/`

| Legacy File | New Location | Notes |
|-------------|--------------|-------|
| `overview.mdx` | `guide/getting-started/workbench-intro.mdx` | |
| `account.mdx` | `reference/workbench/account.mdx` | |
| `ai-assistant.mdx` | `reference/workbench/ai-assistant.mdx` | |
| `file-explorer.mdx` | `reference/workbench/file-explorer.mdx` | |
| `free-tier.mdx` | `reference/workbench/free-tier.mdx` | |
| `preferences.mdx` | `reference/workbench/preferences.mdx` | |
| `udf-catalog.mdx` | `reference/workbench/udf-catalog.mdx` | |
| `udf-builder/*.mdx` | `reference/workbench/udf-builder/*.mdx` | |
| `app-builder/*.mdx` | `reference/workbench/app-builder/*.mdx` | |

---

## Page Count Summary

| Section | Page Count |
|---------|------------|
| `quickstart/` | 4 |
| `guide/getting-started/` | 4 |
| `guide/data/` | 9 (including ingestion/) |
| `guide/processing/` | 13 (including h3-analytics/) |
| `guide/building-apps/` | 8 |
| `guide/use-cases/` | 11 |
| `guide/best-practices/` | 4 |
| `guide/configuration/` | 6 |
| `reference/python-sdk/` | 12 |
| `reference/h3/` | 3 |
| `reference/data/` | 5 |
| `reference/udf-patterns/` | 7 |
| `reference/workbench/` | 15 |
| **Total** | **~101 pages** |
