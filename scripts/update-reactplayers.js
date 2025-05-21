const fs = require('fs');
const path = require('path');
const glob = require('glob');

// Find specific MDX files in the May 20, 2025 blog posts
const mdxFiles = [
  'blog/2025-05-20-launching-fused-apps/index.mdx',
  'blog/2025-05-20-inside-fused-apps/index.mdx'
];

let totalReplacements = 0;
const updatedFiles = [];

mdxFiles.forEach(filePath => {
  const fullPath = path.resolve(filePath);
  let content = fs.readFileSync(fullPath, 'utf8');
  
  // Skip if file doesn't contain ReactPlayer
  if (!content.includes('<ReactPlayer')) {
    return;
  }

  // Check if LazyReactPlayer is already imported
  const hasLazyImport = content.includes("import LazyReactPlayer");
  
  // Add the import if not present and there's a ReactPlayer import
  if (!hasLazyImport && content.includes("import ReactPlayer")) {
    content = content.replace(
      "import ReactPlayer from 'react-player'",
      "import ReactPlayer from 'react-player'\nimport LazyReactPlayer from '@site/src/components/LazyReactPlayer'"
    );
  }
  
  // Replace ReactPlayer with LazyReactPlayer
  let replacementCount = 0;
  
  // Replace ReactPlayer instances
  content = content.replace(/<ReactPlayer([^>]*)>/g, (match, attrs) => {
    // Remove any playing attribute as it's handled by LazyReactPlayer
    attrs = attrs.replace(/playing={[^}]*}/g, '');
    replacementCount++;
    return `<LazyReactPlayer${attrs}>`;
  });
  
  // Replace closing tags
  content = content.replace(/<\/ReactPlayer>/g, '</LazyReactPlayer>');
  
  if (replacementCount > 0) {
    fs.writeFileSync(fullPath, content, 'utf8');
    updatedFiles.push({ path: filePath, count: replacementCount });
    totalReplacements += replacementCount;
  }
});

console.log(`Updated ${totalReplacements} ReactPlayer components in ${updatedFiles.length} files`);
console.log('Updated files:');
updatedFiles.forEach(file => {
  console.log(`- ${file.path} (${file.count} replacements)`);
}); 