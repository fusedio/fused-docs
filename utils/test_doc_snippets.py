# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///
#
# Tier 1: syntax-check every Python code block in the docs.
#
# Used as a pre-commit hook (staged file paths passed as args)
# and as a standalone CI check (no args → all of docs/).
#
# Skip a block by putting "# doctest: skip" on its first line.
#
# Usage:
#   uv run utils/test_doc_snippets.py                      # all docs
#   uv run utils/test_doc_snippets.py docs/guide/foo.mdx   # specific files

import ast
import re
import sys
import textwrap
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DOCS_DIR = ROOT / "docs"

# Generated files — never hand-edited, skip them
SKIP_DIRS = frozenset([
    ROOT / "docs" / "python-sdk" / "api-reference",
])
# Generated files at a specific path (not a directory)
SKIP_FILES = frozenset([
    ROOT / "docs" / "python-sdk" / "top-level-functions.mdx",
])

# Match ```python ... ``` fences; the fence info line may have extras
# (showLineNumbers, title="...", {1-3}, etc.)
_FENCE_RE = re.compile(
    r"^```python[^\n]*\n(.*?)^```",
    re.MULTILINE | re.DOTALL,
)


def _is_excluded(path: Path) -> bool:
    resolved = path.resolve()
    if resolved in SKIP_FILES:
        return True
    return any(str(resolved).startswith(str(d)) for d in SKIP_DIRS)


def _collect(paths: list[Path]) -> list[Path]:
    out: list[Path] = []
    for p in paths:
        if p.is_dir():
            for ext in ("*.mdx", "*.md"):
                out.extend(p.rglob(ext))
        elif p.suffix in {".mdx", ".md"}:
            out.append(p)
    return [f for f in out if not _is_excluded(f)]


def _extract_blocks(source: str) -> list[tuple[int, str]]:
    """Return (fence_start_line, code) for each Python block."""
    return [
        (source[: m.start()].count("\n") + 1, m.group(1))
        for m in _FENCE_RE.finditer(source)
    ]


def _check_file(path: Path) -> list[str]:
    errors: list[str] = []
    source = path.read_text(encoding="utf-8")
    for fence_line, code in _extract_blocks(source):
        first = code.lstrip().splitlines()[0] if code.strip() else ""
        if "doctest: skip" in first:
            continue
        try:
            ast.parse(textwrap.dedent(code))
        except SyntaxError as e:
            rel = path.relative_to(ROOT)
            err_line = fence_line + (e.lineno or 1)
            errors.append(
                f"{rel}:{err_line}: SyntaxError: {e.msg}\n"
                f"    {(e.text or '').rstrip()}"
            )
    return errors


def main(argv: list[str]) -> int:
    targets = [Path(a) for a in argv] if argv else [DOCS_DIR]
    files = _collect(targets)

    if not files:
        print("No .mdx/.md files to check.")
        return 0

    all_errors: list[str] = []
    files_with_blocks = 0
    total_blocks = 0

    for f in sorted(files):
        source = f.read_text(encoding="utf-8")
        blocks = _extract_blocks(source)
        if blocks:
            files_with_blocks += 1
            total_blocks += len(blocks)
        all_errors.extend(_check_file(f))

    if all_errors:
        print(f"Syntax errors found ({len(all_errors)} issue(s)):\n")
        for err in all_errors:
            print(f"  {err}\n")
        print(
            "To skip a block that is intentionally not valid Python, "
            "add '# doctest: skip' as its first line."
        )
        return 1

    print(
        f"PASSED — {total_blocks} Python block(s) across "
        f"{files_with_blocks} file(s) are syntax-valid"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
