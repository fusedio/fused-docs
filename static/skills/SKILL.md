---
name: fused
description: Use when a task involves Fused: calling or chaining UDFs over HTTP (udf.ai/fc_...), H3 hex datasets, fused-map widgets, share-URL widgets or Sentinel-2 imagery. Has the rules for every Fused task and routes to the page each task needs.
---

# Fused

Fused runs Python functions (UDFs) in the cloud. A canvas groups UDFs under one canvas token (`fc_...`), and every UDF on it is an HTTP endpoint with no deploy step.

## Rules for every task

- Take UDF, parameter and column names from the canvas spec (`.api.json`) or a `.json` sample.
- After an error, read it and change the parameter, format or input before you retry.
- Scope each call to the question: a bounding box, an id or a date range.
- Run your own work (partition, index, Sentinel-2 requests) from code on the user's own Fused account. A canvas share link runs as the canvas owner.
- Snippets say what to expect. Numbers come from live data, so they can differ a little: check the shape and columns first.

## Call a UDF

```
GET https://udf.ai/fc_<TOKEN>.api.json
GET https://udf.ai/fc_<TOKEN>/<udf_name>.json?param1=value1&param2=value2
```

- `.api.json` is an OpenAPI 3.0 spec: each path under `paths` is a UDF, with its `description` and `parameters`. Read it before the first call.
- Request `.json` unless the user asks for a visual or you are building a map tile URL.
- Private canvas: add the header `Authorization: Bearer <ACCESS_TOKEN>`.
- Results are cached for 90 days. Add `cache_max_age=0s` for a fresh run.
- Give `.html` and `.png` URLs to the user as links.
- To chain, parse step 1's JSON and put the value you need in step 2's URL.

## Pick a page

- **UDF calls in depth**: formats, response shapes, error codes, parameter types, chaining, tile URLs → https://docs.fused.io/skills/udf-http.md
- **H3 hex datasets**: partition, index and query data with `fused.h3`, over HTTP or on a map → https://docs.fused.io/skills/H3.md
- **Maps in a canvas**: add or edit a `fused-map` widget → https://docs.fused.io/skills/FUSED_MAP.md
- **Charts, tables and inputs from a share URL**: a widget over UDF output, no canvas edit → https://docs.fused.io/skills/WIDGET.md
- **Sentinel-2 imagery**: scenes, composites, indices, time series → https://docs.fused.io/skills/SENTINEL2.md
- **Canvas files** (`canvas.toml`, UDF files, widget JSON): the Workbench skills → https://github.com/fusedio/skills
