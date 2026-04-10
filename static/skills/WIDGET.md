# Fused Widget Guide

Widgets are JSON UI components that query UDF output via SQL and render as charts, tables, or input controls. You create one by encoding a JSON object and appending it to a canvas share URL.

> **Always output widget URLs in a code block, never as a markdown link.** The user copies the URL and pastes it into their browser. Markdown links mangle the encoding and will fail.

---

## Canvas token

The canvas token (`fc_...`) is the same token used for API calls. If the API endpoint is:
```
https://udf.ai/fc_abc123/my_udf.json
```
Then the widget share URL uses the same token:
```
https://www.fused.io/share/fc_abc123?widget=...
```

---

## Core pattern

```
https://www.fused.io/share/fc_<token>?widget=<encoded-json>
```

**Encoding rule:** replace `"` with `%22` and spaces with `%20`. Leave everything else — `{`, `}`, `:`, `,`, `[`, `]` — as literal characters.

```python
encoded = json.dumps(widget).replace('"', '%22').replace(' ', '%20')
url = f"https://www.fused.io/share/fc_{token}?widget={encoded}"
```

> Do not use `#` in prop values (e.g. hex color codes) — `#` terminates the URL. Use named colors (`"steelblue"`, `"orange"`) instead.

---

## Workflow

1. **Get the canvas token** — from the API endpoint URL (`udf.ai/fc_<token>`) or the user's canvas URL.
2. **Discover UDFs** — fetch `https://udf.ai/fc_<token>.api.json` to see UDF names.
3. **Sample the data** — call `https://udf.ai/fc_<token>/<udf_name>.json` to see exact column names (case-sensitive).
4. **Write the SQL** — alias columns to match what the component expects (see table below).
5. **Encode** — `json.dumps(widget).replace('"', '%22').replace(' ', '%20')`
6. **Output as a code block** for the user to copy-paste into their browser.

---

## Column naming by component

| Component | Required SQL columns |
|---|---|
| `bar-chart` | `label` (string), `value` (number) |
| `line-chart` | `label` (x-axis), `value` (y-axis) |
| `big-number` | single `value` column |
| `sql-table` | any — all columns are displayed |

Always alias: `SELECT my_name_col AS label, my_score_col AS value ...`

---

## Examples

All URLs below are ready to copy-paste. Replace `fc_<token>` with the actual canvas token and `my_udf` with the actual UDF name.

**Bar chart — top 10 by score:**
```
https://www.fused.io/share/fc_<token>?widget={%22type%22:%20%22bar-chart%22,%20%22props%22:%20{%22sql%22:%20%22SELECT%20name%20AS%20label,%20score%20AS%20value%20FROM%20{{my_udf}}%20ORDER%20BY%20score%20DESC%20LIMIT%2010%22,%20%22title%22:%20%22Top%2010%20results%22,%20%22barColor%22:%20%22steelblue%22}}
```

**Line chart — time series:**
```
https://www.fused.io/share/fc_<token>?widget={%22type%22:%20%22line-chart%22,%20%22props%22:%20{%22sql%22:%20%22SELECT%20date%20AS%20label,%20revenue%20AS%20value%20FROM%20{{my_udf}}%20ORDER%20BY%20date%22,%20%22title%22:%20%22Revenue%20over%20time%22,%20%22showArea%22:%20true,%20%22curveType%22:%20%22smooth%22}}
```

**Big number — single KPI:**
```
https://www.fused.io/share/fc_<token>?widget={%22type%22:%20%22big-number%22,%20%22props%22:%20{%22sql%22:%20%22SELECT%20COUNT(*)%20AS%20value%20FROM%20{{my_udf}}%22,%20%22label%22:%20%22Total%20records%22}}
```

**Table — all columns:**
```
https://www.fused.io/share/fc_<token>?widget={%22type%22:%20%22sql-table%22,%20%22props%22:%20{%22sql%22:%20%22SELECT%20*%20FROM%20{{my_udf}}%20LIMIT%2020%22,%20%22title%22:%20%22Results%22}}
```

---

## Layout — multiple widgets

Wrap components in a `div` to compose them side by side or stacked. `div` is the only component that accepts `children`; all others are leaf nodes.

```
https://www.fused.io/share/fc_<token>?widget={%22type%22:%20%22div%22,%20%22props%22:%20{%22style%22:%20%22display:%20flex;%20gap:%2016px;%20padding:%2016px%22},%20%22children%22:%20[{%22type%22:%20%22big-number%22,%20%22props%22:%20{%22sql%22:%20%22SELECT%20COUNT(*)%20AS%20value%20FROM%20{{my_udf}}%22,%20%22label%22:%20%22Total%22}},%20{%22type%22:%20%22bar-chart%22,%20%22props%22:%20{%22sql%22:%20%22SELECT%20name%20AS%20label,%20score%20AS%20value%20FROM%20{{my_udf}}%20ORDER%20BY%20score%20DESC%20LIMIT%2010%22,%20%22title%22:%20%22Top%2010%22}}]}
```

The widget JSON before encoding:
```json
{
  "type": "div",
  "props": { "style": "display: flex; gap: 16px; padding: 16px" },
  "children": [
    {
      "type": "big-number",
      "props": {
        "sql": "SELECT COUNT(*) AS value FROM {{my_udf}}",
        "label": "Total"
      }
    },
    {
      "type": "bar-chart",
      "props": {
        "sql": "SELECT name AS label, score AS value FROM {{my_udf}} ORDER BY score DESC LIMIT 10",
        "title": "Top 10"
      }
    }
  ]
}
```

---

## Canvas parameter sync

Input widgets broadcast their value to any UDF on the canvas that has a matching parameter name, triggering a re-run:

```json
{
  "type": "slider",
  "props": {
    "label": "Min score",
    "param": "score_min",
    "min": 0,
    "max": 100,
    "step": 1
  }
}
```

Use `$param_name` in SQL to filter by the current parameter value:

```sql
SELECT name AS label, score AS value
FROM {{my_udf}}
WHERE score >= $score_min
ORDER BY score DESC LIMIT 10
```

---

## Available widget types

**Output:**
- `bar-chart` — vertical bar chart, `label` + `value` columns; props: `barColor`, `rotateLabels`, `showValues`, `barRadius`
- `line-chart` — time series; props: `showArea`, `curveType` (`"smooth"` or `"linear"`)
- `big-number` — single KPI; props: `label`, `prefix`, `suffix`
- `sql-table` — sortable, filterable table
- `text` — static or dynamic markdown
- `image` — URL or base64 image

**Input (sync to canvas parameters via `param` prop):**
- `slider` — numeric range; props: `min`, `max`, `step`, `defaultValue`
- `dropdown` — static `options` list or SQL-driven
- `input` — free-text field
- `button` — increments a parameter on click
