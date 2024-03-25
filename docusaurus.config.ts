import {themes as prismThemes} from 'prism-react-renderer';
import type {Config} from '@docusaurus/types';
import type * as Preset from '@docusaurus/preset-classic';

const config: Config = {
  title: 'Fused',
  tagline: 'Code to map. Instantly.',
  favicon: 'img/favicon.png',


  trailingSlash: false,
  url: "https://fusedio.github.io/",
  // Set the /<baseUrl>/ pathname under which your site is served
  // For GitHub pages deployment, it is often '/<projectName>/'
  baseUrl: '/fused-docs/',


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

  presets: [
    [
      'classic',
      {
        docs: {
          sidebarPath: './sidebars.ts',
          // Please change this to your repo.
          // Remove this to remove the "edit this page" links.
          editUrl:
            'https://github.com/facebook/docusaurus/tree/main/packages/create-docusaurus/templates/',
            // include: ['**/*.md', '**/*.mdx', '**/fused/**/_*.', '**/_*/**'],
            include: ['**/*.md', '**/*.mdx', 'reference/fused/**'],
            exclude: [
              // '**/_*.{js,jsx,ts,tsx,md,mdx}',
              // '**/_*/**',
              '**/*.test.{js,jsx,ts,tsx}',
              '**/__tests__/**',
            ],
  
        },
        blog: {
          showReadingTime: true,
          // Please change this to your repo.
          // Remove this to remove the "edit this page" links.
          editUrl:
            'https://github.com/facebook/docusaurus/tree/main/packages/create-docusaurus/templates/',
        },
        theme: {
          customCss: './src/css/custom.css',
        },
      } satisfies Preset.Options,
    ],
  ],

  themeConfig: {
    // Replace with your project's social card
    image: 'img/logo-black-bg-transparent.svg',
    navbar: {
      title: 'Fused',
      logo: {
        alt: 'Fused Logo',
        src: 'img/logo-black-bg-transparent.svg',
      },
      items: [
        {
          type: 'docSidebar',
          sidebarId: 'tutorialSidebar',
          position: 'left',
          label: 'Docs',
        },
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
              to: '/docs',
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
        '⭐ If you like Fused, give us a star on <a target="_blank" rel="noopener noreferrer" href="https://github.com/fusedio/udfs/">GitHub</a>! ⭐',
      backgroundColor: '#f023c0',
      textColor: '#ffffff',
      isCloseable: false,
    },

    themes: ['docusaurus-theme-search-typesense'],
    themeConfig: {
      typesense: {
        // Replace this with the name of your index/collection.
        // It should match the "index_name" entry in the scraper's "config.json" file.
        typesenseCollectionName: 'docusaurus-2',
  
        typesenseServerConfig: {
          nodes: [
            {
              host: 'o4svizatly9q58nkp-1.a1.typesense.net',
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
    }


  } satisfies Preset.ThemeConfig,
};

export default config;
