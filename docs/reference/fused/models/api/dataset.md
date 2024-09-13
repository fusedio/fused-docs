---
sidebar_label: dataset
title: fused.models.api.dataset
---

## JobMetadata Objects

```python
class JobMetadata(FusedBaseModel)
```

## ec2\_instance\_type

The EC2 instance this job is run on.

## time\_taken

The time taken for the job, if known.

## job\_id

The fused id for the job.

## job

```python
@property
def job() -> AnyJobStepConfig
```

The job step config that created this table.

## udf

```python
@property
def udf() -> Optional[AnyBaseUdf]
```

The user-defined function that created this table.

## udf\_code

```python
@property
def udf_code() -> Optional[str]
```

The code string of the user-defined function that created this table.

## inputs

```python
@property
def inputs() -> Tuple
```

The datasets that were combined to create this table.
