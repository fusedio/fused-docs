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

  trailingSlash: true,
  // url: "https://fusedio.github.io/",
  // url: "https://docs.fused.io",
  // // Set the /<baseUrl>/ pathname under which your site is served
  // // For GitHub pages deployment, it is often '/<projectName>/'
  // // baseUrl: '/fused-docs/', // needed for GitHub pages
  // baseUrl: "/",
  url: process.env.DEPLOYMENT_URL || "https://docs.fused.io",
  baseUrl: process.env.BASE_URL || "/",

  // GitHub pages deployment config.
  // If you aren't using GitHub pages, you don't need these.
  organizationName: "fusedio", // Usually your GitHub org/user name.
  projectName: "fused-docs", // Usually your repo name.

  onBrokenLinks: "throw", // Breaking CI if links aren't good
  // onBrokenLinks: "ignore",
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
        },
        theme: {
          customCss: "./src/css/custom.css",
        },
      } satisfies Preset.Options,
    ],
  ],

  themeConfig: {
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
          // { to: "/basics/core-concepts/faq/", from: ["/basics/faq/"] },
          // {
          //   to: "/user-guide/",
          //   from: ["/basics/user-guide/"],
          // },
          {
            to: "/workbench/udf-builder/code-editor/",
            from: ["/workbench/udf-editor/"],
          },
          {
            to: "/workbench/udf-builder/navigation/",
            from: ["/workbench/navigation/"],
          },
          { to: "/workbench/udf-builder/map/", from: ["/workbench/map/"] },
          {
            to: "/workbench/udf-builder/runtime/",
            from: ["/workbench/runtime/"],
          },
          {
            to: "/workbench/udf-builder/styling/",
            from: ["/workbench/viz-styling/"],
          },
          {
            to: "/core-concepts/generic-data-ingestion",
            from: ["/core-concepts/data_ingestion/"],
          },
          {
            to: "/core-concepts/onprem",
            from: ["/core-concepts/setup-profile/"],
          },
          {
            to: "/tutorials/Geospatial%20with%20Fused/geospatial-use-cases/",
            from: ["/use-cases/"],
          },
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
    [
      "@docusaurus/plugin-google-gtag",
      {
        trackingID: "G-CRPW2C404Y",
        anonymizeIP: true,
      },
    ],

  ],
};

export default config;
