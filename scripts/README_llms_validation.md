# LLMS.txt Generation & Validation

This directory contains scripts to generate and validate the `llms.txt` file for the documentation site.

## 📁 Files

- **`generate-llms-txt.js`** - Generates llms.txt from the docs directory
- **`validate-llms-links.js`** - Validates all links in llms.txt to prevent 404s
- **`pre-commit-hook.sh`** - Optional git pre-commit hook for automatic validation

## 🚀 Quick Start

### Generate llms.txt

```bash
# Generate both curated and full versions
npm run generate-llms

# Or generate separately
npm run generate-llms-curated  # Just the curated version
npm run generate-llms-full      # Just the full version
```

### Validate Links

```bash
# Validate all links in llms.txt
npm run validate-llms
```

## 🔧 Build Integration

The validation is automatically integrated into the build process:

```bash
# Build will fail if any links are broken
npm run build
```

The build process:
1. Generates llms.txt files
2. Validates all internal links
3. Builds the documentation site

If any links are broken, the build will fail with a detailed error message.

## 🪝 Pre-commit Hook (Optional)

To automatically validate links before each commit:

### Install the Hook

```bash
# Copy the hook to .git/hooks
cp scripts/pre-commit-hook.sh .git/hooks/pre-commit

# Make it executable
chmod +x .git/hooks/pre-commit
```

### How It Works

The pre-commit hook will:
1. Check if any documentation files were modified
2. Regenerate llms.txt if docs changed
3. Validate all links
4. Prevent commit if validation fails

You can skip the hook if needed:
```bash
git commit --no-verify
```

## 📊 Validation Output

### Success
```
🔍 Validating links in llms.txt...
📁 Building URL to file mapping...
   Found 88 doc files
📊 Found 83 internal links to validate
✅ Valid links: 83
❌ Broken links: 0
✨ All links are valid!
```

### Failure
```
🔍 Validating links in llms.txt...
📁 Building URL to file mapping...
   Found 88 doc files
📊 Found 83 internal links to validate
✅ Valid links: 81
❌ Broken links: 2

🚨 The following links are broken:

   📄 Load & Export Data
      https://docs.fused.io/tutorials/load-export-data/
      
💡 Fix these issues by:
   1. Ensuring the docs files exist
   2. Regenerating llms.txt: npm run generate-llms
```

## 🔍 How Validation Works

The validation script:
1. Walks through the `docs/` directory
2. Builds a mapping of URLs to actual file paths
3. Extracts all internal links from `llms.txt`
4. Verifies each link maps to an existing file
5. Reports any broken links with their URLs

### URL Normalization

The script handles various file naming conventions:
- Spaces → dashes (`Geospatial with Fused` → `geospatial-with-fused`)
- Underscores → dashes (`load_and_save_data.mdx` → `load-and-save-data`)
- Case insensitive matching
- Trailing slash normalization

## 🛠️ Troubleshooting

### "Broken links found"

If you see broken links:

1. **Check if the file exists**
   ```bash
   # Look for the file in docs/
   find docs -name "*filename*"
   ```

2. **Regenerate llms.txt**
   ```bash
   npm run generate-llms
   npm run validate-llms
   ```

3. **Fix the file path**
   - Ensure the file is not in a hidden directory (starting with `_`)
   - Check that the file extension is `.mdx` or `.md`
   - Verify the file is not marked as `unlisted: true` in frontmatter

### "gray-matter not found"

Install dependencies:
```bash
npm install
```

### Pre-commit Hook Not Running

Make sure the hook is executable:
```bash
chmod +x .git/hooks/pre-commit
```

## 📝 Customization

### Modify URL Generation

Edit `generate-llms-txt.js` to change how URLs are generated:

```javascript
const urlPath = relativePath
  .replace(/\\/g, '/') // Convert Windows paths
  .replace(/\.mdx?$/, '') // Remove file extension
  .replace(/\/index$/, '') // Remove /index
  .replace(/_/g, '-') // Convert underscores to hyphens
  .replace(/\s+/g, '-') // Convert spaces to hyphens
  .toLowerCase(); // Convert to lowercase
```

### Add More Sections

Edit the `SECTIONS` object in `generate-llms-txt.js`:

```javascript
const SECTIONS = {
  'Core Concepts': 'core-concepts',
  'Tutorials': 'tutorials', 
  'Python SDK': 'python-sdk',
  'Workbench': 'workbench',
  'Your Section': 'your-section-path'
};
```

## 🔄 Workflow Integration

### GitHub Actions

Add to your CI/CD pipeline:

```yaml
- name: Validate Documentation Links
  run: |
    npm run generate-llms
    npm run validate-llms
```

### Local Development

Regenerate and validate after making doc changes:

```bash
# After editing docs
npm run generate-llms && npm run validate-llms
```

## 📚 Related Scripts

- `generate-llms-txt.js` - Main generation script
- `validate-llms-links.js` - Link validation script
- `update-reactplayers.js` - Updates ReactPlayer components
- `fetch_notion_docs_tickets.py` - Fetches Notion tickets

## 🎯 Best Practices

1. **Run validation before committing**
   - Use the pre-commit hook or run manually
   
2. **Regenerate after structural changes**
   - Moving files
   - Renaming files
   - Adding new sections

3. **Check validation in CI/CD**
   - Prevent broken links from being deployed
   
4. **Keep URLs stable**
   - Avoid breaking existing links
   - Use redirects for moved content

