import { themes as prismThemes } from "prism-react-renderer";
import type { Config } from "@docusaurus/types";
import type * as Preset from "@docusaurus/preset-classic";

const config: Config = {
  title: "Fused",
  tagline: "Code to map. Instantly.",
  favicon: "img/favicon.png",
  
  // Custom fields for version management
  customFields: {
    fusedPyVersion: '1.20.1',
  },

  trailingSlash: undefined,
  
  // Production URL configuration
  url: process.env.DEPLOYMENT_URL || "https://docs.fused.io",
  baseUrl: process.env.BASE_URL || "/",

  // GitHub pages deployment config.
  // If you aren't using GitHub pages, you don't need these.
  organizationName: "fusedio", // Usually your GitHub org/user name.
  projectName: "fused-docs", // Usually your repo name.

  // TODO: Change back to "throw" after v6 migration fixes all broken links
  onBrokenLinks: "warn", // Temporarily set to warn during v6 docs migration
  // onBrokenLinks: "throw", // Breaking CI if links aren't good
  onBrokenMarkdownLinks: "warn",

  // Mermaid diagrams
  markdown: {
    mermaid: true,
  },
  themes: ["@docusaurus/theme-mermaid"],

  // Even if you don't use internationalization, you can use this field to set
  // useful metadata like html lang. For example, if your site is Chinese, you
  // may want to replace "en" with "zh-Hans".
  i18n: {
    defaultLocale: "en",
    locales: ["en"],
  },

  // Currently set to docs only mode. Change to enable blog and main site. https://docusaurus.io/docs/docs-introduction#docs-only-mode
  presets: [
    [
      "classic",
      {
        docs: {
          routeBasePath: "/",
          editUrl: "https://github.com/fusedio/fused-docs/edit/main/",
          sidebarPath: "./sidebars.ts",
          include: ["**/*.md", "**/*.mdx", "reference/fused/**"],
          exclude: [
            // '**/_*.{js,jsx,ts,tsx,md,mdx}',
            // '**/_*/**',
            // '**/*_unlisted/',
            // '**/*_unlisted.mdx',
            "**/*.test.{js,jsx,ts,tsx}",
            "**/__tests__/**",
          ],
        },
        // blog: false,
        blog: {
          blogTitle: "Fused blog",
          blogDescription: "Latest blog posts from Fused.",
          postsPerPage: 999999,
          blogSidebarTitle: "All posts",
          blogSidebarCount: "ALL",
          showReadingTime: true,
          readingTime: ({ content, frontMatter, defaultReadingTime }) =>
            defaultReadingTime({ content, options: { wordsPerMinute: 300 } }),
          truncateMarker: /(<!--\s*truncate\s*-->)|({\/\*\s*truncate\s*\*\/})/,
          // Ensure consistent canonical URLs
          routeBasePath: "blog",
        },
        theme: {
          customCss: "./src/css/custom.css",
        },
      } satisfies Preset.Options,
    ],
  ],

  themeConfig: {
    // Global site description for SEO
    metadata: [
      {
        name: 'description',
        content: 'Complete documentation for Fused: the Analytics platform where AI, real-time Python execution, and data work together. Build Analytics at the speed of thought',
      },
    ],
    
    tableOfContents: {
      minHeadingLevel: 2,
      maxHeadingLevel: 3,
    },

    algolia: {
      appId: "JNTLW5AVDA",
      apiKey: "b39072abe30fa571950e5c8449fa1552",
      indexName: "fused",
      contextualSearch: true,

      // Optional: Algolia search parameters
      searchParameters: {},

      // Optional: path for search page that enabled by default (`false` to disable it)
      searchPagePath: "search",

      // Optional: whether the insights feature is enabled or not on Docsearch (`false` by default)
      insights: true,
    },
    // Replace with your project's social card
    // image: "https://fused-magic.s3.us-west-2.amazonaws.com/main_marketing_website/product_diagram_october2024_bg_small.png",
    navbar: {
      title: "Fused",
      logo: {
        alt: "Fused Logo",
        src: "img/logo-black-bg-transparent.svg",
        href: "https://www.fused.io",
      },
      items: [
        // {
        //   type: 'html',
        //   position: 'left',
        //   value: '<span class="logo-docs">{{ docs }}</span>'
        // },
        // Show "Docs" in top navbar
        {
          type: "docSidebar",
          sidebarId: "tutorialSidebar",
          position: "left",
          label: "Docs",
        },
        { to: "/blog", label: "Blog", position: "left" },
        {
          href: "https://github.com/fusedio/udfs",
          label: "GitHub",
          position: "right",
        },
        {
          href: "https://www.fused.io/workbench",
          label: "Workbench",
          position: "right",
        },
        {
          href: "https://fused.instatus.com/",
          label: "Status",
          position: "right",
        },
      ],
    },
    footer: {
      // style: 'dark',
      links: [
        {
          title: "Docs",
          items: [
            {
              label: "Overview",
              to: "/",
            },
          ],
        },
        {
          title: "Community",
          items: [
            {
              label: "LinkedIn",
              href: "https://www.linkedin.com/company/fusedio/",
            },
            {
              label: "Discord",
              href: "https://discord.com/invite/BxS5wMzdRk",
            },
          ],
        },
        {
          title: "More",
          items: [
            {
              label: "Blog",
              to: "https://www.fused.io/blog",
            },
            {
              label: "GitHub",
              href: "https://github.com/fusedio/udfs",
            },
            {
              label: "YouTube",
              href: "https://www.youtube.com/@FusedIO",
            },
          ],
        },
      ],
      copyright: `Copyright © ${new Date().getFullYear()} Fused, Inc. Built with Docusaurus.`,
    },
    theme: "@docusaurus/theme-nightOwl",
    colorMode: {
      defaultMode: "dark",
      disableSwitch: true,
      respectPrefersColorScheme: false,
    },
    prism: {
      theme: prismThemes.oneDark,
      darkTheme: prismThemes.oneDark,
      additionalLanguages: ["python", "javascript", "bash", "json"],
    },

    // announcementBar: {
    //   id: "announcement",
    //   content:
    //     '⭐ Join the <a target="_blank" rel="noopener noreferrer" href="https://docs.google.com/forms/d/1NVzMjc2tXxlIgnFrxqQPM_NtG1B2AQ0En_pAbZHYSK0/edit">waitlist</a> for access to Fused Workbench! ⭐',
    //   backgroundColor: "#991199",
    //   textColor: "#ffffff",
    //   isCloseable: false,
    // },
  } satisfies Preset.ThemeConfig,

  plugins: [
    require.resolve("./docusaurus-plugin-custom-webpack"),
    [
      "@docusaurus/plugin-client-redirects",
      {
        redirects: [
          // Revamped Jan 2026 Migration Redirects - Tutorials to new locations
          { to: "/guide/working-with-udfs/building-outputs/standalone-maps", from: ["/tutorials/Analytics%20&%20Dashboard/standalone-maps", "/tutorials/Analytics & Dashboard/standalone-maps"] },
          { to: "/examples/realtime-processing", from: ["/tutorials/Analytics%20&%20Dashboard/realtime-data-processing-with-duckdb-wasm", "/tutorials/Analytics & Dashboard/realtime-data-processing-with-duckdb-wasm"] },
          { to: "/guide/working-with-udfs/building-outputs/charts", from: ["/tutorials/Analytics%20&%20Dashboard/interactive-graphs", "/tutorials/Analytics & Dashboard/interactive-graphs"] },
          { to: "/guide/data-input-outputs/export-api/mcp-servers", from: ["/tutorials/Analytics%20&%20Dashboard/let-anyone-talk-to-your-data", "/tutorials/Analytics & Dashboard/let-anyone-talk-to-your-data"] },
          { to: "/examples/vibe-chart-building", from: ["/tutorials/Analytics%20&%20Dashboard/stack-overflow-surveys", "/tutorials/Analytics & Dashboard/stack-overflow-surveys"] },
          { to: "/examples/currency-prediction", from: ["/tutorials/Analytics%20&%20Dashboard/currency-trading", "/tutorials/Analytics & Dashboard/currency-trading"] },
          
          // Data Science & AI tutorials
          { to: "/examples/data-exploration", from: ["/tutorials/Data%20Science%20&%20AI/discover_data", "/tutorials/Data Science & AI/discover_data"] },
          { to: "/examples/web-scraping", from: ["/tutorials/Data%20Science%20&%20AI/scraping", "/tutorials/Data Science & AI/scraping"] },
          { to: "/examples/pdf-scraping", from: ["/tutorials/Data%20Science%20&%20AI/pdf_scraping", "/tutorials/Data Science & AI/pdf_scraping"] },
          { to: "/examples/competitor-analysis", from: ["/tutorials/Data%20Science%20&%20AI/competitor_analysis", "/tutorials/Data Science & AI/competitor_analysis"] },
          
          // Engineering & ETL tutorials
          { to: "/guide/data-input-outputs/import-connection/cloud-storage", from: ["/tutorials/Engineering%20&%20ETL/connect-your-data-to-fused", "/tutorials/Engineering & ETL/connect-your-data-to-fused"] },
          { to: "/guide/data-input-outputs/import-connection/cloud-storage", from: ["/tutorials/Engineering%20&%20ETL/handling-large-remote-files", "/tutorials/Engineering & ETL/handling-large-remote-files"] },
          { to: "/guide/data-input-outputs/export-api/tokens-endpoints", from: ["/tutorials/Engineering%20&%20ETL/turn-your-data-into-an-api", "/tutorials/Engineering & ETL/turn-your-data-into-an-api"] },
          
          // Geospatial tutorials - H3
          { to: "/guide/h3-analytics/aggregations", from: ["/tutorials/Geospatial%20with%20Fused/h3-tiling", "/tutorials/Geospatial with Fused/h3-tiling"] },
          { to: "/guide/h3-analytics/aggregations", from: ["/tutorials/Geospatial%20with%20Fused/h3-tiling/when-to-use-h3", "/tutorials/Geospatial with Fused/h3-tiling/when-to-use-h3"] },
          { to: "/guide/h3-analytics/converting", from: ["/tutorials/Geospatial%20with%20Fused/h3-tiling/file-to-h3", "/tutorials/Geospatial with Fused/h3-tiling/file-to-h3"] },
          { to: "/guide/h3-analytics/converting", from: ["/tutorials/Geospatial%20with%20Fused/h3-tiling/dynamic-tile-to-h3", "/tutorials/Geospatial with Fused/h3-tiling/dynamic-tile-to-h3"] },
          { to: "/guide/h3-analytics/converting", from: ["/tutorials/Geospatial%20with%20Fused/h3-tiling/ingesting-dataset-to-h3", "/tutorials/Geospatial with Fused/h3-tiling/ingesting-dataset-to-h3"] },
          { to: "/guide/h3-analytics/aggregations", from: ["/tutorials/Geospatial%20with%20Fused/h3-tiling/analysis-with-h3/aggregating-h3-data", "/tutorials/Geospatial with Fused/h3-tiling/analysis-with-h3/aggregating-h3-data"] },
          { to: "/guide/h3-analytics/joining", from: ["/tutorials/Geospatial%20with%20Fused/h3-tiling/analysis-with-h3/joining-h3-data", "/tutorials/Geospatial with Fused/h3-tiling/analysis-with-h3/joining-h3-data"] },
          { to: "/examples/zonal-stats", from: ["/tutorials/Geospatial%20with%20Fused/h3-tiling/analysis-with-h3/zonal-statistics", "/tutorials/Geospatial with Fused/h3-tiling/analysis-with-h3/zonal-statistics"] },
          
          // Geospatial tutorials - Read/Write/Ingestion
          { to: "/guide/data-input-outputs/read-write/geospatial/geospatial-reading", from: ["/tutorials/Geospatial%20with%20Fused/read-data", "/tutorials/Geospatial with Fused/read-data"] },
          { to: "/guide/data-input-outputs/read-write/geospatial/geospatial-writing", from: ["/tutorials/Geospatial%20with%20Fused/write-data", "/tutorials/Geospatial with Fused/write-data"] },
          { to: "/guide/data-input-outputs/read-write/geospatial/ingestion", from: ["/tutorials/Geospatial%20with%20Fused/geospatial-data-ingestion", "/tutorials/Geospatial with Fused/geospatial-data-ingestion"] },
          { to: "/guide/data-input-outputs/read-write/geospatial/ingestion", from: ["/tutorials/Geospatial%20with%20Fused/geospatial-data-ingestion/why-ingestion", "/tutorials/Geospatial with Fused/geospatial-data-ingestion/why-ingestion"] },
          { to: "/guide/data-input-outputs/read-write/geospatial/ingestion", from: ["/tutorials/Geospatial%20with%20Fused/geospatial-data-ingestion/ingest-your-data", "/tutorials/Geospatial with Fused/geospatial-data-ingestion/ingest-your-data"] },
          { to: "/guide/data-input-outputs/read-write/geospatial/ingestion", from: ["/tutorials/Geospatial%20with%20Fused/geospatial-data-ingestion/geospatial-file-formats", "/tutorials/Geospatial with Fused/geospatial-data-ingestion/geospatial-file-formats"] },
          
          // Geospatial tutorials - Other
          { to: "/guide/working-with-udfs/geospatial/single-vs-tile", from: ["/tutorials/Geospatial%20with%20Fused/filetile", "/tutorials/Geospatial with Fused/filetile"] },
          { to: "/guide/data-input-outputs/export-api/geospatial-export", from: ["/tutorials/Geospatial%20with%20Fused/other-integrations", "/tutorials/Geospatial with Fused/other-integrations"] },
          { to: "/guide/data-input-outputs/import-connection/geospatial/gee", from: ["/tutorials/Geospatial%20with%20Fused/gee_bigquery", "/tutorials/Geospatial with Fused/gee_bigquery"] },
          { to: "/examples/canvas-examples", from: ["/tutorials/Geospatial%20with%20Fused/canvas-catalog", "/tutorials/Geospatial with Fused/canvas-catalog"] },
          
          // Geospatial use cases
          { to: "/examples/dark-vessel-detection", from: ["/tutorials/Geospatial%20with%20Fused/use-cases/dark-vessel-detection", "/tutorials/Geospatial with Fused/use-cases/dark-vessel-detection"] },
          { to: "/examples/climate-dashboard", from: ["/tutorials/Geospatial%20with%20Fused/use-cases/Climate%20Dashboard", "/tutorials/Geospatial with Fused/use-cases/Climate Dashboard"] },
          { to: "/examples/satellite-imagery", from: ["/tutorials/Geospatial%20with%20Fused/use-cases/exploring_maxar_data", "/tutorials/Geospatial with Fused/use-cases/exploring_maxar_data"] },
          { to: "/examples/zonal-stats", from: ["/tutorials/Geospatial%20with%20Fused/use-cases/zonal-stats", "/tutorials/Geospatial with Fused/use-cases/zonal-stats"] },
          { to: "/examples/vibe-chart-building", from: ["/tutorials/Geospatial%20with%20Fused/use-cases/vibe-coded-timeseries", "/tutorials/Geospatial with Fused/use-cases/vibe-coded-timeseries"] },
          
          // 2min with Fused / Quickstart
          { to: "/guide/getting-started/first-udf-basics", from: ["/tutorials/2min-with-fused", "/quickstart"] },
          { to: "/guide/getting-started/first-udf-basics", from: ["/tutorials/load-and-export-data", "/tutorials/load_and_save_data"] },
          
          // Core concepts redirects
          { to: "/guide/working-with-udfs/execution/realtime", from: ["/core-concepts/run-udfs/run-small-udfs", "/core-concepts/run-udfs"] },
          { to: "/guide/working-with-udfs/execution/batch-jobs", from: ["/core-concepts/run-udfs/run_large", "/core-concepts/run-udfs/run-large"] },
          { to: "/guide/working-with-udfs/writing-udfs", from: ["/core-concepts/write", "/core-concepts/best-practices/udf-best-practices"] },
          { to: "/guide/working-with-udfs/caching", from: ["/core-concepts/cache"] },
          { to: "/guide/advanced-setup/file-system", from: ["/core-concepts/content-management/file-system"] },
          { to: "/guide/advanced-setup/git-integration", from: ["/core-concepts/content-management/git"] },
          { to: "/guide/advanced-setup/dependencies", from: ["/core-concepts/run-udfs/dependencies"] },
          { to: "/guide/getting-started/workbench-intro", from: ["/core-concepts/best-practices/workbench-best-practices"] },
          { to: "/guide/getting-started/first-udf-basics", from: ["/core-concepts/why"] },
          { to: "/guide/working-with-udfs/execution/realtime", from: ["/core-concepts/async"] },
          
          // Old workbench paths
          { to: "/workbench/udf-explorer", from: ["/workbench/udf-catalog"] },
          { to: "/workbench/udf-builder/code-editor", from: ["/workbench/udf-editor"] },
        ],
        // createRedirects(existingPath) {
        //   if (existingPath.includes("/user-guide/out")) {
        //     return [existingPath.replace("/user-guide/out", "/basics/out")];
        //   }
        //   if (existingPath.includes("/basics/user-guide/")) {
        //     return [
        //       existingPath.replace("/user-guide/", "/basics/user-guide/"),
        //     ];
        //   }
        //   return undefined;
        // },
      },
    ],
    // Only load Google Analytics in production
    ...(process.env.NODE_ENV === 'production' ? [
      [
        "@docusaurus/plugin-google-gtag",
        {
          trackingID: "G-CRPW2C404Y",
          anonymizeIP: true,
        },
      ],
    ] : []),
    

  ],
};

export default config;
