---
name: fused-widget
description: Use when showing UDF output as a chart, table, KPI or input controls through a Fused share URL (`https://www.fused.io/share/fc_<token>?widget=...`), without editing a canvas.
---

# Fused widgets from a share URL

A widget is a JSON UI component that queries UDF output with SQL and renders it as a chart, table or input. Encode the widget JSON into the canvas share URL. Rules for every Fused task: https://docs.fused.io/skills/SKILL.md

```
https://www.fused.io/share/fc_<token>?widget=<encoded-json>
```

The token is the one in the UDF endpoint: `https://udf.ai/fc_abc123/my_udf.json` gives `https://www.fused.io/share/fc_abc123?widget=...`.

## Steps

1. Get the canvas token from the endpoint URL or the user's canvas URL.
2. Find UDF names in `https://udf.ai/fc_<token>.api.json`, and column names (case-sensitive) in `https://udf.ai/fc_<token>/<udf_name>.json`.
3. Write the SQL over `{{udf_name}}`, aliasing columns to what the component reads:

| Component | SQL columns |
|---|---|
| `bar-chart` | `label` (string), `value` (number) |
| `line-chart` | `label` (x-axis), `value` (y-axis) |
| `metric` | one `value` (first column of the first row) |
| `sql-table` | any: every column is shown |

4. Encode: replace `"` with `%22` and spaces with `%20`, and leave `{`, `}`, `:`, `,`, `[`, `]` as they are. Use named colors (`"steelblue"`, `"orange"`) in prop values: a `#` ends the URL.

```python
encoded = json.dumps(widget).replace('"', '%22').replace(' ', '%20')
url = f"https://www.fused.io/share/fc_{token}?widget={encoded}"
```

5. Give the URL to the user in a code block so they can copy it intact; a markdown link mangles the encoding.

## Example: two widgets side by side

Wrap components in a `div` to place them side by side or stacked.

```json
{
  "type": "div",
  "props": {"style": "display: flex; gap: 16px; padding: 16px"},
  "children": [
    {"type": "metric", "props": {"sql": "SELECT COUNT(*) AS value FROM {{my_udf}}", "label": "Total"}},
    {"type": "bar-chart", "props": {"sql": "SELECT name AS label, score AS value FROM {{my_udf}} ORDER BY score DESC LIMIT 10", "title": "Top 10", "barColor": "steelblue"}}
  ]
}
```

Encoded:

```
https://www.fused.io/share/fc_<token>?widget={%22type%22:%20%22div%22,%20%22props%22:%20{%22style%22:%20%22display:%20flex;%20gap:%2016px;%20padding:%2016px%22},%20%22children%22:%20[{%22type%22:%20%22metric%22,%20%22props%22:%20{%22sql%22:%20%22SELECT%20COUNT(*)%20AS%20value%20FROM%20{{my_udf}}%22,%20%22label%22:%20%22Total%22}},%20{%22type%22:%20%22bar-chart%22,%20%22props%22:%20{%22sql%22:%20%22SELECT%20name%20AS%20label,%20score%20AS%20value%20FROM%20{{my_udf}}%20ORDER%20BY%20score%20DESC%20LIMIT%2010%22,%20%22title%22:%20%22Top%2010%22,%20%22barColor%22:%20%22steelblue%22}}]}
```

## Inputs

An input with a `param` sends its value to every UDF on the canvas with a parameter of that name, which runs again. SQL reads it as `$param_name`:

```json
{"type": "slider", "props": {"label": "Min score", "param": "score_min", "min": 0, "max": 100, "step": 1}}
```

```sql
SELECT name AS label, score AS value FROM {{my_udf}} WHERE score >= $score_min ORDER BY score DESC LIMIT 10
```

## Components

- `bar-chart`: props `title`, `barColor`, `rotateLabels`, `showValues`, `barRadius`
- `line-chart`: time series; props `title`, `showArea`, `curveType` (`"smooth"` or `"linear"`)
- `metric`: one KPI; props `label`, `prefix`, `suffix`
- `sql-table`: sortable, filterable table
- `text`: static text, or the first value a `sql` returns
- `image`: URL or base64 image
- `slider`: numeric range; props `min`, `max`, `step`, `defaultValue`
- `dropdown`: static `options` list or SQL-driven
- `text-input`: free-text field
- `button`: each click increments its `param`

Every component and prop: https://docs.fused.io/widget-api/overview. Maps: https://docs.fused.io/skills/FUSED_MAP.md
