import {themes as prismThemes} from 'prism-react-renderer';
import type {Config} from '@docusaurus/types';
import type * as Preset from '@docusaurus/preset-classic';

const config: Config = {
  title: 'Fused',
  tagline: 'Code to map. Instantly.',
  favicon: 'img/favicon.png',


  trailingSlash: true,
  // url: "https://fusedio.github.io/",
  url: "https://docs.fused.io",
  // Set the /<baseUrl>/ pathname under which your site is served
  // For GitHub pages deployment, it is often '/<projectName>/'
  // baseUrl: '/fused-docs/', // needed for GitHub pages
  baseUrl: '/',


  // GitHub pages deployment config.
  // If you aren't using GitHub pages, you don't need these.
  organizationName: 'fusedio', // Usually your GitHub org/user name.
  projectName: 'fused-docs', // Usually your repo name.

  // onBrokenLinks: 'throw',
  onBrokenLinks: 'ignore',
  onBrokenMarkdownLinks: 'warn',
  

  // Even if you don't use internationalization, you can use this field to set
  // useful metadata like html lang. For example, if your site is Chinese, you
  // may want to replace "en" with "zh-Hans".
  i18n: {
    defaultLocale: 'en',
    locales: ['en'],
  },

  // Currently set to docs only mode. Change to enable blog and main site. https://docusaurus.io/docs/docs-introduction#docs-only-mode
  presets: [
    [
      'classic',
      {
        docs: {
          routeBasePath: '/',
          sidebarPath: './sidebars.ts',
            include: ['**/*.md', '**/*.mdx', 'reference/fused/**'],
            exclude: [
              // '**/_*.{js,jsx,ts,tsx,md,mdx}',
              // '**/_*/**',
              '**/*.test.{js,jsx,ts,tsx}',
              '**/__tests__/**',
            ],
        },
        blog: false,
        theme: {
          customCss: './src/css/custom.css',
        },
      } satisfies Preset.Options,
    ],
  ],

  themes: ['docusaurus-theme-search-typesense'],


  themeConfig: {
    tableOfContents: {
      minHeadingLevel: 2,
      maxHeadingLevel: 4,
    },

    typesense: {
      // Replace this with the name of your index/collection.
      // It should match the "index_name" entry in the scraper's "config.json" file.
      typesenseCollectionName: 'fused',

      typesenseServerConfig: {
        nodes: [
          {
            host: 'o4svizatly9q58nkp-1.a1.typesense.net',
            port: 443,
            protocol: 'https',
          },
          {
            host: 'xxx-2.a1.typesense.net',
            port: 443,
            protocol: 'https',
          },
          {
            host: 'xxx-3.a1.typesense.net',
            port: 443,
            protocol: 'https',
          },
        ],
        apiKey: '5xjdcw9HHu92ZkibK6t7uB2ou7bjxZPA', // Search-only API key
      },

      // Optional: Typesense search parameters: https://typesense.org/docs/0.24.0/api/search.html#search-parameters
      typesenseSearchParameters: {},

      // Optional
      contextualSearch: true,
    },
    // Replace with your project's social card
    image: 'https://fused-magic.s3.us-west-2.amazonaws.com/docs_assets/ecosystem_diagram.png',
    navbar: {
      title: 'Fused',
      logo: {
        alt: 'Fused Logo',
        src: 'img/logo-black-bg-transparent.svg',
      },
      items: [
        // {
        //   type: 'html',
        //   position: 'left',
        //   value: '<span class="logo-docs">{{ docs }}</span>'
        // },
        // Show "Docs" in top navbar
        // {
        //   type: 'docSidebar',
        //   sidebarId: 'tutorialSidebar',
        //   position: 'left',
        //   label: 'Docs',
        // },
        // {to: '/blog', label: 'Blog', position: 'left'},
        {
          href: 'https://github.com/fusedio/udfs',
          label: 'GitHub',
          position: 'right',
        },
      ],
    },
    footer: {
      style: 'dark',
      links: [
        {
          title: 'Docs',
          items: [
            {
              label: 'Overview',
              to: '/',
            },
          ],
        },
        {
          title: 'Community',
          items: [
            {
              label: 'LinkedIn',
              href: 'https://www.linkedin.com/company/fusedio/',
            },
            {
              label: 'Discord',
              href: 'https://discord.com/invite/BxS5wMzdRk',
            },
            {
              label: 'Twitter',
              href: 'https://twitter.com/Fused_io',
            },
          ],
        },
        {
          title: 'More',
          items: [
            {
              label: 'Blog',
              to: 'https://www.fused.io/blog',
            },
            {
              label: 'GitHub',
              href: 'https://github.com/fusedio/udfs',
            },
          ],
        },
      ],
      copyright: `Copyright © ${new Date().getFullYear()} Fused, Inc. Built with Docusaurus.`,
    },
    theme: '@docusaurus/theme-nightOwl',
    colorMode: {
      defaultMode: 'dark',
      disableSwitch: true,
      respectPrefersColorScheme: false,
    },
    prism: {
      theme: prismThemes.nightOwl,
      darkTheme: prismThemes.nightOwl,
    },


    announcementBar: {
      id: 'announcement',
      content:
        '⭐ If you like Fused, star the UDF <a target="_blank" rel="noopener noreferrer" href="https://github.com/fusedio/udfs/">GitHub</a> repo! ⭐',
      backgroundColor: '#991199',
      textColor: '#ffffff',
      isCloseable: false,
    },




  } satisfies Preset.ThemeConfig,
};

export default config;
