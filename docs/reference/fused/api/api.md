---
sidebar_label: api
title: fused.api.api
---

## FusedAPI Objects

```python
class FusedAPI()
```

API for running jobs in the Fused service.

## \_\_init\_\_

```python
def __init__(*,
             base_url: Optional[str] = None,
             set_global_api: bool = True,
             credentials_needed: bool = True)
```

Create a FusedAPI instance.

**Arguments**:

- `base_url` - The Fused instance to send requests to. Defaults to `https://www.fused.io/server/v1`.
- `set_global_api` - Set this as the global API object. Defaults to True.
- `credentials_needed` - If True, automatically attempt to log in. Defaults to True.

## start\_job

```python
def start_job(config: Union[JobConfig, JobStepConfig],
              *,
              instance_type: Optional[WHITELISTED_INSTANCE_TYPES] = None,
              region: Optional[str] = None,
              disk_size_gb: Optional[int] = None,
              additional_env: Optional[Sequence[str]] = (
                  "FUSED_CREDENTIAL_PROVIDER=ec2", ),
              image_name: Optional[str] = None) -> RunResponse
```

Execute an operation

**Arguments**:

- `config` - the configuration object to run in the job.


**Arguments**:

- `instance_type` - The AWS EC2 instance type to use for the job. Acceptable strings are "m5.large", "m5.xlarge", "m5.2xlarge", "m5.4xlarge", "r5.large", "r5.xlarge", "r5.2xlarge", "r5.4xlarge". Defaults to None.
- `region` - The AWS region in which to run. Defaults to None.
- `disk_size_gb` - The disk size to specify for the job. Defaults to None.
- `additional_env` - Any additional environment variables to be passed into the job, each in the form KEY=value. Defaults to None.
- `image_name` - Custom image name to run. Defaults to None for default image.

## create\_udf\_access\_token

```python
def create_udf_access_token(udf_email_or_name_or_id: Optional[str] = None,
                            udf_name: Optional[str] = None,
                            *,
                            udf_email: Optional[str] = None,
                            udf_id: Optional[str] = None,
                            client_id: Union[str, Ellipsis, None] = ...,
                            cache: bool = True,
                            metadata_json: Optional[Dict[str, Any]] = None,
                            enabled: bool = True) -> UdfAccessToken
```

Create a token for running a UDF. The token allows anyone who has it to run
the UDF, with the parameters they choose. The UDF will run under your environment.

The token does not allow running any other UDF on your account.

**Arguments**:

- `udf_email_or_name_or_id` - A UDF ID, email address (for use with udf_name), or UDF name.
- `udf_name` - The name of the UDF to create the


**Arguments**:

- `udf_email` - The email of the user owning the UDF, or, if udf_name is None, the name of the UDF.
- `udf_id` - The backend ID of the UDF to create the token for.
- `client_id` - If specified, overrides which realtime environment to run the UDF under.
- `cache` - If True, UDF tiles will be cached.
- `metadata_json` - Additional metadata to serve as part of the tiles metadata.json.
- `enable` - If True, the token can be used.

## get\_jobs

```python
def get_jobs(n: int = 5,
             *,
             skip: int = 0,
             per_request: int = 25,
             max_requests: Optional[int] = 1) -> Jobs
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

## get\_status

```python
def get_status(job: CoerceableToJobId) -> RunResponse
```

Fetch the status of a running job

**Arguments**:

- `job` - the identifier of a job or a `RunResponse` object.


**Returns**:

  The status of the given job.

## get\_logs

```python
def get_logs(job: CoerceableToJobId,
             since_ms: Optional[int] = None) -> List[Any]
```

Fetch logs for a job

**Arguments**:

- `job` - the identifier of a job or a `RunResponse` object.
- `since_ms` - Timestamp, in milliseconds since epoch, to get logs for. Defaults to None for all logs.


**Returns**:

  Log messages for the given job.

## tail\_logs

```python
def tail_logs(job: CoerceableToJobId,
              refresh_seconds: float = 1,
              sample_logs: bool = True,
              timeout: Optional[float] = None,
              get_logs_retries: int = 1)
```

Continuously print logs for a job

**Arguments**:

- `job` - the identifier of a job or a `RunResponse` object.
- `refresh_seconds` - how frequently, in seconds, to check for new logs. Defaults to 1.
- `sample_logs` - if true, print out only a sample of logs. Defaults to True.
- `timeout` - if not None, how long to continue tailing logs for. Defaults to None for indefinite.
- `get_logs_retries` - Number of additional retries for log requests. Defaults to 1.

## wait\_for\_job

```python
def wait_for_job(job: CoerceableToJobId,
                 poll_interval_seconds: float = 5,
                 timeout: Optional[float] = None) -> RunResponse
```

Block the Python kernel until the given job has finished

**Arguments**:

- `job` - the identifier of a job or a `RunResponse` object.
- `poll_interval_seconds` - How often (in seconds) to poll for status updates. Defaults to 5.
- `timeout` - The length of time in seconds to wait for the job. Defaults to None.


**Raises**:

- `TimeoutError` - if waiting for the job timed out.


**Returns**:

  The status of the given job.

## cancel\_job

```python
def cancel_job(job: CoerceableToJobId) -> RunResponse
```

Cancel an existing job

**Arguments**:

- `job` - the identifier of a job or a `RunResponse` object.


**Returns**:

  A new job object.

## \_whoami

```python
def _whoami() -> Any
```

Returns information on the currently logged in user

## \_list\_realtime\_instances

```python
def _list_realtime_instances(*, whose: str = "self") -> List[Any]
```

Returns information about available realtime instances

## upload

```python
def upload(path: str, data: Union[bytes, BinaryIO]) -> None
```

Upload a binary blob to a cloud location

## \_upload\_tmp

```python
def _upload_tmp(extension: str, data: Union[bytes, BinaryIO]) -> str
```

Upload a binary blob to a temporary cloud location, and return the new URL

## \_replace\_df\_input

```python
def _replace_df_input(
    input: Union[str, List[str], Path, "gpd.GeoDataFrame"]
) -> Union[str, List[str]]
```

If the input is a DataFrame, upload it and return a URL to it. Otherwise return input unchanged.

## \_health

```python
def _health() -> bool
```

Check the health of the API backend

## auth\_token

```python
def auth_token() -> str
```

Returns the current user's Fused environment (team) auth token
