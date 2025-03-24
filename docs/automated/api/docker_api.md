---
sidebar_label: docker_api
title: api.docker_api
toc_max_heading_level: 5
unlisted: true
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
class FusedDockerAPI(FusedAPI)
```

API for running jobs in the Fused Docker container.

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

