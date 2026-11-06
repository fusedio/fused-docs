---
name: fused-map
description: Build or edit a `fused-map` widget in a Fused Workbench canvas, with worked examples for points, rasters, tiled UDFs, H3 cells, tile URLs, inputs, synced maps, map clicks and bounds, and indexed `fused.h3` datasets. Use when adding a map to a canvas, changing its layers, or wiring it to inputs and other UDFs.
---

# Fused Map

A `fused-map` is a JSON-UI widget node in a canvas. Each entry in `props.layers` draws one dataset. A layer that reads a canvas UDF needs an edge from the UDF to the widget in `canvas.toml`, for example `["sf_listings", "listings_map"]`. Every layer type and prop: https://docs.fused.io/widget-api/fused-map.

For `canvas.toml`, edges and other widgets, install the Workbench skills: `claude plugin marketplace add fusedio/skills` then `claude plugin install workbench@fused-marketplace`.

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

Expect about 5,800 points over San Francisco, colored by price, with a `Price ($)` legend from 50 to 400. Polygons use the same layer; add `"lineColor": "rgba(255, 255, 255, 0.3)"` and `"lineWidth": 1` to `style`.

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

Expect the seismic hazard raster over the Bay Area, with listings over San Francisco colored by `room_type` and a four-category legend.

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

Expect the map to draw points across central San Francisco, loading more as you pan.

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

Expect hexagons over the United States colored by population, with a legend from 0 to 500,000.

### Query a tiled layer

A tiled layer (`udf` with `"tile": true`, or `fused-hex`) takes a `sql` too. It runs on each tile as it loads, over that tile's rows as `{{source}}` (a udf layer may also write its own `{{udf}}`). Use it for `WHERE`, computed columns and `GROUP BY` the cell column. The result must keep the cell column (`h3`, `fused-hex`) or the geometry (vector layers). `LIMIT`, `ORDER BY`, `USING SAMPLE` and other UDFs are not available per tile; `raster`, `mvt` and `tileUrl` layers take no `sql`.

```json
{
  "type": "fused-map",
  "props": {
    "centerLng": -122.4, "centerLat": 37.75, "zoom": 8,
    "layers": [{
      "id": "hot", "type": "fused-hex",
      "source": {"endpoint": "/retrieve/era5/daily/bbox", "dateMin": "2024-07-01", "dateMax": "2024-07-31", "variables": ["t2m_mean"]},
      "sql": "SELECT hex, date, t2m_mean - 273.15 AS t2m_c FROM {{source}} WHERE t2m_mean > 300",
      "tooltip": ["hex", "t2m_c"],
      "style": {"fillColor": {"type": "continuous", "attr": "t2m_c", "palette": "Sunset", "domain": [27, 40]}}
    }]
  }
}
```

Expect only the hexagons whose July 2024 daily mean passed 300 K, colored in Celsius. The sidebar's Filters tab shows the same query under "Query" with a "Runs per tile" hint; editing it reloads the layer's tiles.

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

Expect satellite imagery of San Francisco.

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
        "centerLng": -122.3, "centerLat": 37.8, "zoom": 12,
        "layers": [{"id": "bands", "type": "raster", "udf": "{{aef_bands?b1=$band}}", "tile": true, "minZoom": 6}]
      }
    }
  ]
}
```

Expect a `Band` box set to 1 above a false-color image of Oakland. Typing another band, such as 30, reruns the tiles and changes the colors.

### Side-by-side maps that move together

Give every map the same `stateParam`, and pass each a different fixed argument.

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

Expect two night-light maps of India, 2010 and 2018. In Workbench, panning or zooming one moves the other.

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

Expect `$map_bounds` to be like `[-122.69, 37.69, -122.21, 37.83]` after a pan, and a click on a point to set `$selected_site` to that point's `{"name": ..., "score": ...}`: only the `tooltip` fields.

- `param` receives the view's `[west, south, east, north]`: the map sends its real bounds once when it is ready, then with `autoSend` on pans (each `moveend` after `autoSendDebounceMs`, default 600, or at most once per animation frame while the map moves when that is `0`). The ready send overwrites a value already on the canvas. A zero-area box (map hidden) is never sent, and a map that cannot load (no WebGL, bad token) never sets it.
- `clickParam`: 64-bit integers arrive as numbers, or as strings when they are outside JavaScript's safe integer range, dates as ISO strings and typed arrays as plain arrays.
- `hoverParam` receives the same object as `clickParam` for the feature under the cursor: at most once per animation frame, only when it changes. A new feature is not sent while the map is dragged. When the cursor leaves every feature the param is removed. After a wheel zoom or a data reload it keeps the last value until the pointer moves. Not saved with the canvas.
- `selectParam` receives the selection, `{layer, key, ids, count, bbox, mode, truncated}`: shift+drag draws a box (`mode: "box"`), shift+click toggles one feature (`mode: "click"`, `bbox: null`). A page or wired widget can write it: `null`, `{"mode": "none"}` or `{"ids": [], "bbox": null}` clears the outline and dimming, and `{"bbox": [west, south, east, north]}` (west < east, south < north) draws and dims to that box without picking ids. A box written by another node is published to the map's own param with `"ids": []`. The map hears only the page it is embedded in and nodes wired to it by an edge in either direction, while it is mounted. Not saved with the canvas.
- `stateParam` receives the map's camera and layer state, saved with the canvas and restored on reload. Its `view` is the camera, `{centerLng, centerLat, zoom, bearing, pitch, width, height}`: `zoom` in Web Mercator with 512 px tiles, to 6 decimals, `bearing` and `pitch` in degrees, `width` and `height` the map canvas in CSS pixels. `view` is written only when a pan, zoom, rotate or tilt gesture ends (and after Reset view), not during the gesture, not after a programmatic move such as fit to data, and not on a resize. It is absent until the viewer first moves the map. Restoring the camera applies the centre, zoom, bearing and pitch and ignores `width` and `height`.

To draw a page's own overlay on the map, convert with these, `x`/`y` in CSS pixels from the map canvas's top-left corner and `v` the param's `view`. They are exact at `bearing` 0 and `pitch` 0, and right once the map has settled: they lag while it moves.

```js
const R = Math.PI / 180;
const worldX = (lng) => (lng + 180) / 360;
const worldY = (lat) => 0.5 - Math.log(Math.tan(Math.PI / 4 + (lat * R) / 2)) / (2 * Math.PI);
function project(lng, lat, v) {
  const size = 512 * 2 ** v.zoom;
  return [(worldX(lng) - worldX(v.centerLng)) * size + v.width / 2, (worldY(lat) - worldY(v.centerLat)) * size + v.height / 2];
}
function unproject(x, y, v) {
  const size = 512 * 2 ** v.zoom;
  const wx = worldX(v.centerLng) + (x - v.width / 2) / size, wy = worldY(v.centerLat) + (y - v.height / 2) / size;
  return [wx * 360 - 180, (2 * Math.atan(Math.exp((0.5 - wy) * 2 * Math.PI)) - Math.PI / 2) / R];
}
```

## Indexed H3 datasets: `fused-hex`

A `fused-hex` layer draws a dataset partitioned and indexed with `fused.h3` straight from the H3 query endpoint (`GET /h3/query`), with no UDF. The map requests each tile's box itself.

- `source.path`: the indexed dataset path, the `path=` of the `/h3/query` URL.
- `h3Column`: the index's `hex_column` (usually `hex`).
- `source.variables`: the columns to fetch. Name one small column when the style only uses `count`, or every column is fetched.
- `source.dateMin`, `source.dateMax` and `source.timeColumn`: the time window.
- `source.reduce`: how each cell's rows collapse to one: `latest` (default), `first`, `mean`, `min`, `max` or `sum`. The aggregates add `count`.
- `source.endpoint`: only for another server, as a full `.../h3/query` URL.

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

Expect hexagons over Midtown colored by request count, with a legend from 0 to 40. Tiles can take 30 seconds or more on the first load. `fused-hex` never auto-fits, so set the center and zoom on the data.
