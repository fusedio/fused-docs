from pathlib import Path
from typing import Protocol


class ExecutionContextProtocol(Protocol):
    @property
    def partition_tempdir(self) -> Path:
        """A partition-level temporary directory for user use during the job.

        A new directory is provided for each file."""
        ...

    @property
    def tempdir(self) -> Path:
        """A chunk-level temporary directory for user use during the job.

        A new directory is provided for each chunk."""
        ...


class LocalContext(ExecutionContextProtocol):
    @property
    def partition_tempdir(self) -> Path:
        raise NotImplementedError()

    @property
    def tempdir(self) -> Path:
        raise NotImplementedError()


context: ExecutionContextProtocol = LocalContext()
local_context = LocalContext()
