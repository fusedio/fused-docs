import argparse
import json
import re
import urllib.request
from pathlib import Path

PAGE = Path(__file__).resolve().parent.parent / "docs/rest-api/h3.mdx"
SPEC_URL = "https://www.fused.io/server/openapi.json"
OPERATION = ("/v1/h3/query", "get")

ROWS = [
    (["path"], "The indexed dataset, as passed to [`fused.h3.index()`](/python-sdk/api-reference/h3#index)"),
    (["min_lng", "min_lat", "max_lng", "max_lat"], "A bounding box. Give all four."),
    (["lat", "lng"], "A point. Give both."),
    (["cell"], "An H3 cell id as a hex string. Returns every row in that cell, or in its descendants when `cell` is coarser than the dataset."),
    (["hex_min", "hex_max"], "An inclusive range of raw H3 cell ids, each as a hex string"),
    (["time_min", "time_max"], "An inclusive ISO datetime window. Omitted, the whole time range is read."),
    (["partition"], "JSON object mapping a partition column to a value, or a list of values that any may match. See [Filter by partition](#filter-by-partition)."),
    (["partition_range"], "JSON object mapping a partition column to an inclusive `[min, max]`, with `null` for an open end"),
    (["columns"], "A column to return. Repeat the parameter for several. Omitted, every column is returned."),
    (["format"], {
        "parquet": "returns rows.",
        "index": "returns the matching row groups as JSON. See [Index format](#index-format).",
    }),
    (["max_row_groups"], "Row groups per page, from {minimum} to {maximum}. Default {default}."),
    (["cursor"], "The cursor from the previous page. See [Page through large results](#page-through-large-results)."),
]

TABLE = re.compile(r"(\*\*Query parameters\*\*\n\n)(?:\|.*\n)+")


def schema_type(schema):
    kind = next(s for s in schema.get("anyOf", [schema]) if s.get("type") != "null")
    return kind["items"]["type"] if kind["type"] == "array" else kind["type"]


def describe(text, schema):
    if isinstance(text, dict):
        default = schema.get("default")
        return " ".join(f"`{v}`{' (default)' if v == default else ''} {text[v]}" for v in schema["enum"])
    values = {k: schema[k] for k in ("minimum", "maximum", "default") if k in schema}
    return text.format(**{k: f"{v:,}" if type(v) in (int, float) else v for k, v in values.items()})


def render_table(spec):
    path, method = OPERATION
    params = {p["name"]: p for p in spec["paths"][path][method]["parameters"] if p["in"] == "query"}
    documented = [name for names, _ in ROWS for name in names]
    errors = [f"{name}: in the spec but not in ROWS" for name in params if name not in documented]
    errors += [f"{name}: in ROWS but not in the spec" for name in documented if name not in params]
    for names, text in ROWS:
        if isinstance(text, dict) and names[0] in params:
            served = params[names[0]]["schema"]["enum"]
            errors += [f"{names[0]}={v}: in the spec but not in ROWS" for v in served if v not in text]
            errors += [f"{names[0]}={v}: in ROWS but not in the spec" for v in text if v not in served]
    if errors:
        raise SystemExit(f"{method.upper()} {path}:\n  " + "\n  ".join(errors))

    lines = ["| Parameter | Type | Required | Description |", "|---|---|---|---|"]
    for names, text in ROWS:
        group = [params[name] for name in names]
        kinds = {schema_type(p["schema"]) for p in group}
        required = {p.get("required", False) for p in group}
        if len(kinds) > 1 or len(required) > 1:
            raise SystemExit(f"{', '.join(names)}: grouped parameters differ in type or required")
        label = ", ".join(f"`{name}`" for name in names)
        lines.append(f"| {label} | {kinds.pop()} | {'Yes' if required.pop() else 'No'} | {describe(text, group[0]['schema'])} |")
    return "\n".join(lines) + "\n"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--spec", default=SPEC_URL)
    args = parser.parse_args()

    with urllib.request.urlopen(args.spec, timeout=60) as response:
        spec = json.load(response)
    before = PAGE.read_text()
    after, count = TABLE.subn(lambda m: m.group(1) + render_table(spec), before)
    if count != 1:
        raise SystemExit(f"expected one **Query parameters** table in {PAGE.name}, found {count}")
    if after == before:
        print(f"{PAGE.name}: up to date")
    else:
        PAGE.write_text(after)
        print(f"{PAGE.name}: updated")


if __name__ == "__main__":
    main()
