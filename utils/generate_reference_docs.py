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


import fused
print(f"Generating reference docs for fused version {fused.__version__}")


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

run_remote_addition = """
#### `job.run_remote`

```python showLineNumbers
def run_remote(output_table: Optional[str] = ...,
    instance_type: Optional[WHITELISTED_INSTANCE_TYPES] = None,
    *,
    region: str | None = None,
    disk_size_gb: int | None = None,
    additional_env: List[str] | None = None,
    image_name: Optional[str] = None,
    ignore_no_udf: bool = False,
    ignore_no_output: bool = False,
    validate_imports: Optional[bool] = None,
    validate_inputs: bool = True,
    overwrite: Optional[bool] = None) -> RunResponse
```

Begin execution of the ingestion job by calling `run_remote` on the job object.

**Arguments**:

- `output_table` - The name of the table to write to. Defaults to None.
- `instance_type` - The AWS EC2 instance type to use for the job. Acceptable strings are `m5.large`, `m5.xlarge`, `m5.2xlarge`, `m5.4xlarge`, `m5.8xlarge`, `m5.12xlarge`, `m5.16xlarge`, `r5.large`, `r5.xlarge`, `r5.2xlarge`, `r5.4xlarge`, `r5.8xlarge`, `r5.12xlarge`, or `r5.16xlarge`. Defaults to None.
- `region` - The AWS region in which to run. Defaults to None.
- `disk_size_gb` - The disk size to specify for the job. Defaults to None.
- `additional_env` - Any additional environment variables to be passed into the job. Defaults to None.
- `image_name` - Custom image name to run. Defaults to None for default image.
- `ignore_no_udf` - Ignore validation errors about not specifying a UDF. Defaults to False.
- `ignore_no_output` - Ignore validation errors about not specifying output location. Defaults to False.

#### Monitor and manage job

Calling `run_remote` returns a `RunResponse` object with helper methods.

```python showLineNumbers
# Declare ingest job
job = fused.ingest(
  input="https://www2.census.gov/geo/tiger/TIGER_RD18/STATE/06_CALIFORNIA/06/tl_rd22_06_bg.zip",
  output="s3://fused-sample/census/ca_bg_2022/main/"
)

# Start ingest job
job_id = job.run_remote()
```

Fetch the job status.

```python showLineNumbers
job_id.get_status()
```

Fetch and print the job's logs.

```python showLineNumbers
job_id.print_logs()
```

Determine the job's execution time.

```python showLineNumbers
job_id.get_exec_time()
```

Continuously print the job's logs.

```python showLineNumbers
job_id.tail_logs()
```

Cancel the job.

```python showLineNumbers
job_id.cancel()
```

---

"""

for obj in api_listing:
    docstring = render_object_docs(mod[obj], default_config)
    result += docstring + "\n---\n\n"
    if obj == "ingest":
        # TODO run_remote does not yet have a proper docstring to include automatically
        result += run_remote_addition


# some post-processing
result = result.replace("## fused.udf", "## @fused.udf")
result = result.replace("## fused.cache", "## @fused.cache")
# griffe cannot handl the x, y, z multiple parameters on one line
result = result.replace("**x,** (<code>y, z</code>)", "**x, y, z** (<code>int</code>)")

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
    result += docstring + "\n---\n\n"

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
result += docstring + "\n---\n\n"

# `default_config["show_root_members_full_path"] = False` does not seem to work for the
# FusedAPI methods, so add them manually with root_full_path set to False
config["heading_level"] = default_config["heading_level"] + 1
config["show_root_full_path"] = False

for meth in methods:
    docstring = render_object_docs(mod_api["FusedAPI"][meth], config)
    result += docstring + "\n---\n\n"

with open(ROOT / "docs" / "python-sdk" / "api-reference" / "api.mdx", "w") as f:
    f.write(result)


## `fused.options` page

result = """\
---
sidebar_label: fused.options
title: fused.options
toc_max_heading_level: 5
---

"""

config = dict(default_config)
docstring = render_object_docs(mod["options"], default_config)
# setting config["show_signature"] to False does not seem to work for this case, so remove it manually
docstring = docstring.replace("""
```python
options = _load_options()
```
""", "")
result += docstring + "\n\n"

config = dict(default_config)
config["summary"] = False
config["show_bases"] = False
config["show_root_full_path"] = False
config["show_root_members_full_path"] = False
config["show_object_full_path"] = False
config["members_order"] = "source"
config["filters"] = ["!model_config"]
docstring = render_object_docs(mod["_options"]["Options"], config)
result += docstring

with open(ROOT / "docs" / "python-sdk" / "api-reference" / "options.mdx", "w") as f:
    f.write(result)


## `JobPool` page

result = """\
---
sidebar_label: JobPool
title: JobPool
toc_max_heading_level: 5
---

"""

result += """\
## JobPool

The `JobPool` class is used to manage, inspect and retrieve results from
submitted jobs from [`fused.submit()`](/python-sdk/top-level-functions/#fusedsubmit).

"""

# listing and rendering the methods separately to avoid including the JobPool 
# class signature and docstring (which is not public -> use submit() to get this object)
import fused
methods = [key for key in fused._submit.JobPool.__dict__.keys() if not key.startswith("_")]

config = dict(default_config)
config["heading_level"] = default_config["heading_level"] + 1
config["show_root_full_path"] = False

for meth in methods:
    docstring = render_object_docs(mod["_submit"]["JobPool"][meth], config)
    result += docstring + "\n---\n\n"

with open(ROOT / "docs" / "python-sdk" / "api-reference" / "jobpool.mdx", "w") as f:
    f.write(result)
