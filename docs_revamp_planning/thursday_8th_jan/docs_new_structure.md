# Fused Docs - Proposed New Structure

## Overview

Two main pillars following Modal/DuckDB patterns:
1. **Reference** - Exhaustive, copy-paste snippets, for users who know what they want
2. **Guide** - Narrative, progressive, for users exploring

---

## Proposed Structure

```
docs/
├── index.mdx                    # Landing page
├── quickstart.mdx               # Keep as entry point
│
├── guide/                       # 📖 GUIDES - "I'm learning"
│   │
│   ├── getting-started/
│   │   ├── index.mdx            # Overview
│   │   ├── your-first-udf.mdx   # From: tutorials/two_min_with_fused
│   │   ├── understanding-udfs.mdx
│   │   └── workbench-intro.mdx  # Basic Workbench orientation
│   │
│   ├── loading-data/            # 🆕 CONSOLIDATED - All data loading in one place
│   │   ├── index.mdx            # Overview of data sources
│   │   ├── local-files.mdx      # CSV, Parquet, GeoJSON, Shapefile
│   │   ├── cloud-storage.mdx    # S3, GCS, Azure Blob
│   │   ├── databases.mdx        # Snowflake, BigQuery, Postgres
│   │   ├── apis.mdx             # REST APIs, STAC Catalogs
│   │   ├── gee.mdx              # From: tutorials/Geospatial/gee_bigquery
│   │   └── file-formats.mdx     # From: tutorials/Geospatial/geospatial-data-ingestion/geospatial-file-formats
│   │
│   ├── writing-data/
│   │   ├── index.mdx
│   │   ├── to-cloud-storage.mdx
│   │   ├── to-databases.mdx
│   │   └── ingesting-large-datasets.mdx  # From: tutorials/Geospatial/geospatial-data-ingestion
│   │
│   ├── h3-hexagons/             # 🆕 DEDICATED H3 SECTION
│   │   ├── index.mdx            # Why H3, when to use it
│   │   ├── getting-started.mdx  # First H3 UDF
│   │   ├── converting-to-h3.mdx # From: tutorials/Geospatial/h3-tiling/file-to-h3
│   │   ├── aggregations.mdx     # From: tutorials/Geospatial/h3-tiling/analysis-with-h3/aggregating-h3-data
│   │   ├── joining-datasets.mdx # From: tutorials/Geospatial/h3-tiling/analysis-with-h3/joining-h3-datasets
│   │   ├── zonal-stats.mdx      # From: tutorials/Geospatial/h3-tiling/analysis-with-h3/h3-zonal-stats
│   │   └── visualization.mdx    # Styling H3 in maps
│   │
│   ├── scaling-up/
│   │   ├── index.mdx
│   │   ├── caching.mdx          # From: core-concepts/cache (narrative version)
│   │   ├── parallel-processing.mdx  # fused.submit guide
│   │   ├── batch-jobs.mdx       # From: core-concepts/run-udfs/large_jobs
│   │   └── performance-tips.mdx # From: core-concepts/best-practices
│   │
│   ├── building-apps/
│   │   ├── index.mdx
│   │   ├── standalone-maps.mdx  # From: tutorials/Analytics & Dashboard/standalone-maps
│   │   ├── dashboards.mdx       # From: tutorials/Analytics & Dashboard/create-interactive-dashboards
│   │   ├── sharing-udfs.mdx     # HTTP endpoints, tokens
│   │   └── integrations.mdx     # Felt, QGIS, Mapbox, etc.
│   │
│   └── use-cases/               # Curated end-to-end examples
│       ├── index.mdx
│       ├── climate-dashboard.mdx
│       ├── dark-vessel-detection.mdx
│       ├── satellite-imagery.mdx
│       └── ...
│
├── reference/                   # 📚 REFERENCE - "I know what I want"
│   │
│   ├── python-sdk/              # From: python-sdk/ (promoted)
│   │   ├── index.mdx            # Installation, auth, overview
│   │   ├── fused-udf.mdx        # @fused.udf decorator
│   │   ├── fused-run.mdx        # fused.run()
│   │   ├── fused-submit.mdx     # fused.submit()
│   │   ├── fused-cache.mdx      # @fused.cache decorator
│   │   ├── fused-load.mdx       # fused.load()
│   │   ├── fused-ingest.mdx     # fused.ingest()
│   │   ├── fused-download.mdx   # fused.download()
│   │   ├── (types.mdx)          # fused.types.Bounds, etc.  -> This isn't needed anymore, don't want to explore 
│   │   └── changelog.mdx
│   │
│   ├── h3/                      # 🆕 H3 API REFERENCE (cheat sheet style)
│   │   ├── index.mdx            # Quick overview + links to guide
│   │   ├── conversions.mdx      # All conversion snippets: point→h3, polygon→h3, resolution changes
│   │   └── operations.mdx       # All operations in ONE page: aggregations, joins, zonal stats
│   │                            # (Keeps reference ultra-minimal, guide has the narrative)
│   │
│   ├── data-loading/            # 🆕 DATA LOADING SNIPPETS (cheat sheet style)
│   │   ├── index.mdx            # Quick reference overview with links
│   │   ├── files.mdx            # All file formats: Parquet, CSV, GeoJSON, Shapefile, COG
│   │   ├── cloud.mdx            # All cloud sources: S3, GCS, Azure, HTTP
│   │   ├── databases.mdx        # All DBs: Snowflake, BigQuery, Postgres
│   │   └── specialized.mdx      # STAC, GEE, Overture, etc.
│   │
│   ├── udf-patterns/            # Common UDF patterns
│   │   ├── index.mdx
│   │   ├── bounds-and-tiles.mdx # Working with fused.types.Bounds
│   │   ├── caching.mdx          # @fused.cache snippets (not narrative)
│   │   ├── http-endpoints.mdx   # URL patterns, formats
│   │   ├── visualization.mdx    # vizConfig patterns
│   │   └── error-handling.mdx
│   │
│   └── workbench/               # Product UI reference
│       ├── index.mdx
│       ├── udf-builder/
│       │   ├── code-editor.mdx
│       │   ├── map.mdx
│       │   ├── results.mdx
│       │   ├── canvas.mdx
│       │   └── viz-styling.mdx
│       ├── app-builder/
│       │   ├── overview.mdx
│       │   ├── add-a-map.mdx
│       │   └── components.mdx
│       ├── file-explorer.mdx
│       ├── udf-catalog.mdx
│       ├── preferences.mdx
│       └── account.mdx
│
└── faq.mdx                      # Keep as-is
```

---

## Content Migration Map

### Loading Data Consolidation

| Current Location | New Location | Notes |
|-----------------|--------------|-------|
| `tutorials/Geospatial/read-data.mdx` | `guide/loading-data/` | Split by source type (narrative) |
| `tutorials/load_and_save_data.mdx` | `guide/loading-data/` | Split by source type (narrative) |
| `tutorials/Geospatial/gee_bigquery.mdx` | `guide/loading-data/gee.mdx` | GEE-specific guide (narrative) |
| `tutorials/Geospatial/geospatial-data-ingestion/` | `guide/loading-data/` + `guide/writing-data/` | Split read vs write |
| Extract snippets from all above | `reference/data-loading/files.mdx` | Snippets: Parquet, CSV, GeoJSON, Shapefile, COG |
| Extract snippets from all above | `reference/data-loading/cloud.mdx` | Snippets: S3, GCS, Azure, HTTP |
| Extract snippets from all above | `reference/data-loading/databases.mdx` | Snippets: Snowflake, BigQuery, Postgres |
| Extract snippets from all above | `reference/data-loading/specialized.mdx` | Snippets: STAC, GEE, Overture |

### H3 Consolidation

| Current Location | New Location | Notes |
|-----------------|--------------|-------|
| `tutorials/Geospatial/h3-tiling/when-to-use-h3.mdx` | `guide/h3-hexagons/index.mdx` | Intro/why |
| `tutorials/Geospatial/h3-tiling/file-to-h3.mdx` | `guide/h3-hexagons/converting-to-h3.mdx` | Guide (narrative) |
| `tutorials/Geospatial/h3-tiling/dynamic-tile-to-h3.mdx` | `guide/h3-hexagons/converting-to-h3.mdx` | Merge into above |
| `tutorials/Geospatial/h3-tiling/ingesting-dataset-to-h3.mdx` | `guide/h3-hexagons/converting-to-h3.mdx` | Merge into above |
| `tutorials/Geospatial/h3-tiling/analysis-with-h3/aggregating-h3-data.mdx` | `guide/h3-hexagons/aggregations.mdx` | Guide (narrative) |
| `tutorials/Geospatial/h3-tiling/analysis-with-h3/joining-h3-datasets.mdx` | `guide/h3-hexagons/joining-datasets.mdx` | Guide (narrative) |
| `tutorials/Geospatial/h3-tiling/analysis-with-h3/h3-zonal-stats.mdx` | `guide/h3-hexagons/zonal-stats.mdx` | Guide (narrative) |
| Extract snippets from all above | `reference/h3/conversions.mdx` | Snippets only: point→h3, polygon→h3 |
| Extract snippets from all above | `reference/h3/operations.mdx` | Snippets only: agg, join, zonal (ONE page) |

### Core Concepts Split

| Current Location | Reference | Guide |
|-----------------|-----------|-------|
| `core-concepts/cache.mdx` | `reference/python-sdk/fused-cache.mdx` | `guide/scaling-up/caching.mdx` |
| `core-concepts/run-udfs/run.mdx` | `reference/python-sdk/fused-run.mdx` | `guide/getting-started/` |
| `core-concepts/run-udfs/large_jobs.mdx` | `reference/python-sdk/` | `guide/scaling-up/batch-jobs.mdx` |
| `core-concepts/async.mdx` | `reference/python-sdk/fused-run.mdx` | `guide/scaling-up/` |
| `core-concepts/best-practices/` | Keep snippets in reference | `guide/scaling-up/performance-tips.mdx` |

---

## Sidebar Structure

```typescript
// sidebars.ts (simplified)
const sidebars = {
  mainSidebar: [
    "index",
    "quickstart",
    {
      type: "category",
      label: "📖 Guide",
      items: [
        { type: "autogenerated", dirName: "guide" }
      ]
    },
    {
      type: "category", 
      label: "📚 Reference",
      items: [
        { type: "autogenerated", dirName: "reference" }
      ]
    },
    "faq"
  ]
};
```

---

## Key Principles

1. **Guide pages** link to **Reference pages** for API details
2. **Reference pages** are short, snippet-focused, no narrative
3. **H3 is first-class** - dedicated sections in both Guide and Reference
4. **Data loading is consolidated** - one place to find how to load any format
5. **Maximum 2 levels of nesting** in sidebar

---

## Example: How Caching Would Work

### Guide: `guide/scaling-up/caching.mdx`
- Why cache?
- When to use `@fused.cache` vs UDF caching
- Best practices narrative
- Links to `reference/python-sdk/fused-cache.mdx` for full API

### Reference: `reference/python-sdk/fused-cache.mdx`
- Function signature
- All parameters
- 3-4 copy-paste examples
- No narrative, just facts

---

## Guide vs Reference: Avoiding Duplication

### The Rule

| Aspect | Guide | Reference |
|--------|-------|-----------|
| **Purpose** | "When/why should I use this?" | "What's the exact syntax?" |
| **Length** | 150-300 lines | 50-100 lines |
| **Narrative** | Yes, explains context | No, just code |
| **Complete examples** | Yes, full UDFs | No, minimal snippets |
| **Links to** | Reference for API details | Guide for context |
| **Duplication** | Links to reference, doesn't repeat | Never duplicates guide prose |

### Example: H3 Aggregations

**Guide** (`guide/h3-hexagons/aggregations.mdx`):
- When to aggregate (use cases)
- Choosing the right aggregation function
- Complete workflow example
- Common pitfalls
- Links to `reference/h3/operations.mdx` for snippet library

**Reference** (`reference/h3/operations.mdx`):
- Just the snippets: sum, mean, mode, count, joins, zonal stats
- No prose, just copy-paste patterns
- Links back to guide for "why"

---

## Docs That Do This Well

### 1. **Stripe** - Gold standard
- **Guide:** [https://stripe.com/docs/payments/quickstart](https://stripe.com/docs/payments/quickstart)
  - Narrative, step-by-step, explains concepts
- **Reference:** [https://stripe.com/docs/api](https://stripe.com/docs/api)
  - Pure API reference, every endpoint, copy-paste examples
- **Why it works:** Clear separation. Guide never duplicates API details, just links.

### 2. **Tailwind CSS** - Cheat sheet reference
- **Docs:** [https://tailwindcss.com/docs](https://tailwindcss.com/docs)
  - Each utility page is a quick reference table
  - Minimal prose, maximum copy-paste
- **Why it works:** You find what you need in seconds.

### 3. **Modal** - Closest to Fused's use case
- **Guide:** [https://modal.com/docs/guide](https://modal.com/docs/guide)
  - Progressive learning path, conceptual
- **Reference:** [https://modal.com/docs/reference](https://modal.com/docs/reference)
  - Function signatures, parameters, minimal examples
- **Why it works:** Guide teaches patterns, Reference is lookup.

### 4. **DuckDB** - Excellent data reference
- **Data Import/Export:** [https://duckdb.org/docs/data/overview](https://duckdb.org/docs/data/overview)
  - Table of all formats with links
  - Each format page: syntax + examples, no fluff
- **Why it works:** "I want to load Parquet" → 10 seconds to find snippet.

### 5. **FastAPI** - Interactive reference
- **Tutorial:** [https://fastapi.tiangolo.com/tutorial/](https://fastapi.tiangolo.com/tutorial/)
  - Step-by-step guide building up concepts
- **Reference:** [https://fastapi.tiangolo.com/reference/](https://fastapi.tiangolo.com/reference/)
  - Auto-generated from code, every parameter
- **Why it works:** Tutorial = learning, Reference = lookup.

### Key Takeaways from These Examples

1. **Reference pages are boring on purpose** - no personality, just facts
2. **Guide pages link liberally** to reference instead of duplicating
3. **Reference pages are scannable** - tables, code blocks, minimal prose
4. **Consistent structure** - every reference page follows same format

---

## TODO

- [ ] Map all existing files to new structure
- [ ] Identify content to merge/delete
- [ ] Create redirect rules for old URLs
- [ ] Update internal links
- [ ] Design new landing page
- [ ] Create template for Guide pages
- [ ] Create template for Reference pages

