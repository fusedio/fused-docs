---
sidebar_label: udf
title: fused._quick.udf
---

#### run

```python
def run(df_left: Optional[Union[pd.DataFrame, gpd.GeoDataFrame, pa.Table, str,
                                Path, Any]],
        df_right: Optional[Union[pd.DataFrame, gpd.GeoDataFrame, pa.Table, str,
                                 Path]] = None,
        step_config: Optional[JobStepConfig] = None,
        udf_email: Optional[str] = None,
        udf_id: Optional[str] = None,
        params: Optional[Dict[str, str]] = None,
        *,
        print_time: bool = False,
        read_options: Optional[Dict] = None,
        client_id: Optional[str] = None,
        dtype_out_vector: str = "parquet",
        dtype_out_raster: str = "tiff") -> pd.DataFrame
```

Run a UDF over a DataFrame.

**Arguments**:

- `df_left` - Input DataFrame, or path to a local Parquet file.
- `df_right` - Input DataFrame, or path to a local Parquet file.
- `step_config` - JobStepConfig, if not running a saved UDF.
- `udf_email` - Saved UDF&#x27;s owner.
- `udf_id` - Saved UDF&#x27;s ID.
- `params` - Additional parameters to pass to the UDF. Must be JSON serializable.
  

**Arguments**:

- `print_time` - If True, print the amount of time taken in the request.
- `read_options` - If not None, options for reading `df` that will be passed to GeoPandas.

