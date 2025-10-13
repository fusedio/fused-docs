const fs = require('fs');
const https = require('https');
const http = require('http');

// Configuration
const LLMS_FILE = 'static/llms.txt';
const BASE_URL = 'https://docs.fused.io';

function extractLinksFromLlmsTxt(filePath) {
  const content = fs.readFileSync(filePath, 'utf8');
  const links = [];
  
  // Extract all markdown links [title](url)
  const linkRegex = /\[([^\]]+)\]\((https?:\/\/[^)]+)\)/g;
  let match;
  
  while ((match = linkRegex.exec(content)) !== null) {
    const title = match[1];
    const url = match[2];
    
    // Only check internal docs links
    if (url.startsWith(BASE_URL)) {
      links.push({ title, url });
    }
  }
  
  return links;
}

function checkUrl(url, followRedirects = true) {
  return new Promise((resolve) => {
    const protocol = url.startsWith('https') ? https : http;
    
    const request = protocol.get(url, { 
      timeout: 10000,
      headers: {
        'User-Agent': 'Mozilla/5.0 (compatible; LinkChecker/1.0)'
      }
    }, (response) => {
      // Handle redirects
      if (followRedirects && response.statusCode >= 300 && response.statusCode < 400 && response.headers.location) {
        // Resolve relative redirect URLs
        let redirectUrl = response.headers.location;
        if (redirectUrl.startsWith('/')) {
          const urlObj = new URL(url);
          redirectUrl = `${urlObj.protocol}//${urlObj.host}${redirectUrl}`;
        }
        // Follow redirect
        checkUrl(redirectUrl, followRedirects).then(resolve);
        return;
      }
      
      resolve({
        url,
        status: response.statusCode,
        ok: response.statusCode === 200 || (response.statusCode >= 300 && response.statusCode < 400)
      });
    });
    
    request.on('error', (error) => {
      resolve({
        url,
        status: 0,
        ok: false,
        error: error.message
      });
    });
    
    request.on('timeout', () => {
      request.destroy();
      resolve({
        url,
        status: 0,
        ok: false,
        error: 'Request timeout'
      });
    });
  });
}

async function testLinks() {
  console.log('🔍 Testing HTTP links in llms.txt...\n');
  
  if (!fs.existsSync(LLMS_FILE)) {
    console.error(`❌ Error: ${LLMS_FILE} not found`);
    process.exit(1);
  }
  
  const links = extractLinksFromLlmsTxt(LLMS_FILE);
  console.log(`📊 Found ${links.length} internal links to test\n`);
  console.log('⏳ Testing links (this may take a minute)...\n');
  
  const results = [];
  let completed = 0;
  
  // Test links in batches to avoid overwhelming the server
  const batchSize = 5;
  for (let i = 0; i < links.length; i += batchSize) {
    const batch = links.slice(i, i + batchSize);
    const batchResults = await Promise.all(
      batch.map(link => checkUrl(link.url))
    );
    
    results.push(...batchResults.map((result, idx) => ({
      ...result,
      title: batch[idx].title
    })));
    
    completed += batch.length;
    process.stdout.write(`\r   Progress: ${completed}/${links.length} links tested`);
  }
  
  console.log('\n');
  
  // Analyze results
  const workingLinks = results.filter(r => r.ok);
  const brokenLinks = results.filter(r => !r.ok);
  
  console.log(`✅ Working links: ${workingLinks.length}`);
  console.log(`❌ Broken links: ${brokenLinks.length}\n`);
  
  if (brokenLinks.length > 0) {
    console.error('🚨 The following links are broken:\n');
    
    brokenLinks.forEach(({ title, url, status, error }) => {
      console.error(`   📄 ${title}`);
      console.error(`      URL: ${url}`);
      console.error(`      Status: ${status || 'ERROR'} ${error ? `(${error})` : ''}`);
      console.error('');
    });
    
    console.error('💡 These links return non-200 status codes or failed to load.');
    console.error('   Check if the pages exist on the deployed site.\n');
    
    process.exit(1);
  }
  
  console.log('✨ All links are working!');
  process.exit(0);
}

// Run tests
testLinks().catch(error => {
  console.error('❌ Error running tests:', error.message);
  process.exit(1);
});

