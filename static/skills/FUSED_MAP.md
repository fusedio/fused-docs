---
name: fused-map
description: Build or edit a `fused-map` widget in a Fused Workbench canvas. Covers layer types, data sources (UDF, tiled UDF, SQL, tile URL, indexed H3 dataset), styling, and wiring inputs, clicks and map bounds to UDFs. Use when adding a map to a canvas, changing its layers or styles, or drawing an indexed `fused.h3` dataset on a map.
---

# Fused Map

A `fused-map` is a JSON-UI widget node in a canvas. Each entry in `props.layers` draws one dataset. A layer that reads a canvas UDF needs an edge from the UDF to the widget in `canvas.toml`, for example `["sf_listings", "listings_map"]`.

## Workflow

1. Pull the canvas: `fused canvas pull <canvas> -o <dir>`.
2. Run each source UDF and read its columns: `fused run "" <dir>/<udf>.py`. Never guess column or argument names.
3. Pick the layer type from what the UDF returns (table below).
4. Validate the widget: `fused json-ui validate <dir>/<widget>.json` prints `{"valid": true, "errors": []}`.
5. Push: `fused canvas push <dir>`, then open the canvas and check every layer draws.

For `canvas.toml`, edges and other widgets, install the Workbench skills: `claude plugin marketplace add fusedio/skills` then `claude plugin install workbench@fused-marketplace`.

## Layer types

| Data | `type` | Also set |
|---|---|---|
| GeoDataFrame: points, lines, polygons | `geojson` | |
| Rows with latitude and longitude columns | `geojson` or `scatterplot` | `latColumn`, `lngColumn` (default `lat`, `lng`) |
| Rows with an H3 cell column | `h3` | `h3Column` |
| Image array | `raster` | `tile: true` for a tile UDF |
| Point density | `heatmap` | weight is `style.fillColor.attr` |
| Origin and destination pairs | `arc` | `startLatColumn`, `startLngColumn`, `endLatColumn`, `endLngColumn` |
| Vector tiles | `mvt` | `tileUrl`, or `udf` with `tile: true`; `sourceLayer` |
| Indexed H3 dataset, no UDF | `fused-hex` | `source`, `h3Column` |

Omit `type` and the map detects it from the data. `fused-hex` is never detected: always set it. `deck-geojson` is an alias of `geojson`; prefer `geojson`.

## Data sources

| Layer prop | What runs |
|---|---|
| `"udf": "{{name}}"` | The UDF once; the whole result is drawn. |
| `"udf": "{{name}}"`, `"tile": true` | The UDF once per XYZ tile. Its first argument must be named `bounds`; it gets `[west, south, east, north]` in EPSG:4326. Use for large data. |
| `"sql": "SELECT ... FROM {{name}}"` | DuckDB over the UDF result. |
| `"tileUrl": "https://.../{z}/{x}/{y}..."` | An XYZ tile server. |
| `"source": {...}` | `fused-hex` only. Queries an indexed H3 dataset per tile. |

Pass UDF arguments in the placeholder: `{{name?year=2016}}` for a fixed value, `{{name?band_index=$band}}` for a canvas parameter. The UDF reruns when the parameter changes.

## Props

Map props, next to `layers`:

- `basemap`: a full Mapbox style URL such as `mapbox://styles/mapbox/dark-v11`, `mapbox://styles/mapbox/light-v11` or `mapbox://styles/mapbox/satellite-streets-v12`, or `blank`. Omit it to follow the app's light or dark theme.
- `centerLng`, `centerLat`, `zoom`, `minZoom`, `maxZoom`. Setting a center turns `autoFit` off; `autoFit: true` flies to the data on first load.
- `showSidebar`, `showLegend`, `showControls`, `showScale`, `showBasemapSwitcher`, `showLayerPanel`: booleans.
- `style`: CSS string, for example `"flex:1;min-height:0"`.
- `param`: canvas parameter that gets the viewport `[west, south, east, north]`. Add `autoSend: true` to send on every pan or zoom, debounced by `autoSendDebounceMs` (default 600).
- `clickParam`: canvas parameter that gets the clicked feature's properties. With a `tooltip` list, only those properties.
- `stateParam`: canvas parameter that holds the camera, styles and filters. Maps that share one move together.

Layer props:

- `id` (unique), `name`, `visible`, `minZoom`, `maxZoom`.
- `tooltip`: `true` for all properties, or a list of column names.
- `legend`: `true`, or `{"title": "..."}`. Needs a data-driven color.
- `filters`: `[{"attr": "score", "type": "range", "min": 0, "max": 10}]` or `[{"attr": "class", "type": "categories", "values": ["A", "B"]}]`.
- `style.fillColor`, `style.lineColor`: `[r, g, b]`, `[r, g, b, a]`, a CSS color, `{"type": "continuous", "attr": "price", "palette": "Sunset", "domain": [0, 400], "steps": 10, "nullColor": "#b8b8b8"}`, or `{"type": "categorical", "attr": "room_type", "palette": "Bold"}`.
- `style.pointRadius`, `style.lineWidth`, `style.opacity` (0 to 1), `style.coverage` (H3 cell size, 0 to 1).
- `style.extruded`, `style.elevationAttr`, `style.elevationScale`: 3D extrusion.

## Examples

### Points colored by a value

The UDF returns a GeoDataFrame of points with `name`, `room_type` and `price_in_dollar`.

```json
{
  "type": "fused-map",
  "props": {
    "basemap": "mapbox://styles/mapbox/dark-v11",
    "layers": [{
      "id": "listings", "name": "SF listings by price", "type": "geojson",
      "udf": "{{sf_listings_points}}",
      "tooltip": ["name", "room_type", "price_in_dollar"],
      "legend": {"title": "Price ($)"},
      "style": {
        "fillColor": {"type": "continuous", "attr": "price_in_dollar", "domain": [50, 400], "steps": 10, "palette": "Sunset", "nullColor": "#b8b8b8"},
        "pointRadius": 3
      }
    }]
  }
}
```

Polygons use the same layer; add `"lineColor": "rgba(255, 255, 255, 0.3)"` and `"lineWidth": 1` to `style`.

### Two layers: a tiled raster under latitude and longitude rows

The first layer runs `bay_area_seismic_raster(bounds)` per tile and draws the image it returns. The second draws a plain DataFrame through `latColumn` and `lngColumn`. Layers draw in list order, so the raster is at the bottom.

```json
{
  "type": "fused-map",
  "props": {
    "basemap": "mapbox://styles/mapbox/dark-v11",
    "centerLng": -122.3, "centerLat": 37.7, "zoom": 9.5,
    "layers": [
      {"id": "seismic", "type": "raster", "udf": "{{bay_area_seismic_raster}}", "tile": true, "style": {"opacity": 0.6}},
      {
        "id": "listings", "type": "geojson",
        "sql": "SELECT name, room_type, latitude, longitude FROM {{sf_listings}}",
        "latColumn": "latitude", "lngColumn": "longitude",
        "tooltip": ["name", "room_type"], "legend": true,
        "style": {"fillColor": {"type": "categorical", "attr": "room_type", "palette": "Bold"}, "pointRadius": 4}
      }
    ]
  }
}
```

### Tiled vector data

For data too large to send at once, return only the rows inside `bounds`. Set `minZoom` so tiles only load when zoomed in.

```python
@fused.udf
def udf(bounds: fused.types.Bounds = [-122.45, 37.75, -122.40, 37.80]):
    import pandas as pd
    west, south, east, north = bounds
    df = pd.read_parquet("s3://fused-sample/demo_data/airbnb_listings_sf.parquet")
    df = df[df.longitude.between(west, east) & df.latitude.between(south, north)]
    return df[["name", "latitude", "longitude", "price_in_dollar"]]
```

```json
{
  "type": "fused-map",
  "props": {
    "centerLng": -122.43, "centerLat": 37.77, "zoom": 13,
    "layers": [{
      "id": "listings", "type": "geojson", "udf": "{{listings_tile}}", "tile": true, "minZoom": 12,
      "latColumn": "latitude", "lngColumn": "longitude",
      "tooltip": ["name", "price_in_dollar"],
      "style": {"fillColor": {"type": "continuous", "attr": "price_in_dollar", "palette": "Sunset", "domain": [50, 400]}, "pointRadius": 3}
    }]
  }
}
```

### H3 cells from a UDF

The UDF returns one row per cell, with the cell in `hex`. Add `"tile": true` and a `bounds` argument to load cells per tile.

```json
{
  "type": "fused-map",
  "props": {
    "layers": [{
      "id": "hex", "type": "h3", "udf": "{{hex_overview}}", "h3Column": "hex",
      "tooltip": ["hex", "POP20"], "legend": {"title": "Population"},
      "style": {"fillColor": {"type": "continuous", "attr": "POP20", "palette": "Sunset", "domain": [0, 500000]}, "opacity": 0.8, "coverage": 0.95}
    }]
  }
}
```

### Raster tiles from a URL

```json
{
  "type": "fused-map",
  "props": {
    "centerLng": -122.43, "centerLat": 37.76, "zoom": 11,
    "layers": [{
      "id": "imagery", "type": "raster",
      "tileUrl": "https://www.fused.io/server/v1/realtime-shared/UDF_Arcgis_Rgb/run/tiles/{z}/{x}/{y}?dtype_out_raster=png"
    }]
  }
}
```

### An input that changes a tile layer

Put the input and the map in one widget. Give the input a `defaultValue` so the first load has a value. Only the UDF → widget edge is needed.

```json
{
  "type": "div",
  "props": {"style": "display:flex;flex-direction:column;gap:8px;height:100%"},
  "children": [
    {"type": "number-input", "props": {"label": "Band", "param": "band", "min": 0, "max": 63, "defaultValue": 1}},
    {
      "type": "fused-map",
      "props": {
        "style": "flex:1;min-height:0",
        "layers": [{"id": "bands", "type": "raster", "udf": "{{aef_bands?b1=$band}}", "tile": true, "minZoom": 6}]
      }
    }
  ]
}
```

### Side-by-side maps that move together

Give every map the same `stateParam`, and a different fixed argument.

```json
{
  "type": "div",
  "props": {"style": "display:flex;gap:12px;height:100%"},
  "children": [
    {"type": "fused-map", "props": {"stateParam": "nl_view", "style": "flex:1;min-width:0", "centerLng": 79, "centerLat": 22, "zoom": 4.2, "layers": [{"id": "nl_2010", "type": "raster", "udf": "{{nightlights?year=2010}}", "tile": true}]}},
    {"type": "fused-map", "props": {"stateParam": "nl_view", "style": "flex:1;min-width:0", "centerLng": 79, "centerLat": 22, "zoom": 4.2, "layers": [{"id": "nl_2018", "type": "raster", "udf": "{{nightlights?year=2018}}", "tile": true}]}}
  ]
}
```

### Send the viewport and clicks to other UDFs

The map writes `map_bounds` and `selected_site`. Another layer or widget reads them as `$map_bounds` and `$selected_site`, for example `"udf": "{{site_stats?bounds=$map_bounds}}"`.

```json
{
  "type": "fused-map",
  "props": {
    "param": "map_bounds", "autoSend": true,
    "clickParam": "selected_site",
    "layers": [{"id": "sites", "type": "geojson", "udf": "{{sites}}", "latColumn": "latitude", "lngColumn": "longitude", "tooltip": ["name", "score"]}]
  }
}
```

## Indexed H3 datasets: `fused-hex`

A `fused-hex` layer draws an H3 dataset straight from the Fused H3 query endpoint, with no UDF. The map sends one request per tile.

1. **Index the data.** The dataset must be partitioned and indexed with `fused.h3`. `partition` takes a source, not a DataFrame: `fused.h3.sources.udf(my_udf)` for a UDF that returns the rows, or a Parquet folder path.

   ```python
   fused.h3.partition(fused.h3.sources.udf(my_udf), path, point_column=("lat", "lng"), h3_res=11).wait()
   fused.h3.index(path, overwrite=True).wait()
   ```

   `fused.h3.index_status(path)["status"]` is `'ready'` once indexed. Note its `hex_column` (usually `hex`).

2. **The URL.** An indexed dataset is served at `https://www.fused.io/server/v1/h3/query?path=<path>`. Check it returns rows for a small box:

   ```bash
   curl -G "https://www.fused.io/server/v1/h3/query" \
     --data-urlencode "path=s3://fused-asset/data/nyc311/" \
     -d min_lng=-73.990 -d min_lat=40.750 -d max_lng=-73.980 -d max_lat=40.758 \
     -d columns=hex -o out.parquet
   ```

   HTTP 200 returns Parquet. A private dataset needs `-H "Authorization: Bearer $TOKEN"`.

3. **Put it in the layer.** Split the URL into the layer's `source`:

   | URL part | Layer prop |
   |---|---|
   | `path=` value | `source.path` |
   | `https://www.fused.io/server/v1/h3/query` | `source.endpoint`. Optional: it defaults to `/h3/query` on the current server. |
   | `min_lng`, `min_lat`, `max_lng`, `max_lat` | Leave out. The map sends each tile's box. |
   | `columns=` | `source.variables`. Defaults to the columns the style, tooltip and filters use, or every column when they name none. |
   | `time_min`, `time_max` | `source.dateMin`, `source.dateMax`, with `source.timeColumn` |
   | the index's `hex_column` | the layer's `h3Column` |

   `source.reduce` collapses each cell's rows in the time window to one: `latest` (default) or `first` need `timeColumn`; `mean`, `min`, `max` and `sum` also add `count` (and `date_min`, `date_max` when `timeColumn` is set).

```json
{
  "type": "fused-map",
  "props": {
    "basemap": "mapbox://styles/mapbox/dark-v11",
    "centerLng": -73.985, "centerLat": 40.754, "zoom": 14,
    "layers": [{
      "id": "nyc311", "name": "NYC 311, December 2025", "type": "fused-hex", "h3Column": "hex",
      "source": {
        "path": "s3://fused-asset/data/nyc311/",
        "timeColumn": "created_date", "dateMin": "2025-12-01", "dateMax": "2025-12-31T23:59:59",
        "variables": ["year"], "reduce": "sum"
      },
      "tooltip": ["hex", "count"], "legend": {"title": "311 requests"},
      "style": {"fillColor": {"type": "continuous", "attr": "count", "palette": "Sunset", "domain": [0, 40]}, "opacity": 0.8}
    }]
  }
}
```

The map shows hexagons over Midtown colored by request count. The style only names `count`, which the server adds, so `variables` asks for one small column; without it every column is fetched. `fused-hex` never auto-fits, so set the center and zoom on the data. To filter or join the rows first, query them in a UDF with `fused.h3.query(path, bbox=bounds, ...)` and draw it as an `h3` layer with `"tile": true`.
