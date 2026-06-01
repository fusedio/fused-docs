# /// script
# requires-python = ">=3.11"
# dependencies = [
#   # replace with "fused @ /path/to/application/fused-py" for local development
#   "fused",
#   "griffe ~= 1.7",
#   "griffe2md @ https://github.com/jorisvandenbossche/griffe2md/archive/refs/heads/parameter-type-description.zip",
#   "black",
# ]
# ///
#
# Use as `uv run --reinstall-package fused utils/generate_reference_docs.py` in the root of this repo

import re
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


def escape_mdx_braces(text: str) -> str:
    """Escape {identifier} patterns in MDX prose to prevent JSX parse errors.

    Docstring path placeholders like {source_dir} are valid Python but MDX
    parses them as JSX expressions, crashing the Docusaurus build.
    Only escapes outside of code blocks.
    """
    parts = re.split(r"(```[\s\S]*?```|`[^`\n]*`)", text)
    return "".join(
        re.sub(r"\{([A-Za-z_]\w*)\}", r"\\{\1\\}", p) if i % 2 == 0 else p
        for i, p in enumerate(parts)
    )


def fix_kwargs_annotations(text: str) -> str:
    """Strip griffe's incorrectly-inferred type annotations from **kwargs parameters.

    griffe has a bug where it copies the annotation from the preceding parameter
    onto an unannotated **kwargs/**kw_parameters, e.g. producing ``**kwargs: bool``
    when the source has a bare ``**kwargs``.  Strip these inside code blocks.
    """
    def process_block(m: re.Match) -> str:
        return re.sub(r"(\*\*\w+): *[^\n]+", r"\1", m.group(0))

    return re.sub(r"```[\s\S]*?```", process_block, text)


def wrap_example_code_blocks(text: str) -> str:
    """Wrap content of <details class="example"> blocks in Python code fences.

    griffe2md renders Example sections as <details> blocks without code fences,
    causing MDX to parse Python f-strings as JSX expressions and crash the build.
    """
    def replacer(m: re.Match) -> str:
        attrs, summary, content = m.group(1), m.group(2), m.group(3).strip()
        if not content.startswith("```"):
            content = f"```python\n{content}\n```"
        return f"<details {attrs}>\n<summary>{summary}</summary>\n\n{content}\n\n</details>"

    return re.sub(
        r'<details (class="example"[^>]*)>\n<summary>(.*?)</summary>\n(.*?)\n</details>',
        replacer,
        text,
        flags=re.DOTALL,
    )


def process_content(text: str) -> str:
    """Apply all post-processing steps to rendered docstring content."""
    text = fix_kwargs_annotations(text)
    text = wrap_example_code_blocks(text)
    text = escape_mdx_braces(text)
    return text


## Individual top-level function pages
#
# Each function gets its own fused-{name}.mdx file matching the existing sidebar entries.
# Modules (context, types, secrets, user_secrets) are maintained manually.

TOP_LEVEL_FUNCTIONS = [
    "udf",
    "cache",
    "load",
    "load_async",
    "run",
    "run_async",
    "submit",
    "download",
    "ingest",
    "ingest_nongeospatial",
    "file_path",
    "find_dataset",
    "register_dataset",
    "get_chunk_from_table",
    "get_chunks_metadata",
]

# Override default "fused.{name}" display name
DISPLAY_NAMES = {
    "udf": "@fused.udf",
    "cache": "@fused.cache",
    "run": "fused.run [Legacy]",
    "run_async": "fused.run_async [Legacy]",
    "submit": "fused.submit [Legacy]",
}

# Custom MDX prepended before the auto-generated docstring
PREAMBLES = {
    "run": """\
:::warning
This function is deprecated and will be removed in a future version. Use [`udf()`](/python-sdk/api-reference/udf#udf) instead.

```python
udf(
    *args,
    engine=None,
    cache_max_age=None,
    cache=True,
    **kwargs
)
```
:::

""",
    "run_async": """\
:::warning
This function is deprecated and will be removed in a future version. Use [`udf.map_async()`](/python-sdk/api-reference/udf#map_async) instead.

```python
udf.map_async(
    arg_list,
    engine='remote',
    instance_type='realtime',
    max_workers=32,
    collect=True,
    cache_max_age=None,
)
```
:::

""",
    "submit": """\
:::warning
This function is deprecated and will be removed in a future version. Use [`udf.map()`](/python-sdk/api-reference/udf#map) instead.

```python
udf.map(
    arg_list,
    engine='remote',
    instance_type='realtime',
    max_workers=32,
    collect=True,
    cache_max_age=None,
)
```
:::

""",
}

# Custom MDX appended after the auto-generated docstring
POSTAMBLES = {
    "ingest": """
---

#### `job.run_batch`

```python showLineNumbers
def run_batch(output_table: Optional[str] = ...,
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

Begin execution of the ingestion job by calling `run_batch` on the job object.

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

Calling `run_batch` returns a `RunResponse` object with helper methods.

```python showLineNumbers
# Declare ingest job
job = fused.ingest(
  input="https://www2.census.gov/geo/tiger/TIGER_RD18/STATE/06_CALIFORNIA/06/tl_rd22_06_bg.zip",
  output="s3://fused-sample/census/ca_bg_2022/main/"
)

# Start ingest job
job_id = job.run_batch()
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

#### `job.run_remote`

Alias of `job.run_batch` for backwards compatibility. See `job.run_batch` above
for details.

---

""",
}

page_config = dict(default_config)
page_config["heading_level"] = 1
page_config["show_root_full_path"] = False

for func_name in TOP_LEVEL_FUNCTIONS:
    if func_name not in mod.members:
        print(f"Warning: {func_name} not found in fused module, skipping")
        continue

    display_name = DISPLAY_NAMES.get(func_name, f"fused.{func_name}")
    slug = func_name.replace("_", "-")
    doc_id = f"fused-{slug}"

    content = process_content(render_object_docs(mod[func_name], page_config))

    if func_name == "udf":
        content = content.replace("# udf", "# @fused.udf", 1)
    elif func_name == "cache":
        content = content.replace("# cache", "# @fused.cache", 1)
    # griffe cannot handle x, y, z multiple parameters on one line
    content = content.replace("**x,** (<code>y, z</code>)", "**x, y, z** (<code>int</code>)")

    preamble = PREAMBLES.get(func_name, "")
    postamble = POSTAMBLES.get(func_name, "")

    full_content = f"""\
---
id: {doc_id}
title: "{display_name}"
sidebar_label: "{display_name}"
---

{preamble}{content}{postamble}"""

    with open(ROOT / "docs" / "python-sdk" / "api-reference" / f"{doc_id}.mdx", "w", encoding="utf-8") as f:
        f.write(full_content)


## `fused.api` page

import fused.api as _fused_api

# Internal/infra items excluded from public docs
API_BLOCKLIST = {
    "_session_token",
    "FusedDockerAPI",
    "DriveFileSystem",
    "FdFileSystem",
    "NotebookCredentials",
    "AUTHORIZATION",
    "FusedAPI",  # rendered separately below
}

# These are public but not in __all__; always include them
_AUTH_SUPPLEMENT = ["access_token", "auth_scheme", "logout"]

# Known functions in preferred display order; auto-detection appends any new ones
_KNOWN_API_FUNCTIONS = [
    # Auth
    "whoami",
    *_AUTH_SUPPLEMENT,
    # File operations
    "delete",
    "list",
    "get",
    "download",
    "upload",
    "sign_url",
    "sign_url_prefix",
    "resolve",
    # UDFs / apps
    "get_udfs",
    "get_apps",
    # Jobs
    "job_get_logs",
    "job_print_logs",
    "job_tail_logs",
    "job_get_status",
    "job_cancel",
    "job_get_exec_time",
    "job_wait_for_job",
    "job_get_results",
    "job_wait_for_results",
    # Scheduling
    "schedule_udf",
    "schedule_list",
    # Utilities
    "session_token",
    "team_info",
    "enable_gcs",
    "log",
    # Integrations
    "snowflake_connect",
    "snowflake_query",
    "airtable_connect",
    "airtable_list_records",
    "huggingface_connect",
    "huggingface_inference",
    "hubspot_connect",
    "notion_connect",
    "modal_connect",
]

_known_set = set(_KNOWN_API_FUNCTIONS)
_auto_detected = [
    name for name in _fused_api.__all__
    if name not in API_BLOCKLIST
    and not (name.startswith("Fused") and name.endswith("Connection"))
    and name not in _known_set
]
if _auto_detected:
    print(f"Auto-detected new fused.api functions: {_auto_detected}")

api_listing = sorted(_KNOWN_API_FUNCTIONS + _auto_detected)

# Auto-detect Fused*Connection classes
connection_classes = [
    name for name in _fused_api.__all__
    if name.startswith("Fused") and name.endswith("Connection")
    and name not in API_BLOCKLIST
]

result = """\
---
sidebar_label: fused.api
title: fused.api
toc_max_heading_level: 5
sidebar_position: 2
---

## Module Functions

The following functions can be called directly from the `fused.api` module:

```python
import fused.api

fused.api.function_name()
```

---

"""

mod_api = mod["api"]

api_func_config = dict(default_config)
api_func_config["show_root_full_path"] = False

for obj in api_listing:
    if obj not in mod_api.members:
        print(f"Warning: {obj} not found in fused.api module, skipping")
        continue
    docstring = render_object_docs(mod_api[obj], api_func_config)
    result += process_content(docstring) + "\n---\n\n"

# fused.api.FusedAPI class

methods = sorted([
    "auth_token",
    "cancel_job",
    "create_udf_access_token",
    "get_jobs",
    "get_logs",
    "get_status",
    "start_job",
    "tail_logs",
    "upload",
    "wait_for_job",
])
config = dict(default_config)
config["filters"] = ["__init__"]
config["summary"] = False
config["show_root_full_path"] = False
docstring = render_object_docs(mod_api["FusedAPI"], config)

fusedapi_note = """\
## FusedAPI Class Methods

The following methods require creating a `FusedAPI` instance first:

```python
from fused.api import FusedAPI
api = FusedAPI()
api.method_name()
```

"""
result += fusedapi_note + process_content(docstring) + "\n---\n\n"

config["heading_level"] = default_config["heading_level"] + 1
config["show_root_full_path"] = False

for meth in methods:
    if meth not in mod_api["FusedAPI"].members:
        print(f"Warning: {meth} not found in FusedAPI class, skipping")
        continue
    docstring = render_object_docs(mod_api["FusedAPI"][meth], config)
    usage_note = f"""
**Usage:** `from fused.api import FusedAPI; api = FusedAPI(); api.{meth}()`
"""
    result += process_content(docstring) + "\n" + usage_note + "\n---\n\n"

# Auto-detected Fused*Connection classes

for class_name in connection_classes:
    if class_name not in mod_api.members:
        print(f"Warning: {class_name} not found in fused.api module, skipping")
        continue

    cls = getattr(_fused_api, class_name)
    cls_methods = sorted(name for name in cls.__dict__ if not name.startswith("_"))

    config_cls = dict(default_config)
    config_cls["filters"] = ["__init__"]
    config_cls["summary"] = False
    config_cls["show_root_full_path"] = False
    result += f"## {class_name}\n\n"
    result += process_content(render_object_docs(mod_api[class_name], config_cls)) + "\n---\n\n"

    config_cls["heading_level"] = default_config["heading_level"] + 1
    config_cls["show_root_full_path"] = False
    for meth in cls_methods:
        if meth not in mod_api[class_name].members:
            print(f"Warning: {meth} not found in {class_name} class, skipping")
            continue
        result += process_content(render_object_docs(mod_api[class_name][meth], config_cls)) + "\n---\n\n"

with open(ROOT / "docs" / "python-sdk" / "api-reference" / "api.mdx", "w", encoding="utf-8") as f:
    f.write(result)


## `fused.options` page

result = """\
---
sidebar_label: fused.options
title: fused.options
toc_max_heading_level: 5
sidebar_position: 4
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

with open(ROOT / "docs" / "python-sdk" / "api-reference" / "options.mdx", "w", encoding="utf-8") as f:
    f.write(result)


## `JobPool` page

result = """\
---
sidebar_label: JobPool
title: JobPool
toc_max_heading_level: 5
sidebar_position: 1
---

"""

result += """\
## JobPool

The `JobPool` class is used to manage, inspect and retrieve results from
submitted jobs from [`fused.submit()`](/python-sdk/api-reference/fused-submit).

"""

# Combine sync and async methods from both JobPool and AsyncJobPool
_sync_methods = set(
    key for key in fused._submit.JobPool.__dict__.keys() if not key.startswith("_")
)
_async_methods = set(
    key for key in fused._submit.AsyncJobPool.__dict__.keys() if not key.startswith("_")
)
methods = sorted(_sync_methods | _async_methods)

config = dict(default_config)
config["heading_level"] = default_config["heading_level"] + 1
config["show_root_full_path"] = False

for meth in methods:
    griffe_class = (
        mod["_submit"]["JobPool"]
        if meth in mod["_submit"]["JobPool"].members
        else mod["_submit"]["AsyncJobPool"]
        if meth in mod["_submit"]["AsyncJobPool"].members
        else None
    )
    if griffe_class is None:
        print(f"Warning: {meth} not found in JobPool or AsyncJobPool, skipping")
        continue
    docstring = render_object_docs(griffe_class[meth], config)
    result += process_content(docstring) + "\n---\n\n"

with open(ROOT / "docs" / "python-sdk" / "api-reference" / "jobpool.mdx", "w", encoding="utf-8") as f:
    f.write(result)


## `Udf` page

result = """\
---
sidebar_label: Udf
title: Udf
toc_max_heading_level: 5
sidebar_position: 0
---

"""

result += """\
## Udf

The `Udf` class is the object you get when defining a UDF with the
[`@fused.udf`](/python-sdk/api-reference/fused-udf) decorator, or when loading
a saved UDF with [`fused.load()`](/python-sdk/api-reference/fused-load).

"""

methods = [
    "cache_max_age",
    "catalog_url",
    "code",
    "collection_id",
    "collection_name",
    "create_access_token",
    "delete_saved",
    "disk_size_gb",
    "engine",
    "entrypoint",
    "from_gist",
    "get_access_token",
    "get_access_tokens",
    "get_canvas_share_token",
    "get_schedule",
    "invalidate_cache",
    "map",
    "map_async",
    "metadata",
    "run_local",
    "schedule",
    "set_parameters",
    "shared_url",
    "to_directory",
    "to_file",
    "to_fused",
]

# Methods are defined across Udf and BaseUdf; look in both
_udf_cls = mod["models"]["udf"]["udf"]["Udf"]
_base_udf_cls = mod["models"]["udf"]["base_udf"]["BaseUdf"]

config = dict(default_config)
config["heading_level"] = default_config["heading_level"] + 1
config["show_root_full_path"] = False

for meth in methods:
    if meth in _udf_cls.members:
        griffe_cls = _udf_cls
    elif meth in _base_udf_cls.members:
        griffe_cls = _base_udf_cls
    else:
        print(f"Warning: {meth} not found in Udf or BaseUdf class, skipping")
        continue
    docstring = render_object_docs(griffe_cls[meth], config)
    result += process_content(docstring) + "\n---\n\n"

with open(ROOT / "docs" / "python-sdk" / "api-reference" / "udf.mdx", "w", encoding="utf-8") as f:
    f.write(result)


## `fused.h3` page

h3_listing = [
    "run_partition_to_h3",
    "run_ingest_raster_to_h3",
    "persist_hex_table_metadata",
    "read_hex_table",
    "read_hex_table_slow",
    "read_hex_table_with_persisted_metadata",
]

result = """\
---
sidebar_label: fused.h3
title: fused.h3
toc_max_heading_level: 5
sidebar_position: 3
---

"""

mod_h3 = mod["h3"]

for obj in h3_listing:
    if obj not in mod_h3.members:
        print(f"Warning: {obj} not found in fused.h3 module, skipping")
        continue
    docstring = render_object_docs(mod_h3[obj], default_config)
    result += process_content(docstring) + "\n---\n\n"

result = result.replace("`fused.submit()`", "[`fused.submit()`](/python-sdk/api-reference/fused-submit)")

with open(ROOT / "docs" / "python-sdk" / "api-reference" / "h3.mdx", "w", encoding="utf-8") as f:
    f.write(result)
