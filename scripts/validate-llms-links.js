const fs = require('fs');
const path = require('path');
const matter = require('gray-matter');

// Configuration
const LLMS_FILE = 'static/llms.txt';
const DOCS_DIR = 'docs';
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

function extractFrontmatter(filePath) {
  try {
    const content = fs.readFileSync(filePath, 'utf8');
    const { data } = matter(content);
    return {
      id: data.id || data.slug || null,
      draft: data.draft || false,
      unlisted: data.unlisted || false
    };
  } catch (error) {
    return { id: null, draft: false, unlisted: false };
  }
}

function buildUrlToFileMapping(dir, basePath = '') {
  const mapping = {};
  
  try {
    const entries = fs.readdirSync(dir, { withFileTypes: true });
    
    for (const entry of entries) {
      const fullPath = path.join(dir, entry.name);
      const relativePath = path.join(basePath, entry.name);
      
      if (entry.isDirectory()) {
        // Skip hidden directories
        if (entry.name.startsWith('_')) continue;
        
        // Recursively process subdirectories
        Object.assign(mapping, buildUrlToFileMapping(fullPath, relativePath));
      } else if (entry.name.endsWith('.mdx') || entry.name.endsWith('.md')) {
        // Skip hidden files
        if (entry.name.startsWith('_')) continue;
        
        const frontmatter = extractFrontmatter(fullPath);
        
        // Skip draft and unlisted content
        if (frontmatter.draft || frontmatter.unlisted) continue;
        
        // Docusaurus URL generation rules:
        // 1. For index.mdx files, the URL is just the parent directory
        // 2. For regular files with an ID, use the ID
        // 3. For regular files without an ID, use the filename (lowercase, _ to -)
        // 4. Directory names preserve case and spaces are URL encoded
        
        const parts = relativePath.replace(/\\/g, '/').split('/');
        const filename = parts[parts.length - 1];
        const isIndexFile = filename.replace(/\.mdx?$/, '').toLowerCase() === 'index';
        
        let urlParts;
        if (isIndexFile) {
          // For index files, just use the directory path
          urlParts = parts.slice(0, -1).map(part => encodeURIComponent(part).replace(/%20/g, '%20'));
        } else {
          // For regular files
          urlParts = parts.map((part, index) => {
            const isLastPart = index === parts.length - 1;
            if (isLastPart) {
              // Use frontmatter ID if available, otherwise use filename
              if (frontmatter.id) {
                return frontmatter.id;
              }
              return part
                .replace(/\.mdx?$/, ''); // Remove extension only, keep underscores and case
            } else {
              // Directory names preserve case, URL encode spaces
              return encodeURIComponent(part).replace(/%20/g, '%20');
            }
          });
        }
        
        const urlPath = urlParts.join('/');
        const url = `${BASE_URL}/${urlPath}`;
        mapping[url] = fullPath;
      }
    }
  } catch (error) {
    console.warn(`Warning: Could not read directory ${dir}:`, error.message);
  }
  
  return mapping;
}

function validateLinks() {
  console.log('🔍 Validating links in llms.txt...\n');
  
  if (!fs.existsSync(LLMS_FILE)) {
    console.error(`❌ Error: ${LLMS_FILE} not found`);
    console.log('💡 Run: node scripts/generate-llms-txt.js');
    process.exit(1);
  }
  
  // Build mapping of URLs to actual file paths
  console.log('📁 Building URL to file mapping...');
  const urlMapping = buildUrlToFileMapping(DOCS_DIR);
  console.log(`   Found ${Object.keys(urlMapping).length} doc files\n`);
  
  const links = extractLinksFromLlmsTxt(LLMS_FILE);
  console.log(`📊 Found ${links.length} internal links to validate\n`);
  
  const brokenLinks = [];
  const validLinks = [];
  
  for (const { title, url } of links) {
    // Normalize URL by removing trailing slashes
    const normalizedUrl = url.replace(/\/+$/, '');
    
    // Check if URL exists in mapping
    if (urlMapping[normalizedUrl]) {
      validLinks.push({ title, url, file: urlMapping[normalizedUrl] });
    } else {
      brokenLinks.push({ title, url });
    }
  }
  
  // Report results
  console.log(`✅ Valid links: ${validLinks.length}`);
  console.log(`❌ Broken links: ${brokenLinks.length}\n`);
  
  if (brokenLinks.length > 0) {
    console.error('🚨 The following links are broken:\n');
    
    brokenLinks.forEach(({ title, url }) => {
      console.error(`   📄 ${title}`);
      console.error(`      ${url}`);
      console.error('');
    });
    
    console.error('💡 Fix these issues by:');
    console.error('   1. Ensuring the docs files exist');
    console.error('   2. Regenerating llms.txt: node scripts/generate-llms-txt.js\n');
    
    process.exit(1);
  }
  
  console.log('✨ All links are valid!');
  process.exit(0);
}

// Run validation
validateLinks();

