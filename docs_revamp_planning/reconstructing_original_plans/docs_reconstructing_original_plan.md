
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
│   │   ├── types.mdx            # fused.types.Bounds, etc.
│   │   └── changelog.mdx
│   │
│   ├── h3/                      # 🆕 H3 API REFERENCE
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