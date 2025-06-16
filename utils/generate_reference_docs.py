# /// script
# requires-python = ">=3.11"
# dependencies = [
#   "fused",
#   "griffe",
#   "griffe2md",
# ]
# ///
#
# Use as `uv run utils/generate_reference_docs.py` in the root of this repo

from pathlib import Path

import griffe
from griffe2md.rendering import default_config
from griffe2md.main import render_object_docs


ROOT = Path(__file__).parent / ".."


mod = griffe.load("fused", docstring_parser="google")

# updated options
default_config["show_signature_annotations"] = True


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


# some post-processing
result = result.replace("## fused.udf", "## @fused.udf")
result = result.replace("## fused.cache", "## @fused.cache")


with open(ROOT / "docs" / "python-sdk" / "top-level-functions.mdx", "w") as f:
    f.write(result)



## `fused.api` page

api_listing = [
    "whoami",
    "delete",
    "list",
    "get",
    "download",
    "upload",
    "sign_url",
    "sign_url_prefix",
    "get_udfs",
    "job_get_logs",
    "job_print_logs",
    "job_tail_logs",
    "job_get_status",
    "job_cancel",
    "job_get_exec_time",
    "job_wait_for_job",
    "FusedAPI",
]

result = """\
---
sidebar_label: fused.api
title: fused.api
toc_max_heading_level: 5
---

"""

mod_api = mod["api"]

for obj in api_listing:
    # result += f"## fused.{obj}\n\n"
    docstring = render_object_docs(mod_api[obj], default_config)
    result += docstring + "\n\n"


with open(ROOT / "docs" / "python-sdk" / "api-reference" / "api.mdx", "w") as f:
    f.write(result)
