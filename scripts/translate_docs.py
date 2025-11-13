#!/usr/bin/env python3
"""
Translate Fused documentation using OpenAI API.

Usage:
    python scripts/translate_docs.py --lang fr
    python scripts/translate_docs.py --lang es --content-type docs
    python scripts/translate_docs.py --lang ja --force  # Retranslate all files
    
    OPENAI_API_KEY environment variable must be set.
"""

import os
import sys
import argparse
from pathlib import Path
import time
from typing import Optional
from tqdm import tqdm

try:
    from openai import OpenAI
except ImportError:
    print("Error: OpenAI package not found. Install with: pip install openai")
    sys.exit(1)

# Try to load .env file if python-dotenv is available
try:
    from dotenv import load_dotenv
    load_dotenv()  # Load .env from project root
except ImportError:
    pass  # python-dotenv not installed, will use environment variables directly


# Language configurations
LANGUAGES = {
    'fr': 'French',
    'es': 'Spanish', 
    'ja': 'Japanese'
}

# Docusaurus i18n paths
I18N_DOCS_PATH = "i18n/{locale}/docusaurus-plugin-content-docs/current"
I18N_BLOG_PATH = "i18n/{locale}/docusaurus-plugin-content-blog"


def get_translation_prompt(content: str, target_language: str) -> str:
    """Generate the translation prompt for OpenAI."""
    return f"""Translate this Docusaurus MDX documentation to {target_language}.

CRITICAL RULES:
1. Keep ALL frontmatter (content between ---) UNCHANGED
2. Keep ALL code blocks unchanged (content between ``` or indented code)
3. Keep ALL MDX component syntax unchanged (e.g., <LazyReactPlayer>, <Tabs>, etc.)
4. Keep ALL URLs and links unchanged
5. Keep ALL technical terms like "Fused", "UDF", "Workbench", "bounds", "geopandas" untranslated
6. Keep ALL file paths and command line examples unchanged
7. Only translate the natural language text content
8. Preserve all markdown formatting (headers, lists, bold, italic, etc.)
9. Keep the same structure and line breaks

Content to translate:

{content}

Return ONLY the translated content, nothing else."""


def translate_file(
    client: OpenAI,
    source_path: Path,
    target_path: Path,
    target_language: str,
    model: str = 'gpt-4o-mini',
    force: bool = False
) -> bool:
    """Translate a single MDX file."""
    
    # Check if already translated
    if target_path.exists() and not force:
        print(f"  ⏭️  Skipping (already exists): {target_path}")
        return False
    
    # Read source content
    try:
        with open(source_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"  ❌ Error reading {source_path}: {e}")
        return False
    
    # Skip if file is too small (likely empty or just frontmatter)
    if len(content.strip()) < 50:
        print(f"  ⏭️  Skipping (too small): {source_path}")
        return False
    
    print(f"  🔄 Translating: {source_path} -> {target_path}")
    
    # Translate with OpenAI
    try:
        prompt = get_translation_prompt(content, LANGUAGES[target_language])
        
        response = client.chat.completions.create(
            model=model,
            messages=[
                {
                    "role": "system",
                    "content": "You are a technical documentation translator. You preserve all code, technical syntax, and formatting while translating natural language text."
                },
                {
                    "role": "user", 
                    "content": prompt
                }
            ],
            temperature=0.3,  # Lower temperature for more consistent translations
        )
        
        translated_content = response.choices[0].message.content
        
        # Ensure target directory exists
        target_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Write translated content
        with open(target_path, 'w', encoding='utf-8') as f:
            f.write(translated_content)
        
        print(f"  ✅ Translated successfully")
        return True
        
    except Exception as e:
        print(f"  ❌ Error translating {source_path}: {e}")
        return False


def translate_directory(
    client: OpenAI,
    source_dir: Path,
    target_dir: Path,
    target_language: str,
    model: str = 'gpt-4o-mini',
    force: bool = False,
    extensions: tuple = ('.mdx', '.md')
) -> tuple[int, int]:
    """Translate all MDX/MD files in a directory recursively."""
    
    translated_count = 0
    skipped_count = 0
    
    # Find all MDX/MD files first to show progress
    all_files = [
        f for f in source_dir.rglob('*') 
        if f.is_file() and f.suffix in extensions
    ]
    
    # Progress bar
    with tqdm(total=len(all_files), desc="Translating", unit="file") as pbar:
        for source_file in all_files:
            # Calculate relative path and target path
            rel_path = source_file.relative_to(source_dir)
            target_file = target_dir / rel_path
            
            # Update progress bar description with current file
            pbar.set_description(f"Translating {rel_path}")
            
            # Translate
            if translate_file(client, source_file, target_file, target_language, model, force):
                translated_count += 1
                pbar.set_postfix({"translated": translated_count, "skipped": skipped_count})
                # Rate limiting - be nice to OpenAI API
                time.sleep(0.5)
            else:
                skipped_count += 1
                pbar.set_postfix({"translated": translated_count, "skipped": skipped_count})
            
            pbar.update(1)
    
    return translated_count, skipped_count


def main():
    parser = argparse.ArgumentParser(
        description='Translate Fused documentation using OpenAI'
    )
    parser.add_argument(
        '--lang',
        required=True,
        choices=list(LANGUAGES.keys()),
        help='Target language code (fr, es, ja)'
    )
    parser.add_argument(
        '--content-type',
        choices=['docs', 'blog', 'all'],
        default='docs',
        help='What to translate (default: docs)'
    )
    parser.add_argument(
        '--model',
        choices=['gpt-4o', 'gpt-4o-mini'],
        default='gpt-4o-mini',
        help='OpenAI model to use (default: gpt-4o-mini, cheaper and good quality)'
    )
    parser.add_argument(
        '--force',
        action='store_true',
        help='Retranslate existing files'
    )
    parser.add_argument(
        '--file',
        type=str,
        help='Translate a single file (relative to docs/ or blog/). Example: --file index.mdx'
    )
    
    args = parser.parse_args()
    
    # Check for OpenAI API key
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        print("❌ Error: OPENAI_API_KEY environment variable not set")
        print("   Set it with: export OPENAI_API_KEY='your-key-here'")
        sys.exit(1)
    
    # Initialize OpenAI client
    client = OpenAI(api_key=api_key)
    
    # Get workspace root (parent of scripts/)
    workspace_root = Path(__file__).parent.parent
    
    print(f"\n🌍 Starting translation to {LANGUAGES[args.lang]} ({args.lang})")
    print(f"📁 Workspace: {workspace_root}")
    print(f"🤖 Model: {args.model}")
    print(f"{'🔄 Force mode: ON' if args.force else '⏭️  Skipping existing files'}\n")
    
    total_translated = 0
    total_skipped = 0
    
    # Handle single file translation
    if args.file:
        print(f"📄 Translating single file: {args.file}")
        
        # Determine if it's a docs or blog file
        source_file = workspace_root / "docs" / args.file
        if not source_file.exists():
            source_file = workspace_root / "blog" / args.file
        
        if not source_file.exists():
            print(f"❌ Error: File not found: {args.file}")
            print(f"   Looked in: docs/{args.file} and blog/{args.file}")
            sys.exit(1)
        
        # Determine target path
        if "docs" in str(source_file.relative_to(workspace_root)):
            rel_path = source_file.relative_to(workspace_root / "docs")
            target_file = workspace_root / I18N_DOCS_PATH.format(locale=args.lang) / rel_path
        else:
            rel_path = source_file.relative_to(workspace_root / "blog")
            target_file = workspace_root / I18N_BLOG_PATH.format(locale=args.lang) / rel_path
        
        # Translate single file
        if translate_file(client, source_file, target_file, args.lang, args.model, args.force):
            print(f"✅ Successfully translated to: {target_file}")
        else:
            print(f"⏭️  File skipped or error occurred")
        
        return
    
    # Translate docs
    if args.content_type in ['docs', 'all']:
        print("📚 Translating documentation...")
        docs_source = workspace_root / "docs"
        docs_target = workspace_root / I18N_DOCS_PATH.format(locale=args.lang)
        
        translated, skipped = translate_directory(
            client, docs_source, docs_target, args.lang, args.model, args.force
        )
        total_translated += translated
        total_skipped += skipped
        print(f"   Docs: {translated} translated, {skipped} skipped\n")
    
    # Translate blog
    if args.content_type in ['blog', 'all']:
        print("📝 Translating blog posts...")
        blog_source = workspace_root / "blog"
        blog_target = workspace_root / I18N_BLOG_PATH.format(locale=args.lang)
        
        translated, skipped = translate_directory(
            client, blog_source, blog_target, args.lang, args.model, args.force
        )
        total_translated += translated
        total_skipped += skipped
        print(f"   Blog: {translated} translated, {skipped} skipped\n")
    
    # Summary
    print("=" * 60)
    print(f"✨ Translation complete!")
    print(f"   Total translated: {total_translated}")
    print(f"   Total skipped: {total_skipped}")
    print(f"\n💡 View your translations:")
    print(f"   npm run start -- --locale {args.lang}")
    print("=" * 60)


if __name__ == '__main__':
    main()

