# /// script
# requires-python = ">=3.11"
# dependencies = [
#   "fused",
#   "griffe ~= 1.7",
#   "griffe2md @ https://github.com/jorisvandenbossche/griffe2md/archive/refs/heads/parameter-type-description.zip",
#   "black",
# ]
# ///
#
# Use as `uv run utils/generate_reference_docs.py` in the root of this repo

from pathlib import Path

import griffe
from griffe2md.rendering import default_config
from griffe2md.main import render_object_docs


ROOT = Path(__file__).parent / ".."

# We assume `fused` is installed in the env where we run this script (when running 
# with `uv run`, this will be the latest released fused which uv installs in an isolated env)
mod = griffe.load("fused", docstring_parser="google")

# updated options
default_config["show_signature_annotations"] = True
default_config["show_root_full_path"] = True
default_config["show_root_members_full_path"] = False
default_config["show_object_full_path"] = True

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
]

result = """\
---
sidebar_label: fused.api
title: fused.api
toc_max_heading_level: 5
---

"""

mod_api = mod["api"]

# fused.api functions

for obj in api_listing:
    docstring = render_object_docs(mod_api[obj], default_config)
    result += docstring + "\n\n"

# fused.api.FusedAPI class

methods = [
    "create_udf_access_token",
    "upload",
    "start_job",
    "get_jobs",
    "get_status",
    "get_logs",
    "tail_logs",
    "wait_for_job",
    "cancel_job",
    "auth_token",
]
config = dict(default_config)
config["filters"] = ["__init__"]
# config["members"] = methods
# config["members_order"] = "source"
config["summary"] = False
docstring = render_object_docs(mod_api["FusedAPI"], config)
result += docstring + "\n\n"

# `default_config["show_root_members_full_path"] = False` does not seem to work for the
# FusedAPI methods, so add them manually with root_full_path set to False
config["heading_level"] = default_config["heading_level"] + 1
config["show_root_full_path"] = False

for meth in methods:
    docstring = render_object_docs(mod_api["FusedAPI"][meth], config)
    result += docstring + "\n\n"

with open(ROOT / "docs" / "python-sdk" / "api-reference" / "api.mdx", "w") as f:
    f.write(result)
