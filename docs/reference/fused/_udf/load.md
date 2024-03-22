---
sidebar_label: load
title: fused._udf.load
---

#### load\_udf

```python
def load_udf(udf_paths: Sequence[str],
             *,
             parameters: Optional[Dict[str, Any]] = None,
             content_type: Optional[str] = None,
             load_schema: bool = True,
             header_paths: Optional[Sequence[Header]] = None) -> UdfRegistry
```

Load UDF(s) in a UdfRegistry object.

**Arguments**:

- `udf_paths` - The paths to the UDF source code files or URLs.
  If provided as a list, it loads and registers multiple UDFs as a UdfRegistry.
- `function` - The name of the UDF function to load.
- `parameters` - A dictionary of parameters to be passed to the UDF.
- `table_schema` - The schema of the input data table.
- `content_type` - The content type of the UDF source, e.g., &quot;file&quot;, &quot;py&quot;, or &quot;url&quot;.
- `load_schema` - Whether to automatically detect and load the table schema.
- `header_paths` - A sequence of headers for the UDF.
  

**Returns**:

  UdfRegistry or UDF: Returns a UdfRegistry containing registered UDFs.
  

**Raises**:

  - ValueError: If multiple UDFs with the same name are found in a list of UDF paths.
  - AssertionError: If an unsupported content type is provided.
  

**Examples**:

  Load multiple UDFs from a list of files and register them in a UdfRegistry:
  
    ```py
    load_udf(udf_paths=["udf1.py", "udf2.py"], header_paths=["header.py"])
    load_udf("my_udf.py", function="my_function", content_type="file")
    ```

