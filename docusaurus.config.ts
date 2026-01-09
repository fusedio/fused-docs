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

  // onBrokenLinks: "throw", // Breaking CI if links aren't good - TEMPORARILY DISABLED FOR REDIRECT TESTING
  onBrokenLinks: "warn", // TODO: Change back to "throw" after updating blog post links
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
          // ============================================
          // DOCS REVAMP REDIRECTS
          // ============================================
          // Old pages moved to: docs_revamp_planning/_archived_docs/
          // To restore: mv docs_revamp_planning/_archived_docs/* docs/
          // ============================================
          
          // --- Tutorials/Analytics → Guide ---
          { to: "/guide/building-apps/standalone-maps", from: ["/tutorials/Analytics%20&%20Dashboard/standalone-maps"] },
          { to: "/guide/use-cases/realtime-data-processing", from: ["/tutorials/Analytics%20&%20Dashboard/realtime-data-processing"] },
          { to: "/guide/building-apps/interactive-graphs-for-your-data", from: ["/tutorials/Analytics%20&%20Dashboard/interactive-graphs-for-your-data"] },
          { to: "/guide/building-apps/let-anyone-talk-to-your-data", from: ["/tutorials/Analytics%20&%20Dashboard/let-anyone-talk-to-your-data"] },
          { to: "/guide/use-cases/stack-overflow-surveys", from: ["/tutorials/Analytics%20&%20Dashboard/stack-overflow-surveys"] },
          { to: "/guide/use-cases/currency-trading-prediction", from: ["/tutorials/Analytics%20&%20Dashboard/currency-trading-prediction"] },
          
          // --- Tutorials/Data Science → Guide ---
          { to: "/guide/use-cases/discover-data", from: ["/tutorials/Data%20Science%20&%20AI/discover_data"] },
          { to: "/guide/use-cases/ai-for-web-scraping", from: ["/tutorials/Data%20Science%20&%20AI/scraping"] },
          { to: "/guide/use-cases/pdf-scraping", from: ["/tutorials/Data%20Science%20&%20AI/pdf_scraping"] },
          { to: "/guide/use-cases/competitor-analysis", from: ["/tutorials/Data%20Science%20&%20AI/competitor_analysis"] },
          
          // --- Tutorials/Engineering → Guide ---
          { to: "/guide/loading-data/", from: ["/tutorials/Engineering%20&%20ETL/connect-your-data-to-fused"] },
          { to: "/guide/loading-data/handling-large-remote-files", from: ["/tutorials/Engineering%20&%20ETL/handling-large-remote-files"] },
          { to: "/guide/writing-data/turn-your-data-into-an-api", from: ["/tutorials/Engineering%20&%20ETL/turn-your-data-into-an-api"] },
          
          // --- Tutorials/Geospatial → Guide ---
          { to: "/guide/", from: ["/tutorials/Geospatial%20with%20Fused", "/tutorials/Geospatial%20with%20Fused/index"] },
          { to: "/guide/loading-data/", from: ["/tutorials/Geospatial%20with%20Fused/read-data"] },
          { to: "/guide/writing-data/", from: ["/tutorials/Geospatial%20with%20Fused/write-data"] },
          { to: "/guide/running-udfs/best-practices/", from: ["/tutorials/Geospatial%20with%20Fused/best-practices"] },
          { to: "/guide/building-apps/visualization", from: ["/tutorials/Geospatial%20with%20Fused/visualization"] },
          { to: "/guide/running-udfs/quality-assurance", from: ["/tutorials/Geospatial%20with%20Fused/quality-assurance"] },
          { to: "/reference/udf-patterns/bounds-and-tiles", from: ["/tutorials/Geospatial%20with%20Fused/filetile"] },
          { to: "/reference/udf-patterns/integrations", from: ["/tutorials/Geospatial%20with%20Fused/other-integrations"] },
          { to: "/guide/use-cases/canvas-catalog", from: ["/tutorials/Geospatial%20with%20Fused/canvas-catalog"] },
          { to: "/guide/loading-data/gee", from: ["/tutorials/Geospatial%20with%20Fused/gee_bigquery"] },
          { to: "/guide/h3-hexagons/h3-zonal-stats", from: ["/tutorials/Geospatial%20with%20Fused/processing-statistics"] },
          
          // --- Tutorials/H3 → Guide/H3 ---
          { to: "/guide/h3-hexagons/", from: ["/tutorials/Geospatial%20with%20Fused/h3-tiling"] },
          { to: "/guide/h3-hexagons/when-to-use-h3", from: ["/tutorials/Geospatial%20with%20Fused/h3-tiling/when-to-use-h3"] },
          { to: "/guide/h3-hexagons/file-to-h3", from: ["/tutorials/Geospatial%20with%20Fused/h3-tiling/file-to-h3"] },
          { to: "/guide/h3-hexagons/dynamic-tile-to-h3", from: ["/tutorials/Geospatial%20with%20Fused/h3-tiling/dynamic-tile-to-h3"] },
          { to: "/guide/h3-hexagons/ingesting-dataset-to-h3", from: ["/tutorials/Geospatial%20with%20Fused/h3-tiling/ingesting-dataset-to-h3"] },
          { to: "/guide/h3-hexagons/aggregating-h3-data", from: ["/tutorials/Geospatial%20with%20Fused/h3-tiling/analysis-with-h3"] },
          { to: "/guide/h3-hexagons/aggregating-h3-data", from: ["/tutorials/Geospatial%20with%20Fused/h3-tiling/analysis-with-h3/aggregating-h3-data"] },
          { to: "/guide/h3-hexagons/joining-h3-datasets", from: ["/tutorials/Geospatial%20with%20Fused/h3-tiling/analysis-with-h3/joining-h3-datasets"] },
          { to: "/guide/h3-hexagons/h3-zonal-stats", from: ["/tutorials/Geospatial%20with%20Fused/h3-tiling/analysis-with-h3/h3-zonal-stats"] },
          
          // --- Tutorials/Geospatial Ingestion → Guide ---
          { to: "/guide/geospatial-ingestion/", from: ["/tutorials/Geospatial%20with%20Fused/geospatial-data-ingestion"] },
          { to: "/guide/geospatial-ingestion/why-ingestion", from: ["/tutorials/Geospatial%20with%20Fused/geospatial-data-ingestion/why-ingestion"] },
          { to: "/guide/geospatial-ingestion/ingest-your-data", from: ["/tutorials/Geospatial%20with%20Fused/geospatial-data-ingestion/ingest-your-data"] },
          { to: "/guide/geospatial-ingestion/geospatial-file-formats", from: ["/tutorials/Geospatial%20with%20Fused/geospatial-data-ingestion/geospatial-file-formats"] },
          
          // --- Tutorials/Use Cases → Guide/Use Cases ---
          { to: "/guide/use-cases/", from: ["/tutorials/Geospatial%20with%20Fused/geospatial-use-cases", "/use-cases/"] },
          { to: "/guide/use-cases/climate-dashboard", from: ["/tutorials/Geospatial%20with%20Fused/use-cases/climate-dashboard"] },
          { to: "/guide/use-cases/dark-vessel-detection", from: ["/tutorials/Geospatial%20with%20Fused/use-cases/dark-vessel-detection"] },
          { to: "/guide/use-cases/zonal-stats", from: ["/tutorials/Geospatial%20with%20Fused/use-cases/zonal-stats"] },
          { to: "/guide/use-cases/exploring_maxar_data", from: ["/tutorials/Geospatial%20with%20Fused/use-cases/exploring_maxar_data"] },
          
          // --- Core Concepts → Guide/Reference ---
          { to: "/guide/running-udfs/realtime", from: ["/core-concepts/run-udfs/run-small-udfs"] },
          { to: "/guide/running-udfs/batch-jobs", from: ["/core-concepts/run-udfs/run_large"] },
          { to: "/guide/running-udfs/writing-udfs", from: ["/core-concepts/write"] },
          { to: "/guide/scaling-up/cache", from: ["/core-concepts/cache"] },
          { to: "/guide/scaling-up/async", from: ["/core-concepts/async"] },
          { to: "/guide/running-udfs/best-practices/", from: ["/core-concepts/best-practices"] },
          { to: "/guide/running-udfs/best-practices/udf-best-practices", from: ["/core-concepts/best-practices/udf-best-practices"] },
          { to: "/guide/content-management/onprem", from: ["/core-concepts/onprem", "/core-concepts/setup-profile/"] },
          { to: "/guide/content-management/git", from: ["/core-concepts/content-management/git"] },
          { to: "/guide/content-management/file-system", from: ["/core-concepts/content-management/file-system"] },
          { to: "/guide/geospatial-ingestion/", from: ["/core-concepts/generic-data-ingestion", "/core-concepts/data_ingestion/"] },
          
          // --- Workbench → Reference/Workbench ---
          { to: "/reference/workbench/udf-builder/", from: ["/workbench/udf-builder"] },
          { to: "/reference/workbench/udf-builder/code-editor/", from: ["/workbench/udf-builder/code-editor", "/workbench/udf-editor/"] },
          { to: "/reference/workbench/udf-builder/map/", from: ["/workbench/udf-builder/map", "/workbench/map/"] },
          { to: "/reference/workbench/udf-builder/results/", from: ["/workbench/udf-builder/results"] },
          { to: "/reference/workbench/udf-builder/viz-styling/", from: ["/workbench/udf-builder/styling", "/workbench/viz-styling/"] },
          { to: "/reference/workbench/udf-builder/navigation/", from: ["/workbench/navigation/"] },
          { to: "/reference/workbench/udf-catalog/", from: ["/workbench/udf-explorer"] },
          { to: "/reference/workbench/file-explorer/", from: ["/workbench/file-explorer"] },
          { to: "/reference/workbench/app-builder/", from: ["/workbench/app-builder"] },
          
          // --- Python SDK → Reference/Python SDK ---
          { to: "/reference/python-sdk/", from: ["/python-sdk"] },
          { to: "/reference/python-sdk/top-level-functions/", from: ["/python-sdk/top-level-functions"] },
          { to: "/reference/python-sdk/authentication/", from: ["/python-sdk/authentication"] },
          { to: "/reference/python-sdk/changelog/", from: ["/python-sdk/changelog"] },
          { to: "/reference/python-sdk/api-reference/api/", from: ["/python-sdk/api-reference/api"] },
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
