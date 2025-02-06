"""Vendored from xarray
https://github.com/pydata/xarray/blob/f4e0523be0ce8babaa8eff38365e5308b1fdb76b/xarray/core/formatting_html.py
"""

from __future__ import annotations

from html import escape
from typing import TYPE_CHECKING, List

from pydantic import BaseModel

from fused._formatter.common import copyable_text, load_static_files

if TYPE_CHECKING:
    from fused._options import Options


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


def _copyable_toml(options: Options) -> str:
    return f'<div style="grid-column: 1 / span 4;">Copy as TOML {copyable_text(text=options._to_toml(), show_text=False)}</div>'


def _options_repr(obj: BaseModel) -> str:
    ret: List[str] = []
    for key in obj.model_dump().keys():
        value = getattr(obj, key)
        if isinstance(value, BaseModel):
            ret.append(f"{key}: {_options_repr(value)}")
        else:
            ret.append(f"{key}: <code>{escape(repr(value))}</code>")
    return f'<div style="grid-column: 1 / span 4;"><ul>{"".join([f"<li>{r}</li>" for r in ret])}</ul></div>'


def fused_options_repr(options: Options) -> str:
    header_components = ["<div class='xr-obj-type'>fused.options</div>"]

    sections: List[str] = []
    if hasattr(options, "_to_toml"):
        sections.append(_copyable_toml(options))
    sections.append(_options_repr(options))

    return _obj_repr(options, header_components, sections)
