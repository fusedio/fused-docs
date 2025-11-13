# Documentation Translation

This script translates Fused documentation to multiple languages using OpenAI GPT-4o.

## Setup

1. Install dependencies:
```bash
pip install openai python-dotenv
```

2. Set your OpenAI API key (choose one method):

**Option A: Using .env file (recommended)**
```bash
# Create .env file in project root
echo "OPENAI_API_KEY=your-actual-key-here" > .env
```

**Option B: Environment variable**
```bash
export OPENAI_API_KEY='your-api-key-here'
```

## Usage

### Translate documentation (default)

```bash
# French (uses gpt-4o-mini by default)
python scripts/translate_docs.py --lang fr

# Spanish
python scripts/translate_docs.py --lang es

# Japanese
python scripts/translate_docs.py --lang ja
```

### Use different model

```bash
# Use GPT-4o for higher quality (more expensive)
python scripts/translate_docs.py --lang fr --model gpt-4o

# Use GPT-4o-mini for lower cost (default, still very good)
python scripts/translate_docs.py --lang fr --model gpt-4o-mini
```

### Translate blog posts too

```bash
# Docs + blog
python scripts/translate_docs.py --lang fr --content-type all

# Only blog posts
python scripts/translate_docs.py --lang fr --content-type blog
```

### Force retranslation of existing files

```bash
python scripts/translate_docs.py --lang fr --force
```

## Output Structure

Translations are saved to:
- **Docs**: `i18n/{locale}/docusaurus-plugin-content-docs/current/`
- **Blog**: `i18n/{locale}/docusaurus-plugin-content-blog/`

## Preview Translations

```bash
# Start dev server with French translations
npm run start -- --locale fr

# Start with Spanish
npm run start -- --locale es

# Start with Japanese  
npm run start -- --locale ja
```

## Build with All Languages

```bash
npm run build
```

This will build all locales (en, fr, es, ja) for production.

## Pricing Comparison

**GPT-4o-mini** (default, recommended):
- Input: $0.15 per 1M tokens
- Output: $0.60 per 1M tokens
- **Cost: ~$0.001-0.003 per page** (~£0.001-0.002)
- **Total for all docs: ~£1-3 per language**

**GPT-4o** (premium quality):
- Input: $2.50 per 1M tokens
- Output: $10.00 per 1M tokens
- **Cost: ~$0.01-0.05 per page** (~£0.01-0.04)
- **Total for all docs: ~£10-15 per language**

**Recommendation**: Start with `gpt-4o-mini` - it's 15-20x cheaper and quality is excellent for documentation.

## Notes

- The script preserves all MDX syntax, code blocks, frontmatter, and technical terms
- Existing files are skipped by default (use `--force` to retranslate)
- Rate limiting: 0.5s delay between API calls to respect OpenAI limits
- Default: Translates docs only (not blog posts)

## What Gets Translated

✅ Natural language text content  
✅ Headers and descriptions  
✅ Tutorial instructions  

❌ Code blocks (preserved as-is)  
❌ Technical terms (Fused, UDF, Workbench, etc.)  
❌ URLs and file paths  
❌ MDX components and syntax  
❌ Frontmatter metadata

