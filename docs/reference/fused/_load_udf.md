---
sidebar_label: _load_udf
title: fused._load_udf
---

#### load

```python
def load(url_or_udf: Union[str, Path], *, cache_key: Any = None) -> BaseUdf
```

Loads a UDF (User-Defined Function) from various sources including GitHub URLs,
local files, or directories, and a Fused platform-specific identifier.

This function supports loading UDFs from a GitHub repository URL, a local file path,
a directory containing UDF definitions, or a Fused platform-specific identifier
composed of an email and UDF name. It intelligently determines the source type based
on the format of the input and retrieves the UDF accordingly.

**Arguments**:

- `url_or_udf` - A string or Path object representing the location of the UDF. This can be
  a GitHub URL starting with "https://github.com", a local file path, a directory
  containing one or more UDFs, or a Fused platform-specific identifier in the
  format "email/udf_name".
- `cache_key` - An optional key used for caching the loaded UDF. If provided, the function
  will attempt to load the UDF from cache using this key before attempting to
  load it from the specified source. Defaults to None, indicating no caching.
  

**Returns**:

- `BaseUdf` - An instance of the loaded UDF.
  

**Raises**:

- `FileNotFoundError` - If a local file or directory path is provided but does not exist.
- `ValueError` - If the URL or Fused platform-specific identifier format is incorrect or
  cannot be parsed.
- `Exception` - For errors related to network issues, file access permissions, or other
  unforeseen errors during the loading process.
  

**Examples**:

  Loading a UDF from a GitHub URL:
    ```py
    udf = fused.load("https://github.com/fusedio/udfs/tree/main/public/REM_with_HyRiver/")
    ```
  
  Loading a UDF from a local file:
    ```py
    udf = fused.load("/localpath/REM_with_HyRiver/")
    ```
  
  Loading a UDF using a Fused platform-specific identifier:
    ```py
    udf = fused.load("username@fused.io/REM_with_HyRiver")
    ```

