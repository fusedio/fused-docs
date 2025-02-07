"""Vendored from xarray
https://github.com/pydata/xarray/blob/f4e0523be0ce8babaa8eff38365e5308b1fdb76b/xarray/core/formatting_html.py
"""

from __future__ import annotations

import uuid
from html import escape
from typing import TYPE_CHECKING, List

from fused._formatter.common import copyable_text, icon, load_static_files

if TYPE_CHECKING:
    from fused.models.api.udf_access_token import UdfAccessToken, UdfAccessTokenList


def _obj_repr(obj, header_components, sections):
    """Return HTML repr of an xarray object.

    If CSS is not injected (untrusted notebook), fallback to the plain text repr.

    """
    header = f"<div class='xr-header'>{''.join(h for h in header_components)}</div>"
    sections = "".join(f"<li class='xr-section-item'>{s}</li>" for s in sections)

    icons_svg, css_style = load_static_files()
    return (
        "<div>"
        f"{icons_svg}<style>{css_style}</style>"
        f"<pre class='xr-text-repr-fallback'>{escape(repr(obj))}</pre>"
        "<div class='xr-wrap' style='display:none'>"
        f"{header}"
        f"<ul class='xr-sections'>{sections}</ul>"
        "</div>"
        "</div>"
    )


def summarize_udf_access_token(
    token: UdfAccessToken,
    *,
    is_index: bool = False,
    dtype=None,
):
    cssclass_idx = " class='xr-has-index'" if is_index else ""
    dims_str = ""
    name = escape(token.token)
    dtype = escape(f"{token.udf_email}/{token.udf_slug}")
    preview = escape(token.client_id)

    # "unique" ids required to expand/collapse subsections
    attrs_id = "attrs-" + str(uuid.uuid4())
    data_id = "data-" + str(uuid.uuid4())

    configuration: List[str] = []
    for key in token.model_dump().keys():
        value = getattr(token, key)
        if key == "last_updated":
            configuration.append(
                f"<li>{key}: <code>{escape(value.isoformat())}</code></li>"
            )
        elif key not in ["token", "udf_email", "udf_slug"]:
            configuration.append(f"<li>{key}: <code>{escape(repr(value))}</code></li>")

    # TODO: Fix for no schema, fix for parameters expected by the UDF, fix for copy decorator, fix for entrypoint
    attrs_ul = f"""
    <h4 style="margin-left: 20px;">Token</h4>
    <ul style="margin-top: 0; margin-bottom: 0px;">
    <li>{copyable_text(token.token, show_text=True)}</li>
    <li>UDF owner email: <code>{escape(token.udf_email) if token.udf_email else 'None'}</code></li>
    <li>UDF name: <code>{escape(token.udf_slug)}</code></li>
    <li>UDF ID: <code>{escape(token.udf_id) if token.udf_id else 'Unknown'}</code></li>
    </ul>
    <h4 style="margin-left: 20px;">Configuration</h4>
    <ul style="margin-top: 0; margin-bottom: 0px;">
    {''.join(configuration)}
    </ul>
    <h4 style="margin-left: 20px;">Toolkit</h4>
    <ul style="margin-top: 0; margin-bottom: 0px;">
    <li>File URL: {copyable_text(token.get_file_url())}</li>
    <li>Tile URL: {copyable_text(token.get_tile_url())}</li>
    </ul>
    """
    attrs_icon = icon("icon-file-text2")
    code_icon = icon("icon-code")

    chunk_repr_disabled = "disabled"
    data_repr = ""

    return (
        f"<div class='xr-var-name'><span{cssclass_idx}>{name}</span></div>"
        f"<div class='xr-var-dims'>{dims_str}</div>"
        f"<div class='xr-var-dtype'>{dtype}</div>"
        f"<div class='xr-var-preview xr-preview'>{preview}</div>"
        f"<input id='{attrs_id}' class='xr-var-attrs-in' "
        f"type='checkbox'>"
        f"<label for='{attrs_id}' title='Show/Hide attributes'>"
        f"{attrs_icon}</label>"
        f"<input id='{data_id}' class='xr-var-data-in' type='checkbox' {chunk_repr_disabled}>"
        f"<label for='{data_id}' title='Show/Hide data repr' {chunk_repr_disabled}>"
        f"{code_icon}</label>"
        f"<div class='xr-var-attrs'>{attrs_ul}</div>"
        f"<div class='xr-var-data'>{data_repr}</div>"
    )


def _udf_access_token_repr_dynamic(obj: UdfAccessToken) -> str:
    ret: List[str] = []

    for key in obj.model_dump().keys():
        value = getattr(obj, key)
        if key == "last_updated":
            ret.append(f"{key}: <code>{escape(value.isoformat())}</code>")
        elif key not in ["token", "udf_email", "udf_slug"]:
            ret.append(f"{key}: <code>{escape(repr(value))}</code>")
    return f'<div style="grid-column: 1 / span 4;"><ul>{"".join([f"<li>{r}</li>" for r in ret])}</ul></div>'


def _udf_access_token_repr_static(obj: UdfAccessToken) -> str:
    ret: List[str] = []

    ret = [
        f"UDF Email: <code>{escape(obj.udf_email)}</code>",
        f"UDF ID: <code>{escape(obj.udf_slug)}</code>",
    ]

    return f'<div style="grid-column: 1 / span 4;"><ul>{"".join([f"<li>{r}</li>" for r in ret])}</ul></div>'


def fused_udf_access_token_repr(token: UdfAccessToken) -> str:
    header_components = [
        f"<div class='xr-obj-type'>UdfAccessToken: {escape(f'{token.udf_email}/{token.udf_slug}')}</div>"
    ]

    sections = [summarize_udf_access_token(token)]
    # sections.append(_udf_access_token_repr_static(token))
    # sections.append(_udf_access_token_repr_dynamic(token))

    return _obj_repr(token, header_components, sections)


def fused_udf_access_token_list_repr(tokens: UdfAccessTokenList) -> str:
    header_components = [
        f"<div class='xr-obj-type'>UdfAccessTokens: {len(tokens)}</div>"
    ]

    sections: List[str] = []
    for token in tokens:
        sections.append(summarize_udf_access_token(token))

    return _obj_repr(tokens, header_components, sections)
