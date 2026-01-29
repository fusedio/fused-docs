import type { SidebarsConfig } from "@docusaurus/plugin-content-docs";

/**
 * Modal-style Sidebar Structure
 * 
 * - 3 separate sidebars: Guide, Examples, Reference
 * - All categories are non-collapsible (flat view)
 * - 2-level hierarchy: Section headers (white) → Pages (grey)
 * - Category headers link to first item when clicked
 */

const sidebars: SidebarsConfig = {
  // ============================================
  // GUIDE SIDEBAR
  // ============================================
  guideSidebar: [
    // Landing page
    "index",

    // Quickstart
    {
      type: "category",
      label: "Quickstart",
      collapsible: false,
      link: { type: "doc", id: "guide/getting-started/first-udf-basics" },
      items: [
        { type: "doc", id: "guide/getting-started/first-udf-basics", label: "First UDF basics" },
        { type: "doc", id: "guide/getting-started/using-ai", label: "Using AI" },
        { type: "doc", id: "guide/getting-started/workbench-intro", label: "Workbench intro" },
      ],
    },

    // UDF Fundamentals
    {
      type: "category",
      label: "UDF Fundamentals",
      collapsible: false,
      link: { type: "doc", id: "guide/working-with-udfs/why-fused" },
      items: [
        { type: "doc", id: "guide/working-with-udfs/why-fused", label: "Why Fused" },
        { type: "doc", id: "guide/working-with-udfs/writing-udfs", label: "Writing UDFs" },
        { type: "doc", id: "guide/working-with-udfs/run-udfs-as-api", label: "UDFs as API" },
        { type: "doc", id: "guide/working-with-udfs/fused-run", label: "Running UDFs" },
        { type: "doc", id: "guide/working-with-udfs/fused-submit", label: "Parallel execution" },
      ],
    },

    // UDF Best Practices
    {
      type: "category",
      label: "UDF Best Practices",
      collapsible: false,
      link: { type: "doc", id: "guide/working-with-udfs/udf-best-practices/realtime" },
      items: [
        { type: "doc", id: "guide/working-with-udfs/udf-best-practices/realtime", label: "Run jobs efficiently" },
        { type: "doc", id: "guide/working-with-udfs/udf-best-practices/scaling-out", label: "Scaling out UDFs" },
        { type: "doc", id: "guide/working-with-udfs/udf-best-practices/caching", label: "Efficient caching" },
        { type: "doc", id: "guide/working-with-udfs/udf-best-practices/geospatial-single-vs-tile", label: "Geospatial processing" },
        { type: "doc", id: "guide/working-with-udfs/udf-best-practices/version-control", label: "Working as a Team" },
      ],
    },

    // Connecting to Data
    {
      type: "category",
      label: "Connecting to Data",
      collapsible: false,
      link: { type: "doc", id: "guide/data-input-outputs/import-connection/local-files" },
      items: [
        { type: "doc", id: "guide/data-input-outputs/import-connection/local-files", label: "Local files" },
        { type: "doc", id: "guide/data-input-outputs/import-connection/cloud-storage", label: "Cloud storage" },
        { type: "doc", id: "guide/data-input-outputs/import-connection/databases", label: "Databases" },
        { type: "doc", id: "guide/data-input-outputs/import-connection/geospatial/stac", label: "STAC catalogs" },
        { type: "doc", id: "guide/data-input-outputs/import-connection/geospatial/gee", label: "Google Earth Engine" },
      ],
    },

    // Reading & Writing Files
    {
      type: "category",
      label: "Reading & Writing Files",
      collapsible: false,
      link: { type: "doc", id: "guide/data-input-outputs/read-write/reading" },
      items: [
        { type: "doc", id: "guide/data-input-outputs/read-write/reading", label: "Reading files" },
        { type: "doc", id: "guide/data-input-outputs/read-write/writing", label: "Writing files" },
        { type: "doc", id: "guide/data-input-outputs/read-write/geospatial/geospatial-reading", label: "Reading geospatial" },
        { type: "doc", id: "guide/data-input-outputs/read-write/geospatial/geospatial-writing", label: "Writing geospatial" },
        { type: "doc", id: "guide/data-input-outputs/read-write/geospatial/ingestion", label: "Geospatial Ingestion" },
      ],
    },

    // Exporting Data
    {
      type: "category",
      label: "Exporting Data",
      collapsible: false,
      link: { type: "doc", id: "guide/data-input-outputs/export-api/tokens-endpoints" },
      items: [
        { type: "doc", id: "guide/data-input-outputs/export-api/tokens-endpoints", label: "Tokens & endpoints" },
        { type: "doc", id: "guide/data-input-outputs/export-api/download", label: "Download" },
        { type: "doc", id: "guide/data-input-outputs/export-api/mcp-servers", label: "MCP servers" },
        { type: "doc", id: "guide/data-input-outputs/export-api/geospatial-export", label: "Geospatial Integration" },
      ],
    },

    // Advanced Setup
    {
      type: "category",
      label: "Advanced Setup",
      collapsible: false,
      link: { type: "doc", id: "guide/advanced-setup/dependencies" },
      items: [
        { type: "doc", id: "guide/advanced-setup/dependencies", label: "Dependencies" },
        { type: "doc", id: "guide/advanced-setup/environment-variables", label: "Environment variables" },
        { type: "doc", id: "guide/advanced-setup/file-system", label: "File system" },
        { type: "doc", id: "guide/advanced-setup/git-integration", label: "Git integration" },
        { type: "doc", id: "guide/advanced-setup/local-installation", label: "Local installation" },
        { type: "doc", id: "guide/advanced-setup/on-prem-setup", label: "On-prem setup" },
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
      link: { type: "doc", id: "guide/h3-analytics/h3-overview" },
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
      link: { type: "doc", id: "examples/zonal-stats" },
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
      link: { type: "doc", id: "examples/web-scraping" },
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
      link: { type: "doc", id: "examples/creating-charts" },
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
      link: { type: "doc", id: "python-sdk/changelog" },
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
      link: { type: "doc", id: "python-sdk/index" },
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
      link: { type: "doc", id: "workbench/overview" },
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
