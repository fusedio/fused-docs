import json
from io import BytesIO
from typing import TYPE_CHECKING, Any, Dict, Optional, Union

import aiohttp
import requests
import yarl

from fused._deserialize_parquet import parquet_to_df
from fused._optional_deps import (
    GPD_GEODATAFRAME,
    HAS_GEOPANDAS,
    HAS_PANDAS,
    PD_DATAFRAME,
)
from fused._options import options as OPTIONS

from ._impl._context_impl import context_get_auth_header, context_get_user_email
from ._impl._realtime_ops_impl import (
    get_recursion_factor,
    make_realtime_url,
    make_shared_realtime_url,
)
from ._serialization import deserialize_tiff

if TYPE_CHECKING:
    import pandas as pd
    import xarray as xr

DEFAULT_DTYPE_VECTOR = "parquet"
DEFAULT_DTYPE_RASTER = "tiff"


class RealtimeInstanceChildError(ChildProcessError):
    pass


def serialize_realtime_params(params: Dict[str, Any]):
    result = {}
    for param_name, param_value in params.items():
        if (HAS_GEOPANDAS and isinstance(param_value, GPD_GEODATAFRAME)) or (
            HAS_PANDAS and isinstance(param_value, PD_DATAFRAME)
        ):
            result[param_name] = param_value.to_json()
        elif isinstance(param_value, (list, tuple, dict, bool)):
            result[param_name] = json.dumps(param_value)
        else:
            result[param_name] = param_value

    return result


def _parse_realtime_response(r: requests.Response, content_type: str):
    if content_type == "application/octet-stream":  # parquet
        return parquet_to_df(r.content)
    elif content_type == "image/png":
        import xarray as xr
        from PIL import Image

        image = Image.open(BytesIO(r.content))
        width, height = image.size
        if len(image.getbands()) == 1:
            image_data = list(image.getdata())
            image_data = [
                image_data[i : i + width] for i in range(0, len(image_data), width)
            ]
            data_array = xr.DataArray(image_data, dims=["y", "x"])
        else:
            image_data = []
            for band in range(len(image.getbands())):
                band_data = list(image.getdata(band=band))
                band_data = [
                    band_data[i : i + width] for i in range(0, len(band_data), width)
                ]
                image_data.append(band_data)
            data_array = xr.DataArray(image_data, dims=["band", "y", "x"])

        # Create the dataset with image, latitude, and longitude data
        dataset = xr.Dataset({"image": data_array})

        return dataset
    elif content_type == "image/tiff":
        return deserialize_tiff(r.content)

    return r.content  # TODO


async def _parse_realtime_response_async(content: bytes, content_type: str):
    if content_type == "application/octet-stream":  # parquet
        return parquet_to_df(content)
    elif content_type == "image/png":
        import xarray as xr
        from PIL import Image

        image = Image.open(BytesIO(content))
        width, height = image.size
        if len(image.getbands()) == 1:
            image_data = list(image.getdata())
            image_data = [
                image_data[i : i + width] for i in range(0, len(image_data), width)
            ]
            data_array = xr.DataArray(image_data, dims=["y", "x"])
        else:
            image_data = []
            for band in range(len(image.getbands())):
                band_data = list(image.getdata(band=band))
                band_data = [
                    band_data[i : i + width] for i in range(0, len(band_data), width)
                ]
                image_data.append(band_data)
            data_array = xr.DataArray(image_data, dims=["band", "y", "x"])

        # Create the dataset with image, latitude, and longitude data
        dataset = xr.Dataset({"image": data_array})

        return dataset
    elif content_type == "image/tiff":
        return deserialize_tiff(content)

    return content  # TODO


def _realtime_raise_for_status(r: requests.Response):
    if r.status_code >= 400 and "x-fused-error" in r.headers:
        msg = str(r.headers["x-fused-error"])
        raise requests.HTTPError(msg, response=r)
    if r.status_code >= 400 and "x-fused-metadata" in r.headers:
        msg = str(r.headers["x-fused-metadata"])
        rt_instance_exception = None
        try:
            rt_instance_exception = json.loads(msg)
        except json.JSONDecodeError:
            raise requests.HTTPError(msg, response=r)
        raise RealtimeInstanceChildError(rt_instance_exception)
    r.raise_for_status()


def _realtime_raise_for_status_async(r: aiohttp.ClientResponse):
    if r.status >= 400 and "x-fused-error" in r.headers:
        msg = str(r.headers["x-fused-error"])
        raise aiohttp.ClientResponseError(
            request_info=None,
            status=r.status,
            message=msg,
            headers=[],
            history=(),
        )
    if r.status >= 400 and "x-fused-metadata" in r.headers:
        msg = str(r.headers["x-fused-metadata"])
        rt_instance_exception = None
        try:
            rt_instance_exception = json.loads(msg)
        except json.JSONDecodeError:
            raise aiohttp.ClientResponseError(
                request_info=None,
                status=r.status,
                message=msg,
                headers=[],
                history=(),
            )
        raise RealtimeInstanceChildError(rt_instance_exception)
    r.raise_for_status()


async def _realtime_follow_redirect_async(
    *, session: aiohttp.ClientSession, r: aiohttp.ClientResponse
):
    if r.status >= 300 and r.status < 400 and "location" in r.headers:
        # Per this link, aiohttp will mangle the redirect URL
        # https://stackoverflow.com/questions/77319421/aiohttp-showing-403-forbidden-error-but-requests-get-giving-200-ok-response
        url = yarl.URL(r.headers["location"], encoded=True)
        return await session.get(url)
    return r


def _run_tile(
    url: str,
    *,
    _dtype_out_vector: str = DEFAULT_DTYPE_VECTOR,
    _dtype_out_raster: str = DEFAULT_DTYPE_RASTER,
    _is_shared: bool = False,
    **params,
):
    access_token_header = context_get_auth_header(missing_ok=_is_shared)
    recursion_factor = get_recursion_factor()

    req_params = {
        # TODO...
        "dtype_out_vector": _dtype_out_vector,
        "dtype_out_raster": _dtype_out_raster,
        **(serialize_realtime_params(params) if params is not None else {}),
    }

    r = requests.get(
        url=url,
        params=req_params,
        headers={
            **access_token_header,
            "Fused-Recursion": f"{recursion_factor}",
        },
    )
    _realtime_raise_for_status(r)

    return _parse_realtime_response(r, content_type=r.headers["content-type"])


def run_tile(
    email: str,
    id: Optional[str] = None,
    *,
    x: int,
    y: int,
    z: int,
    _dtype_out_vector: str = DEFAULT_DTYPE_VECTOR,
    _dtype_out_raster: str = DEFAULT_DTYPE_RASTER,
    _client_id: Optional[str] = None,
    **params,
) -> Optional[Union["pd.DataFrame", "xr.Dataset"]]:
    """
    Executes a private tile-based UDF indexed under the specified email and ID. The calling user must have the necessary permissions to execute the UDF.

    This function constructs a URL to run a UDF on a specific tile defined by its x, y, and z coordinates, and
    sends a request to the server. It supports customization of the output data types for vector and raster data,
    as well as additional parameters for the UDF execution.

    Args:
        email (str): Email address of user account associated with the UDF.
        id (Optional[str]): Unique identifier for the UDF. If None, the user's email is used as the ID.
        x (int): The x coordinate of the tile.
        y (int): The y coordinate of the tile.
        z (int): The zoom level of the tile.
        _dtype_out_vector (str): Desired data type for vector output. Defaults to a pre-defined type.
        _dtype_out_raster (str): Desired data type for raster output. Defaults to a pre-defined type.
        _client_id (Optional[str]): Client identifier for API usage. If None, a default or global client ID may be used.
        **params: Additional keyword arguments for the UDF execution.

    Returns:
        The response from the server after executing the UDF on the specified tile.
    """
    if id is None:
        id = email
        email = context_get_user_email()

    url = f"{make_realtime_url(_client_id)}/api/v1/run/udf/saved/{email}/{id}/tiles/{z}/{x}/{y}"
    return _run_tile(
        url=url,
        _dtype_out_vector=_dtype_out_vector,
        _dtype_out_raster=_dtype_out_raster,
        **params,
    )


def run_shared_tile(
    token: str,
    *,
    x: int,
    y: int,
    z: int,
    _dtype_out_vector: str = DEFAULT_DTYPE_VECTOR,
    _dtype_out_raster: str = DEFAULT_DTYPE_RASTER,
    _client_id: Optional[str] = None,
    **params,
) -> Optional[Union["pd.DataFrame", "xr.Dataset"]]:
    """
    Executes a shared tile-based UDF.

    This function constructs a URL to run a UDF on a specific tile defined by its x, y, and z coordinates, and
    sends a request to the server. It supports customization of the output data types for vector and raster data,
    as well as additional parameters for the UDF execution.

    Args:
        token (str): A shared access token that authorizes the operation.
        id (Optional[str]): Unique identifier for the UDF. If None, the user's email is used as the ID.
        x (int): The x coordinate of the tile.
        y (int): The y coordinate of the tile.
        z (int): The zoom level of the tile.
        _dtype_out_vector (str): Desired data type for vector output. Defaults to a pre-defined type.
        _dtype_out_raster (str): Desired data type for raster output. Defaults to a pre-defined type.
        _client_id (Optional[str]): Client identifier for API usage. If None, a default or global client ID may be used.
        **params: Additional keyword arguments for the UDF execution.

    Returns:
        The response from the server after executing the UDF on the specified tile.
    """
    url = f"{make_shared_realtime_url(token)}/run/tiles/{z}/{x}/{y}"
    return _run_tile(
        url=url,
        _dtype_out_vector=_dtype_out_vector,
        _dtype_out_raster=_dtype_out_raster,
        _client_id=_client_id,
        _is_shared=True,
        **params,
    )


def _run_file(
    url: str,
    *,
    _dtype_out_vector: str = DEFAULT_DTYPE_VECTOR,
    _dtype_out_raster: str = DEFAULT_DTYPE_RASTER,
    _is_shared: bool = False,
    **params,
):
    access_token_header = context_get_auth_header(missing_ok=_is_shared)
    recursion_factor = get_recursion_factor()

    req_params = {
        # TODO...
        "dtype_out_vector": _dtype_out_vector,
        "dtype_out_raster": _dtype_out_raster,
        **(serialize_realtime_params(params) if params is not None else {}),
    }

    r = requests.get(
        url=url,
        params=req_params,
        headers={
            **access_token_header,
            "Fused-Recursion": f"{recursion_factor}",
        },
    )
    _realtime_raise_for_status(r)

    return _parse_realtime_response(r, content_type=r.headers["content-type"])


def run_file(
    email: str,
    id: Optional[str] = None,
    *,
    _dtype_out_vector: str = DEFAULT_DTYPE_VECTOR,
    _dtype_out_raster: str = DEFAULT_DTYPE_RASTER,
    _client_id: Optional[str] = None,
    **params,
) -> Optional[Union["pd.DataFrame", "xr.Dataset"]]:
    """
    Executes a private file-based UDF indexed under the specified email and ID. The calling user must have the necessary permissions to execute the UDF.

    This function constructs a URL to run a UDF associated with the given email and ID, allowing for output data type customization for both vector and raster outputs. It also supports additional parameters for the UDF execution.

    Args:
        email (str): Email address of user account associated with the UDF.
        id (Optional[str]): Unique identifier for the UDF. If None, the user's email is used as the ID.
        _dtype_out_vector (str): Desired data type for vector output, defaults to a predefined type.
        _dtype_out_raster (str): Desired data type for raster output, defaults to a predefined type.
        _client_id (Optional[str]): Client identifier for API usage. If None, a default or global client ID may be used.
        **params: Additional keyword arguments for the UDF execution.

    Returns:
        The response from the server after executing the UDF.
    """
    if id is None:
        id = email
        email = context_get_user_email()

    url = f"{make_realtime_url(_client_id)}/api/v1/run/udf/saved/{email}/{id}"
    return _run_file(
        url=url,
        _dtype_out_vector=_dtype_out_vector,
        _dtype_out_raster=_dtype_out_raster,
        **params,
    )


def run_shared_file(
    token: str,
    *,
    _dtype_out_vector: str = DEFAULT_DTYPE_VECTOR,
    _dtype_out_raster: str = DEFAULT_DTYPE_RASTER,
    **params,
) -> Optional[Union["pd.DataFrame", "xr.Dataset"]]:
    """
    Executes a shared file-based UDF.

    This function constructs a URL for running an operation on a file accessible via a shared token. It allows for customization of the output data types for vector and raster data and supports additional parameters for the operation's execution.

    Args:
        token (str): A shared access token that authorizes the operation.
        _dtype_out_vector (str): Desired data type for vector output, defaults to a predefined type.
        _dtype_out_raster (str): Desired data type for raster output, defaults to a predefined type.
        **params: Additional keyword arguments for the operation execution.

    Returns:
        The response from the server after executing the operation on the file.

    Raises:
        Exception: Describes various exceptions that could occur during the function execution, including but not limited to invalid parameters, network errors, unauthorized access errors, or server-side errors.

    Note:
        This function is designed to access shared operations that require a token for authorization. It requires network access to communicate with the server hosting these operations and may incur data transmission costs or delays depending on the network's performance.
    """
    url = f"{make_shared_realtime_url(token)}/run/file"
    return _run_file(
        url=url,
        _dtype_out_vector=_dtype_out_vector,
        _dtype_out_raster=_dtype_out_raster,
        _is_shared=True,
        **params,
    )


async def _run_tile_async(
    url: str,
    *,
    _dtype_out_vector: str = DEFAULT_DTYPE_VECTOR,
    _dtype_out_raster: str = DEFAULT_DTYPE_RASTER,
    _is_shared: bool = False,
    **params,
):
    access_token_header = context_get_auth_header(missing_ok=_is_shared)
    recursion_factor = get_recursion_factor()

    req_params = {
        # TODO...
        "dtype_out_vector": _dtype_out_vector,
        "dtype_out_raster": _dtype_out_raster,
        **(serialize_realtime_params(params) if params is not None else {}),
    }

    if OPTIONS.pyodide_async_requests:
        import pyodide.http

        url_with_params = yarl.URL(url, encoded=True).with_query(req_params)
        r = await pyodide.http.pyfetch(
            str(url_with_params),
            headers={
                **access_token_header,
                "Fused-Recursion": f"{recursion_factor}",
            },
        )
        redirect = r.headers.get("x-fused-redirect", None)
        if redirect:
            url = yarl.URL(redirect, encoded=True)
            r = await pyodide.http.pyfetch(url)

        _realtime_raise_for_status_async(r)

        return await _parse_realtime_response_async(
            await r.bytes(), content_type=r.headers["content-type"]
        )
    else:
        async with aiohttp.ClientSession() as session:
            async with session.get(
                url=url,
                params=req_params,
                headers={
                    **access_token_header,
                    "Fused-Recursion": f"{recursion_factor}",
                },
                allow_redirects=False,
            ) as r:
                r = await _realtime_follow_redirect_async(session=session, r=r)
                _realtime_raise_for_status_async(r)

                return await _parse_realtime_response_async(
                    await r.read(), content_type=r.headers["content-type"]
                )


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
    **params,
) -> Optional[Union["pd.DataFrame", "xr.Dataset"]]:
    """
    Asynchronously executes a private tile-based UDF indexed under the specified email and ID. The calling user must have the necessary permissions to execute the UDF.

    This function constructs a URL to asynchronously run a UDF on a specific tile defined by its x, y, and z coordinates. It supports customization of the output data types for vector and raster data, and accommodates additional parameters for the UDF execution.

    Args:
        email (str): User's email address. Used to identify the user's saved UDFs. If the ID is not provided, the email is also used as the ID.
        id (Optional[str]): Unique identifier for the UDF. If None, the user's email is used as the ID.
        x (int): The x coordinate of the tile.
        y (int): The y coordinate of the tile.
        z (int): The zoom level of the tile.
        _dtype_out_vector (str): Desired data type for vector output. Defaults to a predefined type.
        _dtype_out_raster (str): Desired data type for raster output. Defaults to a predefined type.
        _client_id (Optional[str]): Client identifier for API usage. If None, a default or global client ID may be used.
        **params: Additional keyword arguments for the UDF execution.

    Returns:
        A coroutine that, when awaited, sends a request to the server to execute the UDF on the specified tile and returns the server's response. The format and content of the response depend on the UDF's implementation and the server's response format.
    """
    if id is None:
        id = email
        email = context_get_user_email()

    url = f"{make_realtime_url(_client_id)}/api/v1/run/udf/saved/{email}/{id}/tiles/{z}/{x}/{y}"
    return await _run_tile_async(
        url=url,
        _dtype_out_vector=_dtype_out_vector,
        _dtype_out_raster=_dtype_out_raster,
        **params,
    )


async def run_shared_tile_async(
    token: str,
    *,
    x: int,
    y: int,
    z: int,
    _dtype_out_vector: str = DEFAULT_DTYPE_VECTOR,
    _dtype_out_raster: str = DEFAULT_DTYPE_RASTER,
    **params,
) -> Optional[Union["pd.DataFrame", "xr.Dataset"]]:
    """
    Asynchronously executes a shared tile-based UDF using a specific access token.

    This function constructs a URL for running an operation on a tile, defined by its x, y, and z coordinates, accessible via a shared token. It allows for customization of the output data types for vector and raster data and supports additional parameters for the operation's execution.

    Args:
        token (str): A shared access token that authorizes the operation on the specified tile.
        x (int): The x coordinate of the tile.
        y (int): The y coordinate of the tile.
        z (int): The zoom level of the tile.
        _dtype_out_vector (str): Desired data type for vector output, defaults to a predefined type.
        _dtype_out_raster (str): Desired data type for raster output, defaults to a predefined type.
        **params: Additional keyword arguments for the operation execution.

    Returns:
        A coroutine that, when awaited, sends a request to the server to execute the operation on the specified tile and returns the server's response. The format and content of the response depend on the operation's implementation and the server's response format.
    """
    url = f"{make_shared_realtime_url(token)}/run/tiles/{z}/{x}/{y}"
    return await _run_tile_async(
        url=url,
        _dtype_out_vector=_dtype_out_vector,
        _dtype_out_raster=_dtype_out_raster,
        _is_shared=True,
        **params,
    )


async def _run_file_async(
    url: str,
    *,
    _dtype_out_vector: str = DEFAULT_DTYPE_VECTOR,
    _dtype_out_raster: str = DEFAULT_DTYPE_RASTER,
    _is_shared: bool = False,
    **params,
):
    access_token_header = context_get_auth_header(missing_ok=_is_shared)
    recursion_factor = get_recursion_factor()

    req_params = {
        # TODO...
        "dtype_out_vector": _dtype_out_vector,
        "dtype_out_raster": _dtype_out_raster,
        **(serialize_realtime_params(params) if params is not None else {}),
    }

    if OPTIONS.pyodide_async_requests:
        import pyodide.http

        url_with_params = yarl.URL(url, encoded=True).with_query(req_params)
        r = await pyodide.http.pyfetch(
            str(url_with_params),
            headers={
                **access_token_header,
                "Fused-Recursion": f"{recursion_factor}",
            },
        )
        redirect = r.headers.get("x-fused-redirect", None)
        if redirect:
            url = yarl.URL(redirect, encoded=True)
            r = await pyodide.http.pyfetch(url)

        _realtime_raise_for_status_async(r)

        return await _parse_realtime_response_async(
            await r.bytes(), content_type=r.headers["content-type"]
        )
    else:
        async with aiohttp.ClientSession() as session:
            async with session.get(
                url=url,
                params=req_params,
                headers={
                    **access_token_header,
                    "Fused-Recursion": f"{recursion_factor}",
                },
                allow_redirects=False,
            ) as r:
                r = await _realtime_follow_redirect_async(session=session, r=r)
                _realtime_raise_for_status_async(r)

                return await _parse_realtime_response_async(
                    await r.read(), content_type=r.headers["content-type"]
                )


async def run_file_async(
    email: str,
    id: Optional[str] = None,
    *,
    _dtype_out_vector: str = DEFAULT_DTYPE_VECTOR,
    _dtype_out_raster: str = DEFAULT_DTYPE_RASTER,
    _client_id: Optional[str] = None,
    **params,
) -> Optional[Union["pd.DataFrame", "xr.Dataset"]]:
    """
    Asynchronously executes a file-based UDF associated with the specific email and ID.

    This function constructs a URL to run a UDF on a server, allowing for output data type customization for vector and raster outputs and supporting additional parameters for the UDF execution. If no ID is provided, the user's email is used as the identifier.

    Args:
        email (str): The user's email address, used to identify the user's saved UDFs. If the ID is not provided, this email will also be used as the ID.
        id (Optional[str]): Unique identifier for the UDF. If None, the function fetches the user's email as the ID.
        _dtype_out_vector (str): Desired data type for vector output, defaults to a predefined type.
        _dtype_out_raster (str): Desired data type for raster output, defaults to a predefined type.
        _client_id (Optional[str]): Client identifier for API usage. If None, a default or global client ID may be used.
        **params: Additional keyword arguments for the UDF execution.

    Returns:
        A coroutine that, when awaited, sends a request to the server to execute the UDF and returns the server's response. The format and content of the response depend on the UDF's implementation and the server's response format.
    """
    if id is None:
        id = email
        email = context_get_user_email()

    url = f"{make_realtime_url(_client_id)}/api/v1/run/udf/saved/{email}/{id}"
    return await _run_file_async(
        url=url,
        _dtype_out_vector=_dtype_out_vector,
        _dtype_out_raster=_dtype_out_raster,
        **params,
    )


async def run_shared_file_async(
    token: str,
    *,
    _dtype_out_vector: str = DEFAULT_DTYPE_VECTOR,
    _dtype_out_raster: str = DEFAULT_DTYPE_RASTER,
    **params,
) -> Optional[Union["pd.DataFrame", "xr.Dataset"]]:
    """
    Asynchronously executes a shared file-based UDF using the specific access token.

    Constructs a URL to run an operation on a file accessible via a shared token, enabling customization of the output data types for vector and raster data. It accommodates additional parameters for the operation's execution.

    Args:
        token (str): A shared access token that authorizes the operation.
        _dtype_out_vector (str): Desired data type for vector output, defaults to a predefined type.
        _dtype_out_raster (str): Desired data type for raster output, defaults to a predefined type.
        **params: Additional keyword arguments for the operation execution.

    Returns:
        A coroutine that, when awaited, sends a request to the server to execute the operation on the file and returns the server's response. The format and content of the response depend on the operation's implementation and the server's response format.
    """
    url = f"{make_shared_realtime_url(token)}/run/file"
    return await _run_file_async(
        url=url,
        _dtype_out_vector=_dtype_out_vector,
        _dtype_out_raster=_dtype_out_raster,
        _is_shared=True,
        **params,
    )
