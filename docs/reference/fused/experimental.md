---
sidebar_label: experimental
title: fused.experimental
---

## open\_project

```python showLineNumbers
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
  folders that `max_depth` would otherwise cause.

## load\_udf

```python showLineNumbers
def load_udf(udf_paths: Sequence[str],
             *,
             parameters: Optional[Dict[str, Any]] = None,
             content_type: Optional[str] = None,
             load_schema: bool = True,
             header_paths: Optional[Sequence[Header]] = None) -> UdfRegistry
```

Load UDF(s) in a UdfRegistry object.

**Arguments**:

- `udf_paths` - The paths to the UDF source code files or URLs.
  If provided as a list, it loads and registers multiple UDFs as a UdfRegistry.
- `function` - The name of the UDF function to load.
- `parameters` - A dictionary of parameters to be passed to the UDF.
- `table_schema` - The schema of the input data table.
- `content_type` - The content type of the UDF source, e.g., "file", "py", or "url".
- `load_schema` - Whether to automatically detect and load the table schema.
- `header_paths` - A sequence of headers for the UDF.


**Returns**:

  UdfRegistry or UDF: Returns a UdfRegistry containing registered UDFs.


**Raises**:

  - ValueError: If multiple UDFs with the same name are found in a list of UDF paths.
  - AssertionError: If an unsupported content type is provided.


**Examples**:

  Load multiple UDFs from a list of files and register them in a UdfRegistry:

    ```py
    load_udf(udf_paths=["udf1.py", "udf2.py"], header_paths=["header.py"])
    load_udf("my_udf.py", function="my_function", content_type="file")
    ```

## open\_table

```python showLineNumbers
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
    table = fused.experimental.open_table("s3://my_bucket/path/to/dataset/table/")
    ```

## job

```python showLineNumbers
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



### job.run_remote

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
               overwrite: Optional[bool] = None) -> RunResponse
```

Run a `JobConfig`, such as an [ingestion job](/core-concepts/content-management/Ingest/#ingest-data).

**Arguments**:

- `output_table` - The name of the table to write to. Defaults to None.
- `instance_type` - The AWS EC2 instance type to use for the job. Acceptable strings are "m5.large", "m5.xlarge", "m5.2xlarge", "m5.4xlarge", "r5.large", "r5.xlarge", "r5.2xlarge", "r5.4xlarge". Defaults to None.
- `region` - The AWS region in which to run. Defaults to None.
- `disk_size_gb` - The disk size to specify for the job. Defaults to None.
- `additional_env` - Any additional environment variables to be passed into the job. Defaults to None.
- `image_name` - Custom image name to run. Defaults to None for default image.

- `ignore_no_udf` - Ignore validation errors about not specifying a UDF. Defaults to False.
- `ignore_no_output` - Ignore validation errors about not specifying output location. Defaults to False.

## sign\_url

```python showLineNumbers
def sign_url(path: str) -> str
```

Create a signed URL to access the path.

This function may not check that the file represented by the path exists.

**Arguments**:

- `path` - URL to a file, like `fd://bucket-name/file.parquet`


**Returns**:

  HTTPS URL to access the file using signed access.


**Examples**:

    ```python showLineNumbers
    fused.experimental.sign_url("fd://bucket-name/table_directory/file.parquet")
    ```

## sign\_url\_prefix

```python showLineNumbers
def sign_url_prefix(path: str) -> Dict[str, str]
```

Create signed URLs to access all blobs under the path.

**Arguments**:

- `path` - URL to a prefix, like `fd://bucket-name/some_directory/`


**Returns**:

  Dictionary mapping from blob store key to signed HTTPS URL.


**Examples**:

    ```python showLineNumbers
    fused.experimental.sign_url_prefix("fd://bucket-name/table_directory/")
    ```
