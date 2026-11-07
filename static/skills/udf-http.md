# Call Fused UDFs over HTTP

The call pattern and the rules are in https://docs.fused.io/skills/SKILL.md. This page has the detail.

## Parameters

Query parameters map to the UDF's Python arguments, and types are coerced (`"42"` becomes `42` for an `int`).

| Python type | In the URL |
|---|---|
| `str` | `?name=hello` |
| `int` / `float` | `?count=10` `?threshold=0.5` |
| `bool` | `?include_empty=true` or `?include_empty=false` |
| `list` | `?ids=1&ids=2&ids=3` or `?ids=[1,2,3]` |
| `dict` | `?filters={"min":0,"max":100}` (URL-encoded) |
| `fused.types.Bbox` | `?bounds=[-122.5,37.7,-122.3,37.9]` (minx, miny, maxx, maxy), tile UDFs only |

## Formats

| Extension | Returns | Use for |
|---|---|---|
| `.json` | JSON | Any UDF return type |
| `.geojson` | GeoJSON | Points, polygons, lines |
| `.csv` | CSV text | Tabular data to parse line by line |
| `.png` / `.jpeg` | Image | Map tiles or rendered visuals, for the user |
| `.html` | HTML | Rendered output, for the user |
| `.parquet` | Binary columnar | Nothing an agent reads: use `.json` |

## Responses

- `pd.DataFrame`: a JSON array of objects, `[{"city": "San Francisco", "population": 873965}, ...]`.
- `gpd.GeoDataFrame`: a GeoJSON `FeatureCollection`.
- `dict` or a single value: a JSON object, `{"total_area_km2": 1520.4, "units": "metric"}`.
- Error: an HTTP error status with a JSON body, `{"error": "Parameter 'state_fips' is required", "status": 400}`.

| Status | Cause | Fix |
|---|---|---|
| `400` | Missing or wrong parameter type | Fix the name or type from the message |
| `401` | Missing or invalid auth token | Add or correct `Authorization: Bearer` |
| `403` | Wrong canvas token, or a private canvas | Check the token; use an access token for a private canvas |
| `404` | UDF name not found | Check the name in `.api.json` |
| `422` | Input data processing error | Check the input format, path or column names |
| `429` | Rate limited | Wait briefly, then retry with fewer parallel requests |
| `500` | UDF execution error | Check parameters and input; report it to the user if it persists |

## Chain UDFs

UDFs are stateless and composable:

```
GET /fc_TOKEN/list_regions.json?country=US   → [{"fips": "06", "name": "California"}, ...]
GET /fc_TOKEN/region_stats.json?fips=06       → detailed stats for California
```

- Fan out: after a search returns ids, call `site_detail.json?id={id}` for each one in parallel.
- A required parameter you don't have may come from another UDF on the canvas. Prefer the UDF whose description matches the task most closely.
- Before an analysis UDF that takes a file path or column name, call the canvas's inspection UDF if it has one: confirm the file exists, the row count and the exact column names.
- Pass stable file paths (`s3://`, `gs://`) between UDFs. A live UDF URL as input can return an unexpected content type:

```
GET /udf_a.json?...&save_to_file=true&output_path=s3://bucket/result.parquet   → {"output_path": "s3://bucket/result.parquet"}
GET /udf_b.json?path=s3://bucket/result.parquet
```

## Tile endpoints

UDFs that serve map tiles follow XYZ conventions, for display only:

```
GET https://udf.ai/fc_<TOKEN>/<udf_name>/run/tiles/{z}/{x}/{y}?=png
GET https://udf.ai/fc_<TOKEN>/<udf_name>/run/tiles/{z}/{x}/{y}?=mvt
```

`png` gives raster tiles, `mvt` vector tiles. Call the `.json` endpoint to extract data.
