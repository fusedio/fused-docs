# Fused Widget Guide

Widgets are JSON UI components that query UDF output via SQL and render as charts, tables, maps, or input controls. You create one by appending a `?widget=` JSON object to a canvas share URL.

> **Always output widget URLs in a code block, never as a markdown link.** The user copies the URL and pastes it into their browser. Markdown links and HTML anchors both mangle the encoding and will fail.

---

## Core pattern

```
https://www.fused.io/share/fc_<canvas_token>?widget={%22type%22:%20%22bar-chart%22,%20%22props%22:%20{%22sql%22:%20%22SELECT%20...%20FROM%20{{udf_name}}%22,%20%22title%22:%20%22Chart%20title%22}}
```

Encoding rule: replace `"` with `%22` and spaces with `%20`. Leave everything else — `{`, `}`, `:`, `,`, `[`, `]` — as literal characters. The browser handles the rest when the URL is pasted.

```python
encoded = json_string.replace('"', '%22').replace(' ', '%20')
```

**Always output widget URLs as plain text (in a code block), not as markdown links.** Markdown link syntax `[text](url)` mangles the literal `{` and `}` characters.

- The canvas token (`fc_...`) comes from the user's canvas URL.
- `{{udf_name}}` references the output of a UDF on that canvas — replace `udf_name` with the actual UDF name (case-sensitive).
- The SQL runs in-browser via DuckDB over the UDF's output.

---

## Workflow

1. **Find out what UDFs are on the canvas** — fetch `https://udf.ai/fc_<token>.api.json` to see UDF names and parameters.
2. **Sample the data** — call `https://udf.ai/fc_<token>/<udf_name>.json` to see exact column names (case-sensitive).
3. **Write the SQL** — alias columns to match what the component expects (e.g. `label` and `value` for charts).
4. **Encode the widget JSON** — only encode `"` → `%22` and space → `%20`. Keep all other characters literal.
5. **Append to the share URL** as `?widget=<encoded-json>`.

---

## Column naming by component

| Component | Required SQL columns |
|---|---|
| `bar-chart` | `label` (string), `value` (number) |
| `line-chart` | `label` (x-axis), `value` (y-axis) |
| `big-number` | single `value` column |
| `sql-table` | any — all columns are displayed |
| `fused-map` | geometry column required |

Always alias: `SELECT store_name AS label, avg_rating AS value ...`

---

## Examples

**Bar chart — top 10 stores by rating:**

Widget JSON (before encoding):
```json
{
  "type": "bar-chart",
  "props": {
    "sql": "SELECT S_NAME AS label, avg_rating AS value FROM {{join_store_infos}} ORDER BY avg_rating DESC LIMIT 10",
    "title": "Top 10 Best Performing Stores",
    "barColor": "#f59e0b",
    "rotateLabels": true,
    "showValues": true
  }
}
```

Encoded URL (only `"` → `%22`, space → `%20`):
```
https://www.fused.io/share/fc_<token>?widget={%22type%22:%20%22bar-chart%22,%20%22props%22:%20{%22sql%22:%20%22SELECT%20S_NAME%20AS%20label,%20avg_rating%20AS%20value%20FROM%20{{join_store_infos}}%20ORDER%20BY%20avg_rating%20DESC%20LIMIT%2010%22,%20%22title%22:%20%22Top%2010%20Best%20Performing%20Stores%22,%20%22barColor%22:%20%22#f59e0b%22,%20%22rotateLabels%22:%20true,%20%22showValues%22:%20true}}
```

**Line chart — time series:**
```
https://fused.io/share/fc_<token>?widget={
  "type": "line-chart",
  "props": {
    "sql": "SELECT date AS label, value FROM {{orders_df}} ORDER BY label",
    "title": "Time Series",
    "showArea": true,
    "curveType": "smooth"
  }
}
```

**Big number — single KPI:**
```
https://fused.io/share/fc_<token>?widget={
  "type": "big-number",
  "props": {
    "sql": "SELECT ROUND(AVG(avg_rating), 2) AS value FROM {{join_store_infos}}",
    "label": "Avg rating across all stores"
  }
}
```

**Table — sortable leaderboard:**
```
https://fused.io/share/fc_<token>?widget={
  "type": "sql-table",
  "props": {
    "sql": "SELECT S_NAME, store_type, avg_rating, net_promoter_score FROM {{join_store_infos}} ORDER BY avg_rating DESC LIMIT 20",
    "title": "Store leaderboard"
  }
}
```

---

## Layout — multiple widgets

Wrap components in a `div` to compose them side by side or stacked. `div` is the only component that accepts `children`; all others are leaf nodes.

```
https://fused.io/share/fc_<token>?widget={
  "type": "div",
  "props": { "style": "display: flex; gap: 16px; padding: 16px" },
  "children": [
    {
      "type": "big-number",
      "props": {
        "sql": "SELECT COUNT(*) AS value FROM {{join_store_infos}}",
        "label": "Total stores"
      }
    },
    {
      "type": "bar-chart",
      "props": {
        "sql": "SELECT S_NAME AS label, avg_rating AS value FROM {{join_store_infos}} ORDER BY value DESC LIMIT 10",
        "title": "Top 10 stores"
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
    "label": "Min rating",
    "param": "avg_rating_min",
    "min": 0,
    "max": 5,
    "step": 0.1
  }
}
```

Use `$param_name` in SQL to filter by the current parameter value:

```sql
SELECT S_NAME AS label, avg_rating AS value
FROM {{join_store_infos}}
WHERE avg_rating >= $avg_rating_min
ORDER BY value DESC LIMIT 10
```

---

## Available widget types

**Output:**
- `bar-chart` — vertical bar chart, `label` + `value` columns
- `line-chart` — time series, supports `showArea`, `curveType`
- `big-number` — single KPI, supports `prefix`, `suffix`
- `sql-table` — sortable, filterable table
- `fused-map` — interactive map, UDF must return a GeoDataFrame
- `text` — static or dynamic markdown
- `image` — URL or base64 image

**Input (sync to canvas parameters via `param` prop):**
- `slider` — numeric range, `min`, `max`, `step`, `defaultValue`
- `dropdown` — static `options` list or SQL-driven
- `input` — free-text field
- `button` — increments a parameter on click
- `map-bounds` — emits `[west, south, east, north]` from map viewport
