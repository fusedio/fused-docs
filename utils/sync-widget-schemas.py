"""
Sync widget JSON schemas from the application repo to fused-docs.

The application repo generates schemas with:
    bun run client/scripts/generate-json-ui-schemas.ts

Then run this script to pull them into docs:
    python utils/sync-widget-schemas.py [/path/to/application]

If the path is omitted, defaults to ../../application relative to fused-docs root.
"""

import sys
import shutil
from pathlib import Path


def main() -> None:
    docs_root = Path(__file__).parent.parent

    if len(sys.argv) > 1:
        app_repo = Path(sys.argv[1]).resolve()
    else:
        app_repo = (docs_root.parent / "application").resolve()

    src_dir = app_repo / "server" / "server" / "json_ui_schemas" / "schema"
    dst_dir = docs_root / "static" / "widget-schema"

    if not src_dir.exists():
        print(f"error: source directory not found: {src_dir}", file=sys.stderr)
        print(
            "  Run 'bun run client/scripts/generate-json-ui-schemas.ts' in the application repo first.",
            file=sys.stderr,
        )
        sys.exit(1)

    dst_dir.mkdir(parents=True, exist_ok=True)

    count = 0
    for src_file in sorted(src_dir.glob("*.json")):
        dst_file = dst_dir / src_file.name
        shutil.copy2(src_file, dst_file)
        print(f"  synced {src_file.name}")
        count += 1

    print(f"\nDone. {count} schemas copied to {dst_dir.relative_to(docs_root)}")
    print("\nNext: npm run build  (to verify the updated schemas render correctly)")


if __name__ == "__main__":
    main()
