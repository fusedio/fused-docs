from __future__ import annotations

from typing import Any, Optional

from ._impl._context_impl import context_get_user_email
from ._impl._reimports import AnyBaseUdf
from ._impl._udf_ops_impl import get_github_udf_from_server, get_step_config_from_server


def load_udf_from_fused(
    email_or_handle_or_id: str, id: Optional[str] = None, *, cache_key: Any = None
) -> AnyBaseUdf:
    """
    Download the code of a UDF, to be run inline.

    Args:
        email_or_handle_or_id: Email or handle of the UDF's owner, or name of the UDF to import.
        id: Name of the UDF to import. If only the first argument is provided, the current user's email will be used.

    Keyword args:
        cache_key: Additional cache key for busting the UDF cache
    """
    if id is None:
        id = email_or_handle_or_id
        try:
            email_or_handle = context_get_user_email()
        except Exception as e:
            raise ValueError(
                "could not detect user ID from context, please specify the UDF as 'user@example.com' (or 'user'), 'udf_name'."
            ) from e
    else:
        email_or_handle = email_or_handle_or_id
    step_config = get_step_config_from_server(
        email_or_handle=email_or_handle,
        slug=id,
        cache_key=cache_key,
    )

    return step_config.udf


def load_udf_from_github(url: str, *, cache_key: Any = None) -> AnyBaseUdf:
    """
    Download the code of a UDF, to be run inline.

    Args:
        email_or_id: Email of the UDF's owner, or name of the UDF to import.
        id: Name of the UDF to import. If only the first argument is provided, the current user's email will be used.

    Keyword args:
        cache_key: Additional cache key for busting the UDF cache
    """
    step_config = get_github_udf_from_server(url=url, cache_key=cache_key)

    return step_config.udf
