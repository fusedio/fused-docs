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
          ],
        },
        // Loading Data
        "guide/loading-data/index",
        // Writing Data
        "guide/writing-data/index",
        // H3 Hexagons - has sub-pages
        {
          type: "category",
          label: "H3 Hexagons",
          collapsed: true,
          link: { type: "doc", id: "guide/h3-hexagons/index" },
          items: [
            "guide/h3-hexagons/when-to-use-h3",
            "guide/h3-hexagons/h3-resolution-guide",
            "guide/h3-hexagons/convert-data-to-h3",
            "guide/h3-hexagons/h3-aggregation",
          ],
        },
        // Scaling Up - has sub-pages
        {
          type: "category",
          label: "Scaling Up",
          collapsed: true,
          link: { type: "doc", id: "guide/scaling-up/index" },
          items: [
            "guide/scaling-up/caching",
          ],
        },
        // Building Apps
        "guide/building-apps/index",
        // Use Cases
        "guide/use-cases/index",
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
        // Data Loading - just a doc link
        "reference/data-loading/index",
        // UDF Patterns - just a doc link
        "reference/udf-patterns/index",
        // Workbench - just a doc link
        "reference/workbench/index",
      ],
    },
    // ============================================
    // LEGACY SECTIONS - Keep until migration complete
    // ============================================
    {
      type: "category",
      label: "📁 Tutorials (Legacy)",
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
      label: "📁 Core Concepts (Legacy)",
      collapsed: true,
      link: { type: "doc", id: "core-concepts" },
      items: [{ type: "autogenerated", dirName: "core-concepts" }],
    },
    {
      type: "category",
      label: "📁 Workbench (Legacy)",
      collapsed: true,
      link: { type: "doc", id: "workbench" },
      items: [
        { type: "autogenerated", dirName: "workbench" }
      ],
    },
    {
      type: "category",
      label: "📁 Python SDK (Legacy)",
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
    {
      type: "doc",
      id: 'faq',
      label: "FAQ",
    },
  ],
};

export default sidebars;
