---
sidebar_label: decorators
title: fused._udf.decorators
---

#### RESERVED\_UDF\_PARAMETERS

Set of UDF parameter names that should not be used because they will cause conflicts
when instantiating the UDF to a job.

#### udf

```python
def udf(
    fn: Optional[Callable] = None,
    *,
    schema: Union[Schema, Dict, None] = None,
    name: Optional[str] = None,
    default_parameters: Optional[Dict[str, Any]] = None,
    headers: Optional[Sequence[Union[str, Header]]] = None
) -> Callable[..., GeoPandasUdfV2Callable]
```

A decorator that transforms a function into a Fused UDF.

**Arguments**:

- `schema` - The schema for the DataFrame returned by the UDF. The schema may be either
  a string (in the form `"field_name:DataType field_name2:DataType"`, or as JSON),
  as a Python dictionary representing the schema, or a `Schema` model object.
  
  Defaults to None, in which case a schema must be evaluated by calling `run_local`
  for a job to be able to write output. The return value of `run_local` will also
  indicate how to include the schema in the decorator so `run_local` does not need
  to be run again.
- `name` - The name of the UDF object. Defaults to the name of the function.
- `default_parameters` - Parameters to embed in the UDF object, separately from the arguments
  list of the function. Defaults to None for empty parameters.
- `headers` - A list of files to include as modules when running the UDF. For example,
  when specifying `headers=['my_header.py']`, inside the UDF function it may be
  referenced as:
  
        `"field_name:DataType field_name2:DataType"`0
  
  Defaults to None for no headers.

**Returns**:

  A callable that represents the transformed UDF. This callable can be used
  within GeoPandas workflows to apply the defined operation on geospatial data.
  

**Examples**:

  To create a simple UDF that calls a utility function to calculate the area of geometries in a GeoDataFrame:
  
    `"field_name:DataType field_name2:DataType"`1

