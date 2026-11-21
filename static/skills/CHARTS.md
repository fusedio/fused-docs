---
name: fused-charts
description: Use when charting a UDF's output in a Fused canvas: a JSON-UI chart widget (`line-chart`, `bar-chart`, `scatter-chart`, `donut-chart`, `heatmap-chart`, stacked charts, `metric`) that runs SQL over `{{udf_name}}`, or a UDF that returns its own HTML chart (Chart.js, Plotly, D3), with inputs that set UDF parameters.
---

# Charts on Fused

A chart in a canvas draws a UDF's output, in one of two ways:

- **Chart widget**: a JSON-UI node that runs DuckDB SQL over `{{udf_name}}` in the browser. No chart code. Use it first.
- **UDF that returns HTML**: for anything a widget can't draw (bands, mixed chart types, annotations, custom interaction). The UDF builds the page with Chart.js, Plotly or D3 and returns it as a `str`, which the canvas shows as HTML.

Rules for every Fused task (accounts, errors, expected outputs): https://docs.fused.io/skills/SKILL.md

References: https://docs.fused.io/widget-api/overview (every widget and prop), https://docs.fused.io/examples/creating-charts (both ways, live). Canvas files (`canvas.toml`, UDF and widget files, pushing) and widget JSON rules: https://github.com/fusedio/skills (`canvas-toml`, `json-ui-schemas`, `html-template-nodes`).

## The user's own data: ask first

With no task, or for the user's own data:

1. Ask where the data is and what question the chart should answer, unless they said. With no data at hand, offer the ERA5 example below.
2. Run the data UDF and read its columns and row count. Then pick the chart from the table below and propose it, with the SQL, and wait for their OK.
3. Build it, push the canvas and give the user its URL.

## Set up

```bash
pip install -U fused
fused workbench login          # opens the browser; check with `fused workbench whoami`
```

## Example: ERA5 temperature, Ames, Iowa

Canvas folder:

```
Iowa_Temperature_Charts/
  canvas.toml
  era5_daily.py           # data UDF
  daily_temperature.json  # line-chart widget
```

`era5_daily.py`:

```python
@fused.udf
def udf(
    min_lng: float = -93.9,
    min_lat: float = 41.8,
    max_lng: float = -93.4,
    max_lat: float = 42.2,
    date_min: str = "2024-06-01",
    date_max: str = "2024-07-31",
):
    df = fused.h3.query(
        "s3://us-west-2.opendata.source.coop/fused/era5-hex/era5_daily",
        bbox=(min_lng, min_lat, max_lng, max_lat),
        time_min=date_min, time_max=date_max,
        columns=["hex", "date", "t2m_min", "t2m_max", "t2m_mean"],
    )
    for col in ["t2m_min", "t2m_max", "t2m_mean"]:
        df[col] = (df[col].astype("float64") - 273.15).round(2)  # Kelvin -> Celsius
    df["hex"] = df["hex"].astype("int64")
    return df.sort_values(["hex", "date"]).reset_index(drop=True)
```

`daily_temperature.json`:

```json
{
  "type": "line-chart",
  "props": {
    "title": "Average daily temperature (°C), Ames, Iowa",
    "sql": "SELECT strftime(date, '%Y-%m-%d') AS label, ROUND(AVG(t2m_mean), 1) AS value FROM {{era5_daily}} GROUP BY 1 ORDER BY 1",
    "beginAtZero": false,
    "showArea": false
  }
}
```

`canvas.toml` has one node per file and the edge `["era5_daily", "daily_temperature"]`.

```bash
fused workbench run "" era5_daily.py    # check the data first
fused workbench canvas validate .
fused workbench canvas push .
```

- `era5_daily` returns 21,960 rows (360 H3 cells × 61 days) with columns `hex`, `date`, `t2m_min`, `t2m_max`, `t2m_mean` (°C). `date` holds Python `datetime.date` values. In widget SQL, format it with `strftime(date, '%Y-%m-%d')`, or the axis shows `2024-06-01T00:00:00.000Z`. In Python, convert with `.astype(str)` before `json.dumps`, or it raises `TypeError`.
- The chart draws 61 points, from about 17.6 to 29.5 °C.
- A UDF that calls `fused.run("era5_daily")` by name works only inside the pushed canvas. `fused workbench run "" other.py` fails with `UDF not found`, so test that logic with the data code inlined.

## Pick a chart

Every chart widget needs `sql`. Alias the columns to the names it reads:

| Widget | Use for | SQL columns |
|---|---|---|
| `line-chart` | A value over time | `label` (x), `value` (y), optional `series` (one line each) |
| `bar-chart` | Compare categories | `label`, `value` |
| `stacked-bar-chart` | Categories split into parts | `label`, `series`, `value` |
| `stacked-area-chart` | Parts of a total over time | `label`, `series`, `value` |
| `scatter-chart` | Two numbers against each other | `x`, `y`, optional `series`, `size`, `label` |
| `donut-chart` | Shares of a whole, few slices | `label`, `value` |
| `heatmap-chart` | A value over two categories | `x`, `y`, `value` |
| `metric` | One KPI | the first column of the first row |

- Aggregate in the SQL (`GROUP BY`, `ORDER BY`, `LIMIT`), not in the browser: send a chart tens to hundreds of points, not every row.
- `line-chart` and `bar-chart` start the y-axis at 0. Set `"beginAtZero": false` for values such as temperatures.
- `bar-chart` has no `xAxisField` or `yAxisField` prop. Only the column aliases pick the axes.
- Check every widget file with `fused workbench json-ui validate <file>.json`, and read a widget's props with `fused workbench json-ui schemas <widget>`.

## Inputs

An input widget with `param` sets that canvas parameter. Every UDF with a parameter of that name runs again, and SQL reads it as `$param_name`. Draw an edge from the input to the UDFs it drives.

```json
{"type": "slider", "props": {"label": "Hot day threshold (°C)", "param": "heat_threshold", "min": 25, "max": 35, "step": 0.5, "defaultValue": 30}}
```

Other inputs: `dropdown` (static `options` or SQL), `number-input`, `text-input`, `datetime-input`, `button`.

## Custom chart: a UDF that returns HTML

Use this when the chart needs more than one widget can draw. Do the data work in pandas, put the result in the page as JSON and return the page as a string:

```python
@fused.udf
def udf(heat_threshold: float = 30.0):
    import json

    df = fused.run("era5_daily")
    daily = df.groupby("date").agg(t_min=("t2m_min", "mean"), t_max=("t2m_max", "mean")).round(1).reset_index()
    data = {"labels": daily["date"].astype(str).tolist(), "min": daily["t_min"].tolist(), "max": daily["t_max"].tolist()}
    return f"""<!DOCTYPE html><html><head><meta charset="UTF-8">
<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"></script></head>
<body style="margin:0;height:100vh;background:#121212"><canvas id="c"></canvas><script>
const d = {json.dumps(data)};
new Chart(document.getElementById("c"), {{type: "line", data: {{labels: d.labels, datasets: [
  {{label: "Low", data: d.min, pointRadius: 0}},
  {{label: "High", data: d.max, pointRadius: 0, fill: "-1"}}]}},
  options: {{maintainAspectRatio: false}}}});
</script></body></html>"""
```

- In an f-string, double every `{` and `}` of the CSS and JavaScript.
- Pin the library version in the CDN URL (`chart.js@4.4.0`). The page has no local files: inline everything else.
- Keep the data small: aggregate first, as above (61 rows here).
- Write non-ASCII text as HTML entities (`&deg;C`) or JavaScript escapes (`"°C"`).
- The full version (band, mean line, hot days, slider): https://docs.fused.io/examples/creating-charts
- A share link (`https://www.fused.io/share/fc_<token>/<node>`) works for widget nodes only: for a UDF it shows "This shared widget is unavailable". To share or embed the chart with its inputs, put it in a widget: an `iframe` widget with `"src": "{{temperature_band?heat_threshold=$heat_threshold}}"`, next to the slider in a `div`. Or link the UDF's own page, `https://udf.ai/fc_<token>/<udf_name>.html?heat_threshold=32`.
- For a page that calls UDFs from JavaScript, keeps state between changes or filters with a map, write an HTML template node instead: the `html-template-nodes` skill at https://github.com/fusedio/skills.

## More

- **Widgets from a share URL** (charts over an existing canvas, no canvas edit) → https://docs.fused.io/skills/WIDGET.md
- **Maps** → https://docs.fused.io/skills/FUSED_MAP.md
- **Large datasets** (query any area or time window in seconds, as `era5_daily` does) → https://docs.fused.io/skills/H3.md
