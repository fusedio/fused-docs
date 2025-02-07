import re
import urllib.parse
from datetime import datetime
from typing import Any, Dict, Optional, Union

from fused._formatter.formatter_udf_access_token import (
    fused_udf_access_token_list_repr,
    fused_udf_access_token_repr,
)
from fused.models.base import FusedBaseModel

from .._inplace import _maybe_inplace


def _make_dtype_query_params(
    *, dtype_out_vector: Optional[str] = None, dtype_out_raster: Optional[str] = None
):
    ret = urllib.parse.urlencode(
        {
            **({"dtype_out_vector": dtype_out_vector} if dtype_out_vector else {}),
            **({"dtype_out_raster": dtype_out_raster} if dtype_out_raster else {}),
        }
    )
    if ret:
        return f"?{ret}"
    return ret


OLD_TOKEN_REGEX = re.compile("^[a-f0-9]{64}$")


def is_udf_token(maybe_token: str):
    if OLD_TOKEN_REGEX.match(maybe_token):
        return True
    return maybe_token.startswith("UDF_") or maybe_token.startswith("fsh_")


class UdfAccessToken(FusedBaseModel):
    token: str
    udf_email: Optional[str] = None
    udf_slug: Optional[str] = None
    udf_id: Optional[str] = None
    enabled: bool
    owning_user_id: str
    client_id: Optional[str]
    cache: Optional[bool] = None
    metadata_json: Optional[Dict[str, Any]]
    last_updated: datetime

    def update(
        self,
        client_id: Optional[str] = None,
        cache: Optional[bool] = None,
        metadata_json: Optional[Dict[str, Any]] = None,
        enabled: Optional[bool] = None,
        inplace: bool = False,
    ) -> "UdfAccessToken":
        ret = _maybe_inplace(self, inplace)
        return ret.model_copy(
            update=self._api.update_udf_access_token(
                token=self.token,
                client_id=client_id,
                cache=cache,
                metadata_json=metadata_json,
                enabled=enabled,
            ).model_dump()
        )

    def refresh(self, inplace: bool = False) -> "UdfAccessToken":
        ret = _maybe_inplace(self, inplace)
        return ret.model_copy(
            update=self._api.get_udf_access_token(self.token).model_dump()
        )

    def delete(self) -> "UdfAccessToken":
        return self._api.delete_udf_access_token(self.token)

    def get_file_url(
        self,
        *,
        dtype_out_vector: Optional[str] = None,
        dtype_out_raster: Optional[str] = None,
    ) -> str:
        query_params = _make_dtype_query_params(
            dtype_out_vector=dtype_out_vector, dtype_out_raster=dtype_out_raster
        )
        return (
            f"{self._api.base_url}/realtime-shared/{self.token}/run/file{query_params}"
        )

    def get_tile_url(
        self,
        *,
        x: Union[int, str, None] = None,
        y: Union[int, str, None] = None,
        z: Union[int, str, None] = None,
        dtype_out_vector: Optional[str] = None,
        dtype_out_raster: Optional[str] = None,
    ) -> str:
        query_params = _make_dtype_query_params(
            dtype_out_vector=dtype_out_vector, dtype_out_raster=dtype_out_raster
        )
        if x is None and y is None and z is None:
            x = "{x}"
            y = "{y}"
            z = "{z}"
        elif x is None or y is None or z is None:
            raise ValueError("All of x, y, and z must be specified")
        return f"{self._api.base_url}/realtime-shared/{self.token}/run/tiles/{z}/{x}/{y}{query_params}"

    def _repr_html_(self) -> str:
        return fused_udf_access_token_repr(self)


class UdfAccessTokenList(list):
    def _repr_html_(self) -> str:
        return fused_udf_access_token_list_repr(self)
