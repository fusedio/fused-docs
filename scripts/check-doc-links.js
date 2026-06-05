#!/usr/bin/env node
// Flags broken internal page/asset links in docs/ against Docusaurus's URL space
// (slug/id rules, folder-index collapse, redirects, blog, widget-api pages,
// static assets). Fast and network-free.
//
// Run as `npm run check-links` (exits non-zero on findings) or as a non-blocking
// pre-commit hook with `--warn` (prints findings, always exits 0). Anchors and
// external links are left to the build (onBrokenLinks / onBrokenAnchors).

const fs = require('fs');
const path = require('path');
const matter = require('gray-matter');

const ROOT = path.resolve(__dirname, '..');
const DOCS = path.join(ROOT, 'docs');
const STATIC = path.join(ROOT, 'static');
const WARN = process.argv.includes('--warn');

const decode = (s) => { try { return decodeURIComponent(s); } catch { return s; } };
const norm = (p) => { const s = decode(p); return s.length > 1 ? s.replace(/\/+$/, '') : s; };
const data = (file) => matter(fs.readFileSync(file, 'utf8')).data;

// Recursively collect files under `dir` whose basename satisfies `match`.
function find(dir, match) {
  if (!fs.existsSync(dir)) return [];
  return fs.readdirSync(dir, { withFileTypes: true }).flatMap((e) => {
    const full = path.join(dir, e.name);
    return e.isDirectory() ? find(full, match) : match(e.name) ? [full] : [];
  });
}

const isPage = (n) => /\.mdx?$/.test(n) && !n.startsWith('_');

// A doc's URL: absolute `slug` wins; else folder path + (`id` or filename), with
// index files and a file named after its folder collapsing to the folder URL.
function docUrl(rel, fm) {
  if (typeof fm.slug === 'string' && fm.slug.startsWith('/')) return fm.slug;
  const parts = rel.replace(/\\/g, '/').split('/');
  const filename = parts.pop().replace(/\.mdx?$/, '');
  const last = typeof fm.id === 'string' ? fm.id : filename;
  if (last.toLowerCase() !== 'index' && last !== parts[parts.length - 1]) parts.push(last);
  return '/' + parts.join('/');
}

// Build the set of valid routes.
function buildRoutes() {
  const routes = new Set(['/', '/search', '/blog'].map(norm));

  for (const file of find(DOCS, isPage)) {
    const fm = data(file);
    if (fm.draft !== true) routes.add(norm(docUrl(path.relative(DOCS, file), fm)));
  }

  for (const file of find(path.join(ROOT, 'blog'), isPage)) {
    const fm = data(file);
    if (fm.draft === true) continue;
    let slug = typeof fm.slug === 'string'
      ? fm.slug
      : path.basename(file).replace(/\.mdx?$/, '').replace(/^\d{4}-\d{2}-\d{2}-/, '');
    routes.add(norm(slug.startsWith('/') ? slug : '/blog/' + slug));
  }

  // widget-api pages are generated from these schemas at build time.
  for (const file of find(path.join(STATIC, 'widget-schema'), (n) => n.endsWith('.json')))
    routes.add('/widget-api/' + path.basename(file, '.json'));

  // generated-index categories serve a route at their folder URL (or link.slug).
  for (const file of find(DOCS, (n) => n === '_category_.json')) {
    let cfg;
    try { cfg = JSON.parse(fs.readFileSync(file, 'utf8')); } catch { continue; }
    if (cfg.link && cfg.link.type === 'generated-index') {
      const dir = path.relative(DOCS, path.dirname(file)).replace(/\\/g, '/');
      routes.add(norm(typeof cfg.link.slug === 'string' ? cfg.link.slug : '/' + dir));
    }
  }

  // redirect `from` paths are valid routes too.
  const config = fs.readFileSync(path.join(ROOT, 'docusaurus.config.ts'), 'utf8');
  for (const m of config.matchAll(/from:\s*(\[[^\]]*\]|["'][^"']*["'])/g))
    for (const q of m[1].match(/["']([^"']+)["']/g) || []) routes.add(norm(q.slice(1, -1)));

  return routes;
}

const assetExists = (p) => fs.existsSync(path.join(STATIC, decode(p).replace(/^\//, '')));

// Internal markdown and JSX (href/to/src) links, ignoring code, comments, and
// templated targets.
function linksIn(file) {
  const body = matter(fs.readFileSync(file, 'utf8')).content
    .replace(/```[\s\S]*?```|~~~[\s\S]*?~~~/g, '') // fenced code
    .replace(/`[^`\n]*`/g, '') // inline code
    .replace(/\{\/\*[\s\S]*?\*\/\}|<!--[\s\S]*?-->/g, ''); // comments
  const out = [];
  for (const m of body.matchAll(/\]\((\/[^)\s]*)\)/g)) out.push(m[1]);
  for (const m of body.matchAll(/\b(?:to|href|src)=["'](\/[^"']*)["']/g)) out.push(m[1]);
  return out.filter((l) => !l.includes('{'));
}

function run() {
  const routes = buildRoutes();
  const broken = [];

  for (const file of find(DOCS, isPage)) {
    const rel = path.relative(ROOT, file).replace(/\\/g, '/');
    for (const link of linksIn(file)) {
      const target = link.split('#')[0]; // anchors are validated by the build
      if (!target || routes.has(norm(target)) || assetExists(target)) continue;
      const reason = /\.[a-z0-9]{2,5}$/i.test(target) ? 'missing static asset' : 'no such page';
      broken.push({ rel, link, reason });
    }
  }

  console.log(`Checked internal links across ${routes.size} routes.\n`);
  if (broken.length === 0) {
    console.log('All internal page and asset links resolve.');
    return;
  }

  const log = WARN ? console.warn : console.error;
  log(`Found ${broken.length} broken link(s):`);
  let current = '';
  for (const b of broken.sort((a, b) => a.rel.localeCompare(b.rel))) {
    if (b.rel !== current) log(`\n${(current = b.rel)}`);
    log(`  ${b.link}  (${b.reason})`);
  }
  if (WARN) console.warn('\nNot blocking the commit — please fix these when you can.');
  else process.exitCode = 1;
}

// Never let an unexpected error block a commit when running as the --warn hook.
try {
  run();
} catch (err) {
  console.warn(`check-doc-links skipped (error: ${err.message})`);
  if (!WARN) process.exitCode = 1;
}
