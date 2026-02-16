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
    // Guide Overview
    { type: "doc", id: "guide/guide-overview", label: "Overview" },

    // Quickstart
    {
      type: "category",
      label: "Quickstart",
      collapsible: false,
      items: [
        { type: "doc", id: "guide/getting-started/first-udf-basics", label: "First UDF & Basics" },
        { type: "doc", id: "guide/getting-started/workbench-intro", label: "Workbench intro" },
        { type: "doc", id: "guide/getting-started/using-ai", label: "Using AI" },
      ],
    },

    // UDF Fundamentals
    {
      type: "category",
      label: "UDF Fundamentals",
      collapsible: false,
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
      items: [
        { type: "doc", id: "guide/working-with-udfs/udf-best-practices/realtime", label: "Run UDFs efficiently" },
        { type: "doc", id: "guide/working-with-udfs/udf-best-practices/scaling-out", label: "Scaling out UDFs" },
        { type: "doc", id: "guide/working-with-udfs/udf-best-practices/caching", label: "Efficient caching" },
        { type: "doc", id: "guide/working-with-udfs/udf-best-practices/storage", label: "Storage Options" },
        { type: "doc", id: "guide/working-with-udfs/udf-best-practices/version-control", label: "Working as a Team" },
        { type: "doc", id: "guide/working-with-udfs/udf-best-practices/geospatial-single-vs-tile", label: "Geospatial processing" },
      ],
    },

    // Connecting to Data
    {
      type: "category",
      label: "Connecting to Data",
      collapsible: false,
      items: [
        { type: "doc", id: "guide/data-input-outputs/import-connection/local-files", label: "Local files" },
        { type: "doc", id: "guide/data-input-outputs/import-connection/cloud-storage", label: "Cloud storage" },
        { type: "doc", id: "guide/data-input-outputs/import-connection/databases", label: "Databases" },
        { type: "doc", id: "guide/data-input-outputs/import-connection/geospatial/stac", label: "STAC catalogs" },
        { type: "doc", id: "guide/data-input-outputs/import-connection/geospatial/gee", label: "Google Earth Engine" },
        { type: "doc", id: "guide/data-input-outputs/import-connection/ai-data-connection", label: "Connecting AI to Data" },
      ],
    },

    // Reading & Writing Files
    {
      type: "category",
      label: "Reading & Writing Files",
      collapsible: false,
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
      items: [
        { type: "doc", id: "guide/data-input-outputs/export-api/tokens-endpoints", label: "Tokens & endpoints" },
        { type: "doc", id: "guide/data-input-outputs/export-api/download", label: "Download" },
        { type: "doc", id: "guide/data-input-outputs/export-api/geospatial-export", label: "Geospatial Integration" },
      ],
    },

    // Advanced Setup
    {
      type: "category",
      label: "Advanced Setup",
      collapsible: false,
      items: [
        { type: "doc", id: "guide/advanced-setup/local-installation", label: "Python installation" },
        { type: "doc", id: "guide/advanced-setup/git-integration", label: "Git integration" },
        { type: "doc", id: "guide/advanced-setup/secrets-management", label: "Secrets management" },
        { type: "doc", id: "guide/advanced-setup/dependencies", label: "Dependencies" },
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
  // API REFERENCE SIDEBAR (Python SDK)
  // ============================================
  apiReferenceSidebar: [
    // Overview
    { type: "doc", id: "python-sdk/overview", label: "Overview" },
    
    {
      type: "category",
      label: "API Reference",
      collapsible: false,
      items: [
        { type: "doc", id: "python-sdk/changelog", label: "Changelog" },
        { type: "doc", id: "python-sdk/api-reference/udf", label: "Udf (class)" },
        { type: "doc", id: "python-sdk/api-reference/jobpool", label: "JobPool (class)" },
        { type: "doc", id: "python-sdk/api-reference/fused-cache", label: "@fused.cache" },
        { type: "doc", id: "python-sdk/api-reference/fused-udf", label: "@fused.udf" },
        { type: "doc", id: "python-sdk/api-reference/api", label: "fused.api" },
        { type: "doc", id: "python-sdk/api-reference/fused-context", label: "fused.context" },
        { type: "doc", id: "python-sdk/api-reference/fused-download", label: "fused.download" },
        { type: "doc", id: "python-sdk/api-reference/fused-file-path", label: "fused.file_path" },
        { type: "doc", id: "python-sdk/api-reference/fused-find-dataset", label: "fused.find_dataset" },
        { type: "doc", id: "python-sdk/api-reference/fused-get-chunk-from-table", label: "fused.get_chunk_from_table" },
        { type: "doc", id: "python-sdk/api-reference/fused-get-chunks-metadata", label: "fused.get_chunks_metadata" },
        { type: "doc", id: "python-sdk/api-reference/h3", label: "fused.h3" },
        { type: "doc", id: "python-sdk/api-reference/fused-ingest", label: "fused.ingest" },
        { type: "doc", id: "python-sdk/api-reference/fused-ingest-nongeospatial", label: "fused.ingest_nongeospatial" },
        { type: "doc", id: "python-sdk/api-reference/fused-load", label: "fused.load" },
        { type: "doc", id: "python-sdk/api-reference/fused-load-async", label: "fused.load_async" },
        { type: "doc", id: "python-sdk/api-reference/options", label: "fused.options" },
        { type: "doc", id: "python-sdk/api-reference/fused-register-dataset", label: "fused.register_dataset" },
        { type: "doc", id: "python-sdk/api-reference/fused-secrets", label: "fused.secrets" },
        { type: "doc", id: "python-sdk/api-reference/fused-types", label: "fused.types" },
        { type: "doc", id: "python-sdk/api-reference/fused-run", label: "fused.run" },
        { type: "doc", id: "python-sdk/api-reference/fused-run-async", label: "fused.run_async" },
        { type: "doc", id: "python-sdk/api-reference/fused-submit", label: "fused.submit" },
      ],
    },
  ],

  // ============================================
  // WORKBENCH SIDEBAR
  // ============================================
  workbenchSidebar: [
    // Overview
    { type: "doc", id: "workbench/overview", label: "Overview" },

    // Canvas
    {
      type: "category",
      label: "Canvas",
      collapsible: false,
      items: [
        { type: "doc", id: "workbench/udf-builder/canvas", label: "Overview" },
        { type: "doc", id: "workbench/udf-builder/code-editor", label: "Code Editor" },
        { type: "doc", id: "workbench/udf-explorer", label: "UDF Explorer" },
        { type: "doc", id: "workbench/ai-chat", label: "AI Chat" },
        { type: "doc", id: "workbench/udf-builder/runtime", label: "Runtime" },
        { type: "doc", id: "workbench/file-explorer", label: "File Explorer" },
      ],
    },

    // UDF Builder
    {
      type: "category",
      label: "UDF Builder",
      collapsible: false,
      items: [
        { type: "doc", id: "workbench/udf-builder/udf-builder", label: "Overview" },
        { type: "doc", id: "workbench/udf-builder/navigation", label: "Map Navigation" },
        { type: "doc", id: "workbench/udf-builder/map", label: "Map View" },
        { type: "doc", id: "workbench/udf-builder/styling", label: "Map Layer Styling" },
      ],
    },

    // Account
    {
      type: "category",
      label: "Account Management",
      collapsible: false,
      items: [
        { type: "doc", id: "workbench/account", label: "Account" },
        { type: "doc", id: "workbench/preferences", label: "Preferences" },
        { type: "doc", id: "workbench/free-tier", label: "Free Tier" },
      ],
    },

    // App Builder
    {
      type: "category",
      label: "Fused Apps",
      collapsible: false,
      items: [
        { type: "doc", id: "workbench/app-builder/app-builder", label: "App Builder" },
        { type: "doc", id: "workbench/app-builder/app-overview", label: "App Overview" },
        { type: "doc", id: "workbench/app-builder/app-map", label: "App Map" },
      ],
    },
  ],
};

export default sidebars;
