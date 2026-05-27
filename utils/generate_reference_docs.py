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


def escape_mdx_braces(text: str) -> str:
    """Escape bare {identifier} patterns in MDX prose.

    Docstring path placeholders like {source_dir} are valid Python but MDX
    parses them as JSX expressions, crashing the Docusaurus build.  Split on
    code spans/fences so we only touch prose text, not code blocks.
    """
    parts = re.split(r"(```[\s\S]*?```|`[^`\n]*`)", text)
    return "".join(
        re.sub(r"\{([A-Za-z_]\w*)\}", r"\\{\1\\}", p) if i % 2 == 0 else p
        for i, p in enumerate(parts)
    )


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

## Top-level functions — individual pages

TOP_LEVEL_FUNCS = [
    "udf", "cache", "load", "load_async", "run", "run_async",
    "submit", "download", "ingest", "ingest_nongeospatial", "file_path",
    "find_dataset", "register_dataset", "get_chunk_from_table", "get_chunks_metadata",
]

run_batch_addition = """
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

"""

top_level_dir = ROOT / "docs" / "python-sdk" / "api-reference" / "top-level"
top_level_dir.mkdir(parents=True, exist_ok=True)

# Remove stale .mdx files from a previous run
for stale in top_level_dir.glob("*.mdx"):
    stale.unlink()

for idx, func_name in enumerate(TOP_LEVEL_FUNCS, start=1):
    if func_name not in mod.members:
        print(f"Warning: {func_name} not found in fused module, skipping")
        continue

    slug = func_name.replace("_", "-")
    # @fused.udf conflicts with the Udf class page (udf.mdx) — use udf-decorator
    url_slug = "udf-decorator" if func_name == "udf" else slug
    label = f"@fused.{func_name}" if func_name in ("udf", "cache") else f"fused.{func_name}"

    result = f"""\
---
sidebar_label: "{label}"
title: "{label}"
slug: /python-sdk/api-reference/{url_slug}
toc_max_heading_level: 4
sidebar_position: {idx}
---

"""
    docstring = render_object_docs(mod[func_name], default_config)
    result += docstring + "\n---\n\n"

    if func_name == "ingest":
        result += run_batch_addition

    # post-processing
    result = result.replace("## fused.udf", "## @fused.udf")
    result = result.replace("## fused.cache", "## @fused.cache")
    result = result.replace("**x,** (<code>y, z</code>)", "**x, y, z** (<code>int</code>)")

    with open(top_level_dir / f"{slug}.mdx", "w") as f:
        f.write(escape_mdx_braces(result))

with open(top_level_dir / "_category_.json", "w") as f:
    f.write("""\
{
  "label": "Top-Level Functions",
  "collapsible": true,
  "collapsed": false
}
""")


## `fused.api` page

API_BLOCKLIST = {
    "_session_token", "FusedDockerAPI", "DriveFileSystem", "FdFileSystem",
    "NotebookCredentials",
    # Handled separately in Layer 2/3:
    "FusedAPI", "FusedSnowflakeConnection", "FusedAirtableConnection", "FusedNotionConnection",
}

mod_api = mod["api"]

# Layer 1: auto-detect from fused.api.__all__ minus blocklist minus classes,
# plus explicit extras not in __all__
import fused.api as _fused_api
_api_all = list(getattr(_fused_api, "__all__", []))
_extra_api = ["access_token", "auth_scheme", "logout"]

layer1_funcs = []
for name in _api_all:
    if name in API_BLOCKLIST:
        continue
    obj = getattr(_fused_api, name, None)
    if obj is not None and isinstance(obj, type):
        continue
    layer1_funcs.append(name)
for name in _extra_api:
    if name not in layer1_funcs:
        layer1_funcs.append(name)

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

for obj in layer1_funcs:
    if obj not in mod_api.members:
        print(f"Warning: {obj} not found in fused.api module, skipping")
        continue
    docstring = render_object_docs(mod_api[obj], default_config)
    result += docstring + "\n---\n\n"

# Layer 2: FusedAPI class (hardcoded methods list)
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
config["summary"] = False
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
result += fusedapi_note + docstring + "\n---\n\n"

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
    result += docstring + "\n" + usage_note + "\n---\n\n"

# Layer 3: auto-detect all Fused*Connection classes
connection_classes = [
    name for name in list(getattr(_fused_api, "__all__", [])) + ["FusedSnowflakeConnection", "FusedAirtableConnection", "FusedNotionConnection"]
    if name.startswith("Fused") and name.endswith("Connection") and name in mod_api.members
]
# deduplicate while preserving order
seen = set()
connection_classes = [c for c in connection_classes if not (c in seen or seen.add(c))]

for cls_name in connection_classes:
    cls_obj = getattr(_fused_api, cls_name, None)
    if cls_obj is None:
        print(f"Warning: {cls_name} not found in fused.api, skipping")
        continue

    cls_methods = [
        k for k in cls_obj.__dict__
        if not k.startswith("_")
    ]

    label = cls_name.replace("Fused", "").replace("Connection", "")
    result += f"## {label}\n\n## {cls_name}\n\n"

    config_cls = dict(default_config)
    config_cls["filters"] = ["__init__"]
    config_cls["summary"] = False
    result += render_object_docs(mod_api[cls_name], config_cls) + "\n---\n\n"

    config_cls["heading_level"] = default_config["heading_level"] + 1
    config_cls["show_root_full_path"] = False
    for meth in cls_methods:
        if meth not in mod_api[cls_name].members:
            print(f"Warning: {meth} not found in {cls_name} class, skipping")
            continue
        result += render_object_docs(mod_api[cls_name][meth], config_cls) + "\n---\n\n"

with open(ROOT / "docs" / "python-sdk" / "api-reference" / "api.mdx", "w") as f:
    f.write(escape_mdx_braces(result))


## `fused.context` page

result = """\
---
sidebar_label: fused.context
title: fused.context
toc_max_heading_level: 4
---

"""

mod_context = mod["context"]
context_funcs = [
    name for name, member in mod_context.members.items()
    if not name.startswith("_") and hasattr(member, "kind") and member.kind.value in ("function",)
]

for func_name in context_funcs:
    docstring = render_object_docs(mod_context[func_name], default_config)
    result += docstring + "\n---\n\n"

with open(ROOT / "docs" / "python-sdk" / "api-reference" / "context.mdx", "w") as f:
    f.write(escape_mdx_braces(result))


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

with open(ROOT / "docs" / "python-sdk" / "api-reference" / "options.mdx", "w") as f:
    f.write(escape_mdx_braces(result))


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
submitted jobs from [`fused.submit()`](/python-sdk/api-reference/top-level/submit).

"""

# Combine JobPool and AsyncJobPool methods, deduplicated
_jobpool_methods = [k for k in fused._submit.JobPool.__dict__ if not k.startswith("_")]
_async_methods = [k for k in fused._submit.AsyncJobPool.__dict__ if not k.startswith("_")]
_seen = set()
methods = []
for m in _jobpool_methods + _async_methods:
    if m not in _seen:
        _seen.add(m)
        methods.append(m)

config = dict(default_config)
config["heading_level"] = default_config["heading_level"] + 1
config["show_root_full_path"] = False

for meth in methods:
    found = False
    for cls_path in ("_submit", ):
        for cls_name in ("JobPool", "AsyncJobPool"):
            if cls_name in mod[cls_path].members and meth in mod[cls_path][cls_name].members:
                docstring = render_object_docs(mod[cls_path][cls_name][meth], config)
                result += docstring + "\n---\n\n"
                found = True
                break
        if found:
            break
    if not found:
        print(f"Warning: {meth} not found in JobPool/AsyncJobPool, skipping")

with open(ROOT / "docs" / "python-sdk" / "api-reference" / "jobpool.mdx", "w") as f:
    f.write(escape_mdx_braces(result))


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
[`@fused.udf`](/python-sdk/api-reference/top-level/udf) decorator, or when loading
a saved UDF with [`fused.load()`](/python-sdk/api-reference/top-level/load).

"""

methods = [
    "to_fused",
    "to_directory",
    "to_file",
    "create_access_token",
    "get_access_tokens",
    "delete_saved",
    "invalidate_cache",
    "catalog_url",
]

config = dict(default_config)
config["heading_level"] = default_config["heading_level"] + 1
config["show_root_full_path"] = False

for meth in methods:
    if meth not in mod["models"]["Udf"].members:
        print(f"Warning: {meth} not found in Udf class, skipping")
        continue
    docstring = render_object_docs(mod["models"]["Udf"][meth], config)
    result += docstring + "\n---\n\n"

with open(ROOT / "docs" / "python-sdk" / "api-reference" / "udf.mdx", "w") as f:
    f.write(escape_mdx_braces(result))


## `fused.h3` page

import fused.h3 as _fused_h3
h3_funcs = list(getattr(_fused_h3, "__all__", []))

result = """\
---
sidebar_label: fused.h3
title: fused.h3
toc_max_heading_level: 5
sidebar_position: 3
---

"""

mod_h3 = mod["_h3"]

for obj in h3_funcs:
    if obj not in mod_h3.members:
        print(f"Warning: {obj} not found in fused.h3 module, skipping")
        continue
    docstring = render_object_docs(mod_h3[obj], default_config)
    result += docstring + "\n---\n\n"

result = result.replace("`fused.submit()`", "[`fused.submit()`](/python-sdk/api-reference/top-level/submit)")

with open(ROOT / "docs" / "python-sdk" / "api-reference" / "h3.mdx", "w") as f:
    f.write(escape_mdx_braces(result))


## `fused.types` page

result = """\
---
sidebar_label: fused.types
title: fused.types
toc_max_heading_level: 4
---

"""

mod_types = mod["types"]
types_classes = [
    name for name, member in mod_types.members.items()
    if not name.startswith("_") and hasattr(member, "kind") and member.kind.value in ("class",)
]

config_types = dict(default_config)
config_types["summary"] = False

for cls_name in types_classes:
    docstring = render_object_docs(mod_types[cls_name], config_types)
    result += docstring + "\n---\n\n"

with open(ROOT / "docs" / "python-sdk" / "api-reference" / "types.mdx", "w") as f:
    f.write(escape_mdx_braces(result))


## `fused.secrets` page

result = """\
---
sidebar_label: fused.secrets
title: fused.secrets
toc_max_heading_level: 4
---

"""

mod_secrets = mod["_secrets"]
secrets_classes = ["SecretsManager", "UserSecretsManager"]

config_secrets = dict(default_config)
config_secrets["filters"] = ["__init__"]
config_secrets["summary"] = False

config_secrets_methods = dict(default_config)
config_secrets_methods["heading_level"] = default_config["heading_level"] + 1
config_secrets_methods["show_root_full_path"] = False

for cls_name in secrets_classes:
    if cls_name not in mod_secrets.members:
        print(f"Warning: {cls_name} not found in fused._secrets, skipping")
        continue

    import fused._secrets as _fused_secrets
    cls_obj = getattr(_fused_secrets, cls_name, None)
    cls_methods = [k for k in (cls_obj.__dict__ if cls_obj else {}) if not k.startswith("_")]

    result += render_object_docs(mod_secrets[cls_name], config_secrets) + "\n---\n\n"

    for meth in cls_methods:
        if meth not in mod_secrets[cls_name].members:
            print(f"Warning: {meth} not found in {cls_name}, skipping")
            continue
        result += render_object_docs(mod_secrets[cls_name][meth], config_secrets_methods) + "\n---\n\n"

with open(ROOT / "docs" / "python-sdk" / "api-reference" / "secrets.mdx", "w") as f:
    f.write(escape_mdx_braces(result))
