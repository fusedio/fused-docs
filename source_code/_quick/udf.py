# TODO: This file is no longer the most recent -- use fused.core.run_* instead
# This file is only for running non-saved (code included) UDFs
from __future__ import annotations

import json
import time
import warnings
from io import BytesIO
from pathlib import Path
from typing import TYPE_CHECKING, Any, Dict, Optional, Union

import pyarrow as pa
import pyarrow.parquet as pq
import requests
from loguru import logger

from fused._environment import infer_display_method
from fused._options import options as OPTIONS
from fused._udf.execute_v2 import _transform_output
from fused.api.api import FusedAPI, resolve_udf_server_url
from fused.core._realtime_ops import serialize_realtime_params
from fused.core._serialization import deserialize_tiff
from fused.models import AnyJobStepConfig
from fused.models.udf._eval_result import UdfEvaluationResult
from fused.models.udf.output import Output
from fused.models.udf.udf import AnyBaseUdf
from fused.warnings import FusedWarning

from ..core._impl._realtime_ops_impl import get_recursion_factor

if TYPE_CHECKING:
    import geopandas as gpd
    import pandas as pd


def run_tile(
    x: float,
    y: float,
    z: float,
    data: Optional[
        Union[pd.DataFrame, gpd.GeoDataFrame, pa.Table, str, Path, Any]
    ] = None,
    step_config: Optional[AnyJobStepConfig] = None,
    params: Optional[Dict[str, str]] = None,
    *,
    print_time: bool = False,
    client_id: Optional[str] = None,
    dtype_out_vector: str = "parquet",
    dtype_out_raster: str = "tiff",
) -> UdfEvaluationResult:  # TODO: return png
    time_start = time.perf_counter()
    # We need to get the auth headers from the FusedAPI. Don't enable set_global_api
    # to avoid messing up the user's environment.
    api = FusedAPI(set_global_api=False)

    udf_server_url = resolve_udf_server_url(client_id)

    assert step_config is not None
    # Apply parameters, if we want to step_config that's returned to have this,
    # overwrite step_config.
    step_config_with_params = step_config.set_udf(
        udf=step_config.udf, parameters=serialize_realtime_params(params)
    )

    url = f"{udf_server_url}/api/v1/run/udf/tiles/{z}/{x}/{y}"

    # Headers
    recursion_factor = get_recursion_factor()
    headers = api._generate_headers({"Content-Type": "application/json"})
    headers["Fused-Recursion"] = f"{recursion_factor}"

    # Payload
    post_attr_json = {
        "data_left": data,
        "data_right": None,
        "step_config": step_config_with_params.model_dump_json(),
        "dtype_in": "json",
        "dtype_out_vector": dtype_out_vector,
        "dtype_out_raster": dtype_out_raster,
    }

    # Params
    req_params = {}

    # Make request
    start = time.time()

    r = requests.post(
        url=url,
        params=req_params,
        json=post_attr_json,
        headers=headers,
        timeout=OPTIONS.request_timeout,
    )

    end = time.time()
    if print_time:
        logger.info(f"Time in request: {end - start}")

    time_end = time.perf_counter()
    time_taken_seconds = time_end - time_start

    return _process_response(
        r, step_config=step_config_with_params, time_taken_seconds=time_taken_seconds
    )


def run(
    step_config: Optional[AnyJobStepConfig] = None,
    params: Optional[Dict[str, str]] = None,
    *,
    print_time: bool = False,
    read_options: Optional[Dict] = None,
    client_id: Optional[str] = None,
    dtype_out_vector: str = "parquet",
    dtype_out_raster: str = "tiff",
) -> pd.DataFrame:
    """Run a UDF.

    Args:
        step_config: AnyJobStepConfig.
        params: Additional parameters to pass to the UDF. Must be JSON serializable.

    Keyword Args:
        print_time: If True, print the amount of time taken in the request.
        read_options: If not None, options for reading `df` that will be passed to GeoPandas.
    """
    # TODO: This function is too complicated

    time_start = time.perf_counter()
    # We need to get the auth headers from the FusedAPI. Don't enable set_global_api
    # to avoid messing up the user's environment.
    api = FusedAPI(set_global_api=False)

    udf_server_url = resolve_udf_server_url(client_id)

    assert step_config is not None
    # Apply parameters, if we want to step_config that's returned to have this,
    # overwrite step_config.
    step_config_with_params = step_config.set_udf(
        udf=step_config.udf, parameters=serialize_realtime_params(params)
    )

    # Note: Custom UDF uses the json POST attribute.
    url = f"{udf_server_url}/api/v1/run/udf"

    # This is the body for when step_config_with_params.type == "udf".
    body = {
        "data_left": None,
        "step_config": step_config_with_params.model_dump_json(),
        "dtype_in": "json",
        "dtype_out_vector": dtype_out_vector,
        "dtype_out_raster": dtype_out_raster,
    }

    method = "POST"
    post_attr_json = body

    recursion_factor = get_recursion_factor()
    post_attr_headers = api._generate_headers({"Content-Type": "application/json"})
    post_attr_headers["Fused-Recursion"] = f"{recursion_factor}"

    req_params = {}

    # Make request
    start = time.time()

    r = requests.request(
        method=method,
        url=url,
        params=req_params,
        json=post_attr_json,
        headers=post_attr_headers,
        timeout=OPTIONS.request_timeout,
    )
    end = time.time()
    if print_time:
        logger.info(f"Time in request: {end - start}")

    time_end = time.perf_counter()
    time_taken_seconds = time_end - time_start

    return _process_response(
        r, step_config=step_config_with_params, time_taken_seconds=time_taken_seconds
    )


async def run_tile_async(
    x: float,
    y: float,
    z: float,
    step_config: Optional[AnyJobStepConfig] = None,
    params: Optional[Dict[str, str]] = None,
    *,
    print_time: bool = False,
    client_id: Optional[str] = None,
    dtype_out_vector: str = "parquet",
    dtype_out_raster: str = "tiff",
) -> UdfEvaluationResult:  # TODO: return png
    time_start = time.perf_counter()
    # We need to get the auth headers from the FusedAPI. Don't enable set_global_api
    # to avoid messing up the user's environment.
    api = FusedAPI(set_global_api=False)

    udf_server_url = resolve_udf_server_url(client_id)

    assert step_config is not None
    # Apply parameters, if we want to step_config that's returned to have this,
    # overwrite step_config.
    step_config_with_params = step_config.set_udf(
        udf=step_config.udf, parameters=serialize_realtime_params(params)
    )

    url = f"{udf_server_url}/api/v1/run/udf/tiles/{z}/{x}/{y}"

    # Headers
    recursion_factor = get_recursion_factor()
    headers = api._generate_headers({"Content-Type": "application/json"})
    headers["Fused-Recursion"] = f"{recursion_factor}"

    # Payload
    post_attr_json = {
        "data_left": None,
        "data_right": None,
        "step_config": step_config_with_params.model_dump_json(),
        "dtype_in": "json",
        "dtype_out_vector": dtype_out_vector,
        "dtype_out_raster": dtype_out_raster,
    }

    # Params
    req_params = {}

    # Make request
    start = time.time()

    if OPTIONS.pyodide_async_requests:
        import pyodide.http
        import yarl

        url_with_params = yarl.URL(url, encoded=True).with_query(req_params)
        r = await pyodide.http.pyfetch(
            str(url_with_params),
            method="POST",
            headers=headers,
            body=json.dumps(post_attr_json),
            # TODO: timeout
        )
    else:
        import aiohttp

        async with aiohttp.ClientSession() as session:
            r = await session.post(
                url=url,
                params=req_params,
                json=post_attr_json,
                headers=headers,
                # TODO: timeout
            )

    end = time.time()
    if print_time:
        logger.info(f"Time in request: {end - start}")

    time_end = time.perf_counter()
    time_taken_seconds = time_end - time_start

    return await _process_response_async(
        r, step_config=step_config_with_params, time_taken_seconds=time_taken_seconds
    )


async def run_async(
    step_config: Optional[AnyJobStepConfig] = None,
    params: Optional[Dict[str, str]] = None,
    *,
    print_time: bool = False,
    client_id: Optional[str] = None,
    dtype_out_vector: str = "parquet",
    dtype_out_raster: str = "tiff",
) -> pd.DataFrame:
    """Run a UDF over a DataFrame.

    Args:
        step_config: AnyJobStepConfig.
        params: Additional parameters to pass to the UDF. Must be JSON serializable.

    Keyword Args:
        print_time: If True, print the amount of time taken in the request.
    """
    # TODO: This function is too complicated

    time_start = time.perf_counter()
    # We need to get the auth headers from the FusedAPI. Don't enable set_global_api
    # to avoid messing up the user's environment.
    api = FusedAPI(set_global_api=False)

    udf_server_url = resolve_udf_server_url(client_id)

    assert step_config is not None
    # Apply parameters, if we want to step_config that's returned to have this,
    # overwrite step_config.
    step_config_with_params = step_config.set_udf(
        udf=step_config.udf, parameters=serialize_realtime_params(params)
    )

    # Note: Custom UDF uses the json POST attribute.
    url = f"{udf_server_url}/api/v1/run/udf"

    # This is the body for when step_config_with_params.type == "udf".
    body = {
        "data_left": None,
        "step_config": step_config_with_params.model_dump_json(),
        "dtype_in": "json",
        "dtype_out_vector": dtype_out_vector,
        "dtype_out_raster": dtype_out_raster,
    }

    post_attr_json = body

    recursion_factor = get_recursion_factor()
    post_attr_headers = api._generate_headers({"Content-Type": "application/json"})
    post_attr_headers["Fused-Recursion"] = f"{recursion_factor}"

    req_params = {}

    # Make request
    start = time.time()

    if OPTIONS.pyodide_async_requests:
        import pyodide.http
        import yarl

        url_with_params = yarl.URL(url, encoded=True).with_query(req_params)
        r = await pyodide.http.pyfetch(
            str(url_with_params),
            method="POST",
            headers=post_attr_headers,
            body=json.dumps(post_attr_json),
            # TODO: timeout
        )
    else:
        import aiohttp

        async with aiohttp.ClientSession() as session:
            r = await session.post(
                url=url,
                params=req_params,
                json=post_attr_json,
                headers=post_attr_headers,
                # TODO: timeout
            )

    end = time.time()
    if print_time:
        logger.info(f"Time in request: {end - start}")

    time_end = time.perf_counter()
    time_taken_seconds = time_end - time_start

    return await _process_response_async(
        r, step_config=step_config_with_params, time_taken_seconds=time_taken_seconds
    )


def _process_response(
    r: requests.Response,
    step_config: AnyJobStepConfig,
    time_taken_seconds: float,
) -> UdfEvaluationResult:
    result_content: Optional[bytes] = None
    output_df: Optional[pd.DataFrame] = None
    stdout: Optional[str] = None
    stderr: Optional[str] = None
    error_message: Optional[str] = None
    error_lineno: Optional[int] = None

    try:
        result_content = r.content
        # x-fused-metadata holds LogHandler as JSON, which contains stdout/stderr.
        _fused_metadata = r.headers.get("x-fused-metadata")
        fused_metadata = json.loads(_fused_metadata) if _fused_metadata else {}

        # Extract stdout/stderr.
        stdout = fused_metadata.get("stdout")
        stderr = fused_metadata.get("stderr")

        # Extract exception details
        exception_class = fused_metadata.get("exception_class")
        has_exception = fused_metadata.get("has_exception", False)

        # Extract udf.
        udf: Optional[AnyBaseUdf] = None
        if step_config is not None:
            udf = step_config.udf

        # Extract error line, if exists.
        error_lineno = fused_metadata.get("lineno")

        if r.status_code == 200:
            # If the UDF returned None.
            if len(result_content) == 0:
                return UdfEvaluationResult(
                    data=None,
                    udf=udf,
                    time_taken_seconds=time_taken_seconds,
                    stdout=stdout,
                    stderr=stderr,
                    error_message=error_message,
                    error_lineno=error_lineno,
                    has_exception=has_exception,
                    exception_class=exception_class,
                )

            # Else, process response output.
            res_buf = BytesIO(result_content)

            if r.headers["content-type"] == "image/png":
                import xarray as xr
                from PIL import Image

                display_method = infer_display_method(None, None)
                if display_method.show_widget:
                    from IPython.display import Image as IPythonImage
                    from IPython.display import display

                    display(IPythonImage(data=r.content, format="png"))

                image = Image.open(BytesIO(r.content))
                width, height = image.size
                if len(image.getbands()) == 1:
                    image_data = list(image.getdata())
                    image_data = [
                        image_data[i : i + width]
                        for i in range(0, len(image_data), width)
                    ]
                    data_array = xr.DataArray(image_data, dims=["y", "x"])
                else:
                    image_data = []
                    for band in range(len(image.getbands())):
                        band_data = list(image.getdata(band=band))
                        band_data = [
                            band_data[i : i + width]
                            for i in range(0, len(band_data), width)
                        ]
                        image_data.append(band_data)
                    data_array = xr.DataArray(image_data, dims=["band", "y", "x"])

                # Create the dataset with image, latitude, and longitude data
                dataset = xr.Dataset({"image": data_array})

                return UdfEvaluationResult(
                    data=dataset,
                    udf=udf,
                    time_taken_seconds=time_taken_seconds,
                    stdout=stdout,
                    stderr=stderr,
                    error_message=error_message,
                    error_lineno=error_lineno,
                    has_exception=has_exception,
                    exception_class=exception_class,
                )
            elif r.headers["content-type"] == "image/tiff":
                # TODO: Automatically display tiff?
                data = deserialize_tiff(r.content)

                return UdfEvaluationResult(
                    data=data,
                    udf=udf,
                    time_taken_seconds=time_taken_seconds,
                    stdout=stdout,
                    stderr=stderr,
                    error_message=error_message,
                    error_lineno=error_lineno,
                    has_exception=has_exception,
                    exception_class=exception_class,
                )
            else:  # assume parquet
                m = pq.read_metadata(res_buf)
                if b"geo" in m.metadata:
                    try:
                        import geopandas as gpd

                        output_df = gpd.read_parquet(res_buf)
                    except ValueError as e:
                        warnings.warn(
                            FusedWarning(
                                f"Result has geo metadata but could not be loaded in GeoPandas: {e}"
                            )
                        )
                if output_df is None:
                    import pandas as pd

                    output_df = pd.read_parquet(res_buf)

                # if "fused_index" not in output_df.columns:
                #     # TODO: Hack since the backend no longer responds with fused_index
                #     output_df["fused_index"] = list(range(len(output_df)))

                new_output = _transform_output(
                    output=Output(data=output_df, skip_fused_index_validation=True)
                )

                new_output.validate_data_with_schema()

                if hasattr(udf, "table_schema") and udf.table_schema is None:
                    udf.table_schema = new_output.table_schema  # TODO: ?
                return UdfEvaluationResult(
                    data=new_output.data,
                    sidecar=new_output.sidecar_output,
                    udf=udf,
                    table_schema=new_output.table_schema,
                    time_taken_seconds=time_taken_seconds,
                    stdout=stdout,
                    stderr=stderr,
                    error_message=error_message,
                    error_lineno=error_lineno,
                    has_exception=has_exception,
                    exception_class=exception_class,
                )
        else:
            if "errormsg" in fused_metadata and fused_metadata["errormsg"]:
                error_message = f"The UDF returned the following error for chunk {fused_metadata['chunkinfo']} in line {fused_metadata.get('lineno')}:\n{fused_metadata['errormsg']}"
            elif "exception" in fused_metadata and fused_metadata["exception"]:
                error_message = fused_metadata["exception"]
            else:
                # No error message was returned, e.g. due to deserialization error
                try:
                    # Look for a "detail" field in the response payload
                    details_obj = json.loads(r.text)
                    error_message = details_obj["detail"]
                except:  # noqa: E722
                    error_message = r.text

            return UdfEvaluationResult(
                data=None,
                udf=udf,
                time_taken_seconds=time_taken_seconds,
                stdout=stdout,
                stderr=stderr,
                error_message=error_message,
                error_lineno=error_lineno,
                has_exception=has_exception,
                exception_class=exception_class,
            )
    except:  # noqa: E722
        r.raise_for_status()
        raise


async def _process_response_async(
    r,
    step_config: AnyJobStepConfig,
    time_taken_seconds: float,
) -> UdfEvaluationResult:
    result_content: Optional[bytes] = None
    output_df: Optional[pd.DataFrame] = None
    stdout: Optional[str] = None
    stderr: Optional[str] = None
    error_message: Optional[str] = None
    error_lineno: Optional[int] = None

    try:
        if r.status != 200 and r.status != 422:
            raise ValueError(await r.read())

        result_content = (
            await r.read() if not OPTIONS.pyodide_async_requests else await r.bytes()
        )
        # x-fused-metadata holds LogHandler as JSON, which contains stdout/stderr.
        _fused_metadata = r.headers.get("x-fused-metadata")
        fused_metadata = json.loads(_fused_metadata) if _fused_metadata else {}

        # Extract stdout/stderr.
        stdout = fused_metadata.get("stdout")
        stderr = fused_metadata.get("stderr")

        # Extract exception details
        exception_class = fused_metadata.get("exception_class")
        has_exception = fused_metadata.get("has_exception", False)

        # Extract udf.
        udf: Optional[AnyBaseUdf] = None
        if step_config is not None:
            udf = step_config.udf

        # Extract error line, if exists.
        error_lineno = fused_metadata.get("lineno")

        if r.status == 200:
            # If the UDF returned None.
            if len(result_content) == 0:
                return UdfEvaluationResult(
                    data=None,
                    udf=udf,
                    time_taken_seconds=time_taken_seconds,
                    stdout=stdout,
                    stderr=stderr,
                    error_message=error_message,
                    error_lineno=error_lineno,
                    has_exception=has_exception,
                    exception_class=exception_class,
                )

            # Else, process response output.
            res_buf = BytesIO(result_content)

            if r.headers["content-type"] == "image/png":
                import xarray as xr
                from PIL import Image

                display_method = infer_display_method(None, None)
                if display_method.show_widget:
                    from IPython.display import Image as IPythonImage
                    from IPython.display import display

                    display(IPythonImage(data=result_content, format="png"))

                image = Image.open(res_buf)
                width, height = image.size
                if len(image.getbands()) == 1:
                    image_data = list(image.getdata())
                    image_data = [
                        image_data[i : i + width]
                        for i in range(0, len(image_data), width)
                    ]
                    data_array = xr.DataArray(image_data, dims=["y", "x"])
                else:
                    image_data = []
                    for band in range(len(image.getbands())):
                        band_data = list(image.getdata(band=band))
                        band_data = [
                            band_data[i : i + width]
                            for i in range(0, len(band_data), width)
                        ]
                        image_data.append(band_data)
                    data_array = xr.DataArray(image_data, dims=["band", "y", "x"])

                # Create the dataset with image, latitude, and longitude data
                dataset = xr.Dataset({"image": data_array})

                return UdfEvaluationResult(
                    data=dataset,
                    udf=udf,
                    time_taken_seconds=time_taken_seconds,
                    stdout=stdout,
                    stderr=stderr,
                    error_message=error_message,
                    error_lineno=error_lineno,
                    has_exception=has_exception,
                    exception_class=exception_class,
                )
            elif r.headers["content-type"] == "image/tiff":
                # TODO: Automatically display tiff?
                data = deserialize_tiff(r.content)

                return UdfEvaluationResult(
                    data=data,
                    udf=udf,
                    time_taken_seconds=time_taken_seconds,
                    stdout=stdout,
                    stderr=stderr,
                    error_message=error_message,
                    error_lineno=error_lineno,
                    has_exception=has_exception,
                    exception_class=exception_class,
                )
            else:  # assume parquet
                m = pq.read_metadata(res_buf)
                if b"geo" in m.metadata:
                    try:
                        output_df = gpd.read_parquet(res_buf)
                    except ValueError as e:
                        warnings.warn(
                            FusedWarning(
                                f"Result has geo metadata but could not be loaded in GeoPandas: {e}"
                            )
                        )
                if output_df is None:
                    import pandas as pd

                    output_df = pd.read_parquet(res_buf)

                # if "fused_index" not in output_df.columns:
                #     # TODO: Hack since the backend no longer responds with fused_index
                #     output_df["fused_index"] = list(range(len(output_df)))

                new_output = _transform_output(
                    output=Output(data=output_df, skip_fused_index_validation=True)
                )

                new_output.validate_data_with_schema()

                if hasattr(udf, "table_schema") and udf.table_schema is None:
                    udf.table_schema = new_output.table_schema  # TODO: ?
                return UdfEvaluationResult(
                    data=new_output.data,
                    sidecar=new_output.sidecar_output,
                    udf=udf,
                    table_schema=new_output.table_schema,
                    time_taken_seconds=time_taken_seconds,
                    stdout=stdout,
                    stderr=stderr,
                    error_message=error_message,
                    error_lineno=error_lineno,
                    has_exception=has_exception,
                    exception_class=exception_class,
                )
        else:
            if "errormsg" in fused_metadata and fused_metadata["errormsg"]:
                error_message = f"The UDF returned the following error for chunk {fused_metadata['chunkinfo']} in line {fused_metadata.get('lineno')}:\n{fused_metadata['errormsg']}"
            elif "exception" in fused_metadata and fused_metadata["exception"]:
                error_message = fused_metadata["exception"]
            else:
                # No error message was returned, e.g. due to deserialization error
                try:
                    # Look for a "detail" field in the response payload
                    details_obj = json.loads(result_content)
                    error_message = details_obj["detail"]
                except:  # noqa: E722
                    error_message = result_content.decode()

            return UdfEvaluationResult(
                data=None,
                udf=udf,
                time_taken_seconds=time_taken_seconds,
                stdout=stdout,
                stderr=stderr,
                error_message=error_message or "Unknown error occured",
                error_lineno=error_lineno,
                has_exception=has_exception,
                exception_class=exception_class,
            )
    except:  # noqa: E722
        r.raise_for_status()
        raise
