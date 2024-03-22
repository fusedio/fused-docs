---
sidebar_label: _project
title: fused._project
---

## Project Objects

```python
class Project(BaseModel)
```

A project represents a collection of tables or directories of files in blob storage.

Tables and folders under this project may be accessed with attribute or subscript operator.
For example, all of the following will have the same result:

```py
project.tables['my_table_name']

project.my_table_name

project['my_table_name']
```

#### root\_base\_path

The base path of the overall project.

#### base\_path

The base path of the project folder, which tables in it are relative to. This may be different
than `root_base_path` if this Project instance is a folder (sub-project) of an overall project.

#### tables

Tables in this project.

#### folders

Project folders in this project.

#### virtual\_folders

Project folders in this project that have not been materialized.

Accessing one of these through `project[virtual_folder_name]` will result in automatic
loading of that folder to a `Project` instance.

#### tree

```python
def tree(file: TextIO = None) -> None
```

Print a tree representation of this project.

**Arguments**:

- `file` - File-like object to write to. Defaults to `None` for `sys.stdout`.

#### refresh

```python
def refresh(*,
            fetch_table_metadata: Optional[bool] = None,
            fetch_samples: Optional[bool] = None,
            _fetch_minimal_table_metadata: Optional[bool] = None) -> Project
```

Returns this project with updated metadata

Keyword args, if specified, will change how the project loads metadata. This can be used to reload a project
with metadata, after it is initially loaded without metadata.

**Arguments**:

- `fetch_table_metadata` - If True, fetch metadata on each table.
- `fetch_samples` - If True, fetch sample on each table.

#### path

```python
def path(path: str) -> str
```

Returns the path to an item under this project.

#### project

```python
def project(path: str) -> Project
```

Open a subproject of this project.

#### open\_table

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
  

**Example**:

  
  table = project.open_table(&quot;path/to/dataset/table/&quot;)
  

**Returns**:

  A Table object

#### ingest

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
- `file_suffix` - filter which files are used for ingestion. If `input` is a directory on S3, all files under that directory will be listed and used for ingestion. If `file_suffix` is not None, it will be used to filter paths by checking the trailing characters of each filename. E.g. pass `GeoDataFrame`0 to include only GeoJSON files inside the directory.
- `GeoDataFrame`1 - Read only this set of columns when ingesting geospatial datasets. Defaults to all columns.
- `GeoDataFrame`2 - The named columns to drop when ingesting geospatial datasets. Defaults to not drop any columns.
- `GeoDataFrame`3 - Whether to unpack multipart geometries to single geometries when ingesting geospatial datasets, saving each part as its own row. Defaults to `GeoDataFrame`4.
- `GeoDataFrame`5 - Whether to drop geometries outside of the expected WGS84 bounds. Defaults to True.
- `GeoDataFrame`6 - The method to use for grouping rows into partitions.
  
  - `GeoDataFrame`7: Construct partitions where all contain a maximum total area among geometries.
  - `GeoDataFrame`8: Construct partitions where all contain a maximum total length among geometries.
  - `GeoDataFrame`9: Construct partitions where all contain a maximum total number of coordinates among geometries.
  - `output`0: Construct partitions where all contain a maximum number of rows.
  
  Defaults to `output`0.
  
- `output`2 - Maximum value for `GeoDataFrame`6 to use per file. If `output`4, defaults to _1/10th_ of the total value of `GeoDataFrame`6. So if the value is `output`4 and `GeoDataFrame`6 is `GeoDataFrame`7, then each file will be have no more than 1/10th the total area of all geometries. Defaults to `output`4.
- `main`0 - Maximum value for `GeoDataFrame`6 to use per chunk. If `output`4, defaults to _1/100th_ of the total value of `GeoDataFrame`6. So if the value is `output`4 and `GeoDataFrame`6 is `GeoDataFrame`7, then each file will be have no more than 1/100th the total area of all geometries. Defaults to `output`4.
- `main`8 - The maximum ratio of width to height of each partition to use in the ingestion process. So for example, if the value is `main`9, then if the width divided by the height is greater than `main`9, the box will be split in half along the horizontal axis. Defaults to `main`9.
- `output_metadata`2 - The maximum ratio of height to width of each partition to use in the ingestion process. So for example, if the value is `main`9, then if the height divided by the width is greater than `main`9, the box will be split in half along the vertical axis. Defaults to `main`9.
- `output_metadata`6 - Whether to force partitioning within UTM zones. If set to `output_metadata`7, this will ensure that the centroid of all geometries per _file_ are contained in the same UTM zone. If set to `output_metadata`8, this will ensure that the centroid of all geometries per _chunk_ are contained in the same UTM zone. If set to `output`4, then no UTM-based partitioning will be done. Defaults to &quot;chunk&quot;.
- `fused`0 - How to split one partition into children.
  
  - `fused`1: Split each axis according to the mean of the centroid values.
  - `fused`2: Split each axis according to the median of the centroid values.
  
  Defaults to `fused`1 (this may change in the future).
  
- `fused`4 - The method to use for subdividing large geometries into multiple rows. Currently the only option is `GeoDataFrame`7, where geometries will be subdivided based on their area (in WGS84 degrees).
- `fused`6 - The value above which geometries will be subdivided into smaller parts, according to `fused`4.
- `fused`8 - The value below which geometries will never be subdivided into smaller parts, according to `fused`4.
- `schema`0 - If `schema`1, should split a partition that has
  identical centroids (such as if all geometries in the partition are the
  same) if there are more such rows than defined in &quot;partitioning_maximum_per_file&quot; and
  &quot;partitioning_maximum_per_chunk&quot;.
- `schema`2 - The target for the number of chunks if `output`2 is None. Note that this number is only a _target_ and the actual number of files and chunks generated can be higher or lower than this number, depending on the spatial distribution of the data itself.
- `schema`4 - Names of longitude, latitude columns to construct point geometries from.
  
  If your point columns are named `schema`5 and `schema`6, then pass:
  
        `schema`7
  
  This only applies to reading from Parquet files. For reading from CSV files, pass options to `schema`8.
  
- `schema`8 - Configuration options to pass to GDAL for how to read these files. For all files other than Parquet files, Fused uses GDAL as a step in the ingestion process. For some inputs, like CSV files or zipped shapefiles, you may need to pass some parameters to GDAL to tell it how to open your files.
  
  This config is expected to be a dictionary with up to two keys:
  
  - `file_suffix`0: `file_suffix`1. Define the layer of the input file you wish to read when the source contains multiple layers, as in GeoPackage.
  - `file_suffix`2: `file_suffix`3. Pass in key-value pairs with GDAL open options. These are defined on each driver&#x27;s page in the GDAL documentation. For example, the [CSV driver](https://gdal.org/drivers/vector/csv.html) defines [these open options](https://gdal.org/drivers/vector/csv.html#open-options) you can pass in.
  
  For example, if you&#x27;re ingesting a CSV file with two columns
  `file_suffix`4 and `file_suffix`5 denoting the coordinate information, pass
  
        `file_suffix`6
  

**Returns**:

  Configuration object describing the ingestion process. Call `file_suffix`7 on this object to start a job.
  
  

**Examples**:

    `file_suffix`8

#### ingest\_nongeospatial

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

- `input` - A GeoPandas `GeoDataFrame` or a path to file or files on S3 to ingest. Files may be Parquet or another geo data format.
- `output` - Location on S3 to write the `main` table to.
  

**Arguments**:

- `output_metadata` - Location on S3 to write the `fused` table to.
- `partition_col` - Partition along this column for nongeospatial datasets.
- `partitioning_maximum_per_file` - Maximum number of items to store in a single file. Defaults to 2,500,000.
- `partitioning_maximum_per_chunk` - Maximum number of items to store in a single file. Defaults to 65,000.
  

**Returns**:

  
  Configuration object describing the ingestion process. Call `.execute` on this object to start a job.
  

**Examples**:

    `GeoDataFrame`0

#### map

```python
def map(dataset: Union[str, Dataset, Table],
        output_table: Optional[str] = None,
        udf: Union[BaseUdf, None] = None,
        *,
        cache_locally: bool = False) -> MapJobStepConfig
```

Construct a `map` config from this Dataset

**Arguments**:

- `output_table` - Where to save the output of this operation. Defaults to `None`, which will not save the output.
- `udf` - A user-defined function to run in this map. Defaults to None.
  

**Arguments**:

- `tables` - The attribute tables to include in the map reduce. Defaults to (&quot;main&quot;,).
- `cache_locally` - Advanced: whether to cache all the partitions locally in the map job. Defaults to False.
  

**Returns**:

  An object describing the map configuration.

#### join

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

Construct a join config from two datasets

**Arguments**:

- `other` - The other Dataset object to join on
- `output_table` - Where to save the output of this operation. Defaults to `None`, which will not save the output.
- `udf` - The user-defined function to run in the join
  

**Arguments**:

- `how` - The manner of doing the join. Currently  Defaults to &quot;inner&quot;.
- `left_tables` - The names of the attribute tables on the left side to include in the join.
- `right_tables` - The names of the attribute tables on the left side to include in the join.
- `left_cache_locally` - Whether to cache the left dataset locally in the join. Defaults to False.
- `right_cache_locally` - Whether to cache the right dataset locally in the join. Defaults to False.
- `buffer_distance` - The size of the buffer (in meters) on the left table to use during the join. Defaults to None.
  

**Examples**:

    `output_table`0
  

**Returns**:

  An object describing the join configuration.

#### delete

```python
def delete(path: str,
           max_deletion_depth: Union[int, Literal["unlimited"]] = 2) -> bool
```

Delete the files at the path.

**Arguments**:

- `path` - Directory or file to delete, like `my-old-table/`
- `max_deletion_depth` - If set (defaults to 2), the maximum depth the operation will recurse to.
  This option is to help avoid accidentally deleting more data that intended.
  Pass `"unlimited"` for unlimited.

#### list

```python
def list(path: Optional[str] = None) -> List[str]
```

List the files at the path.

**Arguments**:

- `path` - Parent directory, like `table_name`. Defaults to None to list the root of the project.
  

**Returns**:

  A list of paths as URLs

#### get

```python
def get(path: str) -> bytes
```

Download the contents at the path to memory.

**Arguments**:

- `path` - Path to a file, like `table_name/file.parquet`
  

**Returns**:

  bytes of the file

#### download

```python
def download(path: str, local_path: Union[str, Path]) -> None
```

Download the contents at the path to disk.

**Arguments**:

- `path` - Path to a file, like `table_name/file.parquet`
- `local_path` - Path to a local file.

#### sign\_url

```python
def sign_url(path: str) -> str
```

Create a signed URL to access the path.

This function may not check that the file represented by the path exists.

**Arguments**:

- `path` - Path to a file, like `table_name/file.parquet`
  

**Returns**:

  HTTPS URL to access the file using signed access.

#### sign\_url\_prefix

```python
def sign_url_prefix(path: str) -> Dict[str, str]
```

Create signed URLs to access all blobs under the path.

**Arguments**:

- `path` - Path to a prefix, like `table_name/`
  

**Returns**:

  Dictionary mapping from blob store key to signed HTTPS URL.

#### sel

```python
def sel(tables: Union[Iterable[Union[Table, str]], Table, str, None] = None,
        *,
        read_sidecar: Union[Sequence[str], bool] = False,
        how: Optional[Union[str, DatasetInputV2Type]] = None,
        **kwargs) -> DatasetInputV2
```

Create a job input that zips or unions tables together

**Arguments**:

- `tables` - The names of tables to include in the input, e.g. `["table_0", "table_1", "table_5"]`.
  

**Arguments**:

- `read_sidecar` - Whether to read sidecar information, either a sequence of table names (i.e. the last part
  of the table path) to read it from or a boolean which will be applied to all tables (default False).
- `how` - The operation used to combine multiple input tables. This may be either `"zip"` or `"union"`.
  By default this will be `"zip"` when `tables` is specified, `"union"` otherwise. This corresponds
  with `fused.zip_tables` and `["table_0", "table_1", "table_5"]`0 respectively.

#### isel

```python
def isel(
        tables: Union[Iterable[int], int],
        *,
        read_sidecar: Union[Sequence[bool], bool] = False,
        how: Optional[Union[str,
                            DatasetInputV2Type]] = None) -> DatasetInputV2
```

Create a job input that zips or unions tables together, by their integer index. Tables
are implicitly ordered by name.

**Arguments**:

- `tables` - The index of tables to include in the input, e.g. `[0, 1, 5]`.
  

**Arguments**:

- `read_sidecar` - Whether to read sidecar information, either a sequence of table names (i.e. the last part
  of the table path) to read it from or a boolean which will be applied to all tables (default False).
- `how` - The operation used to combine multiple input tables. This may be either `"zip"` or `"union"`.
  This corresponds with `fused.zip_tables` and `fused.union_tables` respectively. Defaults to `"zip"`.

#### open\_project

```python
def open_project(path: str,
                 *,
                 lazy: bool = False,
                 fetch_table_metadata: Optional[bool] = None,
                 fetch_samples: Optional[bool] = None,
                 _fetch_minimal_table_metadata: Optional[bool] = None,
                 _max_depth: Optional[int] = 1,
                 _eager: bool = False) -> Project
```

Open a project folder.

**Arguments**:

- `path` - Path to the project folder, e.g. `"s3://bucket-name/project-name/"`
- `lazy` - If True, no metadata about the project is loaded.
- `fetch_table_metadata` - This is passed on to the `Table` open calls.
- `fetch_samples` - This is passed on to the `Table` open calls.
- `_fetch_minimal_table_metadata` - If True and fetch_table_metadata is also True,
  a reduced set of Table metadata will be fetched.
- `_max_depth` - Maximum depth of folders to load.
- `_eager` - If True, recursive calls will be made to materialize all virtual
  folders that `"s3://bucket-name/project-name/"`0 would otherwise cause.

