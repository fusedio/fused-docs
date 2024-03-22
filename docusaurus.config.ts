import {themes as prismThemes} from 'prism-react-renderer';
import type {Config} from '@docusaurus/types';
import type * as Preset from '@docusaurus/preset-classic';

const config: Config = {
  title: 'Fused',
  tagline: 'Code to map. Instantly.',
  favicon: 'img/favicon.png',

  // Set the production url of your site here
  // url: 'https://docs.fused.io',
  url: 'http://localhost:3000',
  // Set the /<baseUrl>/ pathname under which your site is served
  // For GitHub pages deployment, it is often '/<projectName>/'
  baseUrl: '/',

  // GitHub pages deployment config.
  // If you aren't using GitHub pages, you don't need these.
  organizationName: 'fusedlabs', // Usually your GitHub org/user name.
  projectName: 'docs', // Usually your repo name.

  onBrokenLinks: 'throw',
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

    algolia: {
      // The application ID provided by Algolia
      appId: 'JNTLW5AVDA',

      // Public API key: it is safe to commit it
      apiKey: '6ce1dd49f199420095a7d356058a2e49',

      indexName: 'fused',

      // Optional: see doc section below
      contextualSearch: true,

      // Optional: Specify domains where the navigation should occur through window.location instead on history.push. Useful when our Algolia config crawls multiple documentation sites and we want to navigate with window.location.href to them.
      externalUrlRegex: 'external\\.com|domain\\.com',

      // Optional: Replace parts of the item URLs from Algolia. Useful when using the same search index for multiple deployments using a different baseUrl. You can use regexp or string in the `from` param. For example: localhost:3000 vs myCompany.com/docs
      replaceSearchResultPathname: {
        from: '/docs/', // or as RegExp: /\/docs\//
        to: '/',
      },

      // Optional: Algolia search parameters
      searchParameters: {},

      // Optional: path for search page that enabled by default (`false` to disable it)
      searchPagePath: 'search',

      //... other Algolia params
    },


  } satisfies Preset.ThemeConfig,
};

export default config;
