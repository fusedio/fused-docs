"""
pytest-markdown-docs configuration (Tier 2 doc-snippet execution tests).

Blocks are collected from docs/ and run as pytest tests.
Add '# doctest: skip' as the first line of a block to exclude it from
both Tier 1 (syntax check) and Tier 2 (execution).

Run locally only when authenticated with fused — unauthenticated local runs
cause fused to open browser OAuth windows. In headless CI, auth errors surface
as test failures rather than OAuth popups — this is why the CI step uses
continue-on-error while the suite is being stabilized.
"""

import pytest


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
    return {"fused": fused}


def pytest_collection_modifyitems(items: list) -> None:
    """Skip blocks whose first content line contains '# doctest: skip'.

    pytest-markdown-docs' native skip mechanism uses 'notest' in the fence
    info line. This hook makes '# doctest: skip' inside the block body work
    for Tier 2 as well, keeping the convention consistent with Tier 1.
    """
    skip = pytest.mark.skip(reason="doctest: skip")
    for item in items:
        td = getattr(item, "test_definition", None)
        if td is None:
            continue
        code = getattr(td, "code", "") or ""
        lines = [ln for ln in code.splitlines() if ln.strip()]
        first = lines[0] if lines else ""
        if first.lstrip().startswith("#") and "doctest: skip" in first:
            item.add_marker(skip)
