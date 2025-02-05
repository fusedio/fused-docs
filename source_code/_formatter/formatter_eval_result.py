"""Vendored from xarray
https://github.com/pydata/xarray/blob/f4e0523be0ce8babaa8eff38365e5308b1fdb76b/xarray/core/formatting_html.py
"""

from __future__ import annotations

import uuid
from functools import partial
from html import escape
from typing import TYPE_CHECKING, Any, Callable, Dict, List, Optional

from fused._formatter.common import copyable_text, icon, load_static_files
from fused._formatter.noraise import noraise
from fused._formatter.udf import udf_section

if TYPE_CHECKING:
    from fused.models.udf._eval_result import UdfEvaluationResult
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


def _render_decorator(udf: AnyBaseUdf) -> Optional[str]:
    if not hasattr(udf, "table_schema"):
        # Cannot render a decorator here
        return None

    args: List[str] = []
    if (
        hasattr(udf, "table_schema")
        and udf.table_schema is not None
        and not udf.table_schema.is_empty
    ):
        args.append(f"schema={repr(udf.table_schema.to_string())}")
    # Entrypoint isn't set here, because the decorator should be applied to a
    # specific function, and that function will be the entrypoint.
    # Name isn't set here because we are not indexing a registry by the UDF
    # name anymore.

    if udf.original_headers:
        args.append(f"headers={udf.original_headers}")

    return f"@fused.udf({', '.join(args)})"


@noraise(incompat_version_message="Log formatting failed", default="")
def summarize_log(
    log_name: str,
    log: Optional[str],
    *,
    is_index: bool = False,
    dtype=None,
):
    cssclass_idx = " class='xr-has-index'" if is_index else ""
    log_lines = log.splitlines() if log is not None else []
    dims_str = f"lines:{len(log_lines)}"
    name = escape(log_name)
    preview = ""
    dtype = ""

    # "unique" ids required to expand/collapse subsections
    attrs_id = "attrs-" + str(uuid.uuid4())
    data_id = "data-" + str(uuid.uuid4())
    chunk_repr_disabled = "disabled" if not log else ""
    chunk_repr_checked = (
        "checked" if log_name == "stderr" and not chunk_repr_disabled else ""
    )

    # TODO: Fix for no schema, fix for parameters expected by the UDF, fix for copy decorator, fix for entrypoint
    attrs_ul = ""
    rendered_code = "\n".join(
        [f'<span class="fused-udf-body">{escape(line)}</span>' for line in log_lines]
    )
    udf_counter_style_name = f"fused-udf-code-number-style-{len(str(len(log_lines)))}"
    udf_counter_style = f"""
    <style>
    @counter-style {udf_counter_style_name} {{
        system: numeric;
        symbols: "0" "1" "2" "3" "4" "5" "6" "7" "8" "9";
        pad: {len(str(len(log_lines)))} " ";
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
        f"type='checkbox' disabled>"
        f"<label for='{attrs_id}' title='Show/Hide attributes'>"
        f"{attrs_icon}</label>"
        f"<input id='{data_id}' class='xr-var-data-in' type='checkbox' {chunk_repr_disabled} {chunk_repr_checked}>"
        f"<label for='{data_id}' title='Show/Hide data repr'>"
        f"{code_icon}</label>"
        f"<div class='xr-var-attrs'>{attrs_ul}</div>"
        f"<div class='xr-var-data'>{udf_counter_style}{data_repr}</div>"
    )


def summarize_logs(logs: Dict[str, Optional[str]]):
    li_items = []
    for log_name, log in logs.items():
        li_content = summarize_log(log_name, log, is_index=False)
        li_items.append(f"<li class='xr-var-item'>{li_content}</li>")

    vars_li = "".join(li_items)

    return f"<ul class='xr-var-list'>{vars_li}</ul>"


log_section = partial(
    _mapping_section,
    name="Logs",
    details_func=summarize_logs,
    max_items_collapse=25,
)


@noraise(incompat_version_message="Error formatting failed", default="")
def _summarize_error(result: UdfEvaluationResult):
    cssclass_idx = ""
    dims_str = ""
    name = "Error"
    preview = ""
    dtype = ""

    # "unique" ids required to expand/collapse subsections
    attrs_id = "attrs-" + str(uuid.uuid4())
    data_id = "data-" + str(uuid.uuid4())

    # TODO: Fix for no schema, fix for parameters expected by the UDF, fix for copy decorator, fix for entrypoint
    attrs_ul = f"""
    <pre>{escape(result.error_message)}</pre>
    """
    has_error = result.error_lineno is not None
    if has_error:
        chunk_repr_disabled = ""
        code_lines = result.udf.code.splitlines()
        MAGIC_LINENO_OFFSET = 1
        ERROR_CONTEXT_LINE_COUNT = 10
        if ERROR_CONTEXT_LINE_COUNT is not None:
            min_lineno = (
                result.error_lineno - MAGIC_LINENO_OFFSET - ERROR_CONTEXT_LINE_COUNT
            )
            max_lineno = (
                result.error_lineno - MAGIC_LINENO_OFFSET + ERROR_CONTEXT_LINE_COUNT
            )
            start_lineno = max(0, min_lineno + MAGIC_LINENO_OFFSET)
        else:
            min_lineno = 0
            max_lineno = len(code_lines)
            start_lineno = 0
        rendered_code = "\n".join(
            [
                f'<span class="fused-udf-body {"fused-udf-error-line" if lineno == result.error_lineno - MAGIC_LINENO_OFFSET else ""}">{escape(line)}</span>'
                for lineno, line in enumerate(code_lines)
                if min_lineno < lineno < max_lineno
            ]
        )

        udf_counter_style_name = (
            f"fused-udf-code-number-style-{len(str(len(code_lines)))}"
        )
        udf_counter_style = f"""
        <style>
        @counter-style {udf_counter_style_name} {{
            system: numeric;
            symbols: "0" "1" "2" "3" "4" "5" "6" "7" "8" "9";
            pad: {len(str(len(code_lines)))} " ";
        }}
        </style>
        """

        data_repr = f"""<div class="fused-udf-body-wrapper" style="--fused-udf-gutter-counter-style: {udf_counter_style_name};"><pre class="fused-udf-body" style="counter-reset: udf-code-number {start_lineno};"><code>{rendered_code}</code></pre></div>"""
    else:
        chunk_repr_disabled = "disabled"
        data_repr = ""
        udf_counter_style = ""

    attrs_icon = icon("icon-file-text2")
    code_icon = icon("icon-code")

    return (
        f"<div class='xr-var-name'><span{cssclass_idx}>{name}</span></div>"
        f"<div class='xr-var-dims'>{dims_str}</div>"
        f"<div class='xr-var-dtype'>{dtype}</div>"
        f"<div class='xr-var-preview xr-preview'>{preview}</div>"
        f"<input id='{attrs_id}' class='xr-var-attrs-in' "
        f"type='checkbox' checked>"
        f"<label for='{attrs_id}' title='Show/Hide attributes'>"
        f"{attrs_icon}</label>"
        f"<input id='{data_id}' class='xr-var-data-in' type='checkbox' {chunk_repr_disabled} checked>"
        f"<label for='{data_id}' title='Show/Hide data repr'>"
        f"{code_icon}</label>"
        f"<div class='xr-var-attrs'>{attrs_ul}</div>"
        f"<div class='xr-var-data'>{udf_counter_style}{data_repr}</div>"
    )


def summarize_error(results: List[UdfEvaluationResult]):
    assert len(results) == 1
    return f"<ul class='xr-var-list'><li class='xr-var-item'>{_summarize_error(results[0])}</li></ul>"


error_section = partial(
    _mapping_section,
    name="Error",
    details_func=summarize_error,
    max_items_collapse=25,
)


def fused_eval_result_repr(result: UdfEvaluationResult) -> str:
    data_repr = ""
    # TODO: Can't use dict for the schema because the types don't render in that case
    if not result.error_message:
        if result.data is not None and hasattr(result.data, "_repr_html_"):
            data_repr = result.data._repr_html_()
        else:
            data_repr = str(result.data)

    obj_type = f"Local result: {result.udf.name}" if result.udf else "Realtime result"
    header_components = [f"<div class='xr-obj-type'>{escape(obj_type)}</div>"]

    udfs = {result.udf.name: result.udf} if result.udf else {}

    sections: List[str] = [
        data_repr,
        udf_section(udfs),
    ]
    if result.stdout or result.stderr:
        sections.append(log_section({"stdout": result.stdout, "stderr": result.stderr}))
    if result.error_message or result.error_lineno:
        sections.append(error_section([result]))
    decorator_str = _render_decorator(result.udf) if result.udf else None
    sidecar_section = (
        f"<div>Sidecar: <b>{len(result.sidecar)}</b> bytes</div>"
        if result.sidecar is not None
        else ""
    )
    schema_section = (
        f"<div>Decorator: <code>{copyable_text(decorator_str or repr(result.table_schema.model_dump_json()))}</code></div>"
        if not result.error_message and decorator_str
        else ""
    )
    time_taken_section = (
        f"<div>Time taken: <b>{result.time_taken_seconds:.4f}</b> seconds</div>"
    )
    return "".join(
        [
            _obj_repr(udfs, header_components, sections),
            sidecar_section,
            schema_section,
            time_taken_section,
        ]
    )
