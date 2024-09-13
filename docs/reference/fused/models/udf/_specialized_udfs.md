---
sidebar_label: _specialized_udfs
title: fused.models.udf._specialized_udfs
---

## GeoPandasUdfV2Callable Objects

```python
class GeoPandasUdfV2Callable(GeoPandasUdfV2)
```

## type

This class is returned from `@fused.udf` and represents
a UDF that can be instantiated into a job.

## to\_file

```python
def to_file(where: Union[str, Path, BinaryIO], *, overwrite: bool = False)
```

Write the UDF to disk or the specified file-like object.

The UDF will be written as a Zip file.

**Arguments**:

- `where` - A path to a file or a file-like object.


**Arguments**:

- `overwrite` - If true, overwriting is allowed.

## to\_directory

```python
def to_directory(where: Union[str, Path], *, overwrite: bool = False)
```

Write the UDF to disk as a directory (folder).

**Arguments**:

- `where` - A path to a directory.


**Arguments**:

- `overwrite` - If true, overwriting is allowed.

## to\_gist

```python
def to_gist(where: Optional[str] = None, *, overwrite: bool = False)
```

Write the UDF to Github as a Gist.

**Arguments**:

- `gist_id` - Optionally, a Gist ID to overwrite.


**Arguments**:

- `overwrite` - If true, overwriting is allowed.

## \_\_call\_\_

```python
def __call__(*,
             arg_list: Optional[Iterable[Any]] = None,
             **kwargs) -> Union[
                 UdfJobStepConfig,
             ]
```

Create a job from this UDF.

**Arguments**:

- `arg_list` - A list of records to pass in to the UDF as input.
