### Reconstructed original plan - from Cursor history 

```
docs/
docs/
├── index.mdx                    # Landing page with persona selector
│
├── quickstart/                  # 🎯 PERSONA ENTRY POINTS
│   ├── index.mdx                # "Choose your path" overview
│   ├── data-scientist.mdx       # Notebooks, ML, visualization focus
│   ├── data-engineer.mdx        # Ingestion, ETL, batch jobs, APIs
│   └── data-analyst.mdx         # Workbench UI, dashboards, no-code
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
│   │   └── ingesting-large-datasets.mdx
│   │
│   ├── h3-hexagons/             # Dedicated H3 section
│   │   ├── index.mdx            # Why H3, when to use it
│   │   ├── getting-started.mdx  # First H3 UDF
│   │   ├── converting-to-h3.mdx
│   │   ├── aggregations.mdx
│   │   ├── joining-datasets.mdx
│   │   ├── zonal-stats.mdx
│   │   └── visualization.mdx
│   │
│   ├── scaling-up/
│   │   ├── index.mdx
│   │   ├── caching.mdx
│   │   ├── parallel-processing.mdx
│   │   ├── batch-jobs.mdx
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
│       ├── climate-dashboard.mdx
│       ├── dark-vessel-detection.mdx
│       ├── satellite-imagery.mdx
│       └── ...
│
── reference/                   # 📚 REFERENCE - "I know what I want"
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
│   ├── h3/                      # H3 cheat sheet
│   │   ├── index.mdx
│   │   ├── conversions.mdx
│   │   └── operations.mdx
│   │
│   ├── data-loading/            # Data loading cheat sheet
│   │   ├── index.mdx
│   │   ├── files.mdx            # Parquet, CSV, GeoJSON, Shapefile, COG
│   │   ├── cloud.mdx            # S3, GCS, Azure, HTTP
│   │   ├── databases.mdx        # Snowflake, BigQuery, Postgres
│   │   └── specialized.mdx      # STAC, GEE, Overture
│   │
│   ├── udf-patterns/
│   │   ├── index.mdx
│   │   ├── bounds-and-tiles.mdx
│   │   ├── caching.mdx
│   │   ├── http-endpoints.mdx
│   │   ├── visualization.mdx
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
└── faq.mdx
```