"""Run this file to generate markdown files from fused-py docstrings for the Docusaurus documentation.

Currently needs manual intervention to copy the generated markdown files to the Docusaurus project.

Configure `pydoc-markdown.yml` and set the path to the base of `fused-py`.

Run with `python3 pydoc_docusaurus.py`

"""
from pydoc_markdown.main import RenderSession

print("start")

session = RenderSession(
    config="pydoc-markdown.yml",
    render_toc=None,
    search_path=(),
    modules=(),
    packages=(),
    py2=None,
)
session.render(session.load())

print("end")
