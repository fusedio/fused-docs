import type { SidebarsConfig } from "@docusaurus/plugin-content-docs";

const sidebars: SidebarsConfig = {
  tutorialSidebar: [
    "index",
    // ============================================
    // NEW STRUCTURE - Quickstart with Personas
    // ============================================
    {
      type: "category",
      label: "Quickstart",
      collapsed: false,
      link: { type: "doc", id: "quickstart/index" },
      items: [
        "quickstart/data-scientist",
        "quickstart/data-engineer",
        "quickstart/data-analyst",
      ],
    },
    // ============================================
    // NEW STRUCTURE - Guide
    // ============================================
    {
      type: "category",
      label: "Guide",
      collapsed: false,
      link: { type: "doc", id: "guide/index" },
      items: [
        // Getting Started - has sub-pages
        {
          type: "category",
          label: "Getting Started",
          collapsed: true,
          link: { type: "doc", id: "guide/getting-started/index" },
          items: [
            "guide/getting-started/your-first-udf",
            "guide/getting-started/two_min_with_fused",
          ],
        },
        // Loading Data - has sub-pages
        {
          type: "category",
          label: "Loading Data",
          collapsed: true,
          link: { type: "doc", id: "guide/loading-data/index" },
          items: [
            "guide/loading-data/local-files",
            "guide/loading-data/cloud-storage",
            "guide/loading-data/handling-large-remote-files",
            "guide/loading-data/databases",
            "guide/loading-data/apis",
            "guide/loading-data/gee",
            "guide/loading-data/file-formats",
          ],
        },
        // Writing Data - has sub-pages
        {
          type: "category",
          label: "Writing Data",
          collapsed: true,
          link: { type: "doc", id: "guide/writing-data/index" },
          items: [
            "guide/writing-data/to-cloud-storage",
            "guide/writing-data/to-databases",
            "guide/writing-data/ingesting-large-datasets",
            "guide/writing-data/turn-your-data-into-an-api",
          ],
        },
        // Geospatial Ingestion - has sub-pages
        {
          type: "category",
          label: "Geospatial Ingestion",
          collapsed: true,
          link: { type: "doc", id: "guide/geospatial-ingestion/index" },
          items: [
            "guide/geospatial-ingestion/why-ingestion",
            "guide/geospatial-ingestion/ingest-your-data",
            "guide/geospatial-ingestion/geospatial-file-formats",
          ],
        },
        // Running UDFs - execution modes
        {
          type: "category",
          label: "Running UDFs",
          collapsed: true,
          link: { type: "doc", id: "guide/running-udfs/index" },
          items: [
            "guide/running-udfs/writing-udfs",
            "guide/running-udfs/realtime",
            "guide/running-udfs/batch-jobs",
            "guide/running-udfs/parallel-processing",
            "guide/running-udfs/http-endpoints",
            "guide/running-udfs/quality-assurance",
          ],
        },
        // H3 Hexagons - flattened structure
        {
          type: "category",
          label: "H3 Hexagons",
          collapsed: true,
          link: { type: "doc", id: "guide/h3-hexagons/index" },
          items: [
            "guide/h3-hexagons/when-to-use-h3",
            "guide/h3-hexagons/h3-resolution-guide",
            "guide/h3-hexagons/file-to-h3",
            "guide/h3-hexagons/dynamic-tile-to-h3",
            "guide/h3-hexagons/ingesting-dataset-to-h3",
            "guide/h3-hexagons/aggregating-h3-data",
            "guide/h3-hexagons/joining-h3-datasets",
            "guide/h3-hexagons/h3-zonal-stats",
          ],
        },
        // Scaling Up - has sub-pages
        {
          type: "category",
          label: "Scaling Up",
          collapsed: true,
          link: { type: "doc", id: "guide/scaling-up/index" },
          items: [
            "guide/scaling-up/cache",
            "guide/scaling-up/async",
            "guide/scaling-up/fused-advanced",
            "guide/scaling-up/engineering_etl",
          ],
        },
        // Building Apps - has sub-pages
        {
          type: "category",
          label: "Building Apps",
          collapsed: true,
          link: { type: "doc", id: "guide/building-apps/index" },
          items: [
            // "guide/building-apps/create-interactive-dashboards",
            "guide/building-apps/interactive-graphs-for-your-data",
            "guide/building-apps/standalone-maps",
            "guide/building-apps/visualization",
            "guide/building-apps/let-anyone-talk-to-your-data",
          ],
        },
        // Use Cases - has sub-pages
        {
          type: "category",
          label: "Use Cases",
          collapsed: true,
          link: { type: "doc", id: "guide/use-cases/index" },
          items: [
            "guide/use-cases/stack-overflow-surveys",
            "guide/use-cases/currency-trading-prediction",
            "guide/use-cases/scraping",
            "guide/use-cases/pdf_scraping",
            "guide/use-cases/competitor_analysis",
            "guide/use-cases/vibe-coded-dashboard",
            "guide/use-cases/climate-dashboard",
            "guide/use-cases/dark-vessel-detection",
            "guide/use-cases/zonal-stats",
            "guide/use-cases/exploring_maxar_data",
            {
              type: "category",
              label: "Crop Exploration with H3",
              collapsed: true,
              link: { type: "doc", id: "guide/use-cases/Crop Exploration with H3/index" },
              items: [
                "guide/use-cases/Crop Exploration with H3/exploring_individual_dataset",
                "guide/use-cases/Crop Exploration with H3/joining_datasets",
                "guide/use-cases/Crop Exploration with H3/interactive_visualization",
              ],
            },
            "guide/use-cases/canvas-catalog",
            "guide/use-cases/realtime-data-processing",
          ],
        },
        // Content Management - has sub-pages
        {
          type: "category",
          label: "Content Management",
          collapsed: true,
          link: { type: "doc", id: "guide/content-management/index" },
          items: [
            "guide/content-management/file-system",
            "guide/content-management/git",
            "guide/content-management/download",
            "guide/content-management/environment-variables",
            "guide/content-management/onprem",
          ],
        },
        // Best Practices - has sub-pages
        {
          type: "category",
          label: "Best Practices",
          collapsed: true,
          link: { type: "doc", id: "guide/best-practices/index" },
          items: [
            "guide/best-practices/udf-best-practices",
            "guide/best-practices/workbench-best-practices",
            "guide/best-practices/build_with_llms",
          ],
        },
      ],
    },
    // ============================================
    // NEW STRUCTURE - Reference
    // ============================================
    {
      type: "category",
      label: "Reference",
      collapsed: true,
      link: { type: "doc", id: "reference/index" },
      items: [
        // Python SDK - has sub-pages
        {
          type: "category",
          label: "Python SDK",
          collapsed: true,
          link: { type: "doc", id: "reference/python-sdk/index" },
          items: [
            "reference/python-sdk/top-level-functions",
            "reference/python-sdk/authentication",
            "reference/python-sdk/dependencies",
            "reference/python-sdk/batch",
            "reference/python-sdk/changelog",
            {
              type: "category",
              label: "API Reference",
              collapsed: true,
              items: [
                "reference/python-sdk/api-reference/api",
                "reference/python-sdk/api-reference/core",
                "reference/python-sdk/api-reference/h3",
                "reference/python-sdk/api-reference/udf",
                "reference/python-sdk/api-reference/job",
                "reference/python-sdk/api-reference/jobpool",
                "reference/python-sdk/api-reference/options",
              ],
            },
          ],
        },
        // H3 - has sub-pages
        {
          type: "category",
          label: "H3",
          collapsed: true,
          link: { type: "doc", id: "reference/h3/index" },
          items: [
            "reference/h3/conversions",
            "reference/h3/operations",
          ],
        },
        // UDF Patterns - has sub-pages
        {
          type: "category",
          label: "UDF Patterns",
          collapsed: true,
          link: { type: "doc", id: "reference/udf-patterns/index" },
          items: [
            "reference/udf-patterns/bounds-and-tiles",
            "reference/udf-patterns/parallel-processing",
            "reference/udf-patterns/caching",
            "reference/udf-patterns/http-endpoints",
            "reference/udf-patterns/visualization",
            "reference/udf-patterns/error-handling",
            "reference/udf-patterns/integrations",
          ],
        },
        // Data Loading Reference - has sub-pages
        {
          type: "category",
          label: "Data Loading",
          collapsed: true,
          link: { type: "doc", id: "reference/data-loading/index" },
          items: [
            "reference/data-loading/files",
            "reference/data-loading/cloud",
            "reference/data-loading/databases",
            "reference/data-loading/specialized",
          ],
        },
        // Data Writing Reference
        "reference/data-writing/index",
        // Workbench - has sub-pages
        {
          type: "category",
          label: "Workbench",
          collapsed: true,
          link: { type: "doc", id: "reference/workbench/index" },
          items: [
            "reference/workbench/overview",
            "reference/workbench/account",
            "reference/workbench/preferences",
            "reference/workbench/file-explorer",
            "reference/workbench/udf-catalog",
            "reference/workbench/ai-assistant",
            "reference/workbench/free-tier",
            {
              type: "category",
              label: "UDF Builder",
              collapsed: true,
              link: { type: "doc", id: "reference/workbench/udf-builder/udf-builder" },
              items: [
                "reference/workbench/udf-builder/navigation",
                "reference/workbench/udf-builder/code-editor",
                "reference/workbench/udf-builder/map",
                "reference/workbench/udf-builder/results",
                "reference/workbench/udf-builder/canvas",
                "reference/workbench/udf-builder/viz-styling",
              ],
            },
            {
              type: "category",
              label: "App Builder",
              collapsed: true,
              link: { type: "doc", id: "reference/workbench/app-builder/app-builder" },
              items: [
                "reference/workbench/app-builder/app-overview",
                "reference/workbench/app-builder/add-a-map",
              ],
            },
          ],
        },
      ],
    },
    // ============================================
    // LEGACY SECTIONS - Hidden via CSS className
    // ============================================
    {
      type: "category",
      label: "Legacy Docs",
      collapsed: true,
      className: "legacy-sidebar-hidden",
      items: [
        {
          type: "category",
          label: "Tutorials",
          collapsed: true,
          link: { type: "doc", id: "tutorials" },
          items: [
            "tutorials/2min-with-fused",
            "tutorials/load-export-data",
            {
              type: "category",
              label: "Analytics & Dashboard",
              collapsed: true,
              link: { type: "doc", id: "tutorials/Analytics & Dashboard/analytics-dashboard" },
              items: [
                "tutorials/Analytics & Dashboard/standalone-maps",
                "tutorials/Analytics & Dashboard/realtime-data-processing",
                "tutorials/Analytics & Dashboard/interactive-graphs-for-your-data",
                "tutorials/Analytics & Dashboard/let-anyone-talk-to-your-data",
                "tutorials/Analytics & Dashboard/stack-overflow-surveys",
                "tutorials/Analytics & Dashboard/currency-trading-prediction",
              ],
            },
            {
              type: "category",
              label: "Data Science & AI",
              collapsed: true,
              link: { type: "doc", id: "tutorials/Data Science & AI/data-science-ai" },
              items: [
                "tutorials/Data Science & AI/discover_data",
                "tutorials/Data Science & AI/scraping",
                "tutorials/Data Science & AI/pdf_scraping",
                "tutorials/Data Science & AI/competitor_analysis",
              ],
            },
            {
              type: "category",
              label: "Engineering & ETL",
              collapsed: true,
              link: { type: "doc", id: "tutorials/Engineering & ETL/engineering-etl" },
              items: [
                "tutorials/Engineering & ETL/connect-your-data-to-fused",
                "tutorials/Engineering & ETL/handling-large-remote-files",
                "tutorials/Engineering & ETL/turn-your-data-into-an-api",
              ],
            },
            {
              type: "category",
              label: "Geospatial with Fused",
              collapsed: true,
              link: { type: "doc", id: "tutorials/Geospatial with Fused/index" },
              items: [
                "tutorials/Geospatial with Fused/best-practices",
                "tutorials/Geospatial with Fused/read-data",
                "tutorials/Geospatial with Fused/write-data",
                {
                  type: "category",
                  label: "Geospatial Data Ingestion",
                  link: { type: "doc", id: "tutorials/Geospatial with Fused/geospatial-data-ingestion" },
                  items: [
                    { type: "autogenerated", dirName: "tutorials/Geospatial with Fused/geospatial-data-ingestion" },
                  ],
                },
                {
                  type: "category",
                  label: "H3 Tiling",
                  link: { type: "doc", id: "tutorials/Geospatial with Fused/h3-tiling" },
                  items: [
                    "tutorials/Geospatial with Fused/h3-tiling/when-to-use-h3",
                    "tutorials/Geospatial with Fused/h3-tiling/file-to-h3",
                    "tutorials/Geospatial with Fused/h3-tiling/dynamic-tile-to-h3",
                    "tutorials/Geospatial with Fused/h3-tiling/ingesting-dataset-to-h3",
                    {
                      type: "category",
                      label: "Analysis with H3",
                      link: { type: "doc", id: "tutorials/Geospatial with Fused/h3-tiling/analysis-with-h3" },
                      items: [
                        "tutorials/Geospatial with Fused/h3-tiling/analysis-with-h3/aggregating-h3-data",
                        "tutorials/Geospatial with Fused/h3-tiling/analysis-with-h3/joining-h3-datasets",
                        "tutorials/Geospatial with Fused/h3-tiling/analysis-with-h3/h3-zonal-stats",
                      ],
                    },
                  ],
                },
                "tutorials/Geospatial with Fused/processing-statistics",
                "tutorials/Geospatial with Fused/visualization",
                "tutorials/Geospatial with Fused/quality-assurance",
                {
                  type: "category",
                  label: "Use Cases",
                  link: { type: "doc", id: "tutorials/Geospatial with Fused/geospatial-use-cases" },
                  items: [
                    { type: "autogenerated", dirName: "tutorials/Geospatial with Fused/use-cases" },
                  ],
                },
                "tutorials/Geospatial with Fused/canvas-catalog",
                "tutorials/Geospatial with Fused/gee_bigquery",
                "tutorials/Geospatial with Fused/filetile",
                "tutorials/Geospatial with Fused/other-integrations",
                "tutorials/Geospatial with Fused/geo-faq",
              ],
            },
          ],
        },
        {
          type: "category",
          label: "Core Concepts",
          collapsed: true,
          link: { type: "doc", id: "core-concepts" },
          items: [{ type: "autogenerated", dirName: "core-concepts" }],
        },
        {
          type: "category",
          label: "Workbench",
          collapsed: true,
          link: { type: "doc", id: "workbench" },
          items: [
            { type: "autogenerated", dirName: "workbench" }
          ],
        },
        {
          type: "category",
          label: "Python SDK",
          link: { type: "doc", id: "python-sdk/index" },
          items: [
            "python-sdk/top-level-functions",
            {
              type: "category",
              label: "API Reference",
              items: [
                { type: "autogenerated", dirName: "python-sdk/api-reference" },
              ],
            },
            "python-sdk/authentication",
            "python-sdk/changelog",
          ],
        },
      ],
    },
    {
      type: "doc",
      id: 'faq',
      label: "FAQ",
    },
  ],
};

export default sidebars;
