---
sidebar_label: dataset
title: fused.models.api.dataset
---

## JobMetadata Objects

```python
class JobMetadata(FusedBaseModel)
```

#### ec2\_instance\_type

The EC2 instance this job is run on.

#### time\_taken

The time taken for the job, if known.

#### job\_id

The fused id for the job.

#### job

```python
@property
def job() -> JobStepConfig
```

The job step config that created this table.

#### udf

```python
@property
def udf() -> Optional[BaseUdf]
```

The user-defined function that created this table.

#### udf\_code

```python
@property
def udf_code() -> Optional[str]
```

The code string of the user-defined function that created this table.

#### inputs

```python
@property
def inputs() -> Tuple[DatasetInput, ...]
```

The datasets that were combined to create this table.

## Table Objects

```python
class Table(FusedBaseModel, FusedProjectAware)
```

#### url

URL of the table.

#### name

The name of the table.

#### table\_schema

The Schema representing this table.

#### parent

Metadata for the job that created this table.

#### column\_names

The list of column names in the table.

#### num\_rows

The number of rows in the table.

#### num\_files

The number of **non-empty** files.

#### num\_chunks

The number of **non-empty** chunk.

#### status

A status of the table.

#### chunk\_metadata

Descriptive information about each chunk in this table

#### columns

```python
@property
def columns() -> List[str]
```

The list of columns in this table

#### metadata\_gdf

```python
@property
def metadata_gdf() -> gpd.GeoDataFrame
```

The metadata of all chunks as a GeoDataFrame

#### get\_chunk

```python
def get_chunk(file_id: str | int | None = None,
              chunk_id: int | None = None) -> gpd.GeoDataFrame
```

Fetch a single chunk from this table

**Arguments**:

- `file_id` - The identifier of this file. Defaults to None.
- `chunk_id` - The numeric index of the chunk within the file to fetch. Defaults to None.
  

**Returns**:

  
  A `DataFrame` retrieved from the given file, chunk, and tables.

#### get\_dataframe

```python
def get_dataframe(file_id: str | int | None = None,
                  chunk_id: int | None = None,
                  parallel_fetch: bool = True) -> gpd.GeoDataFrame
```

Fetch multiple chunks from this table as a dataframe

**Arguments**:

- `file_id` - The identifier of the file to download. If `None` is passed, all files will be chosen. Defaults to 0.
- `chunk_id` - The numeric index of the chunk within the file to fetch. If `None` is passed, all chunks for the given file(s) will be chosen. Defaults to 0.
- `parallel_fetch` - Fetch in parallel. Defaults to True.
  

**Raises**:

- `ValueError` - If the function would fetch more than `max_rows` rows.
  

**Returns**:

  A `DataFrame` with all chunks concatenated together.

#### get\_dataframe\_bbox

```python
def get_dataframe_bbox(
        minx: float,
        miny: float,
        maxx: float,
        maxy: float,
        n_rows: Optional[int] = None,
        columns: Optional[List[str]] = None,
        clip: bool = True,
        buffer: Optional[float] = None
) -> Union[pd.DataFrame, gpd.GeoDataFrame]
```

Get a DataFrame of this Table of data in partitions matching the bounding box.

**Arguments**:

- `minx` - Left coordinate of the box.
- `miny` - Bottom coordinate of the box.
- `maxx` - Right coordinate of the box.
- `maxy` - Top coordinate of the box.
- `n_rows` - If not None, up to this many rows will be returned.
- `columns` - If not None, only return these columns.
- `clip` - If True, only geometries that intersect the bounding box will be returned.
- `buffer` - If not None, this will be applied as the buffer for the partitions.

#### join

```python
def join(other: Union[Table, str],
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

- `other` - The other Dataset object to join on, or a path to another dataset object.
- `output_table` - Where to save the output of this operation. Defaults to `None`, which will not save the output.
- `udf` - The user-defined function to run in the join.
  

**Arguments**:

- `how` - The manner of doing the join. Currently  Defaults to &quot;inner&quot;.
- `left_cache_locally` - Whether to cache the left dataset locally in the join. Defaults to False.
- `right_cache_locally` - Whether to cache the right dataset locally in the join. Defaults to False.
- `buffer_distance` - The size of the buffer (in meters) on the left table to use during the join. Defaults to None.
  

**Examples**:

    ```py
    import fused

    left_table = fused.open_table("s3://bucket/path/to/table")
    other_table = fused.open_table("s3://bucket/path/to/table")
    join_config = left_table.join(other_table)
    ```
  

**Returns**:

  An object describing the join configuration.

#### join\_singlefile

```python
def join_singlefile(
        other: str,
        output_table: Optional[str] = None,
        udf: Union[BaseUdf, None] = None,
        *,
        left_cache_locally: bool = False,
        buffer_distance: Optional[float] = None) -> JoinJobStepConfig
```

Construct a join config from a dataset and a Parquet file URL.

**Arguments**:

- `other` - The URL to the Parquet file to join all chunks with.
- `output_table` - Where to save the output of this operation. Defaults to `None`, which will not save the output.
- `udf` - The user-defined function to run in the join
  

**Arguments**:

- `left_cache_locally` - Whether to cache the left dataset locally in the join. Defaults to False.
  

**Examples**:

    ```py
    left_table = fused.open_table("s3://bucket/path/to/table")
    other_file = "s3://bucket/path/to/file.parquet"
    join_config = left_table.join_singlefile(other_file)
    ```
  

**Returns**:

  An object describing the join configuration.

#### map

```python
def map(output_table: Optional[str] = None,
        udf: Union[BaseUdf, None] = None,
        *,
        cache_locally: bool = False) -> MapJobStepConfig
```

Construct a `map` config from this Dataset

**Arguments**:

- `output_table` - Where to save the output of this operation. Defaults to `None`, which will not save the output.
- `udf` - A user-defined function to run in this map. Defaults to None.
  

**Arguments**:

- `cache_locally` - Advanced: whether to cache all the partitions locally in the map job. Defaults to False.
  

**Returns**:

  An object describing the map configuration.

#### show

```python
def show(dataset_config: Optional[Union[Dict[str, Any], VizConfig]] = None,
         *,
         open_browser: Optional[bool] = None,
         show_widget: Optional[bool] = None,
         iframe_args: Sequence[Any] = ("100%", "600px"),
         app_config: Optional[Dict[str, Any]] = None,
         _rgb_table: Optional[bool] = None) -> str
```

Open a debugging visualization of this dataset

**Arguments**:

- `dataset_config` - additional dataset configuration options
  

**Arguments**:

- `open_browser` - if True, attempts to open the debugging visualization in a browser window. Defaults to None.
- `show_widget` - if True, attempts to open the debugging visualization in a widget within this notebook. Defaults to None.
- `iframe_args` - parameters to pass into the generated IFrame. Defaults to (&quot;100%&quot;, &quot;600px&quot;).
- `app_config` - additional debugging application configuration options
  

**Returns**:

  The url to the hosted visualization.

#### refresh

```python
def refresh(fetch_samples: Optional[bool] = None) -> Table
```

Returns this table with updated metadata

## Dataset Objects

```python
class Dataset(FusedBaseModel, FusedProjectAware)
```

A class to describe everything that exists for a dataset in an environment

#### base\_path

The path on object storage where this dataset is stored

#### tables

The names of one or more attribute tables in this dataset

#### \_\_dir\_\_

```python
def __dir__() -> List[str]
```

Provide method name lookup and completion. Only provide &#x27;public&#x27;
methods.

#### join

```python
def join(other: Union[Dataset, str],
         output_table: Optional[str] = None,
         udf: Union[BaseUdf, None] = None,
         *,
         how: Union[JoinType, Literal["left", "inner"]] = "inner",
         left_tables: Sequence[str] = DEFAULT_TABLE_NAMES,
         right_tables: Sequence[str] = DEFAULT_TABLE_NAMES,
         left_cache_locally: bool = False,
         right_cache_locally: bool = False,
         buffer_distance: Optional[float] = None) -> JoinJobStepConfig
```

Construct a join config from two datasets

**Arguments**:

- `other` - The other Dataset object to join on, or a path to another dataset object.
- `output_table` - Where to save the output of this operation. Defaults to `None`, which will not save the output.
- `udf` - The user-defined function to run in the join.
  

**Arguments**:

- `how` - The manner of doing the join. Currently  Defaults to &quot;inner&quot;.
- `left_tables` - The names of the attribute tables on the left side to include in the join. Defaults to (&quot;main&quot;,).
- `right_tables` - The names of the attribute tables on the left side to include in the join. Defaults to (&quot;main&quot;,).
- `left_cache_locally` - Whether to cache the left dataset locally in the join. Defaults to False.
- `right_cache_locally` - Whether to cache the right dataset locally in the join. Defaults to False.
- `buffer_distance` - The size of the buffer (in meters) on the left table to use during the join. Defaults to None.
  

**Examples**:

    `output_table`0
  

**Returns**:

  An object describing the join configuration.

#### join\_singlefile

```python
def join_singlefile(
        other: str,
        output_table: Optional[str] = None,
        udf: Union[BaseUdf, None] = None,
        *,
        left_tables: Sequence[str] = DEFAULT_TABLE_NAMES,
        left_cache_locally: bool = False,
        buffer_distance: Optional[float] = None) -> JoinJobStepConfig
```

Construct a join config from a dataset and a Parquet file URL.

**Arguments**:

- `other` - The URL to the Parquet file to join all chunks with.
- `output_table` - Where to save the output of this operation. Defaults to `None`, which will not save the output.
- `udf` - The user-defined function to run in the join
  

**Arguments**:

- `left_tables` - The names of the attribute tables on the left side to include in the join. Defaults to (&quot;main&quot;,).
- `left_cache_locally` - Whether to cache the left dataset locally in the join. Defaults to False.
  

**Examples**:

    ```py
    import fused

    left_table = fused.open_table("s3://bucket/path/to/table")
    other_file = "s3://bucket/path/to/file.parquet"
    join_config = left_table.join_singlefile(other_file)
    ```
  

**Returns**:

  An object describing the join configuration.

#### map

```python
def map(output_table: Optional[str] = None,
        udf: Union[BaseUdf, None] = None,
        *,
        tables: Sequence[str] = DEFAULT_TABLE_NAMES,
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

#### get\_chunk

```python
def get_chunk(
    file_id: str | int | None = None,
    chunk_id: int | None = None,
    tables: Sequence[str] = DEFAULT_TABLE_NAMES
) -> Union[pa.Table, pd.DataFrame, gpd.GeoDataFrame]
```

Fetch a single chunk from this dataset

**Arguments**:

- `file_id` - The identifier of this file. Defaults to None.
- `chunk_id` - The numeric index of the chunk within the file to fetch. Defaults to None.
- `tables` - the list of table names to fetch. Defaults to (&quot;main&quot;,).
  

**Returns**:

  
  A `DataFrame` retrieved from the given file, chunk, and tables.

#### get\_dataframe

```python
def get_dataframe(file_id: str | int | None = None,
                  chunk_id: int | None = None,
                  tables: Sequence[str] = DEFAULT_TABLE_NAMES,
                  max_rows: int | None = 10_000_000,
                  parallel_fetch: bool = True) -> pd.DataFrame
```

Fetch multiple chunks from this dataset as a dataframe

**Arguments**:

- `file_id` - The identifier of the file to download. If `None` is passed, all files will be chosen. Defaults to 0.
- `chunk_id` - The numeric index of the chunk within the file to fetch. If `None` is passed, all chunks for the given file(s) will be chosen. Defaults to 0.
- `tables` - the list of table names to fetch. Defaults to (&quot;main&quot;,).
- `max_rows` - The maximum number of rows to fetch. If `None`, no limiting will be done. Defaults to 10_000_000.
- `parallel_fetch` - Fetch in parallel. Defaults to True.
  

**Raises**:

- `ValueError` - If the function would fetch more than `max_rows` rows.
  

**Returns**:

  A `None`0 with all chunks concatenated together.

#### show

```python
def show(dataset_config: Optional[Union[Dict[str, Any], VizConfig]] = None,
         *,
         open_browser: Optional[bool] = None,
         show_widget: Optional[bool] = None,
         iframe_args: Sequence[Any] = ("100%", "600px"),
         tables: Optional[Sequence[str]] = None,
         app_config: Optional[Dict[str, Any]] = None,
         _rgb_table: Optional[str] = None,
         include_fused_table: bool = True) -> str
```

Open a debugging visualization of this dataset

**Arguments**:

- `dataset_config` - additional dataset configuration options
  

**Arguments**:

- `open_browser` - if True, attempts to open the debugging visualization in a browser window. Defaults to None.
- `show_widget` - if True, attempts to open the debugging visualization in a widget within this notebook. Defaults to None.
- `iframe_args` - parameters to pass into the generated IFrame. Defaults to (&quot;100%&quot;, &quot;600px&quot;).
- `tables` - tables to load attributes from for visualization
- `app_config` - additional debugging application configuration options
- `include_fused_table` - if True, ensure &quot;fused&quot; is in the list of tables to show.
  

**Returns**:

  The url to the hosted visualization.

#### delete

```python
def delete(table_name: str,
           max_deletion_depth: int | Literal["unlimited"] = 2) -> None
```

Delete a table from the dataset.

Specify a table to delete from the dataset using the provided table name.
To prevent inadvertently deleting deeply nested objects in the object directory,
users can specify the depth of deletion by specifying the maximum deletion depth.

**Arguments**:

- `table_name` _str_ - The name of the table to be deleted from the dataset.
- `max_deletion_depth` _Optional[int], optional_ - The maximum depth of deletion.
  If provided, the deletion process will be performed only if there are no objects
  deeper than the specified depth. If set to &quot;unlimited&quot; deletion will be performed
  without any depth restrictions. Defaults to 2.
  

**Returns**:

  None

