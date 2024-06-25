---
sidebar_label: _public_api
title: fused._public_api
---

## get\_jobs

```python
def get_jobs(n: int = 5,
             *,
             skip: int = 0,
             per_request: int = 25,
             max_requests: Optional[int] = None) -> Jobs
```

Get the job history.

**Arguments**:

- `n` - The number of jobs to fetch. Defaults to 5.
  

**Arguments**:

- `skip` - Where in the job history to begin. Defaults to 0, which retrieves the most recent job.
- `per_request` - Number of jobs per request to fetch. Defaults to 25.
- `max_requests` - Maximum number of requests to make. May be None to fetch all jobs. Defaults to 1.
  

**Returns**:

  The job history.

## get\_udfs

```python
def get_udfs(n: int = 10,
             *,
             skip: int = 0,
             per_request: int = 25,
             max_requests: Optional[int] = None,
             by: Literal["name", "id", "slug"] = "name",
             whose: Literal["self", "public"] = "self")
```

Fetches a list of UDFs.

**Arguments**:

- `n` - The total number of UDFs to fetch. Defaults to 10.
- `skip` - The number of UDFs to skip before starting to collect the result set. Defaults to 0.
- `per_request` - The number of UDFs to fetch in each API request. Defaults to 25.
- `max_requests` - The maximum number of API requests to make.
- `by` - The attribute by which to sort the UDFs. Can be "name", "id", or "slug". Defaults to "name".
- `whose` - Specifies whose UDFs to fetch. Can be "self" for the user's own UDFs or "public" for
  UDFs available publicly. Defaults to "self".
  

**Returns**:

  A list of UDFs.
  

**Examples**:

  Fetch UDFs under the user account:
    ```py
    fused.get_udfs()
    ```

## open\_table

```python
def open_table(path: Union[str, DatasetOutputV2],
               *,
               fetch_samples: Optional[bool] = None) -> Table
```

Open a Table object given a path to the root of the table

**Arguments**:

- `path` - The path to the root of the table on remote storage
  

**Arguments**:

- `fetch_samples` - If True, fetch sample on each table when getting dataset metadata.

**Returns**:

  A Table object
  

**Examples**:

    ```py
    table = fused.open_table("s3://my_bucket/path/to/dataset/table/")
    ```

## ingest

```python
def ingest(
    input: Union[str, Sequence[str], Path, gpd.GeoDataFrame],
    output: Optional[str] = None,
    *,
    output_metadata: Optional[str] = None,
    schema: Optional[Schema] = None,
    file_suffix: Optional[str] = None,
    load_columns: Optional[Sequence[str]] = None,
    remove_cols: Optional[Sequence[str]] = None,
    explode_geometries: bool = False,
    drop_out_of_bounds: Optional[bool] = None,
    partitioning_method: Literal["area", "length", "coords", "rows"] = "rows",
    partitioning_maximum_per_file: Union[int, float, None] = None,
    partitioning_maximum_per_chunk: Union[int, float, None] = None,
    partitioning_max_width_ratio: Union[int, float] = 2,
    partitioning_max_height_ratio: Union[int, float] = 2,
    partitioning_force_utm: Literal["file", "chunk", None] = "chunk",
    partitioning_split_method: Literal["mean", "median"] = "mean",
    subdivide_method: Literal["area", None] = None,
    subdivide_start: Optional[float] = None,
    subdivide_stop: Optional[float] = None,
    split_identical_centroids: bool = True,
    target_num_chunks: int = 5000,
    lonlat_cols: Optional[Tuple[str, str]] = None,
    gdal_config: Union[GDALOpenConfig, Dict[str, Any], None] = None
) -> GeospatialPartitionJobStepConfig
```

Ingest a dataset into the Fused partitioned format.

**Arguments**:

- `input` - A GeoPandas `GeoDataFrame` or a path to file or files on S3 to ingest. Files may be Parquet or another geo data format.
- `output` - Location on S3 to write the `main` table to.
  

**Arguments**:

- `output_metadata` - Location on S3 to write the `fused` table to.
- `schema` - Schema of the data to be ingested. This is optional and will be inferred from the data if not provided.
- `file_suffix` - filter which files are used for ingestion. If `input` is a directory on S3, all files under that directory will be listed and used for ingestion. If `file_suffix` is not None, it will be used to filter paths by checking the trailing characters of each filename. E.g. pass `file_suffix=".geojson"` to include only GeoJSON files inside the directory.
- `load_columns` - Read only this set of columns when ingesting geospatial datasets. Defaults to all columns.
- `remove_cols` - The named columns to drop when ingesting geospatial datasets. Defaults to not drop any columns.
- `explode_geometries` - Whether to unpack multipart geometries to single geometries when ingesting geospatial datasets, saving each part as its own row. Defaults to `False`.
- `drop_out_of_bounds` - Whether to drop geometries outside of the expected WGS84 bounds. Defaults to True.
- `partitioning_method` - The method to use for grouping rows into partitions.
  
  - `"area"`: Construct partitions where all contain a maximum total area among geometries.
  - `"length"`: Construct partitions where all contain a maximum total length among geometries.
  - `"coords"`: Construct partitions where all contain a maximum total number of coordinates among geometries.
  - `"rows"`: Construct partitions where all contain a maximum number of rows.
  
  Defaults to `"rows"`.
  
- `partitioning_maximum_per_file` - Maximum value for `partitioning_method` to use per file. If `None`, defaults to _1/10th_ of the total value of `partitioning_method`. So if the value is `None` and `partitioning_method` is `"area"`, then each file will be have no more than 1/10th the total area of all geometries. Defaults to `None`.
- `partitioning_maximum_per_chunk` - Maximum value for `partitioning_method` to use per chunk. If `None`, defaults to _1/100th_ of the total value of `partitioning_method`. So if the value is `None` and `partitioning_method` is `"area"`, then each file will be have no more than 1/100th the total area of all geometries. Defaults to `None`.
- `partitioning_max_width_ratio` - The maximum ratio of width to height of each partition to use in the ingestion process. So for example, if the value is `2`, then if the width divided by the height is greater than `2`, the box will be split in half along the horizontal axis. Defaults to `2`.
- `partitioning_max_height_ratio` - The maximum ratio of height to width of each partition to use in the ingestion process. So for example, if the value is `2`, then if the height divided by the width is greater than `2`, the box will be split in half along the vertical axis. Defaults to `2`.
- `partitioning_force_utm` - Whether to force partitioning within UTM zones. If set to `"file"`, this will ensure that the centroid of all geometries per _file_ are contained in the same UTM zone. If set to `"chunk"`, this will ensure that the centroid of all geometries per _chunk_ are contained in the same UTM zone. If set to `None`, then no UTM-based partitioning will be done. Defaults to "chunk".
- `partitioning_split_method` - How to split one partition into children.
  
  - `"mean"`: Split each axis according to the mean of the centroid values.
  - `"median"`: Split each axis according to the median of the centroid values.
  
  Defaults to `"mean"` (this may change in the future).
  
- `subdivide_method` - The method to use for subdividing large geometries into multiple rows. Currently the only option is `"area"`, where geometries will be subdivided based on their area (in WGS84 degrees).
- `subdivide_start` - The value above which geometries will be subdivided into smaller parts, according to `subdivide_method`.
- `subdivide_stop` - The value below which geometries will never be subdivided into smaller parts, according to `subdivide_method`.
- `split_identical_centroids` - If `True`, should split a partition that has
  identical centroids (such as if all geometries in the partition are the
  same) if there are more such rows than defined in "partitioning_maximum_per_file" and
  "partitioning_maximum_per_chunk".
- `target_num_chunks` - The target for the number of files if `partitioning_maximum_per_file` is None. Note that this number is only a _target_ and the actual number of files generated can be higher or lower than this number, depending on the spatial distribution of the data itself.
- `lonlat_cols` - Names of longitude, latitude columns to construct point geometries from.
  
  If your point columns are named `"x"` and `"y"`, then pass:
  
        ```py
        fused.ingest(
            ...,
            lonlat_cols=("x", "y")
        )
        ```
  
  This only applies to reading from Parquet files. For reading from CSV files, pass options to `gdal_config`.
  
- `gdal_config` - Configuration options to pass to GDAL for how to read these files. For all files other than Parquet files, Fused uses GDAL as a step in the ingestion process. For some inputs, like CSV files or zipped shapefiles, you may need to pass some parameters to GDAL to tell it how to open your files.
  
  This config is expected to be a dictionary with up to two keys:
  
  - `layer`: `str`. Define the layer of the input file you wish to read when the source contains multiple layers, as in GeoPackage.
  - `open_options`: `Dict[str, str]`. Pass in key-value pairs with GDAL open options. These are defined on each driver's page in the GDAL documentation. For example, the [CSV driver](https://gdal.org/drivers/vector/csv.html) defines [these open options](https://gdal.org/drivers/vector/csv.html#open-options) you can pass in.
  
  For example, if you're ingesting a CSV file with two columns
  `"longitude"` and `"latitude"` denoting the coordinate information, pass
  
        ```py
        fused.ingest(
            ...,
            gdal_config={
                "open_options": {
                    "X_POSSIBLE_NAMES": "longitude",
                    "Y_POSSIBLE_NAMES": "latitude",
                }
            }
        )
        ```

**Returns**:

  
  Configuration object describing the ingestion process. Call `.run_remote` on this object to start a job.
  
  

**Examples**:

  For example, to ingest the California Census dataset for the year 2022:
    ```py
    job = fused.ingest(
        input="https://www2.census.gov/geo/tiger/TIGER_RD18/STATE/06_CALIFORNIA/06/tl_rd22_06_bg.zip",
        output="s3://fused-sample/census/ca_bg_2022/main/",
        output_metadata="s3://fused-sample/census/ca_bg_2022/fused/",
        explode_geometries=True,
        partitioning_maximum_per_file=2000,
        partitioning_maximum_per_chunk=200,
    ).run_remote()
    ```

## ingest\_nongeospatial

```python
def ingest_nongeospatial(
    input: Union[str, Sequence[str], Path, gpd.GeoDataFrame],
    output: Optional[str] = None,
    *,
    output_metadata: Optional[str] = None,
    partition_col: Optional[str] = None,
    partitioning_maximum_per_file: int = 2_500_000,
    partitioning_maximum_per_chunk: int = 65_000
) -> NonGeospatialPartitionJobStepConfig
```

Ingest a dataset into the Fused partitioned format.

**Arguments**:

- `input` - A Pandas `DataFrame` or a path to file or files on S3 to ingest. Files may be Parquet or another data format.
- `output` - Location on S3 to write the `main` table to.
  

**Arguments**:

- `output_metadata` - Location on S3 to write the `fused` table to.
- `partition_col` - Partition along this column for nongeospatial datasets.
- `partitioning_maximum_per_file` - Maximum number of items to store in a single file. Defaults to 2,500,000.
- `partitioning_maximum_per_chunk` - Maximum number of items to store in a single file. Defaults to 65,000.
  

**Returns**:

  
  Configuration object describing the ingestion process. Call `.run_remote` on this object to start a job.
  

**Examples**:

    ```py
    job = fused.ingest_nongeospatial(
        input=gdf,
        output="s3://sample-bucket/file.parquet",
    ).run_remote()
    ```

## map

```python
def map(dataset: Union[str, Dataset, Table],
        output_table: Optional[str] = None,
        udf: Union[BaseUdf, None] = None,
        *,
        cache_locally: bool = False) -> MapJobStepConfig
```

Construct a `map` config from this Table

**Arguments**:

- `output_table` - Where to save the output of this operation. Defaults to `None`, which will not save the output.
- `udf` - A user-defined function to run in this map. Defaults to None.
  

**Arguments**:

- `tables` - The attribute tables to include in the map reduce. Defaults to ("main",).
- `cache_locally` - Advanced: whether to cache all the partitions locally in the map job. Defaults to False.
  

**Returns**:

  An object describing the map configuration.

## join

```python
def join(dataset: Union[str, Dataset, Table],
         other: Union[str, Dataset, Table],
         output_table: Optional[str] = None,
         udf: Union[BaseUdf, None] = None,
         *,
         how: Union[JoinType, Literal["left", "inner"]] = "inner",
         left_cache_locally: bool = False,
         right_cache_locally: bool = False,
         buffer_distance: Optional[float] = None) -> JoinJobStepConfig
```

Construct a join config from two tables

**Arguments**:

- `other` - The other Dataset object to join on
- `output_table` - Where to save the output of this operation. Defaults to `None`, which will not save the output.
- `udf` - The user-defined function to run in the join
  

**Arguments**:

- `how` - The manner of doing the join. Currently  Defaults to "inner".
- `left_cache_locally` - Whether to cache the left dataset locally in the join. Defaults to False.
- `right_cache_locally` - Whether to cache the right dataset locally in the join. Defaults to False.
- `buffer_distance` - The size of the buffer (in meters) on the left table to use during the join. Defaults to None.
  

**Returns**:

  An object describing the join configuration.
  

**Examples**:

    ```py
    import fused

    left_table = fused.open_table("s3://bucket/path/to/table")
    other_table = fused.open_table("s3://bucket/path/to/table")
    join_config = fused.join(left_table, other_table)
    ```

## job

```python
def job(input: Union[
    str,
    Dict,
    JobStepConfig,
    JobConfig,
    Sequence[Union[Dict, JobStepConfig, JobConfig]],
],
        content_type: Optional[str] = None,
        ignore_chunk_error: bool = False) -> JobConfig
```

Construct a JobConfig

**Arguments**:

- `input` - A object or list of objects describing job steps.
- `content_type` - How to interpret `input` when it is a string. E.g. "json" for JSON or "fused_job_id" for a Fused Job ID.
  

**Returns**:

  A combined job config.

## \_whoami

```python
def _whoami()
```

Returns information on the currently logged in user

## plot

```python
def plot(gdf: gpd.GeoDataFrame,
         source: Union[str,
                       TileProvider] = cx.providers.CartoDB.DarkMatterNoLabels,
         **geopandas_kwargs: Dict[str, Any])
```

Plot a GeoDataFrame on a map using contextily to add basemap

**Arguments**:

- `gdf` - A GeoPandas `GeoDataFrame` to plot.
  source : Basemap to use. Accepts an xyzservices.TileProvider object or str.
  [Optional. Default: CartoDB DarkMatterNoLabels]
  The tile source: web tile provider, a valid input for a query of a
  :class:`xyzservices.TileProvider` by a name from ``xyzservices.providers`` or
  path to local file.
- `**geopandas_kwargs` - Additional keyword arguments to pass to `gdf.plot`.

## delete

```python
def delete(path: str,
           max_deletion_depth: Union[int, Literal["unlimited"]] = 2) -> bool
```

Delete the files at the path.

**Arguments**:

- `path` - Directory or file to delete, like `fd://my-old-table/`
- `max_deletion_depth` - If set (defaults to 2), the maximum depth the operation will recurse to.
  This option is to help avoid accidentally deleting more data that intended.
  Pass `"unlimited"` for unlimited.
  
  

**Examples**:

    ```python
    fused.delete("fd://bucket-name/deprecated_table/")
    ```

## list

```python
def list(path: str) -> List[str]
```

List the files at the path.

**Arguments**:

- `path` - Parent directory URL, like `fd://bucket-name/`
  

**Returns**:

  A list of paths as URLs
  

**Examples**:

    ```python
    fused.list("fd://bucket-name/")
    ```

## get

```python
def get(path: str) -> bytes
```

Download the contents at the path to memory.

**Arguments**:

- `path` - URL to a file, like `fd://bucket-name/file.parquet`
  

**Returns**:

  bytes of the file
  

**Examples**:

    ```python
    fused.get("fd://bucket-name/file.parquet")
    ```

## download

```python
def download(path: str, local_path: Union[str, Path]) -> None
```

Download the contents at the path to disk.

**Arguments**:

- `path` - URL to a file, like `fd://bucket-name/file.parquet`
- `local_path` - Path to a local file.

## upload

```python
def upload(local_path: Union[str, Path, bytes, BinaryIO],
           remote_path: str) -> None
```

Upload local file to S3.

**Arguments**:

- `local_path` - Either a path to a local file (`str`, `Path`) or the contents to upload.
  Any string will be treated as a Path, if you wish to upload the contents of
  the string, first encode it: `s.encode("utf-8")`
- `remote_path` - URL to upload to, like `fd://new-file.txt`
  

**Examples**:

  To upload a local json file to your Fused-managed S3 bucket:
    ```py
    fused.upload("my_file.json", "fd://my_bucket/my_file.json")
    ```

## sign\_url

```python
def sign_url(path: str) -> str
```

Create a signed URL to access the path.

This function may not check that the file represented by the path exists.

**Arguments**:

- `path` - URL to a file, like `fd://bucket-name/file.parquet`
  

**Returns**:

  HTTPS URL to access the file using signed access.
  

**Examples**:

    ```python
    fused.sign_url("fd://bucket-name/table_directory/file.parquet")
    ```

## sign\_url\_prefix

```python
def sign_url_prefix(path: str) -> Dict[str, str]
```

Create signed URLs to access all blobs under the path.

**Arguments**:

- `path` - URL to a prefix, like `fd://bucket-name/some_directory/`
  

**Returns**:

  Dictionary mapping from blob store key to signed HTTPS URL.
  

**Examples**:

    ```python
    fused.sign_url_prefix("fd://bucket-name/table_directory/")
    ```

## zip\_tables

```python
def zip_tables(
        tables: Iterable[Union[Table, str]],
        *,
        read_sidecar: Union[Sequence[str], bool] = False) -> DatasetInputV2
```

Create a job input that zips the columns of tables together. This takes the partitions from all the listed tables and combines them (as new columns) into a single DataFrame per chunk.

**Arguments**:

- `tables` - The tables to zip together
  

**Arguments**:

- `read_sidecar` - Whether to read sidecar information, either a sequence of table names (i.e. the last part of the table path) to read it from or a boolean which will be applied to all tables (default False).

## union\_tables

```python
def union_tables(
        tables: Iterable[Union[Table, str]],
        *,
        read_sidecar: Union[Sequence[str], bool] = False) -> DatasetInputV2
```

Create a job input that unions the partitions of tables together. This takes the partitions from all the listed tables (which should have the same schema) and runs the operation over each partition.

**Arguments**:

- `tables` - The tables to union together
  

**Arguments**:

- `read_sidecar` - Whether to read sidecar information, either a sequence of table names (i.e. the last part of the table path) to read it from or a boolean which will be applied to all tables (default False).

