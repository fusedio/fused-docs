---
sidebar_label: _download
title: fused.core._download
---

## file\_path

```python
def file_path(file_path: str, mkdir: bool = True) -> str
```

Creates a directory in a predefined temporary directory.

This gives users the ability to manage directories during the execution of a UDF. It takes a relative file_path,
creates the corresponding directory structure, and returns its absolute path.

This is useful for UDFs that temporarily store intermediate results as files,
such as when writing intermediary files to disk when processing large datasets.
file_path ensures that necessary directories exist.

**Arguments**:

- `file_path` - The file path to locate.
- `mkdir` - If True, create the directory if it doesn't already exist. Defaults to True.


**Returns**:

  The located file path.

## download

```python
def download(url: str, file_path: str) -> str
```

Download a file.

May be called from multiple processes with the same inputs to get the same result.

Fused runs UDFs from top to bottom each time code changes. This means objects in the UDF are recreated each time, which can slow down a UDF that downloads files from a remote server.

💡 Downloaded files are written to a mounted volume shared across all UDFs in an organization. This means that a file downloaded by one UDF can be read by other UDFs.

Fused addresses the latency of downloading files with the download utility function. It stores files in the mounted filesystem so they only download the first time.

💡 Because a Tile UDF runs multiple chunks in parallel, the download function sets a signal lock during the first download attempt, to ensure the download happens only once.

**Arguments**:

- `url` - The URL to download.
- `file_path` - The local path where to save the file.


**Returns**:

  The function downloads the file only on the first execution, and returns the file path.


**Examples**:

    ```python
    @fused.udf
    def geodataframe_from_geojson():
        import geopandas as gpd
        url = "s3://sample_bucket/my_geojson.zip"
        path = fused.core.download(url, "tmp/my_geojson.zip")
        gdf = gpd.read_file(path)
        return gdf
    ```

## \_run\_once

```python
def _run_once(signal_name: str, fn: Callable) -> None
```

Run a function once, waiting for another process to run it if in progress.

**Arguments**:

- `signal_key` - A relative key for signalling done status. Files are written using `file_path` and this key to deduplicate runs.
- `fn` - A function that will be run once.
