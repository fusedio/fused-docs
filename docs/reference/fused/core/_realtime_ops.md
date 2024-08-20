---
sidebar_label: _realtime_ops
title: fused.core._realtime_ops
---

## run\_tile

```python showLineNumbers
def run_tile(email: str,
             id: Optional[str] = None,
             *,
             x: int,
             y: int,
             z: int,
             _dtype_out_vector: str = DEFAULT_DTYPE_VECTOR,
             _dtype_out_raster: str = DEFAULT_DTYPE_RASTER,
             _client_id: Optional[str] = None,
             **params) -> Optional[Union[pd.DataFrame, xr.Dataset]]
```

Executes a private tile-based UDF indexed under the specified email and ID. The calling user must have the necessary permissions to execute the UDF.

This function constructs a URL to run a UDF on a specific tile defined by its x, y, and z coordinates, and
sends a request to the server. It supports customization of the output data types for vector and raster data,
as well as additional parameters for the UDF execution.

**Arguments**:

- `email` _str_ - Email address of user account associated with the UDF.
- `id` _Optional[str]_ - Unique identifier for the UDF. If None, the user's email is used as the ID.
- `x` _int_ - The x coordinate of the tile.
- `y` _int_ - The y coordinate of the tile.
- `z` _int_ - The zoom level of the tile.
- `_dtype_out_vector` _str_ - Desired data type for vector output. Defaults to a pre-defined type.
- `_dtype_out_raster` _str_ - Desired data type for raster output. Defaults to a pre-defined type.
- `_client_id` _Optional[str]_ - Client identifier for API usage. If None, a default or global client ID may be used.
- `**params` - Additional keyword arguments for the UDF execution.


**Returns**:

  The response from the server after executing the UDF on the specified tile.

## run\_shared\_tile

```python showLineNumbers
def run_shared_tile(token: str,
                    *,
                    x: int,
                    y: int,
                    z: int,
                    _dtype_out_vector: str = DEFAULT_DTYPE_VECTOR,
                    _dtype_out_raster: str = DEFAULT_DTYPE_RASTER,
                    _client_id: Optional[str] = None,
                    **params) -> Optional[Union[pd.DataFrame, xr.Dataset]]
```

Executes a shared tile-based UDF.

This function constructs a URL to run a UDF on a specific tile defined by its x, y, and z coordinates, and
sends a request to the server. It supports customization of the output data types for vector and raster data,
as well as additional parameters for the UDF execution.

**Arguments**:

- `token` _str_ - A shared access token that authorizes the operation.
- `id` _Optional[str]_ - Unique identifier for the UDF. If None, the user's email is used as the ID.
- `x` _int_ - The x coordinate of the tile.
- `y` _int_ - The y coordinate of the tile.
- `z` _int_ - The zoom level of the tile.
- `_dtype_out_vector` _str_ - Desired data type for vector output. Defaults to a pre-defined type.
- `_dtype_out_raster` _str_ - Desired data type for raster output. Defaults to a pre-defined type.
- `_client_id` _Optional[str]_ - Client identifier for API usage. If None, a default or global client ID may be used.
- `**params` - Additional keyword arguments for the UDF execution.


**Returns**:

  The response from the server after executing the UDF on the specified tile.

## run\_file

```python showLineNumbers
def run_file(email: str,
             id: Optional[str] = None,
             *,
             _dtype_out_vector: str = DEFAULT_DTYPE_VECTOR,
             _dtype_out_raster: str = DEFAULT_DTYPE_RASTER,
             _client_id: Optional[str] = None,
             **params) -> Optional[Union[pd.DataFrame, xr.Dataset]]
```

Executes a private file-based UDF indexed under the specified email and ID. The calling user must have the necessary permissions to execute the UDF.

This function constructs a URL to run a UDF associated with the given email and ID, allowing for output data type customization for both vector and raster outputs. It also supports additional parameters for the UDF execution.

**Arguments**:

- `email` _str_ - Email address of user account associated with the UDF.
- `id` _Optional[str]_ - Unique identifier for the UDF. If None, the user's email is used as the ID.
- `_dtype_out_vector` _str_ - Desired data type for vector output, defaults to a predefined type.
- `_dtype_out_raster` _str_ - Desired data type for raster output, defaults to a predefined type.
- `_client_id` _Optional[str]_ - Client identifier for API usage. If None, a default or global client ID may be used.
- `**params` - Additional keyword arguments for the UDF execution.


**Returns**:

  The response from the server after executing the UDF.

## run\_shared\_file

```python showLineNumbers
def run_shared_file(token: str,
                    *,
                    _dtype_out_vector: str = DEFAULT_DTYPE_VECTOR,
                    _dtype_out_raster: str = DEFAULT_DTYPE_RASTER,
                    **params) -> Optional[Union[pd.DataFrame, xr.Dataset]]
```

Executes a shared file-based UDF.

This function constructs a URL for running an operation on a file accessible via a shared token. It allows for customization of the output data types for vector and raster data and supports additional parameters for the operation's execution.

**Arguments**:

- `token` _str_ - A shared access token that authorizes the operation.
- `_dtype_out_vector` _str_ - Desired data type for vector output, defaults to a predefined type.
- `_dtype_out_raster` _str_ - Desired data type for raster output, defaults to a predefined type.
- `**params` - Additional keyword arguments for the operation execution.


**Returns**:

  The response from the server after executing the operation on the file.


**Raises**:

- `Exception` - Describes various exceptions that could occur during the function execution, including but not limited to invalid parameters, network errors, unauthorized access errors, or server-side errors.


**Notes**:

  This function is designed to access shared operations that require a token for authorization. It requires network access to communicate with the server hosting these operations and may incur data transmission costs or delays depending on the network's performance.

## run\_tile\_async

```python showLineNumbers
async def run_tile_async(
        email: str,
        id: Optional[str] = None,
        *,
        x: int,
        y: int,
        z: int,
        _dtype_out_vector: str = DEFAULT_DTYPE_VECTOR,
        _dtype_out_raster: str = DEFAULT_DTYPE_RASTER,
        _client_id: Optional[str] = None,
        **params) -> Optional[Union[pd.DataFrame, xr.Dataset]]
```

Asynchronously executes a private tile-based UDF indexed under the specified email and ID. The calling user must have the necessary permissions to execute the UDF.

This function constructs a URL to asynchronously run a UDF on a specific tile defined by its x, y, and z coordinates. It supports customization of the output data types for vector and raster data, and accommodates additional parameters for the UDF execution.

**Arguments**:

- `email` _str_ - User's email address. Used to identify the user's saved UDFs. If the ID is not provided, the email is also used as the ID.
- `id` _Optional[str]_ - Unique identifier for the UDF. If None, the user's email is used as the ID.
- `x` _int_ - The x coordinate of the tile.
- `y` _int_ - The y coordinate of the tile.
- `z` _int_ - The zoom level of the tile.
- `_dtype_out_vector` _str_ - Desired data type for vector output. Defaults to a predefined type.
- `_dtype_out_raster` _str_ - Desired data type for raster output. Defaults to a predefined type.
- `_client_id` _Optional[str]_ - Client identifier for API usage. If None, a default or global client ID may be used.
- `**params` - Additional keyword arguments for the UDF execution.


**Returns**:

  A coroutine that, when awaited, sends a request to the server to execute the UDF on the specified tile and returns the server's response. The format and content of the response depend on the UDF's implementation and the server's response format.

## run\_shared\_tile\_async

```python showLineNumbers
async def run_shared_tile_async(
        token: str,
        *,
        x: int,
        y: int,
        z: int,
        _dtype_out_vector: str = DEFAULT_DTYPE_VECTOR,
        _dtype_out_raster: str = DEFAULT_DTYPE_RASTER,
        **params) -> Optional[Union[pd.DataFrame, xr.Dataset]]
```

Asynchronously executes a shared tile-based UDF using a specific access token.

This function constructs a URL for running an operation on a tile, defined by its x, y, and z coordinates, accessible via a shared token. It allows for customization of the output data types for vector and raster data and supports additional parameters for the operation's execution.

**Arguments**:

- `token` _str_ - A shared access token that authorizes the operation on the specified tile.
- `x` _int_ - The x coordinate of the tile.
- `y` _int_ - The y coordinate of the tile.
- `z` _int_ - The zoom level of the tile.
- `_dtype_out_vector` _str_ - Desired data type for vector output, defaults to a predefined type.
- `_dtype_out_raster` _str_ - Desired data type for raster output, defaults to a predefined type.
- `**params` - Additional keyword arguments for the operation execution.


**Returns**:

  A coroutine that, when awaited, sends a request to the server to execute the operation on the specified tile and returns the server's response. The format and content of the response depend on the operation's implementation and the server's response format.

## run\_file\_async

```python showLineNumbers
async def run_file_async(
        email: str,
        id: Optional[str] = None,
        *,
        _dtype_out_vector: str = DEFAULT_DTYPE_VECTOR,
        _dtype_out_raster: str = DEFAULT_DTYPE_RASTER,
        _client_id: Optional[str] = None,
        **params) -> Optional[Union[pd.DataFrame, xr.Dataset]]
```

Asynchronously executes a file-based UDF associated with the specific email and ID.

This function constructs a URL to run a UDF on a server, allowing for output data type customization for vector and raster outputs and supporting additional parameters for the UDF execution. If no ID is provided, the user's email is used as the identifier.

**Arguments**:

- `email` _str_ - The user's email address, used to identify the user's saved UDFs. If the ID is not provided, this email will also be used as the ID.
- `id` _Optional[str]_ - Unique identifier for the UDF. If None, the function fetches the user's email as the ID.
- `_dtype_out_vector` _str_ - Desired data type for vector output, defaults to a predefined type.
- `_dtype_out_raster` _str_ - Desired data type for raster output, defaults to a predefined type.
- `_client_id` _Optional[str]_ - Client identifier for API usage. If None, a default or global client ID may be used.
- `**params` - Additional keyword arguments for the UDF execution.


**Returns**:

  A coroutine that, when awaited, sends a request to the server to execute the UDF and returns the server's response. The format and content of the response depend on the UDF's implementation and the server's response format.

## run\_shared\_file\_async

```python showLineNumbers
async def run_shared_file_async(
        token: str,
        *,
        _dtype_out_vector: str = DEFAULT_DTYPE_VECTOR,
        _dtype_out_raster: str = DEFAULT_DTYPE_RASTER,
        **params) -> Optional[Union[pd.DataFrame, xr.Dataset]]
```

Asynchronously executes a shared file-based UDF using the specific access token.

Constructs a URL to run an operation on a file accessible via a shared token, enabling customization of the output data types for vector and raster data. It accommodates additional parameters for the operation's execution.

**Arguments**:

- `token` _str_ - A shared access token that authorizes the operation.
- `_dtype_out_vector` _str_ - Desired data type for vector output, defaults to a predefined type.
- `_dtype_out_raster` _str_ - Desired data type for raster output, defaults to a predefined type.
- `**params` - Additional keyword arguments for the operation execution.


**Returns**:

  A coroutine that, when awaited, sends a request to the server to execute the operation on the file and returns the server's response. The format and content of the response depend on the operation's implementation and the server's response format.
