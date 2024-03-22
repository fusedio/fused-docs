---
sidebar_label: _specialized_udfs
title: fused.models.udf._specialized_udfs
---

## GeoPandasUdfV2Callable Objects

```python
class GeoPandasUdfV2Callable(GeoPandasUdfV2)
```

This class is returned from `@fused.udf` and represents
a UDF that can be instantiated into a job.

#### to\_file

```python
def to_file(where: Union[str, Path, BinaryIO], *, overwrite: bool = False)
```

Write the UDF to disk or the specified file-like object.

The UDF will be written as a Zip file.

**Arguments**:

- `where` - A path to a file or a file-like object.
  

**Arguments**:

- `overwrite` - If true, overwriting is allowed.

#### to\_directory

```python
def to_directory(where: Union[str, Path], *, overwrite: bool = False)
```

Write the UDF to disk as a directory (folder).

**Arguments**:

- `where` - A path to a directory.
  

**Arguments**:

- `overwrite` - If true, overwriting is allowed.

#### to\_gist

```python
def to_gist(where: Optional[str] = None, *, overwrite: bool = False)
```

Write the UDF to Github as a Gist.

**Arguments**:

- `gist_id` - Optionally, a Gist ID to overwrite.
  

**Arguments**:

- `overwrite` - If true, overwriting is allowed.

#### \_\_call\_\_

```python
def __call__(
    dataset: Optional[CoerceableToDatasetInput] = None,
    right: Optional[CoerceableToDatasetInput] = None,
    *,
    arg_list: Optional[Iterable[Any]] = None,
    output_table: Optional[str] = None,
    buffer_distance: Optional[float] = None,
    join_is_singlefile: Optional[bool] = None,
    join_how: Union[JoinType, Literal["left", "inner"]] = JoinType.INNER,
    **kwargs
) -> Union[
        UdfJobStepConfig,
        MapJobStepConfig,
        JoinJobStepConfig,
        JoinSinglefileJobStepConfig,
]
```

Create a job from this UDF.

**Arguments**:

- `dataset` - The dataset to run the UDF on.
- `right` - The right dataset to join with. If None, no join is performed and only `dataset` is processed. If this is a URL to a single Parquet file, a singlefile join is created. Defaults to None.
- `arg_list` - A list of records to pass in to the UDF as input. This option is mutually exclusive with `dataset` and `right`.
- `output_table` - The name of the table to write output columns on `dataset`.
- `buffer_distance` - For join jobs, the buffer around `dataset` partitions to perform.
- `right`0 - If not None, whether a join operation should be performed in `right`1 mode, i.e. all partitions join with a single Parquet file. Defaults to None, which indicates autodetect.

