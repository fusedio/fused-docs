const fs = require('fs');
const path = require('path');
const matter = require('gray-matter');

// Configuration
const DOCS_DIR = 'docs';
const OUTPUT_FILE = 'static/llms.txt';
const FULL_OUTPUT_FILE = 'static/llms-full.txt';
const BASE_URL = 'https://docs.fused.io';

// Main sections to include
const SECTIONS = {
  'Core Concepts': 'core-concepts',
  'Geospatial with Fused': 'tutorials/Geospatial with Fused',
  'Python SDK': 'python-sdk'
};

function extractFrontmatter(filePath, isFullVersion = false) {
  try {
    const content = fs.readFileSync(filePath, 'utf8');
    const { data, content: body } = matter(content);
    
    const description = isFullVersion 
      ? extractLongDescription(body)
      : (data.description || extractFirstParagraph(body));
    
    return { 
      title: data.title || path.basename(filePath, '.mdx'),
      description,
      unlisted: data.unlisted || false,
      draft: data.draft || false, // Check if page is draft
      fullContent: body,
      frontmatter: data,
      id: data.id || data.slug || null // Extract id or slug from frontmatter
    };
  } catch (error) {
    return { title: path.basename(filePath, '.mdx'), description: '', unlisted: false, draft: false, fullContent: '', frontmatter: {}, id: null };
  }
}

function extractFirstParagraph(content) {
  // Remove markdown syntax and get first meaningful paragraph
  const cleaned = content
    .replace(/```[\s\S]*?```/g, '') // Remove code blocks
    .replace(/<!--[\s\S]*?-->/g, '') // Remove comments
    .replace(/import\s+.*?from\s+['"].*?['"];?\s*/g, '') // Remove import statements
    .replace(/export\s+.*?;?\s*/g, '') // Remove export statements
    .replace(/^#{1,6}\s+.*/gm, '') // Remove headers
    .replace(/^\s*[-*+]\s+.*/gm, '') // Remove list items
    .replace(/!\[.*?\]\(.*?\)/g, '') // Remove images
    .replace(/\[([^\]]+)\]\([^)]+\)/g, '$1') // Replace links with text
    .split('\n')
    .filter(line => line.trim().length > 0)
    .find(line => line.length > 20);
  
  return cleaned ? cleaned.substring(0, 150) + '...' : '';
}

function extractLongDescription(content) {
  // Extract longer, more detailed description for full version
  const cleaned = content
    .replace(/```[\s\S]*?```/g, '') // Remove code blocks
    .replace(/<!--[\s\S]*?-->/g, '') // Remove comments
    .replace(/import\s+.*?from\s+['"].*?['"];?\s*/g, '') // Remove import statements
    .replace(/export\s+.*?;?\s*/g, '') // Remove export statements
    .replace(/^#{1,6}\s+.*/gm, '') // Remove headers
    .replace(/!\[.*?\]\(.*?\)/g, '') // Remove images
    .replace(/\[([^\]]+)\]\([^)]+\)/g, '$1') // Replace links with text
    .split('\n')
    .filter(line => line.trim().length > 0)
    .slice(0, 5) // Take first 5 meaningful lines
    .join(' ')
    .replace(/\s+/g, ' ');
  
  return cleaned ? cleaned.substring(0, 500) + '...' : '';
}

function cleanMarkdownForFullText(content) {
  // Clean markdown but preserve structure and code blocks for full text version
  return content
    .replace(/import\s+.*?from\s+['"].*?['"];?\s*\n/g, '') // Remove import statements
    .replace(/export\s+.*?;?\s*\n/g, '') // Remove export statements
    .replace(/<!--[\s\S]*?-->/g, '') // Remove comments
    .replace(/^\s*<[^>]+>[\s\S]*?<\/[^>]+>\s*$/gm, '') // Remove JSX components
    .replace(/\{[^}]*\}/g, '') // Remove JSX expressions
    .replace(/^\s*import\s+.*$/gm, '') // Remove any remaining imports
    .replace(/:::.*?\n/g, '') // Remove docusaurus admonitions
    .replace(/!\[([^\]]*)\]\([^)]+\)/g, '[Image: $1]') // Replace images with text
    .replace(/\[([^\]]+)\]\([^)]+\)/g, '$1') // Replace links with text only
    .replace(/\n\s*\n\s*\n/g, '\n\n') // Remove excessive newlines
    .trim();
}

function simplifyPythonSignatures(content) {
  // Simplify Python function signatures to just name() -> ReturnType
  // This removes all the parameter details since they're documented separately
  return content.replace(
    /```python\n([a-zA-Z_][a-zA-Z0-9_.]*)\([^)]*(?:\n[^`]*)*?\) -> ([^\n]+)\n```/g,
    (match, funcName, returnType) => {
      return `\`\`\`\n${funcName}() -> ${returnType}\n\`\`\``;
    }
  ).replace(
    /```python\n([a-zA-Z_][a-zA-Z0-9_.]*)\([^)]*(?:\n[^`]*)*?\)\n```/g,
    (match, funcName) => {
      return `\`\`\`\n${funcName}()\n\`\`\``;
    }
  );
}

function ultraCompactFormat(content) {
  // Ultra-compact format: `func()` -> Description\nParams:\n- param (type)\nReturns: type
  
  // First remove all the verbose markup
  content = content
    .replace(/<code>([^<]+)<\/code>/g, '$1')
    .replace(/\*\*/g, '')
    .replace(/:::note\n[\s\S]*?:::/g, '')
    .replace(/:::warning\n[\s\S]*?:::/g, '')
    .replace(/^## [a-zA-Z_][a-zA-Z0-9_.]*\n\n/gm, '');
  
  // Simplify Returns sections - extract just the type (do this early)
  content = content.replace(/Returns:\n\n- ([^–\n]+) –[^\n]*/g, 'Returns: $1');
  content = content.replace(/Returns:\n\n- ([^\n]+)/g, 'Returns: $1');
  
  // Convert code block function signatures to inline format FIRST (before removing code blocks)
  content = content.replace(
    /```\n([a-zA-Z_][a-zA-Z0-9_.()]*(?:\s*->\s*[^\n]+)?)\n```\n\n([^\n]+(?:\n[^\n]+)?)\n\nParameters:\n/g,
    '`$1` - $2\nParams:\n'
  );
  
  // Handle functions without parameters
  content = content.replace(
    /```\n([a-zA-Z_][a-zA-Z0-9_.()]*(?:\s*->\s*[^\n]+)?)\n```\n\n([^\n]+)/g,
    '`$1` - $2'
  );
  
  // NOW remove Examples sections (after preserving function signatures)
  content = content.replace(/Examples:\n\n```\n[^`]*\n```\n\n/g, '');
  content = content.replace(/Examples:\n\n[^\n]*\n\n/g, '');
  content = content.replace(/Examples:\n\n/g, '');
  
  // Remove ALL remaining multi-line code blocks (examples, verbose signatures, etc.)
  // This catches ```python showLineNumbers and other variants
  content = content.replace(/```[\s\S]*?```\n*/g, '');
  
  // Remove standalone code block markers that might remain
  content = content.replace(/```[a-z ]*\n/g, '');
  content = content.replace(/```\n*/g, '');
  
  // Simplify parameter format: remove ALL descriptions, keep just name and type
  content = content.replace(/- ([a-zA-Z_][a-zA-Z0-9_]*) \(([^)]+)\)[\s\S]*?(?=\n-|\nReturns:|\n`|\n\n|$)/g, (match, name, type) => {
    // If there's a newline after, it's a multi-line description - remove it all
    return `- ${name} (${type})\n`;
  });
  
  // Change "Parameters:" and "Arguments:" to "Params:"
  content = content.replace(/Parameters:/g, 'Params:');
  content = content.replace(/Arguments:/g, 'Params:');
  
  // Remove "Other Parameters:" header
  content = content.replace(/Other Parameters:\n/g, '');
  
  // Remove ## function headers (with backticks like ## `run_file`)
  content = content.replace(/^## `[a-zA-Z_][a-zA-Z0-9_]*`\n\n/gm, '');
  
  // Remove verbose parameter format: - `param` _type_ - description
  content = content.replace(/- `([a-zA-Z_][a-zA-Z0-9_]*)` _([^_]+)_ -[^\n]*/g, '- $1 ($2)');
  
  // Remove standalone Returns: sections with verbose descriptions
  content = content.replace(/Returns:\n\n  [^\n]+\n\n/g, '');
  
  // Remove Raises sections
  content = content.replace(/Raises:\n[\s\S]*?(?=\n\n`|\n\n###|$)/g, '');
  
  // Remove any leftover --- lines
  content = content.replace(/\n---\n\n/g, '\n\n');
  content = content.replace(/`[^`]+` - ---/g, '');
  
  // Compress whitespace
  content = content.replace(/\n\n\n+/g, '\n\n');
  content = content.replace(/\n\nParams:\n\n/g, '\nParams:\n');
  
  return content.trim();
}

function walkDirectory(dir, basePath = '', isFullVersion = false, excludeDirs = []) {
  const items = [];
  
  try {
    const entries = fs.readdirSync(dir, { withFileTypes: true });
    
    for (const entry of entries) {
      const fullPath = path.join(dir, entry.name);
      const relativePath = path.join(basePath, entry.name);
      
      if (entry.isDirectory()) {
        // For full version, include hidden directories (but mark them)
        if (!isFullVersion && entry.name.startsWith('_')) continue;
        
        // Skip excluded directories (to avoid duplication)
        if (excludeDirs.includes(entry.name)) continue;
        
        // Recursively process subdirectories
        items.push(...walkDirectory(fullPath, relativePath, isFullVersion, excludeDirs));
      } else if (entry.name.endsWith('.mdx') || entry.name.endsWith('.md')) {
        // For full version, include hidden files
        if (!isFullVersion && entry.name.startsWith('_')) continue;
        
        const frontmatter = extractFrontmatter(fullPath, isFullVersion);
        
        // Skip unlisted and draft content
        if (!isFullVersion && (frontmatter.unlisted || frontmatter.draft)) continue;
        
        // Docusaurus URL generation rules:
        // 1. For index.mdx files with an ID, the URL is just the parent directory
        // 2. For index.mdx files without an ID, the URL is also just the parent directory
        // 3. For regular files with an ID, use the ID
        // 4. For regular files without an ID, use the filename (lowercase, _ to -)
        // 5. Directory names preserve case and spaces are URL encoded
        
        const parts = relativePath.replace(/\\/g, '/').split('/');
        const filename = parts[parts.length - 1];
        const isIndexFile = filename.replace(/\.mdx?$/, '').toLowerCase() === 'index';
        
        let urlParts;
        if (isIndexFile) {
          // For index files, just use the directory path (frontmatter ID doesn't add to path)
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
        
        items.push({
          title: frontmatter.title,
          description: frontmatter.description,
          url: `${BASE_URL}/${urlPath}`,
          path: relativePath,
          unlisted: frontmatter.unlisted,
          fullContent: frontmatter.fullContent,
          frontmatter: frontmatter.frontmatter
        });
      }
    }
  } catch (error) {
    console.warn(`Warning: Could not read directory ${dir}:`, error.message);
  }
  
  return items;
}

function generateLlmsTxt(isFullVersion = false) {
  const outputFile = isFullVersion ? FULL_OUTPUT_FILE : OUTPUT_FILE;
  const versionLabel = isFullVersion ? 'FULL' : 'curated';
  
  console.log(`🤖 Generating ${versionLabel} llms.txt...`);
  
  if (isFullVersion) {
    // Generate comprehensive full-text version
    let content = `# Fused Documentation - Complete Reference

> Fused is an end-to-end cloud platform for data analytics, built around User Defined Functions (UDFs): Python functions that can be run via HTTPS requests from anywhere, without any install required.

This comprehensive reference contains the complete text of all Fused documentation, including all API methods, examples, tutorials, and guides.

================================================================================

`;

    // Process each main section
    for (const [sectionTitle, sectionPath] of Object.entries(SECTIONS)) {
      const sectionDir = path.join(DOCS_DIR, sectionPath);
      
      if (!fs.existsSync(sectionDir)) {
        console.warn(`Warning: Section directory ${sectionDir} not found`);
        continue;
      }
      
      // Exclude "Geospatial with Fused" from Tutorials since it's its own section
      const excludeDirs = sectionPath === 'tutorials' ? ['Geospatial with Fused'] : [];
      const items = walkDirectory(sectionDir, sectionPath, isFullVersion, excludeDirs);
      
      if (items.length === 0) continue;
      
      content += `# ${sectionTitle.toUpperCase()}\n\n`;
      
      // Sort items by path for consistent ordering
      items.sort((a, b) => a.path.localeCompare(b.path));
      
      items.forEach(item => {
        content += `## ${item.title}\n`;
        content += `Path: ${item.path}\n`;
        if (item.unlisted) content += `Status: UNLISTED\n`;
        content += `URL: ${item.url}\n\n`;
        
        if (item.fullContent) {
          const cleanedContent = cleanMarkdownForFullText(item.fullContent);
          if (cleanedContent.length > 50) {
            content += `${cleanedContent}\n\n`;
          }
        }
        
        content += `${'='.repeat(80)}\n\n`;
      });
    }
    
    // Add blog content if it exists
    const blogDir = 'blog';
    if (fs.existsSync(blogDir)) {
      content += `# BLOG POSTS\n\n`;
      
      const blogItems = walkDirectory(blogDir, 'blog', true);
      blogItems.sort((a, b) => b.path.localeCompare(a.path)); // Reverse chronological
      
      blogItems.forEach(item => {
        content += `## ${item.title}\n`;
        content += `Path: ${item.path}\n`;
        content += `URL: ${item.url}\n\n`;
        
        if (item.fullContent) {
          const cleanedContent = cleanMarkdownForFullText(item.fullContent);
          if (cleanedContent.length > 50) {
            content += `${cleanedContent}\n\n`;
          }
        }
        
        content += `${'='.repeat(80)}\n\n`;
      });
    }
    
    content += `\n---\n\nGenerated automatically from Fused documentation. Last updated: ${new Date().toISOString().split('T')[0]}\nTotal sections: ${Object.keys(SECTIONS).length}\n`;
    
    // Write the file
    fs.writeFileSync(outputFile, content, 'utf8');
    const totalSections = content.split('='.repeat(80)).length - 1;
    console.log(`✅ Generated full-text llms.txt with ${totalSections} complete sections`);
    console.log(`📝 File saved to: ${outputFile}`);
    console.log(`📊 File size: ${Math.round(content.length / 1024)} KB`);
    
    return totalSections;
    
  } else {
    // Generate curated link version (existing logic)
    let content = `# Fused Documentation

> Fused is an end-to-end cloud platform for data analytics, built around User Defined Functions (UDFs): Python functions that can be run via HTTPS requests from anywhere, without any install required.

`;

    // Process each main section
    for (const [sectionTitle, sectionPath] of Object.entries(SECTIONS)) {
      const sectionDir = path.join(DOCS_DIR, sectionPath);
      
      if (!fs.existsSync(sectionDir)) {
        console.warn(`Warning: Section directory ${sectionDir} not found`);
        continue;
      }
      
      // Exclude "Geospatial with Fused" from Tutorials since it's its own section
      const excludeDirs = sectionPath === 'tutorials' ? ['Geospatial with Fused'] : [];
      const items = walkDirectory(sectionDir, sectionPath, isFullVersion, excludeDirs);
      
      if (items.length === 0) continue;
      
      content += `## ${sectionTitle}\n\n`;
      
      // Sort items by path for consistent ordering
      items.sort((a, b) => a.path.localeCompare(b.path));
      
      // Regular version - simple list
      const topLevel = items.filter(item => !item.path.includes('/') || item.path.split('/').length === 2);
      const nested = items.filter(item => item.path.split('/').length > 2);
      
      // Filter out index pages
      [...topLevel, ...nested].filter(item => item.title.toLowerCase() !== 'index').forEach(item => {
        content += `- [${item.title}](${item.url})`;
        if (item.description) {
          content += ` - ${item.description}`;
        }
        content += '\n';
      });
      
      content += '\n';
    }
    
    // Add quick start links
    content += `## Quick Start

- [Installation & Setup](${BASE_URL}/quickstart) - Get started with Fused in minutes

---

Generated automatically from Fused documentation. Last updated: ${new Date().toISOString().split('T')[0]}
`;

    // Write the file
    fs.writeFileSync(outputFile, content, 'utf8');
    const linkCount = content.split('\n').filter(line => line.includes('](http')).length;
    console.log(`✅ Generated curated llms.txt with ${linkCount} links`);
    console.log(`📝 File saved to: ${outputFile}`);
    
    return linkCount;
  }
}

// Add gray-matter dependency check
try {
  require.resolve('gray-matter');
} catch (error) {
  console.error('❌ Missing dependency: gray-matter');
  console.log('📦 Install with: npm install gray-matter');
  process.exit(1);
}

function generatePythonSdkTxt() {
  console.log('🐍 Generating Python SDK llms.txt...');
  
  const outputFile = 'static/llms-python-sdk.txt';
  const sdkDir = path.join(DOCS_DIR, 'python-sdk');
  
  if (!fs.existsSync(sdkDir)) {
    console.error(`❌ Error: Python SDK directory not found at ${sdkDir}`);
    return 0;
  }
  
  let content = `# Fused Python SDK Documentation

> Complete reference for the Fused Python SDK - a Python library for creating and running User Defined Functions (UDFs) that can be executed via HTTPS requests.

## Python SDK Reference

`;

  // Walk the python-sdk directory and include everything
  const items = walkDirectory(sdkDir, 'python-sdk', true, []); // Use full version mode
  
  // Filter out changelog.mdx
  const filteredItems = items.filter(item => !item.path.includes('changelog.mdx'));
  
  // Sort items by path
  filteredItems.sort((a, b) => a.path.localeCompare(b.path));
  
  filteredItems.forEach(item => {
    content += `### ${item.title}\n\n`;
    
    if (item.fullContent) {
      let cleanedContent = cleanMarkdownForFullText(item.fullContent);
      // Simplify Python function signatures to reduce verbosity
      cleanedContent = simplifyPythonSignatures(cleanedContent);
      // Apply ultra-compact formatting to minimize tokens
      cleanedContent = ultraCompactFormat(cleanedContent);
      if (cleanedContent.length > 50) {
        content += `${cleanedContent}\n\n`;
      }
    }
    
    content += `---\n\n`;
  });
  
  content += `\n---\n\nGenerated automatically from Fused Python SDK documentation. Last updated: ${new Date().toISOString().split('T')[0]}\nTotal pages: ${filteredItems.length}\n`;
  
  // Write the file
  fs.writeFileSync(outputFile, content, 'utf8');
  console.log(`✅ Generated Python SDK llms.txt with ${filteredItems.length} pages`);
  console.log(`📝 File saved to: ${outputFile}`);
  console.log(`📊 File size: ${Math.round(content.length / 1024)} KB`);
  
  return filteredItems.length;
}

// Handle command line arguments
const args = process.argv.slice(2);
const curatedOnly = args.includes('--curated');
const fullOnly = args.includes('--full');
const pythonSdkOnly = args.includes('--python-sdk');

if (curatedOnly) {
  const curatedLinks = generateLlmsTxt(false);
  console.log(`📊 Generated curated version with ${curatedLinks} links`);
} else if (fullOnly) {
  const fullLinks = generateLlmsTxt(true);
  console.log(`📊 Generated full version with ${fullLinks} complete sections`);
} else if (pythonSdkOnly) {
  const sdkPages = generatePythonSdkTxt();
  console.log(`📊 Generated Python SDK version with ${sdkPages} pages`);
} else {
  // Generate all versions by default
  const curatedLinks = generateLlmsTxt(false);
  const fullLinks = generateLlmsTxt(true);
  const sdkPages = generatePythonSdkTxt();
  
  console.log(`\n📊 Summary:`);
  console.log(`   Curated version: ${curatedLinks} links`);
  console.log(`   Full version: ${fullLinks} complete sections`);
  console.log(`   Python SDK version: ${sdkPages} pages`);
} 