---
sidebar_label: Top-Level Functions
title: Top-Level Functions
toc_max_heading_level: 5
---




## @fused.udf
```python showLineNumbers
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

        ```py
        import my_header
        my_header.my_function()
        ```

  Defaults to None for no headers.

**Returns**:

  A callable that represents the transformed UDF. This callable can be used
  within GeoPandas workflows to apply the defined operation on geospatial data.


**Examples**:

  To create a simple UDF that calls a utility function to calculate the area of geometries in a GeoDataFrame:

    ```py
    @fused.udf
    def udf(bbox, table_path="s3://fused-asset/infra/building_msft_us"):
        ...
        gdf = table_to_tile(bbox, table=table_path)
        return gdf
    ```

---
## @fused.cache

```python showLineNumbers
def cache(
    func: Optional[Callable[..., Any]] = None,
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


  Use the `@cache` decorator to cache the return value of a function in a custom path.

    ```py
    @cache(path="/tmp/custom_path/")
    def expensive_function():
        # Function implementation goes here
        return result
    ```

  If the output of a cached function changes, for example if remote data is modified,
  it can be reset by running the function with the `reset` keyword argument. Afterward,
  the argument can be cleared.

    ```py
    @cache(path="/tmp/custom_path/", reset=True)
    def expensive_function():
        # Function implementation goes here
        return result
    ```


---
## fused.load

```python showLineNumbers
def load(url_or_udf: Union[str, Path], *, cache_key: Any = None) -> AnyBaseUdf
```

Loads a UDF from various sources including GitHub URLs,
local files, or directories, and a Fused platform-specific identifier.

This function supports loading UDFs from a GitHub repository URL, a local file path,
a directory containing UDF definitions, or a Fused platform-specific identifier
composed of an email and UDF name. It intelligently determines the source type based
on the format of the input and retrieves the UDF accordingly.

**Arguments**:

- `url_or_udf` - A string or Path object representing the location of the UDF. This can be
  a GitHub URL starting with "https://github.com", a local file path, a directory
  containing one or more UDFs, or a Fused platform-specific identifier in the
  format "email/udf_name".
- `cache_key` - An optional key used for caching the loaded UDF. If provided, the function
  will attempt to load the UDF from cache using this key before attempting to
  load it from the specified source. Defaults to None, indicating no caching.


**Returns**:

- `AnyBaseUdf` - An instance of the loaded UDF.


**Raises**:

- `FileNotFoundError` - If a local file or directory path is provided but does not exist.
- `ValueError` - If the URL or Fused platform-specific identifier format is incorrect or
  cannot be parsed.
- `Exception` - For errors related to network issues, file access permissions, or other
  unforeseen errors during the loading process.


**Examples**:

  Load a UDF from a GitHub URL:
    ```py
    udf = fused.load("https://github.com/fusedio/udfs/tree/main/public/REM_with_HyRiver/")
    ```

  Load a UDF from a local file:
    ```py
    udf = fused.load("/localpath/REM_with_HyRiver/")
    ```

  Load a UDF using a Fused platform-specific identifier:
    ```py
    udf = fused.load("username@fused.io/REM_with_HyRiver")
    ```





---
## fused.run

```python showLineNumbers
def run(email_or_udf_or_token: Union[str, None, UdfJobStepConfig,
                                     GeoPandasUdfV2, UdfAccessToken] = None,
        udf_name: Optional[str] = None,
        *,
        udf: Optional[GeoPandasUdfV2] = None,
        job_step: Optional[UdfJobStepConfig] = None,
        token: Optional[str] = None,
        udf_email: Optional[str] = None,
        x: Optional[int] = None,
        y: Optional[int] = None,
        z: Optional[int] = None,
        _lat: Optional[float] = None,
        _lng: Optional[float] = None,
        bbox: Union["gpd.GeoDataFrame", "shapely.Geometry", None] = None,
        sync: bool = True,
        engine: Optional[Literal["realtime", "batch", "local"]] = None,
        type: Optional[Literal["tile", "file"]] = None,
        parameters: Optional[Dict[str, Any]] = None,
        **kw_parameters)
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
  _lat, _lng: Latitude and longitude for tile-based UDF execution.
- `bbox` - A geographical bounding box (as a GeoDataFrame or shapely Geometry) defining the area of interest.
- `sync` - If True, execute the UDF synchronously. If False, execute asynchronously.
- `engine` - The execution engine to use ('realtime', 'batch', or 'local').
- `type` - The type of UDF execution ('tile' or 'file').
- `parameters` - Additional parameters to pass to the UDF.
- `**kw_parameters` - Additional parameters to pass to the UDF.


**Raises**:

- `ValueError` - If the UDF is not specified or is specified in more than one way.
- `TypeError` - If the first parameter is not of an expected type.
- `Warning` - Various warnings are issued for ignored parameters based on the execution path chosen.


**Returns**:

  The result of the UDF execution, which varies based on the UDF and execution path.


**Examples**:



  Run a UDF saved in the Fused system:
    ```py
    fused.run(udf_email="username@fused.io", udf_name="my_udf_name")
    ```

  Run a UDF saved in GitHub:
    ```py
    loaded_udf = fused.load("https://github.com/fusedio/udfs/tree/main/public/Building_Tile_Example")
    fused.run(udf=loaded_udf, bbox=bbox)
    ```

  Run a UDF saved in a local directory:
    ```py
    loaded_udf = fused.load("/Users/local/dir/Building_Tile_Example")
    fused.run(udf=loaded_udf, bbox=bbox)
    ```


:::note

This function dynamically determines the execution path and parameters based on the inputs.
  It is designed to be flexible and support various UDF execution scenarios.

Because the output must be serializable and returned via an HTTP response, Fused validates the output of UDFs that execute remotely with the `realtime` engine and will hold back invalid responses. This might result in perceived inconsistencies because running locally with the `local` engine does not validate and will instead return any output. See the set of supported return object types [here](/core-concepts/write/#return-object).

```python showLineNumbers
  import fused

  @fused.udf
  def udf(x=1):
      return x
  fused.run(udf, engine='local') # Returns 1
  fused.run(udf, engine='realtime') # Returns None because output is not a valid response object
  ```

:::

---
## fused.download

```python showLineNumbers
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

The function downloads the file only on the first execution and returns the file path.

**Examples**:


```python showLineNumbers
@fused.udf
def geodataframe_from_geojson():
    import geopandas as gpd
    url = "s3://sample_bucket/my_geojson.zip"
    path = fused.core.download(url, "tmp/my_geojson.zip")
    gdf = gpd.read_file(path)
    return gdf
```



---
## fused.utils

A module to access utility functions located in the UDF called "common".

They can be imported by other UDFs with `common = fused.public.common`. They contain common operations such as:

- read_shape_zip
- url_to_arr
- get_collection_bbox
- read_tiff_pc
- table_to_tile
- rasterize_geometry

**Examples**:

This example shows how to access the `geo_buffer` function from the `common` UDF.
```python showLineNumbers
import fused
import geopandas as gpd

gdf = gpd.read_file('https://www2.census.gov/geo/tiger/TIGER_RD18/STATE/11_DISTRICT_OF_COLUMBIA/11/tl_rd22_11_bg.zip')
gdf_buffered = fused.utils.common.geo_buffer(gdf, 10)
```

This example shows how to load a table with `table_to_tile`, which efficiently loads a table by filtering and adjusting based on the provided bounding box (bbox) and zoom level.

```python showLineNumbers
table_path = "s3://fused-asset/infra/census_bg_us"
gdf = fused.utilscommon.table_to_tile(
    bbox, table_path, use_columns=["GEOID", "geometry"], min_zoom=12
)
```

This example shows how to use `rasterize_geometry` to place an input geometry within an image array.

```python showLineNumbers
geom_masks = [rasterize_geometry(geom, arr.shape[-2:], transform) for geom in gdf.geometry]
```

Public UDFs are listed at https://github.com/fusedio/udfs/tree/main/public



---
## fused.ingest

```python showLineNumbers
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
- `output_metadata` - Location on S3 to write the `fused` table to.
- `schema` - Schema of the data to be ingested. This is optional and will be inferred from the data if not provided.
- `file_suffix` - filter which files are used for ingestion. If `input` is a directory on S3, all files under that directory will be listed and used for ingestion. If `file_suffix` is not None, it will be used to filter paths by checking the trailing characters of each filename. E.g. pass `file_suffix=".geojson"` to include only GeoJSON files inside the directory.
- `load_columns` - Read only this set of columns when ingesting geospatial datasets. Defaults to all columns.
- `remove_cols` - The named columns to drop when ingesting geospatial datasets. Defaults to not drop any columns.
- `explode_geometries` - Whether to unpack multipart geometries to single geometries when ingesting geospatial datasets, saving each part as its own row. Defaults to `False`.
- `drop_out_of_bounds` - Whether to drop geometries outside of the expected WGS84 bounds. Defaults to True.
- `partitioning_method` - The method to use for grouping rows into partitions. Defaults to `"rows"`.
  - `"area"`: Construct partitions where all contain a maximum total area among geometries.
  - `"length"`: Construct partitions where all contain a maximum total length among geometries.
  - `"coords"`: Construct partitions where all contain a maximum total number of coordinates among geometries.
  - `"rows"`: Construct partitions where all contain a maximum number of rows.
- `partitioning_maximum_per_file` - Maximum value for `partitioning_method` to use per file. If `None`, defaults to _1/10th_ of the total value of `partitioning_method`. So if the value is `None` and `partitioning_method` is `"area"`, then each file will be have no more than 1/10th the total area of all geometries. Defaults to `None`.
- `partitioning_maximum_per_chunk` - Maximum value for `partitioning_method` to use per chunk. If `None`, defaults to _1/100th_ of the total value of `partitioning_method`. So if the value is `None` and `partitioning_method` is `"area"`, then each file will be have no more than 1/100th the total area of all geometries. Defaults to `None`.
- `partitioning_max_width_ratio` - The maximum ratio of width to height of each partition to use in the ingestion process. So for example, if the value is `2`, then if the width divided by the height is greater than `2`, the box will be split in half along the horizontal axis. Defaults to `2`.
- `partitioning_max_height_ratio` - The maximum ratio of height to width of each partition to use in the ingestion process. So for example, if the value is `2`, then if the height divided by the width is greater than `2`, the box will be split in half along the vertical axis. Defaults to `2`.
- `partitioning_force_utm` - Whether to force partitioning within UTM zones. If set to `"file"`, this will ensure that the centroid of all geometries per _file_ are contained in the same UTM zone. If set to `"chunk"`, this will ensure that the centroid of all geometries per _chunk_ are contained in the same UTM zone. If set to `None`, then no UTM-based partitioning will be done. Defaults to "chunk".
- `partitioning_split_method` - How to split one partition into children. Defaults to `"mean"` (this may change in the future).
  - `"mean"`: Split each axis according to the mean of the centroid values.
  - `"median"`: Split each axis according to the median of the centroid values.
- `subdivide_method` - The method to use for subdividing large geometries into multiple rows. Currently the only option is `"area"`, where geometries will be subdivided based on their area (in WGS84 degrees).
- `subdivide_start` - The value above which geometries will be subdivided into smaller parts, according to `subdivide_method`.
- `subdivide_stop` - The value below which geometries will never be subdivided into smaller parts, according to `subdivide_method`.
- `split_identical_centroids` - If `True`, should split a partition that has
  identical centroids (such as if all geometries in the partition are the
  same) if there are more such rows than defined in "partitioning_maximum_per_file" and
  "partitioning_maximum_per_chunk".
- `target_num_chunks` - The target for the number of chunks if `partitioning_maximum_per_file` is None. Note that this number is only a _target_ and the actual number of files and chunks generated can be higher or lower than this number, depending on the spatial distribution of the data itself.
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

  Configuration object describing the ingestion process. Call `.execute` on this object to start a job.



**Examples**:

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

---
#### job.run\_remote

```python
def run_remote(output_table: Optional[str] = ...,
               instance_type: Optional[WHITELISTED_INSTANCE_TYPES] = None,
               *,
               region: str | None = None,
               disk_size_gb: int | None = None,
               additional_env: List[str] | None = None,
               image_name: Optional[str] = None,
               ignore_no_udf: bool = False,
               ignore_no_output: bool = False,
               validate_imports: Optional[bool] = None,
               validate_inputs: bool = True,
               overwrite: Optional[bool] = None) -> RunResponse
```

Execute this operation

**Arguments**:

- `output_table` - The name of the table to write to. Defaults to None.
- `instance_type` - The AWS EC2 instance type to use for the job. Acceptable strings are "m5.large", "m5.xlarge", "m5.2xlarge", "m5.4xlarge", "r5.large", "r5.xlarge", "r5.2xlarge", "r5.4xlarge". Defaults to None.
- `region` - The AWS region in which to run. Defaults to None.
- `disk_size_gb` - The disk size to specify for the job. Defaults to None.
- `additional_env` - Any additional environment variables to be passed into the job. Defaults to None.
- `image_name` - Custom image name to run. Defaults to None for default image.

- `ignore_no_udf` - Ignore validation errors about not specifying a UDF. Defaults to False.
- `ignore_no_output` - Ignore validation errors about not specifying output location. Defaults to False.


{/*
---
## ingest\_nongeospatial

```python showLineNumbers
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
- `output_metadata` - Location on S3 to write the `fused` table to.
- `partition_col` - Partition along this column for nongeospatial datasets.
- `partitioning_maximum_per_file` - Maximum number of items to store in a single file. Defaults to 2,500,000.
- `partitioning_maximum_per_chunk` - Maximum number of items to store in a single file. Defaults to 65,000.


**Returns**:


  Configuration object describing the ingestion process. Call `.execute` on this object to start a job.


**Examples**:

    ```py
    job = fused.ingest_nongeospatial(
        input=gdf,
        output="s3://sample-bucket/file.parquet",
    ).execute()
    ```


*/}
