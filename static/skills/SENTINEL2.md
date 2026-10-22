# Sentinel-2 on Fused

Use `sentinel_utils` for Sentinel-2 L2A: scene search, cloud-free composites, indices (NDVI and more), time series, terrain, GeoTIFF export and H3 hexagons. Every call runs on the user's own Fused account. Never call a canvas share link from code: it runs as the canvas owner.

Each snippet says what to expect. Numbers come from live data, so they can differ a little. Check the shape and columns first.

## Set up

```bash
pip install "fused[raster,vector]" odc-stac rio-tiler h3 nest_asyncio
fused login          # opens the browser; check with `fused whoami`
```

```python
import fused

su = fused.load("https://github.com/fusedio/udfs/tree/72d479e153f5bd74f65a1564334f8914c3df66d1/public/sentinel_utils/")
area = [-93.25, 41.95, -93.15, 42.02]  # [west, south, east, north], EPSG:4326
dates = ("2024-07-01", "2024-07-31")
```

Keep a commit in the URL so the code does not change under you. To upgrade, change the commit. `su.api()` lists every function with its signature and doc (77 rows: module, name, signature, doc).

## Search scenes

```python
scenes = su.query(area, dates, cloud_cover=20)
```

Expect a GeoDataFrame, one row per scene, oldest first, with columns `id`, `datetime`, `date`, `tile_id`, `platform`, `cloud_cover`, `nodata_pct`, `crs`, `source`, `offset`, `assets`, `geometry`. Here: 1 row, tile `15TVG`, 2024-07-29, about 14 % cloud.

## Best day

```python
days = su.clearest_days(su.query(area, dates), area)
```

Expect a DataFrame with columns `date`, `scenes`, `cover_pct`, `cloud_cover`, `clear_pct`, the best day first. Here: 6 rows, first date 2024-07-29 with `clear_pct` about 86. Use `mosaic_order="clearest_day"` in `process_request` to build one image from that day.

## Composite or index image, saved as GeoTIFF

```python
req = su.process_request(area, dates, ["B04", "B03", "B02"], resolution=10, mask="clear", reducer="median", output="geotiff")
open("rgb.tif", "wb").write(su.get_data(req))
```

Expect a file that starts with `II*` (TIFF), 3 float32 bands in reflectance, in the UTM zone of the area. Here: EPSG:32615, 832 x 780 pixels. For an index use `index="NDVI"` and no bands. Other indices: NDWI, MNDWI, NDMI, NBR, NDSI, NDRE, EVI, SAVI, BSI. Without `output`, `get_data` returns an xarray Dataset: the bands, `dataMask` and the index as variables over `y` and `x`, with `crs` and `resolution` in `attrs`. NDVI values are between -1 and 1.

## Time series over an area

```python
stats = su.get_data(su.statistical_request(area, ("2024-01-01", "2024-12-31"), index="NDVI", aggregation_interval="P1M"))
```

Expect a DataFrame with one row per interval and columns `interval_from`, `interval_to`, `output`, `mean`, `min`, `max`, `std`, `sample_count`, `no_data_count`. Here: 12 rows, `mean` about 0.2 in January and about 0.86 in July. Intervals: `P1D`, `P10D`, `P1M`, `P1Y`.

## Terrain

```python
dem = su.get_data(su.process_request(area, None, collection=su.DEM, resolution=30))
```

Expect a Dataset with variable `DEM` in metres and `dataMask`. Here: 261 x 278 pixels, 285 to 350 m. Pass `None` as the date.

## Earth Engine style chain

```python
ndvi = su.collection().filter_bounds(area).filter_date(*dates).median().index("NDVI").get_data()
```

Expect the same kind of Dataset as `get_data` of a request, with an `NDVI` variable. Nothing is read until `get_data`.

## H3 hexagons

```python
import h3
import numpy as np
import pandas as pd
from pyproj import Transformer


def ndvi_to_hex(ds, res=9):
    x, y = np.meshgrid(ds.x.values, ds.y.values)
    lon, lat = Transformer.from_crs(ds.attrs["crs"], 4326, always_xy=True).transform(x, y)
    ndvi = ds["NDVI"].values
    ok = np.isfinite(ndvi)
    cells = [h3.latlng_to_cell(la, lo, res) for la, lo in zip(lat[ok], lon[ok])]
    return pd.DataFrame({"hex": cells, "ndvi": ndvi[ok]}).groupby("hex", as_index=False).agg(
        ndvi=("ndvi", "mean"), pixels=("ndvi", "size"))


ds = su.get_data(su.process_request(area, dates, index="NDVI", resolution=60, mask="clear", reducer="median"))
hexes = ndvi_to_hex(ds)
```

Expect a DataFrame with columns `hex`, `ndvi`, `pixels`, one row per H3 cell, `ndvi` between -1 and 1. Here: 687 rows at resolution 9.

## Many requests in parallel

`su.download` runs one request per worker on Fused and returns the results in order. This gives a hexagon time series, one composite per month:

```python
months = [("2024-06-01", "2024-06-30"), ("2024-07-01", "2024-07-31")]
reqs = [su.process_request(area, m, index="NDVI", resolution=60, mask="clear", reducer="median") for m in months]
series = pd.concat([ndvi_to_hex(ds).assign(month=m[0][:7]) for ds, m in zip(su.download(reqs), months)])
```

Expect `su.download(reqs)` to return a list of Datasets, one per request, in the same order. `series` has columns `hex`, `ndvi`, `pixels`, `month`. Here: 1374 rows, 687 for each month. `su.iter_download(reqs)` gives `(i, result)` as each one finishes. Keep one request under about 60 seconds: use a coarser `resolution` or split a large area with `su.utm_zone_splitter(area, 20_000)`.

## Scale your own UDF with `.map`

```python
@fused.udf
def month_ndvi(start: str = "2024-07-01", end: str = "2024-07-31"):
    import pandas as pd

    su = fused.load("https://github.com/fusedio/udfs/tree/72d479e153f5bd74f65a1564334f8914c3df66d1/public/sentinel_utils/")
    req = su.process_request([-93.25, 41.95, -93.15, 42.02], (start, end), index="NDVI", resolution=60, mask="clear", reducer="median")
    return pd.DataFrame({"start": [start], "mean_ndvi": [float(su.get_data(req)["NDVI"].mean())]})


result = month_ndvi.map([{"start": "2024-06-01", "end": "2024-06-30"}, {"start": "2024-07-01", "end": "2024-07-31"}], engine="remote").df()
```

Expect a DataFrame with 2 rows and columns `start`, `mean_ndvi`. Here: about 0.54 for June and 0.82 for July. See [`udf.map`](https://docs.fused.io/python-sdk/api-reference/udf#map) for `max_workers` and caching.

## Errors

- No scene for the area and dates raises `NoDataError` (a `ValueError`), for example `su.get_data(su.process_request([-140.0, 0.0, -139.99, 0.01], dates, index="NDVI", resolution=60))` over open ocean: "no Sentinel-2 scene for area ... and date ...". Widen the dates or raise `cloud_cover`.
- A bad value raises `ValueError` and the message lists the allowed values.

## More examples

These pages describe the public canvases and show how each one works, with small code snippets:

- https://docs.fused.io/examples/sentinel-2-explorer: indices, composites, H3 hexagon time series and downloads, plus a JSON API.
- https://docs.fused.io/examples/sentinel-2-composite: a cloud-free composite for any map view.
- https://docs.fused.io/examples/monthly-median-composite: one composite per month, one machine per month.
- https://docs.fused.io/examples/temporal-pixel-analysis: NDVI time series for farm fields.
