# /// script
# requires-python = ">=3.11"
# dependencies = [
#   "fused",
#   "griffe",
#   "griffe2md",
# ]
# ///
#
# Use as `python utils/generate_reference_docs.py` in the root of this repo

from pathlib import Path

import griffe
from griffe2md.rendering import default_config
from griffe2md.main import render_object_docs


mod = griffe.load("fused")#, docstring_parser="google")


## Top-level API page

api_listing = [
    "udf",
    "cache",
    "load",
    "run",
    "submit",
    "download",
    "ingest",
    "file_path",
    "get_chunks_metadata",
    "get_chunk_from_table",
]

result = """\
---
sidebar_label: Top-Level Functions
title: Top-Level Functions
toc_max_heading_level: 4
---

"""

for obj in api_listing:
    # result += f"## fused.{obj}\n\n"
    docstring = render_object_docs(mod[obj], default_config)
    result += docstring + "\n\n"


result = result.replace("## fused.udf", "## @fused.udf")
result = result.replace("## fused.cache", "## @fused.cache")


with open(Path(__file__).parent / ".." / "docs" / "python-sdk" / "top-level-functions.mdx", "w") as f:
    f.write(result)
