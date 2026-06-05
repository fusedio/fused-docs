#!/usr/bin/env node
// Fast, network-free check for broken internal page links and missing image/
// asset references across docs/ — meant as a pre-commit gate and a quick local
// command (`npm run check-links`).
//
// Why only page + asset links (not anchors or external URLs)?
//   - Broken #anchors and broken page links are already caught authoritatively
//     by `npm run build` (onBrokenLinks / onBrokenAnchors: "throw"), which
//     resolves against the fully-rendered site. Anchors in particular can't be
//     checked from source — many headings are emitted by MDX components.
//   - This script trades that completeness for speed: it resolves every internal
//     link against the real Docusaurus URL space (slug/id rules, folder-index
//     collapse, redirects, blog, the generated widget-api pages, static assets)
//     in well under a second, so it can run on every commit. The build remains
//     the comprehensive gate.

const fs = require('fs');
const path = require('path');
const matter = require('gray-matter');

const ROOT = path.resolve(__dirname, '..');
const DOCS_DIR = path.join(ROOT, 'docs');
const BLOG_DIR = path.join(ROOT, 'blog');
const STATIC_DIR = path.join(ROOT, 'static');
const WIDGET_SCHEMA_DIR = path.join(STATIC_DIR, 'widget-schema');
const CONFIG_FILE = path.join(ROOT, 'docusaurus.config.ts');

// Routes that exist but aren't backed by a doc/blog/static file.
const EXTRA_VALID_PATHS = ['/', '/search', '/blog'];

function walk(dir, exts) {
  const out = [];
  if (!fs.existsSync(dir)) return out;
  for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
    const full = path.join(dir, entry.name);
    if (entry.isDirectory()) out.push(...walk(full, exts));
    else if (exts.some((e) => entry.name.endsWith(e))) out.push(full);
  }
  return out;
}

function normalize(p) {
  let s = decodeURIComponent(p);
  if (s.length > 1) s = s.replace(/\/+$/, '');
  return s;
}

// Derive a doc's Docusaurus URL from its path + frontmatter:
//   - an absolute frontmatter `slug` wins outright
//   - a frontmatter `id` replaces the filename as the last segment
//   - index files, and a file named after its folder, map to the folder URL
function fileToUrl(relPath, data) {
  if (typeof data.slug === 'string' && data.slug.startsWith('/')) return data.slug;
  const parts = relPath.replace(/\\/g, '/').split('/');
  const file = parts.pop().replace(/\.mdx?$/, '');
  const last = typeof data.id === 'string' ? data.id : file;
  if (last.toLowerCase() !== 'index' && last !== parts[parts.length - 1]) parts.push(last);
  return '/' + parts.join('/');
}

const validPaths = new Set(EXTRA_VALID_PATHS.map(normalize));

function registerDocs() {
  for (const file of walk(DOCS_DIR, ['.md', '.mdx'])) {
    if (path.basename(file).startsWith('_')) continue; // partials
    const { data } = matter(fs.readFileSync(file, 'utf8'));
    if (data.draft === true) continue; // not built in production
    validPaths.add(normalize(fileToUrl(path.relative(DOCS_DIR, file), data)));
  }
}

function registerBlog() {
  for (const file of walk(BLOG_DIR, ['.md', '.mdx'])) {
    if (path.basename(file).startsWith('_')) continue;
    const { data } = matter(fs.readFileSync(file, 'utf8'));
    if (data.draft === true) continue;
    let slug = typeof data.slug === 'string'
      ? data.slug
      : path.basename(file).replace(/\.mdx?$/, '').replace(/^\d{4}-\d{2}-\d{2}-/, '');
    if (!slug.startsWith('/')) slug = '/blog/' + slug.replace(/^\//, '');
    validPaths.add(normalize(slug));
  }
}

// docusaurus-plugin-widget-api generates docs/widget-api/<slug>.mdx from these
// schema files at build time — valid routes, but not committed source files.
function registerWidgetApi() {
  if (!fs.existsSync(WIDGET_SCHEMA_DIR)) return;
  for (const f of fs.readdirSync(WIDGET_SCHEMA_DIR)) {
    if (f.endsWith('.json')) validPaths.add('/widget-api/' + f.replace(/\.json$/, ''));
  }
}

function registerRedirects() {
  const config = fs.readFileSync(CONFIG_FILE, 'utf8');
  for (const m of config.matchAll(/from:\s*(\[[^\]]*\]|["'][^"']*["'])/g)) {
    const froms = m[1].startsWith('[')
      ? [...m[1].matchAll(/["']([^"']+)["']/g)].map((x) => x[1])
      : [m[1].slice(1, -1)];
    for (const f of froms) validPaths.add(normalize(f));
  }
}

function staticAssetExists(urlPath) {
  return fs.existsSync(path.join(STATIC_DIR, decodeURIComponent(urlPath.replace(/^\//, ''))));
}

function isAsset(p) {
  return /\.[a-z0-9]{2,5}$/i.test(p);
}

// Internal markdown and JSX links, with code fences stripped and templated
// (${...} / {...}) targets ignored.
function extractLinks(file) {
  const { content } = matter(fs.readFileSync(file, 'utf8'));
  const body = content
    .replace(/```[\s\S]*?```/g, '')
    .replace(/~~~[\s\S]*?~~~/g, '')
    .replace(/\{\/\*[\s\S]*?\*\/\}/g, '') // JSX comments
    .replace(/<!--[\s\S]*?-->/g, ''); // HTML comments
  const links = [];
  for (const m of body.matchAll(/\]\((\/[^)\s]*)\)/g)) links.push(m[1]);
  for (const m of body.matchAll(/\b(?:to|href|src)=["'](\/[^"']*)["']/g)) links.push(m[1]);
  return links.filter((l) => !l.includes('${') && !l.includes('{'));
}

function main() {
  registerDocs();
  registerBlog();
  registerWidgetApi();
  registerRedirects();

  const broken = [];
  let checked = 0;

  for (const file of walk(DOCS_DIR, ['.md', '.mdx'])) {
    if (path.basename(file).startsWith('_')) continue;
    const rel = path.relative(ROOT, file).replace(/\\/g, '/');
    for (const link of extractLinks(file)) {
      checked++;
      const targetPath = link.split('#')[0]; // anchors are checked by the build
      if (targetPath === '') continue; // pure same-page anchor
      if (validPaths.has(normalize(targetPath))) continue;
      if (staticAssetExists(targetPath)) continue;
      broken.push({
        file: rel,
        link,
        reason: isAsset(targetPath) ? 'missing static asset' : 'no such page',
      });
    }
  }

  console.log(`Checked ${checked} internal links across ${validPaths.size} routes.\n`);

  if (broken.length === 0) {
    console.log('All internal page and asset links resolve.');
    return;
  }

  const byFile = new Map();
  for (const b of broken) {
    if (!byFile.has(b.file)) byFile.set(b.file, []);
    byFile.get(b.file).push(b);
  }
  // --warn surfaces findings without failing (for the non-blocking pre-commit
  // hook); without it the command exits non-zero so it can gate when wanted.
  const warnOnly = process.argv.includes('--warn');
  const log = warnOnly ? console.warn : console.error;
  log(`Found ${broken.length} broken link(s):\n`);
  for (const [f, items] of [...byFile].sort()) {
    log(f);
    for (const it of items) log(`  ${it.link}  (${it.reason})`);
    log('');
  }
  if (warnOnly) {
    console.warn('Not blocking the commit — please fix these when you can.');
  } else {
    process.exitCode = 1;
  }
}

main();
