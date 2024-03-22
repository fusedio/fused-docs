---
sidebar_label: context
title: fused._udf.context
---

## ExecutionContextProtocol Objects

```python
class ExecutionContextProtocol(Protocol)
```

#### partition\_tempdir

```python
@property
def partition_tempdir() -> Path
```

A partition-level temporary directory for user use during the job.

A new directory is provided for each file.

#### tempdir

```python
@property
def tempdir() -> Path
```

A chunk-level temporary directory for user use during the job.

A new directory is provided for each chunk.

