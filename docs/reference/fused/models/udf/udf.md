---
sidebar_label: udf
title: fused.models.udf.udf
---

## GeoPandasUdfV2 Objects

```python
class GeoPandasUdfV2(BaseUdf)
```

A user-defined function that operates on [`geopandas.GeoDataFrame`s][geopandas.GeoDataFrame].

## table\_schema

The [`Schema`][fused.models.Schema] describing the output of this UDF.

## entrypoint

Name of the function within the code to invoke.

## parameters

Parameters to pass into the entrypoint.

## \_nested\_callable

TODO : Find out type

## set\_parameters

```python
def set_parameters(parameters: Dict[str, Any],
                   replace_parameters: bool = False,
                   inplace: bool = False) -> "GeoPandasUdfV2"
```

Set the parameters on this UDF.

**Arguments**:

- `parameters` - The new parameters dictionary.
- `replace_parameters` - If True, unset any parameters not in the parameters argument. Defaults to False.
- `inplace` - If True, modify this object. If False, return a new object. Defaults to True.

## eval\_schema

```python
def eval_schema(inplace: bool = False) -> "GeoPandasUdfV2"
```

Reload the schema saved in the code of the UDF.

Note that this will evaluate the UDF function.

**Arguments**:

- `inplace` - If True, update this UDF object. Otherwise return a new UDF object (default).

## run\_local

```python
def run_local(sample: Any | None = ...,
              *,
              inplace: bool = False,
              validate_output: bool = False,
              validate_imports: Optional[bool] = None,
              **kwargs) -> "UdfEvaluationResult"
```

Evaluate this UDF against a sample.

**Arguments**:

- `sample` - Sample (from `get_sample`) to execute against.
- `inplace` - If True, update this UDF object with schema information. (default)
