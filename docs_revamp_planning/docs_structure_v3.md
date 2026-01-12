# Fused Docs - Structure v3 (Fresh Revamp)

## Core Philosophy

**Two pillars with clear intent:**

| Pillar | User State | Content Style | Example |
|--------|-----------|---------------|---------|
| **Reference** | "I know exactly what I need" | Snippets, cheat sheets, exhaustive | DuckDB Data Import |
| **Guide** | "I'm learning / exploring" | Narrative, progressive, links to Reference | Modal Guide |

**Persona entry points** → Quick on-ramps for Data Scientists, Engineers, Analysts

**Geo as default** → We're leaning into geospatial, but content should be accessible to non-geo folks

---

## Proposed Structure

```
docs/
├── index.mdx                       # Landing page with persona selector
│
├── quickstart/                     # 🎯 PERSONA ENTRY POINTS (keep existing)
│   ├── index.mdx                   # "Choose your path"
│   ├── data-scientist.mdx          # Notebooks, ML, viz focus
│   ├── data-engineer.mdx           # Ingestion, ETL, batch jobs, APIs
│   └── data-analyst.mdx            # Workbench UI, dashboards, low-code
│
├── guide/                          # 📖 GUIDES - "Show me how"
│   │
│   ├── index.mdx                   # Guide overview / navigation
│   │
│   ├── getting-started/
│   │   ├── index.mdx               # What is Fused? First steps
│   │   ├── your-first-udf.mdx      # Hello World UDF
│   │   └── workbench-tour.mdx      # Quick UI orientation
│   │
│   ├── loading-data/               # 🆕 CONSOLIDATED DATA LOADING
│   │   ├── index.mdx               # Overview: "Loading data into Fused"
│   │   ├── files.mdx               # Local files: CSV, Parquet, GeoJSON, Shapefile
│   │   ├── cloud-storage.mdx       # S3, GCS, Azure (with links to official docs)
│   │   ├── databases.mdx           # Snowflake, BigQuery, Postgres (link to each)
│   │   ├── apis-and-catalogs.mdx   # REST APIs, STAC Catalogs (link to STAC spec)
│   │   ├── earth-engine.mdx        # Google Earth Engine (link to GEE docs)
│   │   └── large-files.mdx         # Handling massive remote files
│   │
│   ├── writing-data/
│   │   ├── index.mdx               # Overview
│   │   ├── to-cloud-storage.mdx    # S3, GCS exports
│   │   ├── to-databases.mdx        # Push to Snowflake, BigQuery, etc.
│   │   └── data-as-api.mdx         # Turn your UDF into an API endpoint
│   │
│   ├── h3/                         # 🎯 SEO-FOCUSED H3 SECTION
│   │   ├── index.mdx               # "H3 Hexagons with Fused" - Why H3 matters
│   │   ├── when-to-use-h3.mdx      # 🎯 SEO: Decision guide (when H3 vs other approaches)
│   │   ├── choosing-resolution.mdx # 🎯 SEO: H3 Resolution Guide (the famous table!)
│   │   ├── convert-to-h3.mdx       # 🎯 SEO: Converting Points/Polygons to H3
│   │   ├── aggregation.mdx         # 🎯 SEO: H3 Aggregation (sum, mean, mode, count)
│   │   ├── joining-datasets.mdx    # 🎯 SEO: Join H3 Datasets Together
│   │   ├── zonal-statistics.mdx    # 🎯 SEO: H3 Zonal Statistics
│   │   ├── ingesting-to-h3.mdx     # Large-scale H3 ingestion workflows
│   │   └── visualization.mdx       # Styling H3 layers on maps
│   │
│   ├── geospatial-ingestion/       # Cloud-native formats & optimization
│   │   ├── index.mdx               # Why ingestion matters
│   │   ├── when-to-ingest.mdx      # Decision: when do you need to transform data?
│   │   ├── ingest-your-data.mdx    # Step-by-step ingestion guide
│   │   └── file-formats.mdx        # GeoParquet, COG, PMTiles (link to specs)
│   │
│   ├── running-udfs/               # Execution modes
│   │   ├── index.mdx               # Overview: realtime vs batch
│   │   ├── realtime.mdx            # fused.run(), instant execution
│   │   ├── batch-jobs.mdx          # Large-scale batch processing
│   │   ├── parallel-processing.mdx # fused.submit() for many tasks
│   │   └── http-endpoints.mdx      # Share UDFs via URLs (tokens, params)
│   │
│   ├── scaling-up/                 # Performance & optimization
│   │   ├── index.mdx               # Overview
│   │   ├── caching.mdx             # When/how to cache
│   │   ├── async.mdx               # Async patterns
│   │   └── performance-tips.mdx    # Best practices for speed
│   │
│   ├── building-apps/              # End products
│   │   ├── index.mdx               # What can you build?
│   │   ├── standalone-maps.mdx     # Shareable map views
│   │   ├── dashboards.mdx          # Interactive dashboards
│   │   ├── charts.mdx              # Data visualizations
│   │   └── integrations.mdx        # Felt, QGIS, Mapbox, etc. (link to each)
│   │
│   └── use-cases/                  # End-to-end examples
│       ├── index.mdx               # Browse examples by domain
│       ├── canvas-catalog.mdx      # Link to all existing Canvas examples
│       │
│       │  # ACCESSIBLE NAMING (not jargon-heavy)
│       ├── crop-analysis.mdx           # (not "CDL Analysis")
│       ├── buildings-data.mdx          # (not "Overture Buildings")
│       ├── climate-dashboard.mdx
│       ├── vessel-tracking.mdx         # (not "Dark Vessel Detection AIS")
│       ├── satellite-imagery.mdx
│       ├── location-analytics.mdx      # (not "POI Analysis with Overture")
│       ├── trading-prediction.mdx
│       └── web-scraping.mdx
│
├── reference/                      # 📚 REFERENCE - "Show me the syntax"
│   │
│   ├── index.mdx                   # Reference overview / quick links
│   │
│   ├── python-sdk/                 # Core SDK Reference
│   │   ├── index.mdx               # Installation, auth, quick overview
│   │   ├── fused-udf.mdx           # @fused.udf decorator - all options
│   │   ├── fused-run.mdx           # fused.run() - all params
│   │   ├── fused-submit.mdx        # fused.submit() - parallel execution
│   │   ├── fused-cache.mdx         # @fused.cache - caching API
│   │   ├── fused-load.mdx          # fused.load() - loading UDFs
│   │   ├── fused-ingest.mdx        # fused.ingest() - ingestion API
│   │   ├── fused-download.mdx      # fused.download() - file downloads
│   │   ├── types.mdx               # fused.types.Bounds, etc.
│   │   └── changelog.mdx
│   │
│   ├── h3/                         # 🎯 H3 CHEAT SHEET (snippet-focused)
│   │   ├── index.mdx               # Quick overview + links to Guide
│   │   ├── conversions.mdx         # All conversion snippets (point→h3, polygon→h3, resolution)
│   │   └── operations.mdx          # All operations: aggregations, joins, zonal stats
│   │
│   ├── data-loading/               # Data Loading Cheat Sheet
│   │   ├── index.mdx               # Quick reference table
│   │   ├── files.mdx               # Snippets: Parquet, CSV, GeoJSON, Shapefile, COG
│   │   ├── cloud.mdx               # Snippets: S3, GCS, Azure, HTTP
│   │   ├── databases.mdx           # Snippets: Snowflake, BigQuery, Postgres
│   │   └── specialized.mdx         # Snippets: STAC, GEE, Overture
│   │
│   ├── data-writing/
│   │   └── index.mdx               # Writing data snippets
│   │
│   ├── udf-patterns/               # Common UDF Patterns
│   │   ├── index.mdx
│   │   ├── bounds-and-tiles.mdx    # Working with fused.types.Bounds
│   │   ├── parallel-processing.mdx # Parallel execution patterns
│   │   ├── caching.mdx             # @fused.cache snippets
│   │   ├── http-endpoints.mdx      # URL patterns, formats
│   │   ├── visualization.mdx       # vizConfig patterns
│   │   └── error-handling.mdx      # Common error patterns
│   │
│   └── workbench/                  # Product UI Reference
│       ├── index.mdx               # Workbench overview
│       ├── udf-builder/
│       │   ├── index.mdx           # UDF Builder overview
│       │   ├── code-editor.mdx
│       │   ├── map.mdx
│       │   ├── results.mdx
│       │   ├── canvas.mdx
│       │   └── viz-styling.mdx
│       ├── app-builder/
│       │   ├── index.mdx           # App Builder overview
│       │   └── components.mdx
│       ├── file-explorer.mdx
│       ├── udf-catalog.mdx
│       ├── ai-assistant.mdx
│       ├── account.mdx
│       └── preferences.mdx
│
└── faq.mdx
```

---

## Key Changes from Previous Structure

### 1. **H3 Section Elevated & SEO-Optimized**

The H3 section is now top-level in Guide with clear, searchable page titles:

| Page | Target Search Query |
|------|---------------------|
| `when-to-use-h3.mdx` | "when to use H3", "H3 vs other spatial indexes" |
| `choosing-resolution.mdx` | "H3 resolution guide", "H3 resolution table", "what H3 resolution to use" |
| `convert-to-h3.mdx` | "how to convert data to H3", "convert points to H3" |
| `aggregation.mdx` | "H3 aggregation", "aggregate data with H3" |
| `zonal-statistics.mdx` | "H3 zonal statistics", "zonal stats with hexagons" |
| `joining-datasets.mdx` | "join H3 datasets", "H3 spatial join" |

### 2. **Data Loading Consolidated**

Everything about loading data is now in one place:

| Current Location (scattered) | New Location |
|------------------------------|--------------|
| `tutorials/Geospatial/read-data.mdx` | `guide/loading-data/` |
| `tutorials/load_and_save_data.mdx` | `guide/loading-data/` |
| `tutorials/Geospatial/gee_bigquery.mdx` | `guide/loading-data/earth-engine.mdx` |

### 3. **Accessible Naming**

Use-case pages use plain language:

| ❌ Don't Use | ✅ Use Instead | Why |
|-------------|----------------|-----|
| "CDL Analysis" | "Crop Analysis" | More searchable, less jargon |
| "Overture Buildings" | "Buildings Data" | Focus on outcome, not data source |
| "Dark Vessel Detection" | "Vessel Tracking" | More intuitive |
| "STAC Catalog" | Include link to [STAC spec](https://stacspec.org/) | Explain, don't assume knowledge |

### 4. **Guide vs Reference - Clear Separation**

| Aspect | Guide | Reference |
|--------|-------|-----------|
| **Question answered** | "How do I do this?" | "What's the exact syntax?" |
| **Length** | 150-300 lines | 50-100 lines |
| **Narrative** | Yes, explains context | No, just code snippets |
| **Links** | → Reference for syntax | → Guide for context |

---

## Content Principles

### 1. **Link to External Resources**

Don't explain what STAC or Snowflake is. Link to their official docs:

```markdown
Load data from [STAC Catalogs](https://stacspec.org/) using...
Connect to [Snowflake](https://docs.snowflake.com/) warehouses with...
```

### 2. **Reference Pages are Boring (On Purpose)**

Reference pages should be:
- Scannable (tables, code blocks)
- Minimal prose
- Copy-paste ready
- Consistent structure

### 3. **Keep the Persona Entry Points**

The quickstart personas work well:
- Data Scientist → Notebooks, ML
- Data Engineer → ETL, APIs
- Data Analyst → Workbench UI

---

## H3 SEO Strategy

### Target Keywords

| Keyword | Priority | Page |
|---------|----------|------|
| "H3 hexagon tutorial" | High | `guide/h3/index.mdx` |
| "when to use H3" | High | `guide/h3/when-to-use-h3.mdx` |
| "H3 resolution guide" | High | `guide/h3/choosing-resolution.mdx` |
| "convert data to H3" | High | `guide/h3/convert-to-h3.mdx` |
| "H3 aggregation python" | High | `guide/h3/aggregation.mdx` |
| "H3 zonal statistics" | Medium | `guide/h3/zonal-statistics.mdx` |
| "H3 spatial join" | Medium | `guide/h3/joining-datasets.mdx` |

### Content for SEO

Each H3 guide page should include:

1. **H1 with target keyword** - e.g., "H3 Resolution Guide: Choosing the Right Resolution"
2. **Quick summary** - What you'll learn in 2 sentences
3. **The resolution table** (for choosing-resolution.mdx)
4. **Code snippets** with Fused
5. **Link to Reference** for cheat sheet snippets

---

## Sidebar Structure

```typescript
// sidebars.ts
const sidebars = {
  mainSidebar: [
    "index",
    {
      type: "category",
      label: "Quickstart",
      collapsed: false,
      items: [
        "quickstart/data-scientist",
        "quickstart/data-engineer",
        "quickstart/data-analyst",
      ],
    },
    {
      type: "category",
      label: "📖 Guide",
      collapsed: false,
      items: [
        "guide/getting-started/index",
        "guide/loading-data/index",
        "guide/writing-data/index",
        "guide/h3/index",           // H3 prominent in sidebar
        "guide/geospatial-ingestion/index",
        "guide/running-udfs/index",
        "guide/scaling-up/index",
        "guide/building-apps/index",
        "guide/use-cases/index",
      ],
    },
    {
      type: "category",
      label: "📚 Reference",
      collapsed: true,
      items: [
        "reference/python-sdk/index",
        "reference/h3/index",
        "reference/data-loading/index",
        "reference/udf-patterns/index",
        "reference/workbench/index",
      ],
    },
    "faq",
  ],
};
```

---

## Migration Checklist

- [ ] Map all existing files to new structure
- [ ] Create redirects for old URLs
- [ ] Extract snippets from Guide pages → Reference
- [ ] Rename use-case pages to accessible names
- [ ] Add external links (STAC, Snowflake, GEE, etc.)
- [ ] Update internal links
- [ ] Optimise H3 pages for SEO (H1s, meta descriptions)
- [ ] Test all anchor links

---

## Examples of Docs That Do This Well

| Docs | Guide Link | Reference Link | Why It Works |
|------|-----------|----------------|--------------|
| **Stripe** | [Payments Quickstart](https://stripe.com/docs/payments/quickstart) | [API Reference](https://stripe.com/docs/api) | Clear separation, Guide never duplicates API |
| **Modal** | [Guide](https://modal.com/docs/guide) | [Reference](https://modal.com/docs/reference) | Progressive learning vs lookup |
| **DuckDB** | [Data Import](https://duckdb.org/docs/data/overview) | Each format page | Table of all formats, find snippet in seconds |
| **Tailwind** | [Docs](https://tailwindcss.com/docs) | Utility tables | Scannable, minimal prose |

---

## Notes

- **Geo is the default** but we explain concepts for non-geo users
- **Don't over-engineer** - keep Reference pages minimal
- **Link liberally** - Guide → Reference, external docs
- **Consistent structure** - every Reference page follows same format

