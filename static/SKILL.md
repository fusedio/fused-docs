# Fused Skill

Fused is a serverless data platform where Python functions called **UDFs** (User Defined Functions) run in the cloud and are instantly accessible as HTTP endpoints. You can call any UDF with a simple GET request and get back structured data — no SDK, no setup required.

This document teaches you how to discover, call, and chain Fused UDFs as tools.

---

## Agent Invariants

These rules apply to every interaction. Never violate them:

1. **Always use `.json` format** unless the user explicitly asks for a visual output or you are constructing a map tile URL
2. **Never retry the same failing call without changing something** — read the error, fix the parameter or format, then retry
3. **When chaining UDFs, parse the JSON from step 1 first** — extract the value you need, then construct step 2's URL. Do not pass a live UDF URL as an input to another UDF
4. **Share `.html` and `.png` URLs with the user as links — do not try to parse them**
5. **Do not assume parameter names or column names** — verify against the UDF's documented parameters or use an inspection UDF if one is available
6. **Do not call a UDF broader than necessary** — prefer a county-scoped call over a country-scoped one when the user's question is local

---

## Quick Reference

| Task | Pattern |
|---|---|
| Get structured data | `GET /fc_TOKEN/udf_name.json?param=value` |
| Get geographic data | `GET /fc_TOKEN/udf_name.geojson?param=value` |
| Show a map or visual to user | Give user link: `https://udf.ai/fc_TOKEN/udf_name.html?param=value` |
| Force a fresh (uncached) run | Append `&cache_max_age=0s` |
| Authenticate (private canvas) | Add header `Authorization: Bearer {ACCESS_TOKEN}` |
| Pass a list parameter | `?ids=1&ids=2&ids=3` or `?ids=[1,2,3]` |
| Pass a bounding box | `?bounds=[-122.5,37.7,-122.3,37.9]` (minx,miny,maxx,maxy) |

---

## Core Concepts

**UDF** — A Python function decorated with `@fused.udf`. It runs serverlessly and returns data (tables, geospatial data, images, or raw values).

**Canvas** — A project that groups related UDFs together. Every canvas has a unique **canvas token** (`fc_***`) that scopes access to all UDFs within it.

**Endpoint** — Every UDF on a canvas is immediately callable as an HTTP endpoint. No deployment step needed.

---

## Discovering UDFs

The available UDFs for a canvas are listed in the **Available UDFs on This Canvas** section at the bottom of this document. The canvas token and UDF names are provided by the user when they share this skill with you.

Do not attempt to discover UDFs dynamically — use only what is documented in this file.

---

## Calling a UDF

### URL structure
```
GET https://udf.ai/fc_{CANVAS_TOKEN}/{udf_name}.{format}
```

### Passing parameters
Append as URL query strings:
```
https://udf.ai/fc_{CANVAS_TOKEN}/{udf_name}.json?param1=value1&param2=value2
```

Parameters map directly to the UDF's Python function arguments. Types are coerced automatically (`"42"` becomes `42` for `int` parameters).

### Authentication
- **Public canvas**: no auth needed — the canvas token in the URL is sufficient
- **Private canvas**: add header `Authorization: Bearer {ACCESS_TOKEN}`

### Caching
Results are cached by default (90 days). To force a fresh run:
```
?cache_max_age=0s
```

---

## Choosing an Output Format

| Extension | Format | When to use |
|---|---|---|
| `.json` | JSON | Default for agents — works for any UDF return type |
| `.geojson` | GeoJSON | When the UDF returns geographic data (points, polygons, lines) |
| `.csv` | CSV text | Tabular data you want to parse line by line |
| `.png` / `.jpeg` | Raster image | Map tiles or rendered visualizations — share as link, don't parse |
| `.html` | HTML | Pre-rendered output for display — share as link, don't parse |
| `.parquet` | Binary columnar | Avoid — not useful for agents |

---

## Understanding Responses

**Tabular data** — UDF returns a `pd.DataFrame`. Comes back as a JSON array of objects:
```json
[
  {"city": "San Francisco", "population": 873965, "area_km2": 121},
  {"city": "Oakland", "population": 440981, "area_km2": 145}
]
```

**Geographic data** — UDF returns a `gpd.GeoDataFrame`. Comes back as a GeoJSON FeatureCollection:
```json
{
  "type": "FeatureCollection",
  "features": [
    {
      "type": "Feature",
      "geometry": {"type": "Point", "coordinates": [-122.4, 37.8]},
      "properties": {"name": "Mission Bay", "parcels": 412}
    }
  ]
}
```

**Summary / scalar** — UDF returns a `dict` or single value. Comes back as a JSON object:
```json
{"total_area_km2": 1520.4, "mean_elevation_m": 38, "units": "metric"}
```

**Error** — If a call fails, you get a JSON error body alongside an HTTP error status:
```json
{"error": "Parameter 'state_fips' is required", "status": 400}
```

---

## Error Reference

| HTTP status | Cause | What to do |
|---|---|---|
| `400` | Missing or wrong parameter type | Read the error message, fix the parameter name or type, retry |
| `401` | Missing or invalid auth token | Add or correct the `Authorization: Bearer` header |
| `403` | Canvas token wrong or canvas is private | Verify the canvas token; use an access token for private canvases |
| `404` | UDF name not found | Check the UDF name against the canvas index or this document's canvas section |
| `422` | Input data processing error | Check the input data format, path, or column names; use an inspection UDF if available |
| `429` | Rate limited | Wait briefly and retry; do not fan out too many parallel requests |
| `500` | UDF execution error | Check parameters and input data; report the error to the user if it persists |

---

## How to Decide Which UDF to Call

1. Read the **purpose** statements of all UDFs in the canvas section below
2. Match the user's task to the closest purpose
3. Check you have all required parameters — if not, see if another UDF can supply them
4. If the task requires data from multiple UDFs, chain them (see below)
5. When uncertain, prefer the UDF with the most specific match over a general one

---

## Chaining UDFs

UDFs are stateless and composable. A common pattern is to use the output of one UDF as the input to another:

```
Step 1: GET /fc_TOKEN/list_regions.json?country=US
→ returns [{"fips": "06", "name": "California"}, ...]

Step 2: GET /fc_TOKEN/region_stats.json?fips=06
→ returns detailed stats for California
```

Fan out in parallel:
```
Step 1: GET /fc_TOKEN/search_sites.json?query=solar+farms
→ returns list of site IDs

Step 2 (parallel): GET /fc_TOKEN/site_detail.json?id={id} for each result
→ returns detail for each site
```

When chaining, parse the JSON from step 1 and extract the value you need before constructing step 2's URL.

---

## Parameter Types Reference

| Python type | How to pass in URL |
|---|---|
| `str` | `?name=hello` |
| `int` / `float` | `?count=10` `?threshold=0.5` |
| `bool` | `?include_empty=true` or `?include_empty=false` |
| `list` | `?ids=1&ids=2&ids=3` or `?ids=[1,2,3]` |
| `dict` | `?filters={"min":0,"max":100}` (URL-encoded) |
| `fused.types.Bbox` | `?bounds=[-122.5,37.7,-122.3,37.9]` (minx, miny, maxx, maxy) — tile UDFs only |

---

## Tile Endpoints (Map Layers)

Some UDFs serve map tiles for visualization. Their endpoints follow XYZ tile conventions:

```
GET https://udf.ai/fc_{CANVAS_TOKEN}/{udf_name}/run/tiles/{z}/{x}/{y}?=png
GET https://udf.ai/fc_{CANVAS_TOKEN}/{udf_name}/run/tiles/{z}/{x}/{y}?=mvt
```

Use `.png` for raster tiles, `.mvt` for vector tiles. These are for display only — call the regular `.json` endpoint to extract data.

---

## Working with Data Pipelines

### Verify inputs before processing

Before calling an analysis UDF with a file path or column name parameter, call a lightweight inspection UDF first (if the canvas provides one) to confirm the file exists, check row count, and identify exact column names. This avoids 422 errors from typos, wrong casing, or missing files.

```bash
GET /fc_TOKEN/inspect_file.json?path=s3://bucket/data.parquet
→ [{"column": "latitude", "dtype": "float64", "total_rows": 25600}, ...]
```

### Prefer stable file paths over live UDF URLs as inputs

Always pass a stable S3 or GCS path rather than the URL of another live UDF. Passing a live endpoint URL as input creates a fragile chain — the receiving UDF will fetch the URL and may fail trying to parse it as the format it expects.

```
# Fragile: UDF B fetches UDF A's live URL, gets unexpected content type
GET /udf_b.json?path=https://.../udf_a?param=value

# Stable: UDF A saves to S3, UDF B reads from S3
GET /udf_a.json?...&save_to_file=true&output_path=s3://bucket/result.parquet
→ {"output_path": "s3://bucket/result.parquet"}

GET /udf_b.json?path=s3://bucket/result.parquet
```

If a UDF supports `save_to_file` and `output_path` parameters, use them to persist intermediate results and create a clean handoff between steps.

### Reading `save_to_file` responses

When a UDF saves its result to cloud storage, it returns a status object with an `output_path` field. Extract that path and pass it directly as the `path` parameter to the next UDF:

```json
{"status": "success", "output_path": "s3://bucket/result.parquet", "rows": 1240}
```

### Use `.json` to extract values, visual formats only for display

```bash
# Extract a value to use in the next call
GET /fc_TOKEN/some_udf.json?param=value
→ [{"id": "abc", "score": 0.92, "lat": 37.8, "lng": -122.4}]

# Share a rendered result with the user — do not parse this
GET /fc_TOKEN/some_udf.html?param=value   ← give this URL to the user
```

---

## Available UDFs on This Canvas

> Canvas token: `fc_{YOUR_TOKEN}`
> Base URL: `https://udf.ai/fc_{YOUR_TOKEN}/`

---

### `{udf_name}`

**Purpose:** {One sentence — what question does this UDF answer or what task does it perform?}

**When to use:** {What user request or situation should trigger this UDF? Be specific about what distinguishes it from other UDFs on this canvas.}

**Parameters:**

| Name | Type | Required | Default | Description |
|---|---|---|---|---|
| `param1` | `str` | yes | — | {what this parameter controls} |
| `param2` | `int` | no | `10` | {what this parameter controls} |

**Returns:** {Describe the output — what fields/columns are in the response, what they mean, what units}

**Example call:**
```
GET https://udf.ai/fc_{YOUR_TOKEN}/{udf_name}.json?param1=example_value
```

**Example response:**
```json
{
  "field1": "value",
  "field2": 42
}
```

---

*(Add one block per UDF on the canvas)*
