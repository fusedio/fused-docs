---
sidebar_label: docker_http_api
title: fused.api.docker_http_api
---

## DockerHTTPRunnable Objects

```python
class DockerHTTPRunnable(BaseModel)
```

#### run\_and\_get\_bytes

```python
def run_and_get_bytes() -> bytes
```

Run the command and return the bytes written to stdout.

Raises an exception if an HTTP error status is returned.

#### run\_and\_get\_output

```python
def run_and_get_output() -> str
```

Run the command and return the utf-8 string written to stdout.

Raises an exception if an HTTP error status is returned.

#### run\_and\_tail\_output

```python
def run_and_tail_output() -> None
```

Run the command and print output to stdout.

Raises an exception if an HTTP error status is returned.

## FusedDockerHTTPAPI Objects

```python
class FusedDockerHTTPAPI()
```

API for running jobs in the Fused Docker container over an HTTP connection.

#### \_\_init\_\_

```python
def __init__(endpoint: str = DEFAULT_ENDPOINT, *, set_global_api: bool = True)
```

Create a FusedDockerHTTPAPI instance.

**Arguments**:

- `endpoint` - The HTTP endpoint to connect to. Defaults to `"http://localhost:8789"`.
  

**Arguments**:

- `set_global_api` - Set this as the global API object. Defaults to True.

#### sample\_map

```python
def sample_map(config: MapJobStepConfig,
               *,
               file_id: Optional[Union[str, int]] = None,
               chunk_id: Optional[int] = None,
               n_rows: Optional[int] = None) -> MapInput
```

Fetch a sample of an operation

**Arguments**:

- `config` - The configuration to sample from.
  

**Arguments**:

- `file_id` - The identifier of this file. Defaults to None.
- `chunk_id` - The numeric index of the chunk within the file to fetch. Defaults to None.
- `n_rows` - The maximum number of rows to sample. Defaults to None for all rows in the chunk.

#### sample\_join

```python
def sample_join(config: JoinJobStepConfig,
                *,
                file_id: Optional[Union[str, int]] = None,
                chunk_id: Optional[int] = None,
                n_rows: Optional[int] = None) -> JoinInput
```

Fetch a sample of an operation

**Arguments**:

- `config` - The configuration to sample from.
  

**Arguments**:

- `file_id` - The identifier of this file. Defaults to None.
- `chunk_id` - The numeric index of the chunk within the file to fetch. Defaults to None.
- `n_rows` - The maximum number of rows to sample from the left dataset. Defaults to None for all rows in the chunk.

#### sample\_single\_file\_join

```python
def sample_single_file_join(
        config: JoinSinglefileJobStepConfig,
        *,
        file_id: Optional[Union[str, int]] = None,
        chunk_id: Optional[int] = None,
        n_rows: Optional[int] = None) -> JoinSingleFileInput
```

Fetch a sample of an operation

**Arguments**:

- `config` - The configuration to sample from.
  

**Arguments**:

- `file_id` - The identifier of this file. Defaults to None.
- `chunk_id` - The numeric index of the chunk within the file to fetch. Defaults to None.
- `n_rows` - The maximum number of rows to sample from the left dataset. Defaults to None for all rows in the chunk.

#### start\_job

```python
def start_job(config: Union[JobConfig, JobStepConfig],
              **kwargs) -> DockerHTTPRunnable
```

Execute an operation

**Arguments**:

- `config` - the configuration object to run in the job.

#### open\_table

```python
def open_table(path: str, *, fetch_samples: Optional[bool] = None) -> Table
```

Open a Table object given a path to the root of the table

**Arguments**:

- `path` - The path to the root of the table on remote storage
  

**Arguments**:

- `fetch_samples` - If True, fetch sample of each table when opening the dataset.
  

**Example**:

  
  table = fused.open_table(
  path=&quot;s3://my_bucket/path/to/dataset/table/&quot;
  )
  

**Returns**:

  A Table object

#### open\_folder

```python
def open_folder(path: str,
                *,
                fetch_minimal_table_metadata: Optional[bool] = None,
                fetch_table_metadata: Optional[bool] = None,
                fetch_samples: Optional[bool] = None,
                table_mode: bool = True,
                max_depth: Optional[int] = None) -> Folder
```

Open all Table objects under the path.

**Arguments**:

- `path` - The path to the root of the folder on remote storage
  

**Arguments**:

- `fetch_table_metadata` - If True, fetch metadata on each table when getting dataset metadata.
- `fetch_samples` - If True, fetch sample of each table when opening the dataset.
- `max_depth` - Maximum depth of Tables to open. Beyond this tables will be opened virtually.
  

**Example**:

  
  datasets = fused.open_folder(
  path=&quot;s3://my_bucket/path/to/folder/&quot;
  )
  

**Returns**:

  A list of Dataset objects

#### upload

```python
def upload(path: str, data: Union[bytes, BinaryIO]) -> None
```

Upload a binary blob to a cloud location

