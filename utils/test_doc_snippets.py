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

# Match ```python ... ``` fences at any indentation level (column 0, inside
# <Tabs>, blockquotes, etc.). The `indent` group captures leading whitespace
# on the opening fence and is backreferenced on the closing fence so indented
# fences are paired correctly. The fence info line may carry extras like
# showLineNumbers, title="...", or {1-3}.
_FENCE_RE = re.compile(
    r"^(?P<indent>[ \t]*)```python[^\n]*\n(.*?)^(?P=indent)```",
    re.MULTILINE | re.DOTALL,
)


def _is_excluded(path: Path) -> bool:
    resolved = path.resolve()
    if resolved in SKIP_FILES:
        return True
    return any(resolved.is_relative_to(d) for d in SKIP_DIRS)


def _collect(paths: list[Path]) -> list[Path]:
    out: list[Path] = []
    for p in paths:
        if not p.exists():
            print(f"WARNING: path does not exist, skipping: {p}", file=sys.stderr)
            continue
        if p.is_dir():
            for ext in ("*.mdx", "*.md"):
                out.extend(p.rglob(ext))
        elif p.suffix in {".mdx", ".md"}:
            out.append(p)
    return [f for f in out if not _is_excluded(f)]


def _extract_blocks(source: str) -> list[tuple[int, str]]:
    """Return (opening_fence_line, code) for each Python block.

    opening_fence_line is the 1-based line number of the ```python line itself
    (not the first line of the code body). _check_file computes the error line
    as opening_fence_line + e.lineno, which is only correct because of this.
    """
    return [
        (source[: m.start()].count("\n") + 1, m.group(2))
        for m in _FENCE_RE.finditer(source)
    ]


def _check_file(path: Path, source: str) -> tuple[list[str], int, int]:
    """Return (errors, blocks_checked, blocks_skipped) for one file."""
    errors: list[str] = []
    checked = skipped = 0
    for fence_line, code in _extract_blocks(source):
        lines = [ln for ln in code.splitlines() if ln.strip()]
        first = lines[0] if lines else ""
        if first.lstrip().startswith("#") and "doctest: skip" in first:
            skipped += 1
            continue
        checked += 1
        try:
            ast.parse(textwrap.dedent(code))
        except (SyntaxError, ValueError) as e:
            rel = path.relative_to(ROOT)
            err_line = fence_line + (getattr(e, "lineno", None) or 1)
            errors.append(
                f"{rel}:{err_line}: {type(e).__name__}: {getattr(e, 'msg', str(e))}\n"
                f"    {(getattr(e, 'text', None) or '').rstrip()}"
            )
    return errors, checked, skipped


def main(argv: list[str]) -> int:
    is_precommit = bool(argv)
    targets = [Path(a) for a in argv] if argv else [DOCS_DIR]
    files = _collect(targets)

    if not files:
        if is_precommit:
            # Empty staged set is normal — nothing to check.
            print("No .mdx/.md files to check.")
            return 0
        # Standalone (CI) run: docs/ must always contain files.
        print(
            f"ERROR: No .mdx/.md files found under {DOCS_DIR}. "
            "Check that the directory exists and is not entirely excluded.",
            file=sys.stderr,
        )
        return 1

    all_errors: list[str] = []
    files_with_blocks = 0
    total_checked = 0
    total_skipped = 0

    for f in sorted(files):
        try:
            source = f.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError) as e:
            print(f"ERROR: could not read {f.relative_to(ROOT)}: {e}", file=sys.stderr)
            all_errors.append(str(e))
            continue
        errors, checked, skipped = _check_file(f, source)
        if checked + skipped > 0:
            files_with_blocks += 1
        total_checked += checked
        total_skipped += skipped
        all_errors.extend(errors)

    if all_errors:
        print(f"Syntax errors found ({len(all_errors)} issue(s)):\n")
        for err in all_errors:
            print(f"  {err}\n")
        print(
            "To skip a block that is intentionally not valid Python, "
            "add '# doctest: skip' as its first line."
        )
        return 1

    skip_note = f", {total_skipped} skipped" if total_skipped else ""
    print(
        f"PASSED — {total_checked} Python block(s) syntax-valid"
        f"{skip_note} across {files_with_blocks} file(s)"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
