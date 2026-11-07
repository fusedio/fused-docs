# Inputs and interaction in a `fused-map`

Widget basics and edges: https://docs.fused.io/skills/FUSED_MAP.md

## An input that changes a tile layer

Put the input and the map in one widget, and give the input a `defaultValue` so the first load has a value. Only the UDF → widget edge is needed.

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

## Side-by-side maps that move together

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

## Send the viewport and clicks to other UDFs

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
