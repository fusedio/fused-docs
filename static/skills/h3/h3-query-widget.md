# Query a dataset in the browser: `h3-query` widget

A JSON-UI `h3-query` widget runs one `GET /h3/query`, loads the Parquet result into the browser's DuckDB and publishes it as `{{name}}`. A `fused-map` layer draws it with `"data": "{{name}}"`, and no UDF runs. Partition and index the dataset first: https://docs.fused.io/skills/H3.md. Every prop: https://docs.fused.io/widget-api/h3-query.

Node `h3_query.json`:

```json
{
  "type": "div",
  "props": {"style": "display:flex;flex-direction:column;gap:12px;padding:16px;height:100%"},
  "children": [
    {"type": "datetime-input", "props": {"label": "Date", "param": "date", "mode": "date", "defaultValue": "2024-07-01"}},
    {
      "type": "h3-query",
      "props": {
        "name": "h3_rows", "path": "s3://us-west-2.opendata.source.coop/fused/era5-hex/era5_daily",
        "minLng": -123.5, "minLat": 37, "maxLng": -121.5, "maxLat": 38.5,
        "timeMin": "$date", "timeMax": "$date", "columns": ["hex", "t2m_max"]
      },
      "children": [
        {"type": "sql-table", "props": {"sql": "SELECT COUNT(*) AS cells, ROUND(MAX(t2m_max) - 273.15, 1) AS max_c FROM {{h3_rows}}"}}
      ]
    }
  ]
}
```

Node `map.json`:

```json
{
  "type": "fused-map",
  "props": {
    "style": "height:100%",
    "layers": [{
      "id": "t2m", "type": "h3", "h3Column": "hex", "data": "{{h3_rows}}",
      "sql": "SELECT hex, t2m_max - 273.15 AS t2m_c FROM {{source}}", "tooltip": true,
      "style": {"fillColor": {"type": "continuous", "attr": "t2m_c", "palette": "Sunset"}, "opacity": 0.8}
    }]
  }
}
```

In `canvas.toml`, add the edge `["h3_query", "map"]` (publisher to map) and `[validate] skip = ["widget_refs"]`. Expect `/h3/query` to return 5,474 rows for the default date, drawn as hexagons over the Bay Area.

- `name` is what readers reference (`{{h3_rows}}`), not the node name.
- `path` is required: the indexed dataset, sent as `path=`. `endpoint` is optional and defaults to `/h3/query` on the current server; a full URL on another server gets no token.
- List `hex` in `columns` when a map draws the rows.
- Give at most one spatial selector: `cell`, `lat` and `lng`, the four bbox edges, or `hexMin` and `hexMax`.
- Every string or number prop takes `$param`. The query waits until the param is set and runs again when it changes. The param comes from the same node or a node with an edge into it.
- The area is fixed: a map's `param` bounds (one `[w,s,e,n]` array) cannot fill the bbox props.
- The whole result stays in browser memory, capped by `maxPages` (default 16). For large data, or data that follows the map as it pans, use a `fused-hex` layer: https://docs.fused.io/skills/h3/map.md
- `"data": "{{name}}"` works on row layers (`h3`, `geojson`, `scatterplot`, `heatmap`, `arc`), not on `tile`, `udf`, `tileUrl` or `fused-hex` layers. A `sql` on the layer reads the rows as `{{source}}`.
