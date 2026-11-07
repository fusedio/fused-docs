---
name: fused-map
description: Use when adding a `fused-map` widget to a Fused Workbench canvas, changing its layers, or wiring it to inputs and other UDFs. Covers points, polygons, rasters, tiled UDFs, tile URLs, H3 cells, synced maps, map clicks and bounds.
---

# Fused Map

A `fused-map` is a JSON-UI widget node in a canvas. Each entry in `props.layers` draws one dataset. A layer that reads a canvas UDF needs an edge from the UDF to the widget in `canvas.toml`, for example `["sf_listings", "listings_map"]`. Every layer type and prop: https://docs.fused.io/widget-api/fused-map. Rules for every Fused task: https://docs.fused.io/skills/SKILL.md

For `canvas.toml`, edges and other widgets, install the Workbench skills: `claude plugin marketplace add fusedio/skills` then `claude plugin install workbench@fused-marketplace`.

## Example: points colored by a value

The UDF `sf_listings_points` returns a GeoDataFrame of points with `name`, `room_type` and `price_in_dollar`.

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

Expect about 5,800 points over San Francisco, colored by price, with a `Price ($)` legend from 50 to 400.

- Polygons use the same layer; add `"lineColor": "rgba(255, 255, 255, 0.3)"` and `"lineWidth": 1` to `style`.
- A plain DataFrame with coordinates draws through `"latColumn": "latitude", "lngColumn": "longitude"`.
- A category instead of a number: `"fillColor": {"type": "categorical", "attr": "room_type", "palette": "Bold"}`.
- Layers draw in list order, so the first one is at the bottom.

## More

- **Rasters and tiles**: a raster UDF, data too large to send at once, a tile URL, or a `sql` over a tiled layer → https://docs.fused.io/skills/fused-map/tiles.md
- **Inputs and interaction**: an input that changes a layer, maps that move together, the viewport or a click sent to other UDFs → https://docs.fused.io/skills/fused-map/interaction.md
- **H3 cells**: a UDF that returns cells (`h3` layer), or an indexed `fused.h3` dataset with no UDF (`fused-hex` layer) → https://docs.fused.io/skills/h3/map.md
- **Rows from an `h3-query` widget**: a layer that draws a browser-side `/h3/query` result → https://docs.fused.io/skills/h3/h3-query-widget.md
