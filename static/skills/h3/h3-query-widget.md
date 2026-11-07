# Query a dataset in the browser: `h3-query` widget

A JSON-UI `h3-query` widget runs one `GET /h3/query`, loads the Parquet result into the browser's DuckDB and publishes it as `{{name}}`. A `fused-map` layer draws it with `"data": "{{name}}"`, and no UDF runs. Partition and index the dataset first: https://docs.fused.io/skills/H3.md. Every prop: https://docs.fused.io/widget-api/h3-query.

NYC 311 calls for one week, in the area the map shows (`s3://fused-asset/data/nyc311/` is indexed and public):

```json
{
  "type": "h3-query",
  "props": {
    "name": "nyc311", "path": "s3://fused-asset/data/nyc311/",
    "minLng": "$w", "minLat": "$s", "maxLng": "$e", "maxLat": "$n",
    "timeMin": "2024-07-01", "timeMax": "2024-07-07T23:59:59",
    "columns": ["hex", "unique_key", "created_date", "complaint_type", "latitude", "longitude"]
  },
  "children": [
    {"type": "sql-table", "props": {"sql": "SELECT COUNT(*) AS calls_in_view FROM {{nyc311}}"}}
  ]
}
```

The map layer: `{"id": "calls", "type": "h3", "h3Column": "hex", "data": "{{nyc311}}"}`.

To make the query follow the map, put both widgets in one HTML page node, each in a `<fused-widget>`. The map (`"param": "bounds", "autoSend": true`) publishes its bounds as one `[w,s,e,n]` array, which the four bbox props cannot index, so the page splits it:

```js
function splitBounds(p) {
  const b = p.bounds;
  if (b && String(b) !== String([p.w, p.s, p.e, p.n])) fused.params.set({ w: b[0], s: b[1], e: b[2], n: b[3] });
}
fused.params.onChange(splitBounds);
splitBounds(fused.params.getAll());
```

Each move runs the query again, aborting the one in flight, and the layer redraws. Expect about 3,700 rows at zoom 14 over Midtown. Give the map `"minZoom": 12` so a zoomed-out view does not fetch the whole city. Full canvas (map, `h3-query`, a histogram that cross-filters the map): https://github.com/fusedio/skills/tree/main/workbench/skills/html-template-nodes/examples/crossfilter

- `name` is what readers reference (`{{nyc311}}`), not the node name.
- `path` is required: the indexed dataset, sent as `path=`. `endpoint` is optional and defaults to `/h3/query` on the current server; a full URL on another server gets no token.
- List `hex` in `columns` when a map draws the rows.
- Give at most one spatial selector: `cell`, `lat` and `lng`, the four bbox edges, or `hexMin` and `hexMax`.
- Every string or number prop takes `$param`. The query waits until the param is set and runs again when it changes. The param comes from the same page or node, or a node with an edge into it.
- The whole result stays in browser memory, capped by `maxPages` (default 16). For a large area at every zoom, use a `fused-hex` layer, which tiles the index: https://docs.fused.io/skills/h3/map.md
- `"data": "{{name}}"` works on row layers (`h3`, `geojson`, `scatterplot`, `heatmap`, `arc`), not on `tile`, `udf`, `tileUrl` or `fused-hex` layers. A `sql` on the layer reads the rows as `{{source}}`.
