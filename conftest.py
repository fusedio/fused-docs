"""
pytest-markdown-docs configuration (Tier 2 doc-snippet execution tests).

Blocks are collected from docs/ and run as pytest tests.
Add '# doctest: skip' as the first line of a block to exclude it from execution.

Run locally only when authenticated with fused — unauthenticated local runs
cause fused to open browser OAuth windows. In headless CI this is not an issue.
"""


def pytest_markdown_docs_globals():
    """Inject fused into every code block's global scope.

    Most doc blocks assume fused is already in scope (e.g. @fused.udf)
    without an explicit 'import fused' at the top.
    """
    import fused

    class _MockSecrets:
        def __getitem__(self, key: str) -> str:
            return f"<test:{key}>"

        def get(self, key: str, default=None):
            return default

    fused.secrets = _MockSecrets()  # type: ignore[assignment]
    return {"fused": fused}
