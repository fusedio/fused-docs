# Top-Level Functions


## @fused.udf 

```python
def udf(
    fn: Optional[Callable] = None,
    *,
    schema: Union[Schema, Dict, None] = None,
    name: Optional[str] = None,
    default_parameters: Optional[Dict[str, Any]] = None,
    headers: Optional[Sequence[Union[str, Header]]] = None
) -> Callable[..., GeoPandasUdfV2Callable]
```

A decorator that transforms a function into a Fused UDF.

**Arguments**:

- `schema` - The schema for the DataFrame returned by the UDF. The schema may be either
  a string (in the form `"field_name:DataType field_name2:DataType"`, or as JSON),
  as a Python dictionary representing the schema, or a `Schema` model object.
  
  Defaults to None, in which case a schema must be evaluated by calling `run_local`
  for a job to be able to write output. The return value of `run_local` will also
  indicate how to include the schema in the decorator so `run_local` does not need
  to be run again.
- `name` - The name of the UDF object. Defaults to the name of the function.
- `default_parameters` - Parameters to embed in the UDF object, separately from the arguments
  list of the function. Defaults to None for empty parameters.
- `headers` - A list of files to include as modules when running the UDF. For example,
  when specifying `headers=['my_header.py']`, inside the UDF function it may be
  referenced as:
  
        `"field_name:DataType field_name2:DataType"`0
  
  Defaults to None for no headers.

**Returns**:

  A callable that represents the transformed UDF. This callable can be used
  within GeoPandas workflows to apply the defined operation on geospatial data.
  

**Examples**:

  To create a simple UDF that calls a utility function to calculate the area of geometries in a GeoDataFrame:
  
    `"field_name:DataType field_name2:DataType"`



## run

```python
def run(email_or_udf_or_token: Union[str, None, UdfJobStepConfig,
                                     GeoPandasUdfV2] = None,
        udf_name: Optional[str] = None,
        *,
        udf: Optional[GeoPandasUdfV2] = None,
        job_step: Optional[UdfJobStepConfig] = None,
        token: Optional[str] = None,
        udf_email: Optional[str] = None,
        x: Optional[int] = None,
        y: Optional[int] = None,
        z: Optional[int] = None,
        lat: Optional[float] = None,
        lng: Optional[float] = None,
        bbox: Union[gpd.GeoDataFrame, shapely.Geometry, None] = None,
        sync: bool = True,
        engine: Optional[Literal["realtime", "batch", "local"]] = None,
        type: Optional[Literal["tile", "file"]] = None,
        **parameters)
```

Executes a user-defined function (UDF) with various execution and input options.

This function supports executing UDFs in different environments (realtime, batch, local),
with different types of inputs (tile coordinates, geographical bounding boxes, etc.), and
allows for both synchronous and asynchronous execution. It dynamically determines the execution
path based on the provided parameters.

**Arguments**:

- `email_or_udf_or_token` - A string that can either be an email, a UDF token, or a direct
  reference to a UDF object. It can also be a UdfJobStepConfig object for detailed
  configuration, or None to specify UDF details in other parameters.
- `udf_name` - The name of the UDF to execute.
- `udf` - A GeoPandasUdfV2 object for direct execution.
- `job_step` - A UdfJobStepConfig object for detailed execution configuration.
- `token` - A token representing a shared UDF.
- `udf_email` - The email associated with the UDF.
  x, y, z: Tile coordinates for tile-based UDF execution.
  lat, lng: Latitude and longitude for location-based UDF execution.
- `bbox` - A geographical bounding box (as a GeoDataFrame or shapely Geometry) defining the area of interest.
- `sync` - If True, execute the UDF synchronously. If False, execute asynchronously.
- `engine` - The execution engine to use (&#x27;realtime&#x27;, &#x27;batch&#x27;, or &#x27;local&#x27;).
- `type` - The type of UDF execution (&#x27;tile&#x27; or &#x27;file&#x27;).
- `udf_name`0 - Additional parameters to pass to the UDF.
  

**Raises**:

- `udf_name`1 - If the UDF is not specified or is specified in more than one way.
- `udf_name`2 - If the first parameter is not of an expected type.
- `udf_name`3 - Various warnings are issued for ignored parameters based on the execution path chosen.
  

**Returns**:

  The result of the UDF execution, which varies based on the UDF and execution path.
  

**Examples**:

  
  # Run a UDF saved in the Fused system:
  fused.run(udf_email=&quot;username@fused.io&quot;, udf_name=&quot;my_udf_name&quot;)
  
  # Run a UDF saved in GitHub:
  loaded_udf = fused.load(&quot;https://github.com/fusedio/udfs/tree/main/public/Building_Tile_Example&quot;)
  fused.run(udf=loaded_udf, bbox=bbox)
  
  # Run a UDF saved in a local directory:
  loaded_udf = fused.load(&quot;/Users/local/dir/Building_Tile_Example&quot;)
  fused.run(udf=loaded_udf, bbox=bbox)
  

**Notes**:

  This function dynamically determines the execution path and parameters based on the inputs.
  It is designed to be flexible and support various UDF execution scenarios.


## @fused.cache

```python
def cache(func: Optional[Callable[..., Any]] = None,
          **kwargs: Any) -> Callable[..., Any]
```

Decorator to cache the return value of a function.

This function serves as a decorator that can be applied to any function
to cache its return values. The cache behavior can be customized through
keyword arguments.

**Arguments**:

- `func` _Callable, optional_ - The function to be decorated. If None, this
  returns a partial decorator with the passed keyword arguments.
- `**kwargs` - Arbitrary keyword arguments that are passed to the internal
  caching mechanism. These could specify cache size, expiration time,
  and other cache-related settings.
  

**Returns**:

- `Callable` - A decorator that, when applied to a function, caches its
  return values according to the specified keyword arguments.
  

**Examples**:

  
  # Use the `@cache` decorator to cache the return value of a function in a custom path.
  
  @cache(path=&quot;/tmp/custom_path/&quot;)
  def expensive_function():
  # Function implementation goes here
  return result
  
  # If the output of a cached function changes, for example if remote data is modified,
  # it can be reset by running the function with the `reset` keyword argument. Afterward,
  # the argument can be
  
  @cache(path=&quot;/tmp/custom_path/&quot;, reset=True)
  def expensive_function():
  # Function implementation goes here
  return result



## load

```python
def load(url_or_udf: Union[str, Path], *, cache_key: Any = None) -> BaseUdf
```

Loads a UDF (User-Defined Function) from various sources including GitHub URLs,
local files, or directories, and a Fused platform-specific identifier.

This function supports loading UDFs from a GitHub repository URL, a local file path,
a directory containing UDF definitions, or a Fused platform-specific identifier
composed of an email and UDF name. It intelligently determines the source type based
on the format of the input and retrieves the UDF accordingly.

**Arguments**:

- `url_or_udf` - A string or Path object representing the location of the UDF. This can be
  a GitHub URL starting with &quot;https://github.com&quot;, a local file path, a directory
  containing one or more UDFs, or a Fused platform-specific identifier in the
  format &quot;email/udf_name&quot;.
- `cache_key` - An optional key used for caching the loaded UDF. If provided, the function
  will attempt to load the UDF from cache using this key before attempting to
  load it from the specified source. Defaults to None, indicating no caching.
  

**Returns**:

- `BaseUdf` - An instance of the loaded UDF.
  

**Raises**:

- `FileNotFoundError` - If a local file or directory path is provided but does not exist.
- `ValueError` - If the URL or Fused platform-specific identifier format is incorrect or
  cannot be parsed.
- `Exception` - For errors related to network issues, file access permissions, or other
  unforeseen errors during the loading process.
  

**Examples**:

  Loading a UDF from a GitHub URL:
    ```py
    udf = fused.load("https://github.com/fusedio/udfs/tree/main/public/REM_with_HyRiver/")
    ```
  
  Loading a UDF from a local file:
    ```py
    udf = fused.load("/localpath/REM_with_HyRiver/")
    ```
  
  Loading a UDF using a Fused platform-specific identifier:
    ```py
    udf = fused.load("username@fused.io/REM_with_HyRiver")
    ```
















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

  
  @fused.udf
  def geodataframe_from_geojson():
  import geopandas as gpd
  url = &quot;s3://sample_bucket/my_geojson.zip&quot;
  path = fused.core.download(url, &quot;tmp/my_geojson.zip&quot;)
  gdf = gpd.read_file(path)
  return gdf








## utils

A module to access utility functions located in the UDF called &quot;common&quot;.

They can be imported by other UDFs with `common = fused.public.common`. They contain common operations such as:
- read_shape_zip
- url_to_arr
- get_collection_bbox
- read_tiff_pc
- table_to_tile
- rasterize_geometry


**Examples**:

  
  # This example shows how to access the `geo_buffer` function from the `common` UDF.
  import fused
  import geopandas as gpd
  
  gdf = gpd.read_file(&#x27;https://www2.census.gov/geo/tiger/TIGER_RD18/STATE/11_DISTRICT_OF_COLUMBIA/11/tl_rd22_11_bg.zip&#x27;)
  gdf_buffered = fused.public.common.geo_buffer(gdf, 10)
  
  
  # This example shows how to load a table with `table_to_tile`, which efficiently loads a table by filtering and adjusting based on the provided bounding box (bbox) and zoom level.
  table_path = &quot;s3://fused-asset/infra/census_bg_us&quot;
  gdf = fused.public.common.table_to_tile(
  bbox, table_path, use_columns=[&quot;GEOID&quot;, &quot;geometry&quot;], min_zoom=12
  )
  
  
  # This example shows how to use `rasterize_geometry` to place an input geometry within an image array.
  geom_masks = [
  rasterize_geometry(geom, arr.shape[-2:], transform) for geom in gdf.geometry
  ]
  
  
  Public UDFs are listed at https://github.com/fusedio/udfs/tree/main/public



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
- `schema`2 - The target for the number of files if `output`2 is None. Note that this number is only a _target_ and the actual number of files generated can be higher or lower than this number, depending on the spatial distribution of the data itself.
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

  For example, to ingest the California Census dataset for the year 2022:
    `file_suffix`8

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

  
  fused.get(&quot;fd://bucket-name/file.parquet&quot;)


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
- `by` - The attribute by which to sort the UDFs. Can be &quot;name&quot;, &quot;id&quot;, or &quot;slug&quot;. Defaults to &quot;name&quot;.
- `whose` - Specifies whose UDFs to fetch. Can be &quot;self&quot; for the user&#x27;s own UDFs or &quot;public&quot; for
  UDFs available publicly. Defaults to &quot;self&quot;.
  

**Returns**:

  A list of UDFs.
  

**Examples**:

  Fetch UDFs under the user account:
    ```py
    get_udfs()
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

  
  fused.list(&quot;fd://bucket-name/&quot;)

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

  
  fused.delete(&quot;fd://bucket-name/deprecated_table/&quot;)


## options

List global configuration options.

This object contains a set of configuration options that control global behavior of the library. This object can be used to modify the options.

**Examples**:

  Change the `request_timeout` option from its default value to 120 seconds:
    ```py
    fused.options.request_timeout = 120
    ```

## set\_option

```python
def set_option(option_name: str, option_value: Any)
```

Sets the value of a configuration option.

This function updates the global `options` object with a new value for a specified option.
It supports setting values for nested options using dot notation. For example, if the
`options` object has a nested structure, you can set a value for a nested attribute
by specifying the option name in the form &quot;parent.child&quot;.

**Arguments**:

- `option_name` - A string specifying the name of the option to set. This can be a simple
  attribute name or a dot-separated path for nested attributes.
- `option_value` - The new value to set for the specified option. This can be of any type
  that is compatible with the attribute being set.
  

**Raises**:

- `AttributeError` - If the specified attribute path is not valid, either because a part
  of the path does not exist or the final attribute cannot be set with
  the provided value.
  

**Examples**:

  Set the `request_timeout` top-level option to 120 seconds:
    ```py
    set_option('request_timeout', 120)
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

  
  fused.sign_url(&quot;fd://bucket-name/table_directory/file.parquet&quot;)

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

    ```py
    fused.sign_url_prefix("fd://bucket-name/table_directory/")
    ```

## get\_chunks\_metadata

```python
def get_chunks_metadata(url: str) -> gpd.GeoDataFrame
```

Returns a GeoDataFrame with each chunk in the table as a row.

**Arguments**:

- `url` - URL of the table.

## get\_chunk\_from\_table

```python
def get_chunk_from_table(
        url: str,
        file_id: Union[str, int, None],
        chunk_id: Optional[int],
        *,
        columns: Optional[Iterable[str]] = None) -> gpd.GeoDataFrame
```

Returns a chunk from a table and chunk coordinates.

This can be called with file_id and chunk_id from `get_chunks_metadata`.

**Arguments**:

- `url` - URL of the table.
- `file_id` - File ID to read.
- `chunk_id` - Chunk ID to read.
  

**Other Arguments**:

- `columns` - Read only the specified columns.
