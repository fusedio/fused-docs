# Partition data with `fused.h3.partition`

Setup and the end-to-end example (`nyc311_day`) are in https://docs.fused.io/skills/H3.md.

## Sources

- `fused.h3.sources.udf(my_udf)`: a UDF that returns the rows. Use this for data you have in Python.
- `fused.h3.sources.era5(outputs=[...], date=..., bbox=...)`: ERA5 weather, with `fill="nearest"`.
- A folder path on `fd://`, `s3://` or `gs://`, or `fused.h3.sources.parquet(path)`: Parquet already in storage.

## How rows get a cell

Pass exactly one of `point_column` and `hex_column`. Data with both a cell column and a geometry needs only `hex_column`, and the geometry stays in the files.

- Latitude and longitude: `point_column=("lat", "lon")`, in degrees (EPSG:4326). Projected coordinates raise.
- A WKB geometry column, such as building polygons: `point_column="geometry"`. Each row gets the cell of its centroid; nothing is polyfilled. A GeoDataFrame returned by a source UDF arrives as WKB.
- An H3 cell column (uint64) with any name: `hex_column="my_cells"`. The cells are kept as they are and `h3_res` does not change them. The output column is always `hex`.

## Parameters

- `h3_res` (default 7): the resolution of each row's cell, which queries select by. Set it from the size of your features: https://docs.fused.io/guide/h3-analytics/resolution-guide. Res 11, about 25 m across, fits buildings and street-level points.
- `file_res` (default 1): the parent cell that groups rows into one file. Raise it for more, smaller files, so a query reads less.
- `partition_by`: nonspatial columns such as `date` or `scenario`, never location. Each value becomes a `col=value` folder, so values must not be null or empty, contain `/` or start with `_`. Pick the column queries filter on, and avoid one where a single value holds most rows: a query for it still reads almost every file. A column name, or a list of them, takes the folders from the data in one job; a dict splits the run into one job per value (below).
- `engine`: `"small"` (the default, 2 vCPUs, 2 GB), `"medium"` (16 vCPUs, 64 GB) or `"large"` (64 vCPUs, 512 GB), all batch jobs with no time limit. `"realtime"` starts at once but stops after 2 minutes, so it suits only small Parquet sources; a UDF source raises with it.
- `read_engine="large"` for large reads.
- `options`: tuning as a dict, such as `{"row_group_size": 65536, "workers": 4}`. An unknown key raises. A partition running out of memory: `{"workers": 2}`; 2 to 4 works.
- Hundreds of GB or tens of thousands of files: contact info@fused.io.

## Running again

- With column names in `partition_by`, every run reads the source again and replaces the folders it writes; all other folders stay.
- With a dict `partition_by`, jobs already done are skipped.
- Without `partition_by`, a run into an existing output raises, and `redo=True` replaces it.
- To change `h3_res`, `file_res`, `fill`, `sort_by` or the partition columns, write to a new output path; a run whose settings differ from the existing output raises.

## One job per value

Give the source UDF a parameter and pass its values as `partition_by={"date": [...]}`. Each value becomes one job, bound to the UDF's `date` parameter, and the jobs run in parallel.

```python
import fused
import pandas as pd

days = pd.date_range("2024-07-04", "2024-07-05").strftime("%Y-%m-%d")
run = fused.h3.partition(
    fused.h3.sources.udf(nyc311_day),
    "fd://h3_examples/nyc311_days/",
    point_column=("latitude", "longitude"),
    h3_res=11,
    partition_by={"date": days},
)
run.tail()
```

Expect `started run grp:... (2 jobs)`, with jobs `date=2024-07-04` and `date=2024-07-05`, about 2 minutes.

- Each key must be a column the source returns (`date` here). Otherwise the job fails with `... returned no 'date' column; partition keys must be output columns`.
- `run.errors()` only says `Batch job ... ended with status Failed`; `run.tail()` prints the cause. `run.retry()` runs the failed jobs again and leaves the others alone.
- Running again skips jobs that are already done, so adding a day costs one job; then index only the new folder with `subset` (https://docs.fused.io/skills/h3/index.md). `redo=True` reads those jobs again and rewrites them.
- A list of dicts, such as `[{"date": "2024-07-04"}, {"date": "2024-07-05"}]`, is an explicit job list. Every dict needs the same keys.
- A run started elsewhere (for example inside a UDF that returned `run.id`): `fused.h3.get_run(run_id).status()`.

## Old arguments

Old code still works for one release and warns. `parts=` is now `partition_by`, `force=` and `refresh=` are `redo=True`, `append=` can go (a rerun merges), `only=` means passing only those values, and the one-by-one tuning arguments go in `options`. `overwrite=` has no replacement: write to a new output path, since `redo=True` never clears old folders.
