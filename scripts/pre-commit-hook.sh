#!/bin/bash
# Pre-commit hook to validate llms.txt links
# To install: cp scripts/pre-commit-hook.sh .git/hooks/pre-commit && chmod +x .git/hooks/pre-commit

echo "🔍 Running pre-commit checks..."

# Check if llms.txt has been modified or if any docs have been modified
DOCS_CHANGED=$(git diff --cached --name-only | grep -E '^docs/.*\.(mdx?|md)$')
LLMS_CHANGED=$(git diff --cached --name-only | grep 'static/llms.txt')

if [ -n "$DOCS_CHANGED" ] || [ -n "$LLMS_CHANGED" ]; then
  echo "📝 Documentation files changed, validating llms.txt..."
  
  # Regenerate llms.txt if docs were changed
  if [ -n "$DOCS_CHANGED" ]; then
    echo "🔄 Regenerating llms.txt..."
    node scripts/generate-llms-txt.js
    
    # Stage the updated llms files
    git add static/llms.txt static/llms-full.txt
  fi
  
  # Validate links
  echo "✅ Validating links..."
  node scripts/validate-llms-links.js
  
  if [ $? -ne 0 ]; then
    echo "❌ Link validation failed!"
    echo "💡 Fix the broken links or regenerate llms.txt with: npm run generate-llms"
    exit 1
  fi
  
  echo "✅ All links are valid!"
else
  echo "📄 No documentation changes detected, skipping validation"
fi

echo "✨ Pre-commit checks passed!"
exit 0

