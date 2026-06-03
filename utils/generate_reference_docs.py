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
import griffe2md as _griffe2md
from griffe2md.rendering import default_config
from griffe2md.main import prepare_env as _prepare_env, prepare_context as _prepare_context
from jinja2 import Environment, FileSystemLoader
import mdformat as _mdformat


def fix_code_tags(text: str) -> str:
    """Replace <code>...</code> with backtick inline code for readability.

    griffe2md templates hardcode <code> HTML tags for parameter/return types.
    Backticks render identically but are far more readable in raw markdown.
    """
    return re.sub(r'<code>(.*?)</code>', r'`\1`', text, flags=re.DOTALL)


def escape_mdx_braces(text: str) -> str:
    """Escape bare {expr} outside fenced code blocks and inline code spans.

    griffe2md sometimes renders docstring template variables like {source_dir} directly
    into text sections. MDX 3 treats those as JSX expressions and fails to render. Using
    backslash escapes (\{ \}) renders them as literal characters.
    Inline code spans (`...`) are left untouched — their content is already safe.
    """
    lines = text.split('\n')
    result = []
    in_fence = False
    for line in lines:
        if re.match(r'^\s*```', line):
            in_fence = not in_fence
        if in_fence:
            result.append(line)
        else:
            # Split by inline code spans so we don't escape inside them
            parts = re.split(r'(`[^`]*`)', line)
            escaped = []
            for i, part in enumerate(parts):
                if i % 2 == 1:  # inside a backtick span — leave as-is
                    escaped.append(part)
                else:
                    escaped.append(re.sub(r'\{', r'\\{', re.sub(r'\}', r'\\}', part)))
            result.append(''.join(escaped))
    return '\n'.join(result)


# Custom Jinja env: searches our template overrides first, then griffe2md's defaults.
# This lets us override individual templates (e.g. admonition) without forking the library.
_custom_templates = Path(__file__).parent / "griffe2md_templates"
_builtin_templates = Path(_griffe2md.__file__).parent / "templates"


def _strip_doctest(code: str) -> str:
    """Strip doctest >>> / ... prefixes and mark output lines as comments.

    If the content has no >>> lines it's plain Python — return as-is.
    """
    if '>>> ' not in code and not code.strip().startswith('>>>'):
        return code
    lines = []
    for line in code.split('\n'):
        if line.startswith('>>> '):
            lines.append(line[4:])
        elif line.startswith('... '):
            lines.append(line[4:])
        elif line in ('>>>', '...'):
            lines.append('')
        else:
            lines.append(f'# {line}' if line.strip() else '')
    while lines and not lines[-1].strip():
        lines.pop()
    return '\n'.join(lines)


_env = _prepare_env(Environment(
    autoescape=False,
    loader=FileSystemLoader([str(_custom_templates), str(_builtin_templates)]),
    auto_reload=False,
))
_env.filters['strip_doctest'] = _strip_doctest


def render_object_docs(obj, config=None):
    """render_object_docs using the custom env (template overrides + strip_doctest filter)."""
    context = _prepare_context(obj, config)
    rendered = _env.get_template(f"{obj.kind.value}.md.jinja").render(**context)
    return _mdformat.text(rendered)


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
    "ingest_nongeospatial",
    "file_path",
    "get_chunks_metadata",
    "get_chunk_from_table",
]

# Append any public top-level functions from `fused.__all__` not already listed
# (e.g. find_dataset, load_async, register_dataset, run_async) so new functions
# appear automatically. The curated entries above keep their preferred order;
# auto-detected ones are appended alphabetically. Modules, attributes, and
# unresolvable re-export aliases are skipped.
_known_top = set(api_listing)
for name in sorted(fused.__all__):
    if name.startswith("_") or name in _known_top:
        continue
    member = mod.members.get(name)
    if member is None:
        continue
    try:
        if (
            member.kind.value == "function"
            and member.docstring
            and member.docstring.value.strip()
        ):
            api_listing.append(name)
    except Exception:
        # Unresolvable alias (e.g. load_ipython_extension) — skip
        continue

result = """\
---
sidebar_label: Top-Level Functions
title: Top-Level Functions
toc_max_heading_level: 4
---

"""

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

for obj in api_listing:
    if obj not in mod.members:
        print(f"Warning: {obj} not found in fused module, skipping")
        continue
    docstring = render_object_docs(mod[obj], default_config)
    result += docstring + "\n---\n\n"
    if obj == "ingest":
        # TODO run_batch does not yet have a proper docstring to include automatically
        result += run_batch_addition


# some post-processing
result = result.replace("## fused.udf", "## @fused.udf")
result = result.replace("## fused.cache", "## @fused.cache")
# griffe cannot handl the x, y, z multiple parameters on one line
result = result.replace("**x,** (<code>y, z</code>)", "**x, y, z** (`int`)")

with open(ROOT / "docs" / "python-sdk" / "top-level-functions.mdx", "w", encoding="utf-8") as f:
    f.write(escape_mdx_braces(fix_code_tags(result)))



## `fused.api` page

import fused.api as _fused_api

mod_api = mod["api"]

# Auto-detect public fused.api symbols from the module's `__all__`, minus a
# blocklist of internal/infra items. New integrations (airtable, notion,
# huggingface, etc.) then appear automatically — no allowlist to maintain.
API_BLOCKLIST = {
    "_session_token",       # internal
    "FusedAPI",             # rendered in its own section below
    "FusedDockerAPI",       # internal infra
    "DriveFileSystem",      # internal infra
    "FdFileSystem",         # internal infra
    "NotebookCredentials",  # internal infra
}

# Public but absent from `__all__` — always include.
_AUTH_SUPPLEMENT = {"access_token", "auth_scheme", "logout"}

# Module-level functions: everything public in `__all__` except the blocklist and
# the Fused*Connection classes (documented in their own sections below).
api_listing = sorted(
    _AUTH_SUPPLEMENT
    | {
        name for name in _fused_api.__all__
        if not name.startswith("_")
        and name not in API_BLOCKLIST
        and not (name.startswith("Fused") and name.endswith("Connection"))
        and name in mod_api.members
        and mod_api[name].kind.value == "function"
    }
)

# Fused*Connection classes each get their own section (Snowflake, Airtable, Notion, …).
connection_classes = sorted(
    name for name in _fused_api.__all__
    if name.startswith("Fused") and name.endswith("Connection")
    and name not in API_BLOCKLIST
)

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

# fused.api functions — bare name headings (## access_token, not ## fused.api.access_token)
config_api_mod = dict(default_config)
config_api_mod["show_root_full_path"] = False

for obj in api_listing:
    if obj not in mod_api.members:
        print(f"Warning: {obj} not found in fused.api module, skipping")
        continue
    docstring = render_object_docs(mod_api[obj], config_api_mod)
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

# Add usage note for FusedAPI instance methods directly into the class documentation
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

# `default_config["show_root_members_full_path"] = False` does not seem to work for the
# FusedAPI methods, so add them manually with root_full_path set to False
config["heading_level"] = default_config["heading_level"] + 1
config["show_root_full_path"] = False

for meth in methods:
    if meth not in mod_api["FusedAPI"].members:
        print(f"Warning: {meth} not found in FusedAPI class, skipping")
        continue
    docstring = render_object_docs(mod_api["FusedAPI"][meth], config)
    
    # Add explicit usage instructions after each method
    # Use inline format so it survives the ultra-compact formatting in llms.txt
    usage_note = f"""
**Usage:** `from fused.api import FusedAPI; api = FusedAPI(); api.{meth}()`
"""
    result += docstring + "\n" + usage_note + "\n---\n\n"

# fused.api Fused*Connection classes (Snowflake, Airtable, Notion, …).
# One section per class; methods discovered dynamically so new connections and
# new methods appear automatically.
config_conn = dict(default_config)
config_conn["filters"] = ["__init__"]
config_conn["summary"] = False

config_conn_meth = dict(config_conn)
config_conn_meth["heading_level"] = default_config["heading_level"] + 1
config_conn_meth["show_root_full_path"] = False

for class_name in connection_classes:
    if class_name not in mod_api.members:
        print(f"Warning: {class_name} not found in fused.api module, skipping")
        continue
    cls = mod_api[class_name]
    # Friendly label: FusedSnowflakeConnection -> Snowflake
    label = class_name.removeprefix("Fused").removesuffix("Connection")
    result += f"## {label}\n\n## {class_name}\n\n"
    result += render_object_docs(cls, config_conn) + "\n---\n\n"

    methods = sorted(
        name for name, member in cls.members.items()
        if not name.startswith("_")
        and member.kind.value == "function"
        and member.docstring and member.docstring.value.strip()
    )
    for meth in methods:
        result += render_object_docs(cls[meth], config_conn_meth) + "\n---\n\n"

with open(ROOT / "docs" / "python-sdk" / "api-reference" / "api.mdx", "w", encoding="utf-8") as f:
    f.write(escape_mdx_braces(fix_code_tags(result)))


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
    f.write(escape_mdx_braces(fix_code_tags(result)))


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
submitted jobs from [`fused.submit()`](/python-sdk/top-level-functions/#fusedsubmit).

"""

# Dynamic: all public JobPool members with docstrings — picks up new additions automatically
methods = sorted(
    name for name, member in mod["_submit"]["JobPool"].members.items()
    if not name.startswith("_")
    and member.docstring and member.docstring.value.strip()
)

config = dict(default_config)
config["heading_level"] = default_config["heading_level"] + 1
config["show_root_full_path"] = False

for meth in methods:
    docstring = render_object_docs(mod["_submit"]["JobPool"][meth], config)
    result += docstring + "\n---\n\n"

# AsyncJobPool section (returned by udf.map_async())

result += """\
## AsyncJobPool

`AsyncJobPool` is returned by [`udf.map_async()`](/python-sdk/api-reference/udf/#map_async).
It inherits all [`JobPool`](#jobpool) methods and adds async counterparts for each one.

"""

async_methods = sorted(
    name for name, member in mod["_submit"]["AsyncJobPool"].members.items()
    if name.endswith("_async")
    and not name.startswith("_")
    and member.docstring and member.docstring.value.strip()
)

config_async = dict(default_config)
config_async["heading_level"] = default_config["heading_level"] + 1
config_async["show_root_full_path"] = False

for meth in async_methods:
    docstring = render_object_docs(mod["_submit"]["AsyncJobPool"][meth], config_async)
    result += docstring + "\n---\n\n"

with open(ROOT / "docs" / "python-sdk" / "api-reference" / "jobpool.mdx", "w", encoding="utf-8") as f:
    f.write(escape_mdx_braces(fix_code_tags(result)))


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
[`@fused.udf`](/python-sdk/top-level-functions/#fusedudf) decorator, or when loading
a saved UDF with [`fused.load()`](/python-sdk/top-level-functions/#fusedload).

"""

# Dynamic: all public Udf members with docstrings (methods + pydantic fields).
# Use `all_members` so methods inherited from `BaseUdf` (schedule, get_schedule,
# to_fused, etc.) are included — `members` only holds members defined directly on
# `Udf`. Picks up new additions automatically — no hardcoded list to maintain.
# Skip deprecation stubs (e.g. `original_headers`, `headers`, `utils`) whose only
# docstring is "Deprecated.".
methods = sorted(
    name for name, member in mod["models"]["Udf"].all_members.items()
    if not name.startswith("_")
    and member.docstring and member.docstring.value.strip()
    and member.docstring.value.strip() != "Deprecated."
)

config = dict(default_config)
config["heading_level"] = default_config["heading_level"] + 1
config["show_root_full_path"] = False

for meth in methods:
    docstring = render_object_docs(mod["models"]["Udf"][meth], config)
    result += docstring + "\n---\n\n"

with open(ROOT / "docs" / "python-sdk" / "api-reference" / "udf.mdx", "w", encoding="utf-8") as f:
    f.write(escape_mdx_braces(fix_code_tags(result)))


## `fused.h3` page

api_listing = sorted([
    "persist_hex_table_metadata",
    "read_hex_table",
    "read_hex_table_slow",
    "read_hex_table_with_persisted_metadata",
    "run_ingest_raster_to_h3",
    "run_partition_to_h3",
])

result = """\
---
sidebar_label: fused.h3
title: fused.h3
toc_max_heading_level: 5
sidebar_position: 3
---

"""

mod_api = mod["h3"]

# bare name headings (## run_ingest_raster_to_h3, not ## fused.h3.run_ingest_raster_to_h3)
config_h3 = dict(default_config)
config_h3["show_root_full_path"] = False

for obj in api_listing:
    if obj not in mod_api.members:
        print(f"Warning: {obj} not found in fused.h3 module, skipping")
        continue
    docstring = render_object_docs(mod_api[obj], config_h3)
    result += docstring + "\n---\n\n"

result = result.replace("`fused.submit()`", "[`fused.submit()`](/python-sdk/top-level-functions/#fusedsubmit)")

with open(ROOT / "docs" / "python-sdk" / "api-reference" / "h3.mdx", "w", encoding="utf-8") as f:
    f.write(escape_mdx_braces(fix_code_tags(result)))


## ---------------------------------------------------------------------------
## CLI reference (docs/cli/) — generated from the live Click command tree
## ---------------------------------------------------------------------------
#
# Mechanical generation: imports the installed `fused` CLI (a Click group) and
# renders one page per top-level command — help, usage synopsis, and an options
# table — plus the overview command table. No hand-written prose; edit the CLI
# command definitions in fused-py (or this generator) instead of the .mdx files.

import click
from fused.cli import cli as cli_group

CLI_DIR = ROOT / "docs" / "cli"

# Top-level commands that get their own page, in sidebar order. Everything else
# (login, logout, whoami, completion) is listed in the overview command table.
CLI_PAGES = [
    "canvas",
    "claude",
    "cronjob",
    "files",
    "integrations",
    "json-ui",
    "run",
    "secrets",
    "udf",
    "udf-schema",
]

_CLI_TYPE_METAVARS = {
    "text": "TEXT",
    "integer": "INTEGER",
    "float": "FLOAT",
    "path": "PATH",
    "filename": "PATH",
    "file": "FILENAME",
    "boolean": "",
}


def _cli_clean(text: str) -> str:
    """Collapse a Click help string to a single clean markdown line."""
    if not text:
        return ""
    text = text.replace("\b", "")
    text = re.sub(r"``([^`]+)``", r"`\1`", text)
    return " ".join(text.split())


def _cli_short(cmd) -> str:
    return _cli_clean(cmd.get_short_help_str(limit=300))


def _cli_metavar(param) -> str:
    t = param.type
    if isinstance(t, click.Choice):
        return "[" + "|".join(str(c) for c in t.choices) + "]"
    name = (getattr(t, "name", "") or "").lower()
    return _CLI_TYPE_METAVARS.get(name, name.upper())


def _cli_flag_cell(param) -> str:
    """Single backtick-wrapped flag cell, e.g. `--engine [remote\\|local]`."""
    if param.secondary_opts:  # boolean --flag/--no-flag pair
        inside = " / ".join(param.opts + param.secondary_opts)
    else:
        metavar = "" if param.is_flag else _cli_metavar(param)
        inside = ", ".join(param.opts) + (f" {metavar}" if metavar else "")
    return "`" + inside.replace("|", "\\|") + "`"


def _cli_desc_cell(param, with_default: bool = True) -> str:
    parts = []
    if param.help:
        parts.append(_cli_clean(param.help))
    default = param.default
    if (
        with_default
        and default is not None
        and not callable(default)
        and not (param.is_flag and default is False)
    ):
        parts.append(f"(default: `{default}`)")
    return (" ".join(parts) or "—").replace("|", "\\|")


def _cli_options_table(cmd) -> str:
    opts = [
        p
        for p in cmd.params
        if isinstance(p, click.Option) and not getattr(p, "hidden", False)
    ]
    if not opts:
        return ""
    rows = ["| Flag | Description |", "|---|---|"]
    rows += [f"| {_cli_flag_cell(p)} | {_cli_desc_cell(p)} |" for p in opts]
    return "\n".join(rows)


def _cli_synopsis(cmd, path: str) -> str:
    parts = [path]
    for p in cmd.params:
        if isinstance(p, click.Argument):
            name = p.name.upper()
            if p.nargs == -1:
                name = f"[{name}...]"
            elif not p.required:
                name = f"[{name}]"
            parts.append(name)
    if any(
        isinstance(p, click.Option) and not getattr(p, "hidden", False)
        for p in cmd.params
    ):
        parts.append("[OPTIONS]")
    return " ".join(parts)


def _cli_render_command(cmd, path: str, level: int) -> str:
    """Render a sub(command) at the given heading level, recursing into groups."""
    h = "#" * min(level, 4)
    out = [f"{h} `{path}`", ""]
    short = _cli_short(cmd)
    if short:
        out += [short, ""]
    if isinstance(cmd, click.Group):
        subs = [
            (n, s)
            for n, s in sorted(cmd.commands.items())
            if not getattr(s, "hidden", False)
        ]
        out += ["| Subcommand | Description |", "|---|---|"]
        out += [f"| `{n}` | {_cli_short(s)} |" for n, s in subs]
        out.append("")
        for n, s in subs:
            out.append(_cli_render_command(s, f"{path} {n}", level + 1))
    else:
        out += ["```", _cli_synopsis(cmd, path), "```", ""]
        table = _cli_options_table(cmd)
        if table:
            out += ["**Options**", "", table, ""]
    return "\n".join(out)


def _cli_render_page(name: str) -> str:
    cmd = cli_group.commands[name]
    out = [
        "---",
        f"id: {name}",
        f"title: fused {name}",
        f"sidebar_label: fused {name}",
        "---",
        "",
        f"# `fused {name}`",
        "",
    ]
    short = _cli_short(cmd)
    if short:
        out += [short, ""]
    if isinstance(cmd, click.Group):
        out += ["```", f"fused {name} [SUBCOMMAND] [OPTIONS]", "```", ""]
        subs = [
            (n, s)
            for n, s in sorted(cmd.commands.items())
            if not getattr(s, "hidden", False)
        ]
        out += ["## Subcommands", "", "| Subcommand | Description |", "|---|---|"]
        out += [f"| `{n}` | {_cli_short(s)} |" for n, s in subs]
        out.append("")
        for n, s in subs:
            out.append(_cli_render_command(s, f"fused {name} {n}", 2))
            out.append("")
    else:
        out += ["```", _cli_synopsis(cmd, f"fused {name}"), "```", ""]
        table = _cli_options_table(cmd)
        if table:
            out += ["## Options", "", table, ""]
    return "\n".join(out) + "\n"


# Per-page command files
for _name in CLI_PAGES:
    if _name not in cli_group.commands:
        print(f"Warning: CLI command '{_name}' not found, skipping page")
        continue
    with open(CLI_DIR / f"{_name}.mdx", "w", encoding="utf-8") as f:
        f.write(escape_mdx_braces(_cli_render_page(_name)))

# Overview page: global flags + a generated command table
_global_rows = ["| Flag | Env var | Description |", "|---|---|---|"]
for p in cli_group.params:
    if isinstance(p, click.Option) and not getattr(p, "hidden", False):
        envvar = f"`{p.envvar}`" if p.envvar else ""
        _global_rows.append(
            f"| {_cli_flag_cell(p)} | {envvar} | {_cli_desc_cell(p, with_default=False)} |"
        )

_command_rows = ["| Command | Description |", "|---|---|"]
for _name in sorted(cli_group.commands):
    _cmd = cli_group.commands[_name]
    if getattr(_cmd, "hidden", False):
        continue
    _label = f"[`fused {_name}`](/cli/{_name})" if _name in CLI_PAGES else f"`fused {_name}`"
    _command_rows.append(f"| {_label} | {_cli_short(_cmd)} |")

_overview = f"""---
id: overview
title: CLI Reference
sidebar_label: Overview
---

# CLI Reference

The `fused` CLI lets you manage Fused from your terminal — run UDFs, manage canvases and files, handle secrets, and connect integrations. Install it with the `fused` package:

```bash
pip install --upgrade fused
```

## Global flags

These flags apply to every command:

{chr(10).join(_global_rows)}

## Commands

{chr(10).join(_command_rows)}
"""

with open(CLI_DIR / "overview.mdx", "w", encoding="utf-8") as f:
    f.write(escape_mdx_braces(_overview))

print(f"Generated CLI reference for {len(CLI_PAGES)} commands + overview")
