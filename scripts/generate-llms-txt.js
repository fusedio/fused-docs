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
  'Tutorials': 'tutorials', 
  'Python SDK': 'python-sdk',
  'Workbench': 'workbench',
  'Use Cases': 'tutorials/Geospatial with Fused/geospatial-use-cases'
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
      fullContent: body,
      frontmatter: data
    };
  } catch (error) {
    return { title: path.basename(filePath, '.mdx'), description: '', unlisted: false, fullContent: '', frontmatter: {} };
  }
}

function extractFirstParagraph(content) {
  // Remove markdown syntax and get first meaningful paragraph
  const cleaned = content
    .replace(/```[\s\S]*?```/g, '') // Remove code blocks
    .replace(/<!--[\s\S]*?-->/g, '') // Remove comments
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

function walkDirectory(dir, basePath = '', isFullVersion = false) {
  const items = [];
  
  try {
    const entries = fs.readdirSync(dir, { withFileTypes: true });
    
    for (const entry of entries) {
      const fullPath = path.join(dir, entry.name);
      const relativePath = path.join(basePath, entry.name);
      
      if (entry.isDirectory()) {
        // For full version, include hidden directories (but mark them)
        if (!isFullVersion && entry.name.startsWith('_')) continue;
        
        // Recursively process subdirectories
        items.push(...walkDirectory(fullPath, relativePath, isFullVersion));
      } else if (entry.name.endsWith('.mdx') || entry.name.endsWith('.md')) {
        // For full version, include hidden files
        if (!isFullVersion && entry.name.startsWith('_')) continue;
        
        const frontmatter = extractFrontmatter(fullPath, isFullVersion);
        
        // For regular version, skip unlisted content
        if (!isFullVersion && frontmatter.unlisted) continue;
        
        const urlPath = relativePath
          .replace(/\\/g, '/') // Convert Windows paths
          .replace(/\.mdx?$/, '') // Remove file extension
          .replace(/\/index$/, ''); // Remove /index
        
        items.push({
          title: frontmatter.title,
          description: frontmatter.description,
          url: `${BASE_URL}/${urlPath}/`,
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

> Fused is an end-to-end cloud platform for data analytics, built around User Defined Functions (UDFs): Python functions that can be run via HTTP requests from anywhere, without any install required.

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
      
      const items = walkDirectory(sectionDir, sectionPath, isFullVersion);
      
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

> Fused is an end-to-end cloud platform for data analytics, built around User Defined Functions (UDFs): Python functions that can be run via HTTP requests from anywhere, without any install required.

## Core Concepts

Learn the fundamental concepts behind Fused's serverless geospatial platform.

`;

    // Process each main section
    for (const [sectionTitle, sectionPath] of Object.entries(SECTIONS)) {
      const sectionDir = path.join(DOCS_DIR, sectionPath);
      
      if (!fs.existsSync(sectionDir)) {
        console.warn(`Warning: Section directory ${sectionDir} not found`);
        continue;
      }
      
      const items = walkDirectory(sectionDir, sectionPath, isFullVersion);
      
      if (items.length === 0) continue;
      
      content += `## ${sectionTitle}\n\n`;
      
      // Sort items by path for consistent ordering
      items.sort((a, b) => a.path.localeCompare(b.path));
      
      // Regular version - simple list
      const topLevel = items.filter(item => !item.path.includes('/') || item.path.split('/').length === 2);
      const nested = items.filter(item => item.path.split('/').length > 2);
      
      [...topLevel, ...nested].forEach(item => {
        content += `- [${item.title}](${item.url})`;
        if (item.description) {
          content += ` - ${item.description}`;
        }
        content += '\n';
      });
      
      content += '\n';
    }
    
    // Add quick start and essential links
    content += `## Quick Start

- [Installation & Setup](${BASE_URL}/quickstart/) - Get started with Fused in minutes
- [Python SDK](${BASE_URL}/python-sdk/) - Install and use the Fused Python SDK
- [Workbench](${BASE_URL}/workbench/overview/) - Browser-based IDE for developing UDFs

## Examples & Use Cases

- [Load & Export Data](${BASE_URL}/tutorials/load-export-data/) - Learn to work with various data formats
- [Use Cases](${BASE_URL}/tutorials/Geospatial%20with%20Fused/geospatial-use-cases/) - Real-world applications and case studies

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

// Handle command line arguments
const args = process.argv.slice(2);
const curatedOnly = args.includes('--curated');
const fullOnly = args.includes('--full');

if (curatedOnly) {
  const curatedLinks = generateLlmsTxt(false);
  console.log(`📊 Generated curated version with ${curatedLinks} links`);
} else if (fullOnly) {
  const fullLinks = generateLlmsTxt(true);
  console.log(`📊 Generated full version with ${fullLinks} complete sections`);
} else {
  // Generate both versions by default
  const curatedLinks = generateLlmsTxt(false);
  const fullLinks = generateLlmsTxt(true);
  
  console.log(`\n📊 Summary:`);
  console.log(`   Curated version: ${curatedLinks} links`);
  console.log(`   Full version: ${fullLinks} complete sections`);
} 