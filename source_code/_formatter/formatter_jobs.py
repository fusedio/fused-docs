"""Vendored from xarray
https://github.com/pydata/xarray/blob/f4e0523be0ce8babaa8eff38365e5308b1fdb76b/xarray/core/formatting_html.py
"""

from __future__ import annotations

import uuid
from functools import partial
from html import escape
from typing import TYPE_CHECKING, Any, Callable, List, Optional

from fused._formatter.common import copyable_text, icon, load_static_files
from fused._options import options as OPTIONS

if TYPE_CHECKING:
    from fused.models.internal import JobResponse, Jobs, RunResponse


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


def _obj_repr(obj, header_components, sections, sections_class="xr-sections"):
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
        f"<ul class='{sections_class}'>{sections}</ul>"
        "</div>"
        "</div>"
    )


def render_command_toolkit(job_id: str):
    """Render a command toolkit for a job"""
    text = """
    <h4 style="margin-left: 20px;">Command Toolkit</h4>
    <ul style="margin-top: 0; margin-bottom: 0px;">
    """
    for command_description, command_code in [
        # (
        #     "Get job config",
        #     f'fused.experimental.job("{job_id}", content_type="fused_job_id")',
        # ),
        # ("Get status", f'fused.api.job_get_status("{job_id}")'),
        ("Tail logs", f'fused.api.job_tail_logs("{job_id}")'),
        ("Print logs", f'fused.api.job_print_logs("{job_id}")'),
        ("Get execution time", f'fused.api.job_get_exec_time("{job_id}")'),
        ("Cancel", f'fused.api.job_cancel("{job_id}")'),
    ]:
        text += f"<li>{copyable_text(command_code, show_text=False)} {command_description} <code>{command_code}</code></li>"
    text += "</ul>"
    return text


def summarize_job(
    job: JobResponse,
    *,
    is_index: bool = False,
    dtype=None,
):
    cssclass_idx = " class='xr-has-index'" if is_index else ""
    dims_str = f"{job.job_status}" if job.job_status else "?"
    name = escape(str(job.id))
    dtype = ""  # f"rows:{table.num_rows}"

    # "unique" ids required to expand/collapse subsections
    attrs_id = "attrs-" + str(uuid.uuid4())
    # data_id = "data-" + str(uuid.uuid4())
    # chunk_repr_disabled = "disabled" if table.sample is None else ""

    # Convert DataFrame to HTML table
    # TODO: escape html characters # escape(inline_variable_array_repr(variable, 35))
    preview = f"{job.creation_date}"

    attrs_ul = f"""
    <h4 style="margin-left: 20px;">Details</h4>
    <ul style="margin-top: 0; margin-bottom: 0px;">
    <li>ID: {copyable_text(job.id)}</li>
    <li>Instance: {copyable_text(job.instance_id) if job.instance_id else "<code>None</code>"}</li>
    <li>Instance type: {copyable_text(job.instance_type) if job.instance_type else "<code>None</code>"}</li>
    <li>Job status: <code>{job.job_status}</code> {f"(last updated {job.job_status_date})" if job.job_status_date else ""}</li>
    <li><a href="{OPTIONS.base_web_url}/job_status/{job.id}">Logs</a></li>
    </ul>

    {render_command_toolkit(job.id)}
    """

    attrs_icon = icon("icon-file-text2")

    return (
        f"<div class='xr-var-name'><span{cssclass_idx}>{name}</span></div>"
        f"<div class='xr-var-dims'>{dims_str}</div>"
        f"<div class='xr-var-dtype'>{dtype}</div>"
        f"<div class='xr-var-preview xr-preview'>{preview}</div>"
        f"<input id='{attrs_id}' class='xr-var-attrs-in' "
        f"type='checkbox'>"
        f"<label for='{attrs_id}' title='Show/Hide attributes'>"
        f"{attrs_icon}</label>"
        f"<label></label>"
        f"<div class='xr-var-attrs'>{attrs_ul}</div>"
    )


def summarize_jobs(jobs: List[JobResponse]):
    li_items = []
    for job in jobs:
        li_content = summarize_job(job, is_index=False)
        li_items.append(f"<li class='xr-var-item'>{li_content}</li>")

    vars_li = "".join(li_items)

    return f"<ul class='xr-var-list'>{vars_li}</ul>"


job_section = partial(
    _mapping_section,
    name="Jobs",
    details_func=summarize_jobs,
    max_items_collapse=25,
)


def fused_jobs_repr(jobs: Jobs) -> str:
    obj_type = f"fused.{jobs.__class__.__name__}"
    header_components = [
        f"<div class='xr-obj-type'>{escape(obj_type)}</div>",
        # get_object_settings(join, exclude=["input_left", "input_right", "udf", "type"]),
    ]

    sections: List[str] = [
        job_section(jobs.jobs),
    ]

    return _obj_repr(jobs, header_components, sections)


def fused_runresponse_repr(runresponse: RunResponse) -> str:
    terminal = " - final status" if runresponse.terminal_status else ""
    icons_svg, css_style = load_static_files()
    return f"""
    <div>
    {icons_svg}<style>{css_style}</style>
    <h4 style="margin-left: 20px;">Job Run</h4>
    <ul style="margin-top: 0; margin-bottom: 0px;">
    <li>Job ID: {copyable_text(runresponse.job_id)}</li>
    <li>Job name: {copyable_text(runresponse.job_name)}</li>
    <li>Instance ID: {copyable_text(runresponse.instance_id)} [{copyable_text(runresponse.instance_type)}] ({runresponse.status}{terminal})</li>
    <li><a href="{OPTIONS.base_web_url}/job_status/{runresponse.job_id}">Logs</a></li>
    </ul>

    {render_command_toolkit(runresponse.job_id)}
    </div>
    """
