# /// script
# requires-python = ">=3.11"
# dependencies = [
#   "fused",
#   "griffe ~= 1.7",
# ]
# ///
#
# Checks that every method in the allowlists from generate_reference_docs.py:
#   1. Exists in the installed fused package
#   2. Appears as a heading in the corresponding MDX file
#
# Red-green usage:
#   uv run utils/test_api_reference_coverage.py           # red: see what's missing
#   uv run --reinstall-package fused utils/generate_reference_docs.py  # fix
#   uv run utils/test_api_reference_coverage.py           # green: confirm all pass

import sys
from pathlib import Path

import griffe
import fused

ROOT = Path(__file__).parent / ".."

# ── Package load ───────────────────────────────────────────────────────────────

print(f"Testing API reference coverage for fused v{fused.__version__}\n")
mod = griffe.load("fused", docstring_parser="google")

# ── Allowlists ─────────────────────────────────────────────────────────────────
# Curated lists (intentional subsets of larger modules — stay hardcoded)
# Class-level lists are dynamic (all public documented members auto-discovered)

TOP_LEVEL_FUNCTIONS = [
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

FUSED_API_FUNCTIONS = [
    "whoami",
    "access_token",
    "auth_scheme",
    "logout",
    "delete",
    "list",
    "get",
    "download",
    "upload",
    "sign_url",
    "sign_url_prefix",
    "resolve",
    "get_udfs",
    "get_apps",
    "job_get_logs",
    "job_print_logs",
    "job_tail_logs",
    "job_get_status",
    "job_cancel",
    "job_get_exec_time",
    "job_wait_for_job",
    "job_get_results",
    "job_wait_for_results",
    "schedule_udf",
    "schedule_list",
    "session_token",
    "team_info",
    "enable_gcs",
    "log",
    "snowflake_connect",
    "snowflake_query",
]

FUSED_API_CLASS_METHODS = [
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

H3_FUNCTIONS = sorted([
    "persist_hex_table_metadata",
    "read_hex_table",
    "read_hex_table_slow",
    "read_hex_table_with_persisted_metadata",
    "run_ingest_raster_to_h3",
    "run_partition_to_h3",
])

FUSED_SNOWFLAKE_METHODS = [
    "connect",
    "query",
    "execute",
    "list_databases",
    "list_schemas",
    "list_tables",
    "list_stages",
    "list_stage_files",
    "read_stage",
    "write",
]

# Dynamic: all public documented members — picks up new additions automatically
JOBPOOL_METHODS = sorted(
    name for name, member in mod["_submit"]["JobPool"].members.items()
    if not name.startswith("_")
    and member.docstring and member.docstring.value.strip()
)

# Mirror the generator: `all_members` includes methods inherited from `BaseUdf`
# (schedule, get_schedule, to_fused, etc.); skip deprecation stubs whose only
# docstring is "Deprecated." (original_headers, headers, utils).
UDF_MEMBERS = sorted(
    name for name, member in mod["models"]["Udf"].all_members.items()
    if not name.startswith("_")
    and member.docstring and member.docstring.value.strip()
    and member.docstring.value.strip() != "Deprecated."
)

ASYNC_JOBPOOL_ASYNC_METHODS = sorted(
    name for name, member in mod["_submit"]["AsyncJobPool"].members.items()
    if name.endswith("_async")
    and not name.startswith("_")
    and member.docstring and member.docstring.value.strip()
)

# ── Helpers ───────────────────────────────────────────────────────────────────

failures: list[str] = []
warnings: list[str] = []
checks_run = 0

# Heading format per file (from inspecting generate_reference_docs.py output):
#   top-level-functions.mdx : ## @fused.udf / ## fused.run  (level 2, full path)
#   api.mdx module functions : ## {name}                     (level 2, bare name)
#   api.mdx FusedAPI methods : ### {name}                    (level 3, bare name)
#   h3.mdx                  : ## {name}                      (level 2, bare name)
#   udf.mdx members         : ### {name}                     (level 3, bare name)
#   jobpool.mdx methods     : ### {name}                     (level 3, bare name)


def check_in_package(mod_obj, name: str, context: str) -> bool:
    """Returns True if name exists in the package; warns (doesn't fail) if missing."""
    global checks_run
    checks_run += 1
    if name not in mod_obj.members:
        warnings.append(
            f"[STALE ALLOWLIST] {context}.{name} not in package"
            " — remove from allowlist in generate_reference_docs.py"
        )
        return False
    return True


_missing_mdx_reported: set[Path] = set()


def check_in_mdx(mdx_path: Path, heading: str, context: str, level: int = 2) -> bool:
    """Fails if the MDX file is missing or doesn't contain the expected heading."""
    global checks_run
    checks_run += 1
    if not mdx_path.exists():
        if mdx_path not in _missing_mdx_reported:
            failures.append(
                f"[MDX FILE MISSING] {mdx_path.relative_to(ROOT)}"
                " — run generate_reference_docs.py to create it"
            )
            _missing_mdx_reported.add(mdx_path)
        return False
    content = mdx_path.read_text(encoding="utf-8")
    marker = f"{'#' * level} {heading}"
    if marker not in content:
        failures.append(
            f"[NOT IN DOCS] {context}"
            f" — heading '{marker}' missing in {mdx_path.name}"
        )
        return False
    return True


# ── Top-level functions ────────────────────────────────────────────────────────
# Headings: ## @fused.udf / ## @fused.cache  OR  ## fused.{name}

top_level_mdx = ROOT / "docs" / "python-sdk" / "top-level-functions.mdx"

for name in TOP_LEVEL_FUNCTIONS:
    if not check_in_package(mod, name, "fused"):
        continue
    if name in ("udf", "cache"):
        heading = f"@fused.{name}"
    else:
        heading = f"fused.{name}"
    check_in_mdx(top_level_mdx, heading, f"fused.{name}", level=2)

# ── fused.api module functions ─────────────────────────────────────────────────
# Headings: ## {name}  (bare name, not fused.api.{name})

api_mdx = ROOT / "docs" / "python-sdk" / "api-reference" / "api.mdx"
mod_api = mod["api"]

for name in FUSED_API_FUNCTIONS:
    if check_in_package(mod_api, name, "fused.api"):
        check_in_mdx(api_mdx, name, f"fused.api.{name}", level=2)

# ── FusedAPI class methods ─────────────────────────────────────────────────────
# Headings: ### {name}  (under ## FusedAPI)

if "FusedAPI" in mod_api.members:
    for name in FUSED_API_CLASS_METHODS:
        if check_in_package(mod_api["FusedAPI"], name, "fused.api.FusedAPI"):
            check_in_mdx(api_mdx, name, f"FusedAPI.{name}", level=3)

# ── JobPool methods ────────────────────────────────────────────────────────────
# Headings: ### {name}  (under ## JobPool)

jobpool_mdx = ROOT / "docs" / "python-sdk" / "api-reference" / "jobpool.mdx"

for name in JOBPOOL_METHODS:
    check_in_mdx(jobpool_mdx, name, f"JobPool.{name}", level=3)

# ── AsyncJobPool async methods ─────────────────────────────────────────────────
# Headings: ### {name}  (under ## AsyncJobPool)

for name in ASYNC_JOBPOOL_ASYNC_METHODS:
    check_in_mdx(jobpool_mdx, name, f"AsyncJobPool.{name}", level=3)

# ── Udf members ────────────────────────────────────────────────────────────────
# Headings: ### {name}  (under ## Udf)

udf_mdx = ROOT / "docs" / "python-sdk" / "api-reference" / "udf.mdx"

for name in UDF_MEMBERS:
    check_in_mdx(udf_mdx, name, f"Udf.{name}", level=3)

# ── fused.h3 functions ─────────────────────────────────────────────────────────
# Headings: ## {name}  (bare name, not fused.h3.{name})

h3_mdx = ROOT / "docs" / "python-sdk" / "api-reference" / "h3.mdx"
mod_h3 = mod["h3"]

for name in H3_FUNCTIONS:
    if check_in_package(mod_h3, name, "fused.h3"):
        check_in_mdx(h3_mdx, name, f"fused.h3.{name}", level=2)

# ── FusedSnowflakeConnection methods ──────────────────────────────────────────
# Headings: ### {name}  (under ## FusedSnowflakeConnection)

if "FusedSnowflakeConnection" in mod_api.members:
    for name in FUSED_SNOWFLAKE_METHODS:
        if check_in_package(mod_api["FusedSnowflakeConnection"], name, "fused.api.FusedSnowflakeConnection"):
            check_in_mdx(api_mdx, name, f"FusedSnowflakeConnection.{name}", level=3)

# ── Report ────────────────────────────────────────────────────────────────────

if warnings:
    print(f"Warnings ({len(warnings)} stale allowlist entries):\n")
    for w in warnings:
        print(f"  {w}")
    print()

if failures:
    print(f"FAILED — {len(failures)} issue(s) found (out of {checks_run} checks):\n")
    for f in failures:
        print(f"  {f}")
    print(
        "\nTo regenerate missing or stale docs, run:\n"
        "  uv run --reinstall-package fused utils/generate_reference_docs.py\n"
        "Then re-run this script to confirm all checks pass."
    )
    sys.exit(1)
else:
    print(f"PASSED — all {checks_run} checks passed")
    sys.exit(0)
