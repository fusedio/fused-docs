from __future__ import annotations

import uuid
from functools import partial
from html import escape
from typing import TYPE_CHECKING, Any, Callable, Dict, List, Optional, Sequence

from fused._formatter.common import copyable_text, icon, load_static_files
from fused._formatter.noraise import noraise

if TYPE_CHECKING:
    from fused.models.udf.header import Header
    from fused.models.udf.udf import AnyBaseUdf


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


def collapsible_section(
    name,
    inline_details: str = "",
    details: str = "",
    n_items: Optional[int] = None,
    enabled: bool = True,
    collapsed: bool = False,
):
    # "unique" id to expand/collapse the section
    data_id = "section-" + str(uuid.uuid4())

    has_items = n_items is not None and n_items
    n_items_span = "" if n_items is None else f" <span>({n_items})</span>"
    enabled_str = "" if enabled and has_items else "disabled"
    collapsed_str = "" if collapsed or not has_items else "checked"
    tip = " title='Expand/collapse section'" if enabled else ""

    return (
        f"<input id='{data_id}' class='xr-section-summary-in' "
        f"type='checkbox' {enabled_str} {collapsed_str}>"
        f"<label for='{data_id}' class='xr-section-summary' {tip}>"
        f"{name}:{n_items_span}</label>"
        f"<div class='xr-section-inline-details'>{inline_details}</div>"
        f"<div class='xr-section-details'>{details}</div>"
    )


def _mapping_section(
    mapping,
    name: str,
    details_func: Callable[[Any], str],
    max_items_collapse,
    enabled: bool = True,
):
    n_items = len(mapping)
    expanded = n_items < max_items_collapse
    collapsed = not expanded

    return collapsible_section(
        name,
        details=details_func(mapping),
        n_items=n_items,
        enabled=enabled,
        collapsed=collapsed,
    )


@noraise(incompat_version_message="Header formatting failed", default="")
def summarize_header(
    header: Header,
    *,
    is_index: bool = False,
    dtype=None,
):
    cssclass_idx = " class='xr-has-index'" if is_index else ""
    name = header.module_name
    source_file = header.source_file or name + ".py"
    code_lines = header.source_code.splitlines()
    dims_str = f"lines:{len(code_lines)}"

    # "unique" ids required to expand/collapse subsections
    attrs_id = "attrs-" + str(uuid.uuid4())
    data_id = "data-" + str(uuid.uuid4())
    chunk_repr_disabled = "disabled" if not code_lines else ""

    html_rendered_code = "\n".join(
        [f'<span class="fused-udf-body">{line}</span>' for line in code_lines]
    )
    data_repr = f"""<div class="fused-udf-body-wrapper"><pre class="fused-udf-body"><code>{html_rendered_code}</code></pre></div>"""
    attrs_ul = f"""
    <h4 style="margin-left: 20px;">Attributes</h4>
    <ul style="margin-top: 0; margin-bottom: 0px;">
    <li>Source file: <code>{header.source_file}</code></li>
    <li>Module name: <code>{copyable_text(header.module_name)}</code></li>
    </ul>
    <h4 style="margin-left: 20px;">Toolkit</h4>
    <ul style="margin-top: 0; margin-bottom: 0px;">
    <li>{copyable_text(header._generate_cell_code(), show_text=False)} Copy as notebook cell</li>
    <li>{copyable_text(header.source_code, show_text=False)} Copy source</li>
    </ul>
     """

    attrs_icon = icon("icon-file-text2")
    code_icon = icon("icon-code")
    return (
        f"<div class='xr-var-name'><span{cssclass_idx}>{name}</span></div>"
        f"<div class='xr-var-dims'>{dims_str}</div>"
        f"<div class='xr-var-dtype'>{source_file}</div>"
        f"<div class='xr-var-preview xr-preview'></div>"
        f"<input id='{attrs_id}' class='xr-var-attrs-in' "
        f"type='checkbox'>"
        f"<label for='{attrs_id}' title='Show/Hide attributes'>"
        f"{attrs_icon}</label>"
        f"<input id='{data_id}' class='xr-var-data-in' type='checkbox' {chunk_repr_disabled}>"
        f"<label for='{data_id}' title='Show/Hide data repr'>"
        f"{code_icon}</label>"
        f"<div class='xr-var-attrs'>{attrs_ul}</div>"
        f"<div class='xr-var-data'>{data_repr}</div>"
    )


@noraise(incompat_version_message="UDF formatting failed", default="")
def summarize_udf(
    udf_name: str,
    udf: AnyBaseUdf,
    *,
    is_index: bool = False,
    dtype=None,
):
    # TODO: Fix for not having table_schema
    if not hasattr(udf, "table_schema"):
        return ""

    cssclass_idx = " class='xr-has-index'" if is_index else ""
    code_lines = udf.code.splitlines()
    if udf.table_schema is not None:
        dims_str = f"cols:{len(udf.table_schema.fields)}, lines:{len(code_lines)}"
    else:
        dims_str = f"cols:?, lines:{len(code_lines)}"
    name = escape(str(udf_name))
    dtype = ""

    # "unique" ids required to expand/collapse subsections
    attrs_id = "attrs-" + str(uuid.uuid4())
    data_id = "data-" + str(uuid.uuid4())
    chunk_repr_disabled = "disabled" if udf.code is None else ""

    # Convert DataFrame to HTML udf
    # TODO: escape html characters # escape(inline_variable_array_repr(variable, 35))
    if udf.table_schema is not None:
        preview = f"[{', '.join([i.name for i in udf.table_schema.fields])}]"
        table_schema = [
            f"<li><code>{i.name}</code>: {i.type}</li>" for i in udf.table_schema.fields
        ]
    else:
        preview = "?"
        table_schema = []

    if hasattr(udf, "parameters"):
        parameters = [
            f"<li><code>{k}</code>: <code>{v}</code></li>"
            for k, v in udf.parameters.items()
        ]
        if hasattr(udf, "_parameter_list") and udf._parameter_list is not None:
            for param in udf._parameter_list:
                if param not in udf.parameters:
                    parameters.append(f"<li><code>{param}</code></li>")
    else:
        parameters = []

    entrypoint_str = (
        f"<br>Entrypoint: <code>{udf.entrypoint}</code>"
        if hasattr(udf, "entrypoint")
        else ""
    )

    # TODO: Fix for no schema, fix for parameters expected by the UDF, fix for copy decorator, fix for entrypoint
    attrs_ul = f"""
    <h4 style="margin-left: 20px;">Table Schema</h4>
    <ul style="margin-top: 0; margin-bottom: 0px;">
    {''.join(table_schema) if udf.table_schema is not None else "(No schema)"}
    </ul>
    <h4 style="margin-left: 20px;">Parameters</h4>
    <ul style="margin-top: 0; margin-bottom: 0px;">
    {''.join(parameters)}
    </ul>
    <h4 style="margin-left: 20px;">Headers</h4>
    <ul style="margin-top: 0; margin-bottom: 0px;">
    {fused_header_repr(udf.headers) if hasattr(udf, 'headers') else ""}
    </ul>
    <h4 style="margin-left: 20px;">Type</h4>
    <ul style="margin-top: 0; margin-bottom: 0px;">
    {udf.type.name}
    {entrypoint_str}
    </ul>
    <h4 style="margin-left: 20px;">Toolkit</h4>
    <ul style="margin-top: 0; margin-bottom: 0px;">
    <li>{copyable_text(udf._generate_code()[0], show_text=False)} Copy code</li>
     """  # summarize_attrs(var.attrs)
    rendered_code = "\n".join(
        [f'<span class="fused-udf-body">{escape(line)}</span>' for line in code_lines]
    )
    udf_counter_style_name = f"fused-udf-code-number-style-{len(str(len(code_lines)))}"
    udf_counter_style = f"""
    <style>
    @counter-style {udf_counter_style_name} {{
        system: numeric;
        symbols: "0" "1" "2" "3" "4" "5" "6" "7" "8" "9";
        pad: {len(str(len(code_lines)))} " ";
    }}
    </style>
    """
    data_repr = f"""<div class="fused-udf-body-wrapper" style="--fused-udf-gutter-counter-style: {udf_counter_style_name};"><pre class="fused-udf-body"><code>{rendered_code}</code></pre></div>"""
    attrs_icon = icon("icon-file-text2")
    code_icon = icon("icon-code")

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
        f"<label for='{data_id}' title='Show/Hide data repr'>"
        f"{code_icon}</label>"
        f"<div class='xr-var-attrs'>{attrs_ul}</div>"
        f"<div class='xr-var-data'>{udf_counter_style}{data_repr}</div>"
    )


def summarize_headers(headers: Sequence[Header]):
    li_items = []
    for header in headers:
        li_content = summarize_header(header, is_index=False)
        li_items.append(f"<li class='xr-var-item'>{li_content}</li>")

    vars_li = "".join(li_items)

    return f"<ul class='xr-var-list'>{vars_li}</ul>"


def summarize_udfs(udfs: Dict[str, AnyBaseUdf]):
    li_items = []
    for udf_name, udf in udfs.items():
        li_content = summarize_udf(udf_name, udf, is_index=False)
        li_items.append(f"<li class='xr-var-item'>{li_content}</li>")

    vars_li = "".join(li_items)

    return f"<ul class='xr-var-list'>{vars_li}</ul>"


udf_section = partial(
    _mapping_section,
    name="UDF",
    details_func=summarize_udfs,
    max_items_collapse=25,
)

headers_section = partial(
    _mapping_section,
    name="Headers",
    details_func=summarize_headers,
    max_items_collapse=25,
)


def format_dims(dims, dims_with_index):
    if not dims:
        return ""

    dim_css_map = {
        dim: " class='xr-has-index'" if dim in dims_with_index else "" for dim in dims
    }

    dims_li = "".join(
        f"<li><span{dim_css_map[dim]}>" f"{escape(str(dim))}</span>: {size}</li>"
        for dim, size in dims.items()
    )

    return f"<ul class='xr-dim-list'>{dims_li}</ul>"


def fused_registry_repr(registry: Dict[str, AnyBaseUdf]) -> str:
    obj_type = "fused.UdfRegistry"
    header_components = [f"<div class='xr-obj-type'>{escape(obj_type)}</div>"]

    sections: List[str] = [
        udf_section(registry),
    ]

    return _obj_repr(registry, header_components, sections)


def fused_udf_repr(udf: AnyBaseUdf) -> str:
    obj_type = f"fused.{udf.__class__.__name__}: {udf.name}"
    header_components = [f"<div class='xr-obj-type'>{escape(obj_type)}</div>"]

    udfs = {udf.name: udf}

    sections: List[str] = [
        udf_section(udfs),
    ]

    return _obj_repr(udfs, header_components, sections)


def fused_header_repr(headers: Sequence[Header]) -> str:
    obj_type = "fused.Header"
    header_components = [f"<div class='xr-obj-type'>{escape(obj_type)}</div>"]

    sections: List[str] = [
        headers_section(headers),
    ]

    return _obj_repr(headers, header_components, sections)
