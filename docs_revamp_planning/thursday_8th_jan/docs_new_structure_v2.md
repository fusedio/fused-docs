# Fused Docs - Structure v2 (with Persona Quickstarts)

## Overview

Two main pillars + persona entry points:
1. **Persona Quickstarts** - "I'm a Data Scientist/Engineer/Analyst"
2. **Guide** - Progressive learning, narrative
3. **Reference** - Exhaustive, copy-paste snippets

**Geo approach:** Geo is the default. Domain-specific examples (logistics, finance, etc.) woven throughout rather than separated.

---

## Proposed Structure

```
docs/
├── index.mdx                    # Landing page with persona selector
│
├── quickstart/                  # 🎯 PERSONA ENTRY POINTS
│   ├── index.mdx                # "Choose your path" overview
│   ├── data-scientist.mdx       # (implemented in v2) Notebooks, ML, visualization focus
│   ├── data-engineer.mdx        # (implemented in v2) Ingestion, ETL, batch jobs, APIs
│   ├── data-analyst.mdx         # (implemented in v2) Workbench UI, dashboards, no-code
│   └── (geospatial-and-h3.mdx)  # (Optional) Geospatial with H3: spatial indexes, aggregations, use cases 
│
├── guide/                       # 📖 GUIDES - "I'm learning"
│   │
│   ├── getting-started/
│   │   ├── index.mdx            # Overview
│   │   ├── your-first-udf.mdx   # From: tutorials/two_min_with_fused
│   │   ├── understanding-udfs.mdx
│   │   └── workbench-intro.mdx  # Basic Workbench orientation
│   │
│   ├── loading-data/            # All data loading in one place
│   │   ├── index.mdx            # Overview of data sources
│   │   ├── local-files.mdx      # CSV, Parquet, GeoJSON, Shapefile
│   │   ├── cloud-storage.mdx    # S3, GCS, Azure Blob
│   │   ├── databases.mdx        # Snowflake, BigQuery, Postgres
│   │   ├── apis.mdx             # REST APIs, STAC Catalogs
│   │   ├── gee.mdx              # Google Earth Engine
│   │   └── file-formats.mdx     # When to use what format
│   │
│   ├── writing-data/
│   │   ├── index.mdx
│   │   ├── to-cloud-storage.mdx
│   │   ├── to-databases.mdx
│   │   └── ingesting-large-datasets.mdx  # -> This needs to join with geospatial ingestion 
│   │
│   ├── running-udfs/            # Execute UDFs from anywhere
│   │   ├── index.mdx            # Overview: realtime vs batch
│   │   ├── realtime.mdx         # fused.run(), HTTPS calls, <120s
│   │   ├── batch-jobs.mdx       # job.run_batch(), large instances
│   │   ├── parallel-processing.mdx  # fused.submit() for many tasks
│   │   └── http-endpoints.mdx   # Tokens, parameters, tiling
│   │
│   ├── h3-hexagons/             # 🎯 SEO-OPTIMIZED H3 SECTION
│   │   ├── index.mdx            # "H3 Hexagons with Fused" overview
│   │   ├── when-to-use-h3.mdx   # 🎯 SEO: "When to Use H3" 
│   │   ├── h3-resolution-guide.mdx  # 🎯 SEO: "H3 Resolution Guide" (includes the table)
│   │   ├── convert-data-to-h3.mdx   # 🎯 SEO: "How to Convert Data to H3"
│   │   ├── h3-aggregation.mdx       # 🎯 SEO: "H3 Aggregation"
│   │   ├── h3-zonal-statistics.mdx  # 🎯 SEO: "H3 Zonal Statistics"
│   │   ├── joining-h3-datasets.mdx  # 🎯 SEO: "Join H3 Datasets"
│   │   └── visualizing-h3.mdx       # "Visualizing H3 Hexagons"
│   │
│   ├── scaling-up/
│   │   ├── index.mdx
│   │   ├── caching.mdx
│   │   ├── parallel-processing.mdx
│   │   ├── batch-jobs.mdx
│   │   ├── geospatial_ingestion
│   │   |   ├── why need ingesiton.mdx
│   │   |   ├── ingest your own data
│   │   |   ├── geospatial cloud formats
│   │   └── performance-tips.mdx
│   │
│   ├── building-apps/
│   │   ├── index.mdx
│   │   ├── standalone-maps.mdx
│   │   ├── dashboards.mdx
│   │   ├── sharing-udfs.mdx
│   │   └── integrations.mdx     # Felt, QGIS, Mapbox, etc.
│   │
│   └── use-cases/               # Curated end-to-end examples
│       ├── index.mdx
│       ├── canvas-catalog.mdx    (from current legacy, a list of all the existing canvas)
│       ├── climate-dashboard.mdx
│       ├── dark-vessel-detection.mdx
│       ├── satellite-imagery.mdx
│       └── ...
│
├── reference/                   # 📚 REFERENCE - "I know what I want"
│   │
│   ├── python-sdk/
│   │   ├── index.mdx            # Installation, auth, overview
│   │   ├── fused-udf.mdx
│   │   ├── fused-run.mdx
│   │   ├── fused-submit.mdx
│   │   ├── fused-cache.mdx
│   │   ├── fused-load.mdx
│   │   ├── fused-ingest.mdx
│   │   ├── fused-download.mdx
│   │   ├── types.mdx
│   │   └── changelog.mdx
│   │
│   ├── h3/                      # H3 cheat sheet -> Also canvas down the line
│   │   ├── index.mdx
│   │   ├── conversions.mdx
│   │   └── operations.mdx
│   │
│   ├── data-loading/            # Data loading cheat sheet -> Prime candidate for becoming a canvas focused first
│   │   ├── index.mdx
│   │   ├── files.mdx            # Parquet, CSV, GeoJSON, Shapefile, COG -> This is already file UDFs. Don't need to re-write these sections (https://github.com/fusedio/udfs/tree/main/files) 
│   │   ├── cloud.mdx            # S3, GCS, Azure, HTTP                                 -> Can also become UDFs 
│   │   ├── databases.mdx        # Snowflake, BigQuery, Postgres                        -> Can become UDFs
│   │   └── specialized.mdx      # STAC (Microsoft Planetary Computer), GEE, Overture   -> Cane become UDFs
│   │
│   ├── udf-patterns/
│   │   ├── index.mdx
│   │   ├── bounds-and-tiles.mdx
│   │   ├── parallel-processing.mdx
│   │   ├── caching.mdx
│   │   ├── http-endpoints.mdx (should be merged with geospatial/other-integrations section)
│   │   ├── visualization.mdx
│   │   └── error-handling.mdx
│   │
│   └── workbench/               # Product UI reference
│       ├── index.mdx
│       ├── canvas/
│       │   ├── index.mdx            # Overview of Canvas features
│       │   ├── ...                  # TODO: Need to find what's going here next 
│       ├── udf-builder/
│       │   ├── index.mdx            # Overview of UDF Builder
│       │   ├── code-editor.mdx      # Writing and editing code
│       │   ├── map.mdx              # Map interactions, layers
│       │   ├── results.mdx          # Viewing output/results
│       │   └── viz-styling.mdx      # Styling and visualization options
│       │   └── running-udfs.mdx     # Running and managing UDF jobs
│       ├── app-builder/
│       │   ├── overview.mdx
│       │   ├── add-a-map.mdx
│       │   └── components.mdx
│       ├── file-explorer.mdx
│       ├── udf-catalog.mdx
│       ├── preferences.mdx
│       └── account.mdx
│
└── faq.mdx
```