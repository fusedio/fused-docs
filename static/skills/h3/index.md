# Index a dataset with `fused.h3.index`

Setup and the end-to-end example are in https://docs.fused.io/skills/H3.md.

```python
fused.h3.index(path).tail()
status = fused.h3.index_status(path)
```

Expect `status` to be a dict: `status` `'ready'`, `visibility` `'team'`, `files` 1, `resolution` 11, `hex_column` `'hex'`, `partition_columns` `[{'name': 'date', 'type': 'string', 'distinct': 1, 'min': '2024-07-04', 'max': '2024-07-04'}]`, plus `time_min`, `time_max`, `row_groups`, `failures`. A query before the run finishes gets `This location is still 'indexing'`.

- `time_column="name"`: a timestamp column inside the files.
- `engine`: the default `"realtime"` stops after 2 minutes. When a run times out, pass a batch instance with no time limit: `"small"` (2 vCPUs, 2 GB), `"medium"` (16 vCPUs, 64 GB) or `"large"` (64 vCPUs, 512 GB).
- New data: run index again. It indexes only new, changed and removed files and skips unchanged folders. On a large dataset, pass `subset={"date": "2024-07-06"}` (a value or a list of them) so index lists only those folders; the keys must be the leading partition columns.
- `redo=True` reads files again: with `subset`, only the files in those folders; without it, the whole tree from scratch, which is also how to change the dataset's columns.
- Parquet not written by partition: every file must have an integer H3 cell column at one resolution; name it with `hex_column` if it is not `hex`.
- Old code: `prefix=` (use `subset=`), `overwrite=` and `force=` (use `redo=True`) and `workers=` (use `options={"workers": ...}`) still work and warn. `delete_index` and `indexed_files` still take `prefix=`, a folder.

`index_status` also works on a public dataset you did not build. Expect `fused.h3.index_status("s3://fused-asset/data/nyc311/")` to give `files` 1923, `resolution` 11, `partition_columns` `[{'name': 'month', 'type': 'string', 'distinct': 192, 'min': '2010-01', 'max': '2025-12'}]`, `time_min` `'2010-01-01T00:00:00'`.

## List or remove indexed files

```python
files = list(fused.h3.indexed_files(path))
fused.h3.delete_index(path, prefix="date=2024-07-04")
fused.h3.index(path).tail()
```

Expect `files` to hold one path ending in `date=2024-07-04/812a3ffffffffff.parquet`. `delete_index` with `prefix` drops only that folder from the index and returns `count` 1 and `folders` 1. The Parquet files stay, and `index_status` shows `files` 0 until the last line indexes the folder again. Without `prefix` the whole index is deleted.
