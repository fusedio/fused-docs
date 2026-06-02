# /// script
# requires-python = ">=3.11"
# dependencies = ["pytest", "pytest-markdown-docs", "fused[all]"]
# ///
#
# Tier 2: execute the runnable Python blocks in the docs via
# pytest-markdown-docs.
#
# Runs in CI (the `execution-check` job) over the full docs/ tree. Pass file
# paths to scope a local run; with no args it runs all of docs/ (minus
# generated / credential-gated paths).
#
# Execution is local: conftest.py defaults fused.run (and direct UDF calls) to
# engine="local", and auto-skips any block that needs external context — data
# files/URLs, cloud storage, a database, the network, or a live Fused
# catalog/account call. So only self-contained, pure-compute blocks run, which
# keeps the suite fast and needs no authentication.
#
# Skip a single block explicitly by putting "# doctest: skip" on its first line
# (same convention as Tier 1).

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
    targets = _select(argv)
    if not targets:
        print("Tier 2: no changed runnable docs to execute.")
        return 0

    # Self-contained blocks run offline, so login is optional. A logged-in
    # session only matters for blocks that opt into remote execution; without
    # one they fail fast rather than hanging (conftest sets no_login).
    if not CREDENTIALS.is_file():
        print(
            "Tier 2: no fused session found — run `fused login` if a block "
            "needs remote execution. Running self-contained blocks locally."
        )

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
