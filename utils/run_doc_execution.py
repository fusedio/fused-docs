# /// script
# requires-python = ">=3.11"
# dependencies = ["pytest", "pytest-markdown-docs", "fused"]
# ///
#
# Tier 2: execute the runnable Python blocks in changed docs via
# pytest-markdown-docs, using the developer's local fused session.
#
# Runs as a pre-commit hook (changed file paths passed as args). With no
# args it runs the full docs/ tree (minus generated / credential-gated paths).
#
# Requires an active fused login (~/.fused/credentials). If not logged in it
# fails fast and asks you to run `fused login` — so a block never triggers a
# browser OAuth popup mid-run.
#
# Skip a block by putting "# doctest: skip" on its first line (handled by
# conftest.py, same convention as Tier 1).

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DOCS_DIR = ROOT / "docs"
CREDENTIALS = Path.home() / ".fused" / "credentials"

# Generated or credential-gated — never executed.
IGNORE_PREFIXES = (
    "docs/python-sdk/api-reference/",
    "docs/workbench/integrations/",
)
IGNORE_FILES = ("docs/python-sdk/top-level-functions.mdx",)


def _login_error() -> int:
    print(
        "\nFused is not logged in — no credentials found at:\n"
        f"  {CREDENTIALS}\n\n"
        "Tier 2 executes the docs' code blocks against Fused servers, which needs\n"
        "an active session. Log in once, then retry your commit:\n\n"
        "  fused login\n",
        file=sys.stderr,
    )
    return 1


def _select(argv: list[str]) -> list[Path]:
    if not argv:
        return [DOCS_DIR]
    out: list[Path] = []
    for a in argv:
        p = Path(a)
        if p.suffix not in {".mdx", ".md"} or not p.exists():
            continue
        resolved = p.resolve()
        rel = (
            resolved.relative_to(ROOT).as_posix()
            if resolved.is_relative_to(ROOT)
            else p.as_posix()
        )
        if rel in IGNORE_FILES or rel.startswith(IGNORE_PREFIXES):
            continue
        out.append(p)
    return out


def main(argv: list[str]) -> int:
    if not CREDENTIALS.is_file():
        return _login_error()

    targets = _select(argv)
    if not targets:
        print("Tier 2: no changed runnable docs to execute.")
        return 0

    import pytest

    args = ["--markdown-docs", "-q", "--tb=short"]
    if targets == [DOCS_DIR]:
        args += [
            "--ignore=docs/python-sdk/api-reference",
            "--ignore=docs/python-sdk/top-level-functions.mdx",
            "--ignore=docs/workbench/integrations",
        ]
    args += [str(t) for t in targets]

    code = int(pytest.main(args))
    # Exit code 5 = "no tests collected" (a changed file had no runnable
    # blocks) — that's a pass, not a failure.
    return 0 if code == 5 else code


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
