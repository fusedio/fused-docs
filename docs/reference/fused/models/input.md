---
sidebar_label: input
title: fused.models.input
---

## BaseInput Objects

```python
class BaseInput(BaseModel)
```

A base class for inputs into a UDF

#### step\_config

The currently executing [`step configuration`][fused.models.api.job.JobStepConfig]

## JoinInput Objects

```python
class JoinInput(BaseInput)
```

#### left

The [`chunk`][fused.models.udf.common.Chunk] containing data used as the left side of the join.

#### right

A list of [`chunk`][fused.models.udf.common.Chunk] objects containing data used as the right side of the join.

Only chunks whose bounding box intersects with the left chunk will be included.

#### data

```python
@property
def data() -> Tuple[ChunkData, ChunkData]
```

Returns the left and right data

## JoinSingleFileInput Objects

```python
class JoinSingleFileInput(BaseInput)
```

#### left

The [`chunk`][fused.models.udf.common.Chunk] containing data used as the left side of the join.

#### right

The data used as the right side of the join.

This will either be a [`pandas.DataFrame`][pandas.DataFrame],
[`geopandas.GeoDataFrame`][geopandas.GeoDataFrame], or
[`pyarrow.Table`][pyarrow.Table], depending on the type of user-defined function in
use.

#### data

```python
@property
def data() -> Tuple[ChunkData, ChunkData]
```

Returns the left and right data

## MapInput Objects

```python
class MapInput(BaseInput, Chunk)
```

The [`chunk`][fused.models.udf.common.Chunk] containing data used for the map operation.

