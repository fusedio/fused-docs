"""Vendored from xarray
https://github.com/pydata/xarray/blob/f4e0523be0ce8babaa8eff38365e5308b1fdb76b/xarray/core/formatting_html.py
"""

from __future__ import annotations

import json
import uuid
from functools import partial
from html import escape
from typing import TYPE_CHECKING, Any, Callable, Dict, List, Optional, Sequence

from pydantic import BaseModel

from fused._formatter.common import copyable_text, load_static_files
from fused._formatter.udf import udf_section

if TYPE_CHECKING:
    from fused.models.api import (
        JobConfig,
        JobStepConfig,
        PartitionJobStepConfig,
        UdfJobStepConfig,
    )
    from fused.models.udf import AnyBaseUdf


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
    **kwargs,
):
    n_items = len(mapping)
    expanded = n_items < max_items_collapse
    collapsed = not expanded

    return collapsible_section(
        name,
        details=details_func(mapping, **kwargs),
        n_items=n_items,
        enabled=enabled,
        collapsed=collapsed,
    )


def _obj_repr(obj, header_components, sections, sections_class="xr-sections"):
    """Return HTML repr of an xarray object.

    If CSS is not injected (untrusted notebook), fallback to the plain text repr.

    """
    header = f"<div class='xr-header'>{''.join(h for h in header_components)}</div>"
    sections = "".join(
        f"<li class='xr-section-item'>{s}</li>" for s in sections if s is not None
    )

    icons_svg, css_style = load_static_files()
    return (
        "<div>"
        f"{icons_svg}<style>{css_style}</style>"
        f"<pre class='xr-text-repr-fallback'>{escape(repr(obj))}</pre>"
        "<div class='xr-wrap' style='display:none'>"
        f"{header}"
        f"<ul class='{sections_class}'>{sections}</ul>"
        "</div>"
        "</div>"
    )


def summarize_ingest_input(
    input: str,
    *,
    is_index: bool = False,
):
    cssclass_idx = " class='xr-has-index'" if is_index else ""
    name = escape(str(input))

    return (
        f'<div class="xr-var-name" style="grid-column: 1 / -2;"><span{cssclass_idx}>{name}</span></div>'
        f"{copyable_text(name, show_text=False)}"
    )


def summarize_ingest_inputs(inputs: List[str]):
    li_items = []
    for input in inputs:
        li_content = summarize_ingest_input(input, is_index=False)
        li_items.append(f"<li class='xr-var-item'>{li_content}</li>")

    vars_li = "".join(li_items)

    return f'<ul class="xr-var-list">{vars_li}</ul>'


ingest_inputs_section = partial(
    _mapping_section,
    name="Inputs",
    details_func=summarize_ingest_inputs,
    max_items_collapse=25,
)


def get_object_settings(obj: BaseModel, exclude: Sequence[str] = ()) -> str:
    def _format_kv(key: str, val: Any) -> str:
        if key in exclude:
            return ""
        return f"<li>{key}: <code>{val}</code></li>"

    return f"<ul>{''.join([_format_kv(key, val) for key, val in obj.model_dump().items()])}</ul>"


def _collect_udfs(
    config: JobStepConfig, *, names: Sequence[str] = ("udf",)
) -> Dict[str, AnyBaseUdf]:
    results = {}
    for udf_name in names:
        if hasattr(config, udf_name):
            udf_attr = getattr(config, udf_name)
            if udf_attr is not None:
                results[udf_attr.name] = udf_attr
    return results


def fused_ingestion_repr(ingest: PartitionJobStepConfig) -> str:
    obj_type = f"fused.{ingest.__class__.__name__}: {ingest.name or ingest.output or ingest.output_metadata}"
    header_components = [
        f"<div class='xr-obj-type'>{escape(obj_type)}</div>",
        get_object_settings(ingest, exclude=["input", "type"]),
    ]

    inputs = ingest.input if isinstance(ingest.input, list) else [ingest.input]

    sections: List[str] = [
        ingest_inputs_section(inputs),
    ]

    return _obj_repr(ingest, header_components, sections)


def fused_udf_step_repr(step: UdfJobStepConfig) -> str:
    name = step.name
    if not name and step.udf is not None:
        name = step.udf.name
    obj_type = f"fused.{step.__class__.__name__}: {name}"
    header_components = [
        f"<div class='xr-obj-type'>{escape(obj_type)}</div>",
        get_object_settings(step, exclude=["input", "udf", "type"]),
    ]

    inputs = [json.dumps(i) for i in step.input] if step.input is not None else []
    udfs = _collect_udfs(step)

    sections: List[str] = [
        ingest_inputs_section(inputs) if step.input is not None else None,
        udf_section(udfs),
    ]

    return _obj_repr(step, header_components, sections)


def _get_job_repr(i: int, step: JobStepConfig) -> str:
    if hasattr(step, "_repr_html_"):
        html = step._repr_html_()
    else:
        html = repr(step)
    return f'<li><h4>Step {i}</h4><div style="padding-left: 2em;">{html}</div></li>'


def fused_job_repr(job: JobConfig) -> str:
    return f"""
    <div class='xr-obj-type'>fused.JobConfig: {job.name}</div>
    <ul>
    {''.join([_get_job_repr(step_idx, step) for step_idx, step in enumerate(job.steps)])}
    </ul>
    """
