---
sidebar_label: job
title: fused.models.internal.job
---

## RunResponse Objects

```python
class RunResponse(BaseModel)
```

## job\_id

The identifier of this job.

## status

The status of the instance running this job.

## get\_status

```python
def get_status() -> RunResponse
```

Fetch the status of this job

**Returns**:

  The status of the given job.

## get\_logs

```python
def get_logs(since_ms: Optional[int] = None) -> List[Any]
```

Fetch logs for this job

**Arguments**:

- `since_ms` - Timestamp, in milliseconds since epoch, to get logs for. Defaults to None for all logs.


**Returns**:

  Log messages for the given job.

## print\_logs

```python
def print_logs(since_ms: Optional[int] = None,
               file: Optional[IO] = None) -> None
```

Fetch and print logs for this job

**Arguments**:

- `since_ms` - Timestamp, in milliseconds since epoch, to get logs for. Defaults to None for all logs.
- `file` - Where to print logs to. Defaults to sys.stdout.


**Returns**:

  None

## get\_exec\_time

```python
def get_exec_time() -> timedelta
```

Determine the execution time of this job, using the logs.

**Returns**:

  Time the job took. If the job is in progress, time from first to last log message is returned.

## tail\_logs

```python
def tail_logs(refresh_seconds: float = 1,
              sample_logs: bool = True,
              timeout: Optional[float] = None,
              get_logs_retries: int = 1) -> None
```

Continuously print logs for this job

**Arguments**:

- `refresh_seconds` - how frequently, in seconds, to check for new logs. Defaults to 1.
- `sample_logs` - if true, print out only a sample of logs. Defaults to True.
- `timeout` - if not None, how long to continue tailing logs for. Defaults to None for indefinite.
- `get_logs_retries` - Number of additional retries for log requests. Defaults to 1.

## wait\_for\_job

```python
def wait_for_job(poll_interval_seconds: float = 5,
                 timeout: Optional[float] = None) -> RunResponse
```

Block the Python kernel until this job has finished

**Arguments**:

- `poll_interval_seconds` - How often (in seconds) to poll for status updates. Defaults to 5.
- `timeout` - The length of time in seconds to wait for the job. Defaults to None.


**Raises**:

- `TimeoutError` - if waiting for the job timed out.


**Returns**:

  The status of the given job.

## cancel

```python
def cancel() -> RunResponse
```

Cancel this job

**Returns**:

  A new job object.

## refresh\_status

```python
def refresh_status() -> RunResponse
```

Refresh the status of this job.

## from\_job\_id

```python
@classmethod
def from_job_id(cls, job: Union[str, RunResponse]) -> RunResponse
```

Creates a RunResponse object from either a job ID or a RunResponse.

**Arguments**:

- `job` - Either a job ID string, or a RunResponse.


**Returns**:

  A RunResponse object.

## JobResponse Objects

```python
class JobResponse(BaseModel)
```

## id

The identifier of this job.

## creation\_date

When this job was started.

## job\_status

The status of this job.

## job\_status\_date

When the job_status was last updated

## config

```python
def config() -> JobStepConfig
```

Fetch the job step configuration

**Returns**:

  The configuration for the job step in this job.

## steps\_config

```python
def steps_config() -> JobConfig
```

Fetch the job configuration

**Returns**:

  The configuration for all job steps in this job.

## get\_status

```python
def get_status() -> RunResponse
```

Fetch the status of this job

**Returns**:

  The status of the given job.

## get\_logs

```python
def get_logs(since_ms: Optional[int] = None) -> List[Any]
```

Fetch logs for this job

**Arguments**:

- `since_ms` - Timestamp, in milliseconds since epoch, to get logs for. Defaults to None for all logs.


**Returns**:

  Log messages for the given job.

## print\_logs

```python
def print_logs(since_ms: Optional[int] = None,
               file: Optional[IO] = None) -> None
```

Fetch and print logs for this job

**Arguments**:

- `since_ms` - Timestamp, in milliseconds since epoch, to get logs for. Defaults to None for all logs.
- `file` - Where to print logs to. Defaults to sys.stdout.


**Returns**:

  None

## get\_exec\_time

```python
def get_exec_time() -> timedelta
```

Determine the execution time of this job, using the logs.

**Returns**:

  Time the job took. If the job is in progress, time from first to last log message is returned.

## tail\_logs

```python
def tail_logs(refresh_seconds: float = 1,
              sample_logs: bool = True,
              timeout: Optional[float] = None,
              get_logs_retries: int = 1)
```

Continuously print logs for this job

**Arguments**:

- `refresh_seconds` - how frequently, in seconds, to check for new logs. Defaults to 1.
- `sample_logs` - if true, print out only a sample of logs. Defaults to True.
- `timeout` - if not None, how long to continue tailing logs for. Defaults to None for indefinite.
- `get_logs_retries` - Number of additional retries for log requests. Defaults to 1.

## wait\_for\_job

```python
def wait_for_job(poll_interval_seconds: float = 5,
                 timeout: Optional[float] = None) -> RunResponse
```

Block the Python kernel until this job has finished

**Arguments**:

- `poll_interval_seconds` - How often (in seconds) to poll for status updates. Defaults to 5.
- `timeout` - The length of time in seconds to wait for the job. Defaults to None.


**Raises**:

- `TimeoutError` - if waiting for the job timed out.


**Returns**:

  The status of the given job.

## cancel

```python
def cancel() -> RunResponse
```

Cancel this job

**Returns**:

  A new job object.

## Jobs Objects

```python
class Jobs(BaseModel)
```

## jobs

The list of jobs.

## refresh

```python
def refresh() -> Jobs
```

Returns this object with an updated job list
