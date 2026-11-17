# Draw H3 cells on a `fused-map`

A `fused-map` widget in a Workbench canvas draws H3 cells as hexagons. Widget basics, edges and other layers: https://docs.fused.io/skills/FUSED_MAP.md. Guide: https://docs.fused.io/guide/h3-analytics/visualization.

## From a UDF: `h3` layer

A UDF returns one row per cell and the widget draws the result. Save the UDF as `nyc311_hexes`, the widget as a JSON-UI node, and add the edge `["nyc311_hexes", "hex_map"]` in `canvas.toml`.

```python
import fused


@fused.udf
def udf(month: str = "2025-12"):
    df = fused.h3.query(
        "s3://fused-asset/data/nyc311/",
        bbox=(-73.990, 40.750, -73.980, 40.758),
        partition={"month": month},
        columns=["hex", "complaint_type"],
    )
    return df.groupby("hex", as_index=False).size().rename(columns={"size": "count"})
```

```json
{
  "type": "fused-map",
  "props": {
    "layers": [
      {
        "id": "nyc311_hexes",
        "name": "NYC 311, December 2025",
        "udf": "{{nyc311_hexes}}",
        "type": "h3",
        "h3Column": "hex",
        "tooltip": true,
        "legend": true,
        "style": {
          "fillColor": {"type": "continuous", "attr": "count", "palette": "OrYel", "domain": [0, 40]},
          "opacity": 0.8
        }
      }
    ]
  }
}
```

Expect the UDF to return 167 rows with columns `hex`, `count`, and the map to fly to Midtown with 167 hexagons coloured by `count` and a legend from 0 to 40.

- `{{nyc311_hexes?month=$month}}` lets a `dropdown` with `"param": "month"` in the same widget change the month.
- Add `"tile": true` and a `bounds` argument to the UDF to load cells per tile.

## Straight from the index: `fused-hex` layer

A `fused-hex` layer draws a dataset indexed with `fused.h3` with no UDF: the map sends one `GET /h3/query` per tile. Set `"type": "fused-hex"`; it is never detected.

The layer needs a dataset built with `fused.h3.partition` (https://docs.fused.io/skills/h3/partition.md) and `fused.h3.index` (https://docs.fused.io/skills/h3/index.md).

- `source.path`: the indexed dataset, the `path=` of the `/h3/query` URL.
- `h3Column`: the index's `hex_column` (usually `hex`).
- `source.variables`: the columns to fetch. Name one small column when the style only uses `count`, or every column is fetched.
- `source.dateMin`, `source.dateMax` and `source.timeColumn`: the time window.
- `source.reduce`: how each cell's rows in the window collapse to one: `latest` (default), `first`, `mean`, `min`, `max` or `sum`. The aggregates add `count`, `date_min` and `date_max`.
- `source.endpoint`: only for another server, as a full URL such as `https://www.fused.io/server/v1/h3/query`.

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

Expect hexagons over Midtown at zoom 14, coloured by request count, with a legend from 0 to 40. Tiles can take 30 seconds or more on the first load. `fused-hex` never auto-fits, so set the center and zoom on the data.

A `sql` on a `fused-hex` layer filters or computes columns over the tiles in view: https://docs.fused.io/skills/fused-map/tiles.md
