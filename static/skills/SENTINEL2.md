# Sentinel-2 on Fused

Use `sentinel_utils` for Sentinel-2 L2A: scene search, cloud-free composites, indices (NDVI and more), time series, GeoTIFF export and H3 hexagons. Every call runs on the user's own Fused account. Never call a canvas share link from code: it runs as the canvas owner.

## Set up

```bash
pip install fused h3 nest_asyncio
fused login          # opens the browser; check with `fused whoami`
```

```python
import fused

su = fused.load("https://github.com/fusedio/udfs/tree/72d479e153f5bd74f65a1564334f8914c3df66d1/public/sentinel_utils/")
area = [-93.25, 41.95, -93.15, 42.02]  # [west, south, east, north], EPSG:4326
dates = ("2024-07-01", "2024-07-31")
```

Keep a commit in the URL so the code does not change under you. To upgrade, change the commit. `su.api()` lists every function with its signature and doc.

## Search scenes

```python
scenes = su.query(area, dates, cloud_cover=20)  # GeoDataFrame: id, datetime, tile_id, cloud_cover, assets, geometry
```

## Composite or index image, saved as GeoTIFF

```python
req = su.process_request(area, dates, ["B04", "B03", "B02"], resolution=10, mask="clear", reducer="median", output="geotiff")
open("rgb.tif", "wb").write(su.get_data(req))
```

For an index use `index="NDVI"` and no bands. Other indices: NDWI, MNDWI, NDMI, NBR, NDSI, NDRE, EVI, SAVI, BSI. `mosaic_order="clearest_day"` takes one date over the whole area. Without `output`, `get_data` returns an xarray Dataset.

## Time series over an area

```python
stats = su.get_data(su.statistical_request(area, ("2024-01-01", "2024-12-31"), index="NDVI", aggregation_interval="P1M"))
```

One row per interval with `mean`, `min`, `max`, `std` and `sample_count`. Intervals: `P1D`, `P10D`, `P1M`, `P1Y`.

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
hexes = ndvi_to_hex(ds)  # columns: hex, ndvi, pixels
```

## Many requests in parallel

`su.download` runs one request per worker on Fused and returns the results in order. This gives a hexagon time series, one composite per month:

```python
months = [("2024-06-01", "2024-06-30"), ("2024-07-01", "2024-07-31")]
reqs = [su.process_request(area, m, index="NDVI", resolution=60, mask="clear", reducer="median") for m in months]
series = pd.concat([ndvi_to_hex(ds).assign(month=m[0][:7]) for ds, m in zip(su.download(reqs), months)])
```

`su.iter_download(reqs)` gives each result as it finishes. Keep one request under about 60 seconds: use a coarser `resolution` or split a large area with `su.utm_zone_splitter(area, 20_000)`.

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

See [`udf.map`](https://docs.fused.io/python-sdk/api-reference/udf#map) for `max_workers` and caching.

## Pull the example canvases and check the pull worked

The public canvases `Sentinel2_Toolkit` (the library and twelve examples) and `Sentinel2_Explorer` (indices, composites, H3 hexagon time series and downloads built on `sentinel_utils`) are worth reading.

```bash
fused canvas pull --team Sentinel2_Toolkit -o Sentinel2_Toolkit    # a canvas in your team
fused canvas pull Sentinel2_Toolkit -o Sentinel2_Toolkit           # a canvas in your own account
ls Sentinel2_Toolkit
fused canvas validate Sentinel2_Toolkit
```

The pull worked when `ls` shows `canvas.toml`, `README.md`, `su_search.py`, `su_read.py`, `su_analysis.py` and the `ex_*.py` examples, and `validate` prints `Canvas is valid.` For `Sentinel2_Explorer` expect `sentinel_api.py`, `sentinel_core.py`, `sentinel_products.py` and `sentinel_explorer.json`. Read `README.md` first, then the `ex_*.py` files (search, time series, timelapse, classification, change detection, embeddings).

If the pull fails with `Could not resolve canvas by name`, the canvas is not in your account or team. Do not guess a name. Tell the user, and ask them to open https://www.fused.io/canvas/fc_fused/Sentinel2_Toolkit, export the canvas as a zip from Workbench and unzip it: the zip has the same layout as a pull.
