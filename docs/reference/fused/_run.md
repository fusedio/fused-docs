---
sidebar_label: _run
title: fused._run
---

## run

```python showLineNumbers
def run(email_or_udf_or_token: Union[str, None, UdfJobStepConfig,
                                     GeoPandasUdfV2] = None,
        udf_name: Optional[str] = None,
        *,
        udf: Optional[GeoPandasUdfV2] = None,
        job_step: Optional[UdfJobStepConfig] = None,
        token: Optional[str] = None,
        udf_email: Optional[str] = None,
        x: Optional[int] = None,
        y: Optional[int] = None,
        z: Optional[int] = None,
        lat: Optional[float] = None,
        lng: Optional[float] = None,
        bbox: Union[gpd.GeoDataFrame, shapely.Geometry, None] = None,
        sync: bool = True,
        engine: Optional[Literal["realtime", "batch", "local"]] = None,
        type: Optional[Literal["tile", "file"]] = None,
        **parameters)
```

Executes a user-defined function (UDF) with various execution and input options.

This function supports executing UDFs in different environments (realtime, batch, local),
with different types of inputs (tile coordinates, geographical bounding boxes, etc.), and
allows for both synchronous and asynchronous execution. It dynamically determines the execution
path based on the provided parameters.

**Arguments**:

- `email_or_udf_or_token` - A string that can either be an email, a UDF token, or a direct
  reference to a UDF object. It can also be a UdfJobStepConfig object for detailed
  configuration, or None to specify UDF details in other parameters.
- `udf_name` - The name of the UDF to execute.
- `udf` - A GeoPandasUdfV2 object for direct execution.
- `job_step` - A UdfJobStepConfig object for detailed execution configuration.
- `token` - A token representing a shared UDF.
- `udf_email` - The email associated with the UDF.
  x, y, z: Tile coordinates for tile-based UDF execution.
  lat, lng: Latitude and longitude for location-based UDF execution.
- `bbox` - A geographical bounding box (as a GeoDataFrame or shapely Geometry) defining the area of interest.
- `sync` - If True, execute the UDF synchronously. If False, execute asynchronously.
- `engine` - The execution engine to use ('realtime', 'batch', or 'local').
- `type` - The type of UDF execution ('tile' or 'file').
- `**parameters` - Additional parameters to pass to the UDF.


**Raises**:

- `ValueError` - If the UDF is not specified or is specified in more than one way.
- `TypeError` - If the first parameter is not of an expected type.
- `Warning` - Various warnings are issued for ignored parameters based on the execution path chosen.


**Returns**:

  The result of the UDF execution, which varies based on the UDF and execution path.


**Examples**:


  # Run a UDF saved in the Fused system:
    ```py
    fused.run(udf_email="username@fused.io", udf_name="my_udf_name")
    ```

  # Run a UDF saved in GitHub:
    ```py
    loaded_udf = fused.load("https://github.com/fusedio/udfs/tree/main/public/Building_Tile_Example")
    fused.run(udf=loaded_udf, bbox=bbox)
    ```

  # Run a UDF saved in a local directory:
    ```py
    loaded_udf = fused.load("/Users/local/dir/Building_Tile_Example")
    fused.run(udf=loaded_udf, bbox=bbox)
    ```


**Notes**:

  This function dynamically determines the execution path and parameters based on the inputs.
  It is designed to be flexible and support various UDF execution scenarios.
