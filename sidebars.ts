import type { SidebarsConfig } from "@docusaurus/plugin-content-docs";

/**
 * Modal-style Sidebar Structure
 * 
 * - 3 separate sidebars: Guide, Examples, Reference
 * - All categories are non-collapsible (flat view)
 * - 2-level hierarchy: Section headers (white) → Pages (grey)
 */

const sidebars: SidebarsConfig = {
  // ============================================
  // GUIDE SIDEBAR
  // ============================================
  guideSidebar: [
    // Landing page
    "index",

    // Introduction
    {
      type: "category",
      label: "Introduction",
      collapsible: false,
      items: [
        "guide/getting-started/first-udf-basics",
        "guide/getting-started/using-ai",
        "guide/getting-started/workbench-intro",
      ],
    },

    // UDF Fundamentals
    {
      type: "category",
      label: "UDF Fundamentals",
      collapsible: false,
      items: [
        "guide/working-with-udfs/why-fused",
        "guide/working-with-udfs/writing-udfs",
        "guide/working-with-udfs/run-udfs-as-api",
        "guide/working-with-udfs/fused-run",
        "guide/working-with-udfs/fused-submit",
      ],
    },

    // UDF Best Practices
    {
      type: "category",
      label: "UDF Best Practices",
      collapsible: false,
      items: [
        "guide/working-with-udfs/udf-best-practices/realtime",
        "guide/working-with-udfs/udf-best-practices/batch-jobs",
        "guide/working-with-udfs/udf-best-practices/parallel",
        "guide/working-with-udfs/udf-best-practices/caching",
        "guide/working-with-udfs/udf-best-practices/geospatial-single-vs-tile",
        "guide/working-with-udfs/udf-best-practices/version-control",
      ],
    },

    // Connecting to Data
    {
      type: "category",
      label: "Connecting to Data",
      collapsible: false,
      items: [
        "guide/data-input-outputs/import-connection/local-files",
        "guide/data-input-outputs/import-connection/cloud-storage",
        "guide/data-input-outputs/import-connection/databases",
        "guide/data-input-outputs/import-connection/geospatial/stac",
        "guide/data-input-outputs/import-connection/geospatial/gee",
      ],
    },

    // Reading & Writing Files
    {
      type: "category",
      label: "Reading & Writing Files",
      collapsible: false,
      items: [
        "guide/data-input-outputs/read-write/reading",
        "guide/data-input-outputs/read-write/writing",
        "guide/data-input-outputs/read-write/geospatial/geospatial-reading",
        "guide/data-input-outputs/read-write/geospatial/geospatial-writing",
        "guide/data-input-outputs/read-write/geospatial/ingestion",
      ],
    },

    // Exporting Data
    {
      type: "category",
      label: "Exporting Data",
      collapsible: false,
      items: [
        "guide/data-input-outputs/export-api/tokens-endpoints",
        "guide/data-input-outputs/export-api/download",
        "guide/data-input-outputs/export-api/mcp-servers",
        "guide/data-input-outputs/export-api/geospatial-export",
      ],
    },

    // Advanced Setup
    {
      type: "category",
      label: "Advanced Setup",
      collapsible: false,
      items: [
        "guide/advanced-setup/dependencies",
        "guide/advanced-setup/environment-variables",
        "guide/advanced-setup/file-system",
        "guide/advanced-setup/git-integration",
        "guide/advanced-setup/on-prem-setup",
      ],
    },

    // FAQ
    {
      type: "doc",
      id: "faq",
      label: "FAQ",
    },
  ],

  // ============================================
  // EXAMPLES SIDEBAR
  // ============================================
  examplesSidebar: [
    // H3 Analytics
    {
      type: "category",
      label: "H3 Analytics",
      collapsible: false,
      items: [
        "guide/h3-analytics/h3-overview",
        "guide/h3-analytics/converting",
        "guide/h3-analytics/aggregations",
        "guide/h3-analytics/joining",
        "guide/h3-analytics/resolution-guide",
        "guide/h3-analytics/visualization",
      ],
    },

    // Use Cases & Demos
    {
      type: "category",
      label: "Use Cases & Demos",
      collapsible: false,
      items: [
        "examples/zonal-stats",
        "examples/ais-dark-vessels",
        "examples/climate-dashboard",
        "examples/maxar-satellite-imagery",
        "examples/site-selection-analysis",
        "examples/currency-prediction",
      ],
    },

    // Data & Scraping
    {
      type: "category",
      label: "Data & Scraping",
      collapsible: false,
      items: [
        "examples/web-scraping",
        "examples/pdf-scraping",
      ],
    },

    // Visualization
    {
      type: "category",
      label: "Visualization",
      collapsible: false,
      items: [
        "examples/creating-charts",
        "examples/standalone-html-maps",
        "examples/realtime-filtering-duckdb",
        "examples/canvas-gallery",
        "examples/sharing-canvas-dashboards",
      ],
    },
  ],

  // ============================================
  // REFERENCE SIDEBAR
  // ============================================
  referenceSidebar: [
    // API Reference
    {
      type: "category",
      label: "API Reference",
      collapsible: false,
      items: [
        "python-sdk/changelog",
        "python-sdk/top-level-functions",
        "python-sdk/api-reference/udf",
        "python-sdk/api-reference/jobpool",
        "python-sdk/api-reference/api",
        "python-sdk/api-reference/h3",
        "python-sdk/api-reference/options",
      ],
    },

    // Python SDK
    {
      type: "category",
      label: "Python SDK",
      collapsible: false,
      items: [
        "python-sdk/index",
        "python-sdk/authentication",
      ],
    },

    // Workbench
    {
      type: "category",
      label: "Workbench",
      collapsible: false,
      items: [
        "workbench/overview",
        "workbench/udf-builder/udf-builder",
        "workbench/udf-builder/code-editor",
        "workbench/udf-builder/map",
        "workbench/udf-builder/canvas",
        "workbench/udf-builder/runtime",
        "workbench/udf-builder/navigation",
        "workbench/udf-builder/styling",
        "workbench/app-builder/app-builder",
        "workbench/app-builder/app-overview",
        "workbench/app-builder/app-map",
        "workbench/file-explorer",
        "workbench/udf-explorer",
        "workbench/ai-assistant",
        "workbench/account",
        "workbench/preferences",
        "workbench/free-tier",
      ],
    },
  ],
};

export default sidebars;
