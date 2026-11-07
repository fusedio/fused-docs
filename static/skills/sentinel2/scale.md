# Scale Sentinel-2 work on Fused

Setup (`su`, `area`, `dates`) is in https://docs.fused.io/skills/SENTINEL2.md.

## Many requests in parallel

- `su.download(reqs)` runs one request per worker on Fused and returns a list of results, one per request, in the same order. A worked example, one composite per month: https://docs.fused.io/skills/sentinel2/h3.md
- `su.iter_download(reqs)` gives `(i, result)` as each one finishes.
- Keep one request under about 60 seconds: use a coarser `resolution`, or split a large area with `su.utm_zone_splitter(area, 20_000)`.

## Your own UDF with `.map`

```python
@fused.udf
def month_ndvi(start: str = "2024-07-01", end: str = "2024-07-31"):
    import pandas as pd

    su = fused.load("https://github.com/fusedio/udfs/tree/72d479e153f5bd74f65a1564334f8914c3df66d1/public/sentinel_utils/")
    req = su.process_request([-93.25, 41.95, -93.15, 42.02], (start, end), index="NDVI", resolution=60, mask="clear", reducer="median")
    return pd.DataFrame({"start": [start], "mean_ndvi": [float(su.get_data(req)["NDVI"].mean())]})


result = month_ndvi.map([{"start": "2024-06-01", "end": "2024-06-30"}, {"start": "2024-07-01", "end": "2024-07-31"}], engine="remote").df()
```

Expect a DataFrame with 2 rows and columns `start`, `mean_ndvi`. Here: about 0.54 for June and 0.82 for July. `max_workers` and caching: https://docs.fused.io/python-sdk/api-reference/udf#map
