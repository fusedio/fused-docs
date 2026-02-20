#!/usr/bin/env node
/**
 * Pings UDF embed URLs (udf.ai and unstable.udf.ai fsh_*.html) from docs to ensure
 * they return HTML, not error payloads (invalid token, UDF not found, etc.).
 * Only scans docs/ — skips docs_backup_jan2026 and any other dirs outside docs/.
 */

const fs = require('fs');
const path = require('path');
const https = require('https');

const DOCS_DIR = 'docs';
const SKIP_DIRS = new Set(['docs_backup_jan2026']);
const UDF_EMBED_REGEX = /https:\/\/(?:udf\.ai|unstable\.udf\.ai)\/fsh_[a-zA-Z0-9]+\.html/g;
const REQUEST_TIMEOUT_MS = 15000;
const BAD_BODY_MARKERS = [
  'Access token invalid',
  'UDF not found',
  "'detail': 'UDF not found'",
  '"detail":"UDF not found"',
];

function extractUdfEmbedUrls() {
  const urls = new Set();
  const dir = path.join(process.cwd(), DOCS_DIR);
  if (!fs.existsSync(dir)) {
    console.error(`❌ ${DOCS_DIR}/ not found`);
    process.exit(1);
  }
  const walk = (d) => {
    for (const name of fs.readdirSync(d)) {
      if (SKIP_DIRS.has(name)) continue;
      const full = path.join(d, name);
      const st = fs.statSync(full);
      if (st.isDirectory()) walk(full);
      else if (name.endsWith('.mdx')) {
        const content = fs.readFileSync(full, 'utf8');
        let m;
        while ((m = UDF_EMBED_REGEX.exec(content)) !== null) urls.add(m[0]);
      }
    }
  };
  walk(dir);
  return [...urls];
}

function fetchUrl(url) {
  return new Promise((resolve) => {
    const req = https.get(url, {
      timeout: REQUEST_TIMEOUT_MS,
      headers: { 'User-Agent': 'FusedDocs-UDF-Embed-Check/1.0' },
    }, (res) => {
      const chunks = [];
      res.on('data', (c) => chunks.push(c));
      res.on('end', () => {
        const body = Buffer.concat(chunks).toString('utf8');
        resolve({
          url,
          status: res.statusCode,
          body,
          ok: res.statusCode === 200 && !body.includes(BAD_BODY_MARKER) && (body.trimStart().startsWith('<') || body.includes('<!')),
        });
      });
    });
    req.on('error', (err) => resolve({ url, status: 0, body: '', ok: false, error: err.message }));
    req.on('timeout', () => {
      req.destroy();
      resolve({ url, status: 0, body: '', ok: false, error: 'timeout' });
    });
  });
}

async function main() {
  const urls = extractUdfEmbedUrls();
  if (urls.length === 0) {
    console.log('✅ No UDF embed URLs found in docs — nothing to check.');
    process.exit(0);
  }
  console.log(`🔗 Found ${urls.length} UDF embed URL(s) in ${DOCS_DIR}/\n`);
  const results = await Promise.all(urls.map(fetchUrl));
  const ok = results.filter((r) => r.ok);
  const bad = results.filter((r) => !r.ok);
  for (const r of ok) console.log(`  ✅ ${r.url}`);
  if (bad.length > 0) {
    console.error('\n❌ UDF embeds not returning valid HTML:\n');
    for (const r of bad) {
      console.error(`  📄 ${r.url}`);
      console.error(`     Status: ${r.status || 'ERROR'} ${r.error || ''}`);
      if (r.body && r.body.length < 200) console.error(`     Body: ${r.body.replace(/\n/g, ' ')}`);
      console.error('');
    }
    console.error('💡 Fix: refresh or recreate the shared token so the .html endpoint returns the map page.\n');
    process.exit(1);
  }
  console.log('\n✨ All UDF embeds returned valid HTML.');
  process.exit(0);
}

main().catch((e) => {
  console.error('❌', e.message);
  process.exit(1);
});
