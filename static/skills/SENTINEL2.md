---
name: fused-sentinel2
description: Use when working with Sentinel-2 L2A imagery on Fused through `sentinel_utils`: scene search, cloud-free composites, NDVI and other indices, area time series, terrain, GeoTIFF export, H3 hexagons, or many requests in parallel.
---

# Sentinel-2 on Fused

`sentinel_utils` covers Sentinel-2 L2A: scene search, cloud-free composites, indices (NDVI and more), time series, terrain, GeoTIFF export and H3 hexagons. Rules for every Fused task (accounts, errors, expected outputs): https://docs.fused.io/skills/SKILL.md

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

Keep a commit in the URL so the code does not change under you; to upgrade, change the commit. `su.api()` lists every function with its signature and doc (77 rows: module, name, signature, doc).

## Search scenes

```python
scenes = su.query(area, dates, cloud_cover=20)
days = su.clearest_days(su.query(area, dates), area)
```

- `scenes`: a GeoDataFrame, one row per scene, oldest first, with columns `id`, `datetime`, `date`, `tile_id`, `platform`, `cloud_cover`, `nodata_pct`, `crs`, `source`, `offset`, `assets`, `geometry`. Here: 1 row, tile `15TVG`, 2024-07-29, about 14 % cloud.
- `days`: a DataFrame with columns `date`, `scenes`, `cover_pct`, `cloud_cover`, `clear_pct`, the best day first. Here: 6 rows, first date 2024-07-29 with `clear_pct` about 86. `mosaic_order="clearest_day"` in `process_request` builds one image from that day.

## Composite or index image, saved as GeoTIFF

```python
req = su.process_request(area, dates, ["B04", "B03", "B02"], resolution=10, mask="clear", reducer="median", output="geotiff")
open("rgb.tif", "wb").write(su.get_data(req))
```

Expect a file that starts with `II*` (TIFF), 3 float32 bands in reflectance, in the UTM zone of the area. Here: EPSG:32615, 832 x 780 pixels.

- For an index, pass `index="NDVI"` and no bands. Others: NDWI, MNDWI, NDMI, NBR, NDSI, NDRE, EVI, SAVI, BSI. NDVI values are between -1 and 1.
- Without `output`, `get_data` returns an xarray Dataset: the bands, `dataMask` and the index as variables over `y` and `x`, with `crs` and `resolution` in `attrs`.
- Earth Engine style, read only at `get_data`: `su.collection().filter_bounds(area).filter_date(*dates).median().index("NDVI").get_data()` gives the same kind of Dataset.

## Time series over an area

```python
stats = su.get_data(su.statistical_request(area, ("2024-01-01", "2024-12-31"), index="NDVI", aggregation_interval="P1M"))
```

Expect a DataFrame with one row per interval and columns `interval_from`, `interval_to`, `output`, `mean`, `min`, `max`, `std`, `sample_count`, `no_data_count`. Here: 12 rows, `mean` about 0.2 in January and about 0.86 in July. Intervals: `P1D`, `P10D`, `P1M`, `P1Y`.

## Terrain

```python
dem = su.get_data(su.process_request(area, None, collection=su.DEM, resolution=30))
```

Pass `None` as the date. Expect a Dataset with variable `DEM` in metres and `dataMask`. Here: 261 x 278 pixels, 285 to 350 m.

## Errors

- No scene for the area and dates raises `NoDataError` (a `ValueError`): "no Sentinel-2 scene for area ... and date ...", for example over open ocean at `[-140.0, 0.0, -139.99, 0.01]`. Widen the dates or raise `cloud_cover`.
- A bad value raises `ValueError`, and the message lists the allowed values.

## More

- **H3 hexagons**: NDVI per H3 cell, from one composite or one per month → https://docs.fused.io/skills/sentinel2/h3.md
- **Scale**: many requests in parallel, a large area, your own UDF over many dates → https://docs.fused.io/skills/sentinel2/scale.md
- **Examples** (public canvases): indices, composites, hexagon time series and a JSON API https://docs.fused.io/examples/sentinel-2-explorer; a cloud-free composite for any map view https://docs.fused.io/examples/sentinel-2-composite; one composite per month https://docs.fused.io/examples/monthly-median-composite; NDVI time series for farm fields https://docs.fused.io/examples/temporal-pixel-analysis
