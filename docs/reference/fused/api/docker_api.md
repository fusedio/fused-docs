---
sidebar_label: docker_api
title: fused.api.docker_api
---

## DockerRunnable Objects

```python
class DockerRunnable(BaseModel)
```

#### run\_and\_get\_bytes

```python
def run_and_get_bytes() -> bytes
```

Run the command and return the bytes written to stdout.

Raises an exception if the return code is not 0.

#### run\_and\_get\_output

```python
def run_and_get_output() -> str
```

Run the command and return the utf-8 string written to stdout.

Raises an exception if the return code is not 0.

#### run\_and\_tail\_output

```python
def run_and_tail_output() -> None
```

Run the command and print output to stdout.

Raises an exception if the return code is not 0.

## FusedDockerAPI Objects

```python
class FusedDockerAPI()
```

API for running jobs in the Fused Docker container.

#### \_\_init\_\_

```python
def __init__(*,
             repository: str = DEFAULT_REPOSITORY,
             tag: str = DEFAULT_TAG,
             mount_aws_credentials: bool = False,
             mount_data_directory: Optional[str] = None,
             mount_job_input_directory: Optional[str] = DEFAULT_JOB_INPUT_HOST,
             additional_docker_args: Sequence[str] = (),
             docker_command_wrapper: Optional[Callable[[str], str]] = None,
             auth_token: Optional[str] = None,
             auto_auth_token: bool = True,
             set_global_api: bool = True,
             is_staging: Optional[bool] = None,
             is_gcp: bool = False,
             is_aws: bool = False,
             pass_config_as_file: bool = True)
```

Create a FusedDockerAPI instance.

**Arguments**:

- `repository` - Repository name for jobs to start.
- `tag` - Tag name for jobs to start. Defaults to `'latest'`.
- `mount_aws_credentials` - Whether to add an additional volume for AWS credentials in the job. Defaults to False.
- `mount_data_directory` - If not None, path on the host to mount as the /data directory in the container. Defaults to None.
- `mount_job_input_directory` - If not None, path on the host to mount as the /job/input/ directory in the container. Defaults to None.
- `additional_docker_args` - Additional arguments to pass to Docker. Defaults to empty.
- `docker_command_wrapper` - Command to wrap the Docker execution in, e.g. `'echo {} 1>&2; exit 1'`. Defaults to None for no wrapping.
- `auth_token` - Auth token to pass to the Docker command. Defaults to automatically detect when auto_auth_token is True.
- `tag`0 - Obtain the auth token from the (previous) global Fused API. Defaults to True.
- `tag`1 - Set this as the global API object. Defaults to True.
- `tag`2 - Set this if connecting to the Fused staging environment. Defaults to None to automatically detect.
- `tag`3 - Set this if running in GCP. Defaults to False.
- `tag`4 - Set this if running in AWS. Defaults to False.
- `tag`5 - If True, job configurations are first written to a temporary file and then passed to Docker. Defaults to True.

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
              *,
              additional_env: Optional[Sequence[str]] = (
                  "FUSED_CREDENTIAL_PROVIDER=ec2", ),
              **kwargs) -> DockerRunnable
```

Execute an operation

**Arguments**:

- `config` - the configuration object to run in the job.
  

**Arguments**:

- `additional_env` - Any additional environment variables to be passed into the job, each in the form KEY=value. Defaults to None.

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

#### ssh\_command\_wrapper

```python
def ssh_command_wrapper(conn_string: str) -> Callable[[str], str]
```

Creates a command wrapper that connects via SSH and sudo runs the command.

#### gcloud\_command\_wrapper

```python
def gcloud_command_wrapper(
        conn_string: str,
        *,
        zone: Optional[str] = None,
        project: Optional[str] = None) -> Callable[[str], str]
```

Creates a command wrapper that connects via gcloud and runs the command.

