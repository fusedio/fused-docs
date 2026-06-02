"""
pytest-markdown-docs configuration (Tier 2 doc-snippet execution tests).

Blocks are collected from docs/ and run as pytest tests. Tier 2 runs as a local
pre-commit hook (`doc-snippet-execution`), not in CI.

Execution is local and fast: this file defaults fused.run (and direct UDF calls)
to engine="local" so UDFs run in-process with no auth, and auto-skips any block
that needs external context (data files/URLs, cloud storage, a database, the
network, or a live Fused catalog/account call) — see `_DATA_DEPENDENT`. Only
self-contained, pure-compute blocks actually run, so the full suite finishes in
a few seconds.

To exclude a single block explicitly, put '# doctest: skip' on its first line
(also honored by Tier 1's syntax check). To run a block that reuses names from
the block above it, add `{/* pmd-metadata: continuation */}` directly above its
fence (pytest-markdown-docs prepends the previous block's source).
"""

import re
import socket

import pytest

# A doc block that makes a network call should never hang the run forever.
socket.setdefaulttimeout(30)

# Tier 2 only executes self-contained blocks locally. A block that needs
# external context — data files/URLs, cloud storage, a database, the network,
# or a live Fused catalog/account call — is auto-skipped: it can't run locally
# without that context, and running it would be slow and flaky. This keeps the
# full suite fast (only pure-compute blocks run) and is applied centrally so no
# doc file needs editing and any future block is covered automatically.
_DATA_DEPENDENT = re.compile(
    r"""(?x)
      \bfused\.run\(\s*['"]        # run a catalog UDF by name (remote load)
    | \bfused\.(load|submit|ingest|get|list|delete|upload|download)\b
    | \bfused\.api\.               # account/server calls (whoami, log, ...)
    | \brun_remote\b
    | s3://|gs://|gcs://|az://|abfs://|ftp://|https?://
    | read_parquet|read_csv|read_json|read_feather|read_excel|read_file
    | (gpd|geopandas|pd|pandas|xr|xarray)\.(read_|open)
    | rioxarray|rasterio\.open|open_dataset
    | \bopen\(|/mnt/|/mount/|fsspec|s3fs|gcsfs|boto3
    | requests\.(get|post|put|delete|head)|urlopen|urllib|httpx|aiohttp
    | duckdb|\.sql\(|psycopg|sqlalchemy|snowflake|bigquery|\.connect\(
    | micropip|pyodide|\bawait\b|\bjs\.
    | \blogout\b|fused\.secrets|secrets\.set\b
    """
)


def pytest_markdown_docs_globals():
    """Inject fused into every code block's global scope.

    Most doc blocks assume fused is already in scope (e.g. @fused.udf)
    without an explicit 'import fused' at the top.
    """
    try:
        import fused
    except ImportError as exc:
        raise ImportError(
            "conftest.py: 'fused' is required for Tier 2 doc tests. "
            "Install with: uv run --with fused pytest --markdown-docs docs/\n"
            f"Original error: {exc}"
        ) from exc

    # Prevent doc blocks that access fused.secrets from raising KeyErrors
    # or requiring real credentials during testing.
    class _MockSecrets:
        def __getitem__(self, key: str) -> str:
            return f"<test:{key}>"

        def __setitem__(self, key: str, value: str) -> None:
            pass

        def __delitem__(self, key: str) -> None:
            pass

        def __contains__(self, key: str) -> bool:
            return True

        def get(self, key: str, default=None) -> str:
            return f"<test:{key}>"

    fused.secrets = _MockSecrets()  # type: ignore[assignment]

    # Never open a browser OAuth flow mid-run. When logged in, fused uses the
    # on-disk credentials; when logged out, auth-requiring blocks fail fast
    # instead of popping a browser.
    fused.options.no_login = True  # type: ignore[attr-defined]

    # Default execution to local: the UDF body runs in-process instead of being
    # shipped to Fused servers — fast and no auth needed for self-contained UDFs.
    # This covers both fused.run(udf) and a direct call udf(); the latter routes
    # through fused.run with engine=None (its default), so we treat an unset OR
    # None engine as local. A block that asks for a specific engine/instance
    # type (remote, "small", ...) keeps its choice.
    _orig_run = fused.run

    def _run(*args, **kwargs):
        if kwargs.get("engine") is None and not kwargs.get("instance_type"):
            kwargs["engine"] = "local"
        return _orig_run(*args, **kwargs)

    fused.run = _run  # type: ignore[assignment]

    # Neutralize destructive session ops so executing a doc block can't log the
    # developer out (fused.api.logout() deletes ~/.fused/credentials).
    fused.api.logout = lambda *a, **k: None  # type: ignore[assignment]

    return {"fused": fused}


def pytest_collection_modifyitems(items: list) -> None:
    """Skip blocks whose first content line contains '# doctest: skip'.

    pytest-markdown-docs' native skip mechanism uses 'notest' in the fence
    info line. This hook makes '# doctest: skip' inside the block body work
    for Tier 2 as well, keeping the convention consistent with Tier 1.
    """
    skip = pytest.mark.skip(reason="doctest: skip")
    skip_data = pytest.mark.skip(reason="data-dependent (auto)")
    for item in items:
        code = getattr(item, "code", "") or ""
        lines = [ln for ln in code.splitlines() if ln.strip()]
        first = lines[0] if lines else ""
        if first.lstrip().startswith("#") and "doctest: skip" in first:
            item.add_marker(skip)
        elif _DATA_DEPENDENT.search(code):
            item.add_marker(skip_data)
