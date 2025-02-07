from __future__ import annotations

from typing import TYPE_CHECKING, Optional, Type, Union

if TYPE_CHECKING:
    from fused.api import FusedAPI, FusedDockerAPI, FusedDockerHTTPAPI


API: Optional[Union[FusedAPI, FusedDockerAPI, FusedDockerHTTPAPI]] = None

# We expect this to be set after import
API_CLASS: Optional[Type[FusedAPI]] = None


def get_api(**api_kwargs) -> Union[FusedAPI, FusedDockerAPI, FusedDockerHTTPAPI]:
    global API
    if API is not None:
        return API

    if API_CLASS is not None:
        API = API_CLASS(**api_kwargs)
        return API

    raise ValueError("Internal error: Global API_CLASS was not set.")


def set_api(api: Union[FusedAPI, FusedDockerAPI, FusedDockerHTTPAPI]) -> None:
    global API
    API = api


def set_api_class(api_class: Type[FusedAPI]) -> None:
    global API_CLASS
    API_CLASS = api_class


def reset_api():
    global API
    API = None
