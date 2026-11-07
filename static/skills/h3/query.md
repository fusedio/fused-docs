# Query a dataset with `fused.h3.query`

The query wrapped in a UDF (`nyc311_area`) is in https://docs.fused.io/skills/H3.md. Row counts below are for that dataset.

Give at most one spatial selector:

| Selector | Example | Rows here |
|---|---|---|
| `bbox=(min_lng, min_lat, max_lng, max_lat)` | `bbox=(-74.02, 40.70, -73.93, 40.80)` | 1,312 |
| `cell=` a coarser or equal cell, as a hex string | `cell="872a10088ffffff"` | 67 |
| `lat=`, `lng=` | a point | the rows in that cell |
| `hex_range=(min, max)` | two hex strings | every row between them |

- Narrow further with `time_min`/`time_max` (ISO strings), `partition={...}`, `partition_range={"date": ["2024-07-01", "2024-07-07"]}` and `columns=[...]`.
- Only the named columns come back, so list `"hex"` in `columns` when you need the cell.
- Only place, time and partition values are filtered. Filter other columns, such as a category, on the returned DataFrame.
- A query matches whole cells. For an exact edge, pad the box by about one cell and filter by latitude and longitude.
- The whole result is held in the UDF's memory, so a result too large fails the job. Split the area or time window, and run the smaller queries in parallel with `fused.submit`.
