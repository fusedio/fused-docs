# Rasters and tiles in a `fused-map`

Widget basics and edges: https://docs.fused.io/skills/FUSED_MAP.md

## A tiled raster under latitude and longitude rows

The first layer runs `bay_area_seismic_raster(bounds)` per tile and draws the image it returns. The second draws a plain DataFrame from a `sql`.

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

## Tiled vector data

For data too large to send at once, return only the rows inside `bounds`, and set `minZoom` so tiles load only when zoomed in.

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

Expect points across central San Francisco, loading more as you pan.

## Raster tiles from a URL

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

## A `sql` over a tiled layer

A tiled layer (`udf` with `"tile": true`, or `fused-hex`) takes a `sql` too. It runs once over the rows of every tile in view, read as `{{source}}` (a udf layer may also write its own `{{udf}}`), and again when the view moves or a `$param` changes; no tile is refetched.

- `WHERE`, computed columns, `GROUP BY`, aggregates, `LIMIT`, `ORDER BY` and `USING SAMPLE` apply to the whole view.
- Write one `SELECT` over `{{source}}` (a `WITH` is fine); a join or another UDF is rejected.
- The result keeps the cell column (`h3`, `fused-hex`) or the geometry (vector layers).
- `raster`, `mvt` and `tileUrl` layers take no `sql`.

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

Expect only the hexagons whose July 2024 daily mean passed 300 K, colored in Celsius. The sidebar's Filters tab shows the same query under "Query" with a "Runs on the tiles in view" hint; editing it redraws the layer.
