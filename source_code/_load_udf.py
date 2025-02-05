from pathlib import Path
from typing import Any, Union

from fused.models.api.udf_access_token import is_udf_token

from .core import load_udf_from_fused, load_udf_from_github
from .core._impl._reimports import AnyBaseUdf


def load(url_or_udf: Union[str, Path], /, *, cache_key: Any = None) -> AnyBaseUdf:
    """
    Loads a UDF from various sources including GitHub URLs,
    and a Fused platform-specific identifier.

    This function supports loading UDFs from a GitHub repository URL, or a Fused
    platform-specific identifier composed of an email and UDF name. It intelligently
    determines the source type based on the format of the input and retrieves the UDF
    accordingly.

    Args:
        url_or_udf: A string or Path object representing the location of the UDF. This can be
            a GitHub URL starting with "https://github.com", or a Fused platform-specific
            identifier in the format "email/udf_name".
        cache_key: An optional key used for caching the loaded UDF. If provided, the function
            will attempt to load the UDF from cache using this key before attempting to
            load it from the specified source. Defaults to None, indicating no caching.

    Returns:
        AnyBaseUdf: An instance of the loaded UDF.

    Raises:
        ValueError: If the URL or Fused platform-specific identifier format is incorrect or
            cannot be parsed.
        Exception: For errors related to network issues, file access permissions, or other
            unforeseen errors during the loading process.

    Examples:
        Load a UDF from a GitHub URL:
        ```py
        udf = fused.load("https://github.com/fusedio/udfs/tree/main/public/REM_with_HyRiver/")
        ```

        Load a UDF using a Fused platform-specific identifier:
        ```py
        udf = fused.load("username@fused.io/REM_with_HyRiver")
        ```
    """
    if is_udf_token(url_or_udf):
        raise ValueError(
            "It looks like you tried to load a UDF from a share token. "
            "You may want to call `run` instead of `load`"
        )

    if url_or_udf.startswith("https://github.com"):
        return load_udf_from_github(url_or_udf, cache_key=cache_key)
    else:
        parts = url_or_udf.split("/", maxsplit=1)
        if len(parts) == 2:
            email_or_handle, udf_name = parts
            return load_udf_from_fused(email_or_handle, udf_name, cache_key=cache_key)
        elif len(parts) == 1:
            udf_name = parts[0]
            return load_udf_from_fused(udf_name, cache_key=cache_key)
