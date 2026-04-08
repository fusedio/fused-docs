# Fused Widget Visualisation Guide

JSON-UI widgets let you build interactive, shareable visualisations directly from canvas data. Each widget is a JSON node rendered by the Fused client at a share URL. This guide explains the node structure, available components, data-binding patterns, and the MCP tools you use to build and share them.

---

## Node structure

Every widget node follows this shape:

```json
{
  "type": "<component-type>",
  "props": { ... },
  "children": [ ... ]
}
```

- **`type`** — the component identifier (e.g. `"bar-chart"`, `"text"`, `"div"`).
- **`props`** — component-specific properties. Use `get_widget_schema` to get the exact JSON Schema for any component's props.
- **`children`** — nested nodes. Only `div` and `form` accept children (`hasChildren: true`); all other components are leaf nodes.

A standalone widget is a single root node. To compose multiple components, wrap them in a `div`.

---

## Data binding

Most display components accept a `sql` prop that runs a DuckDB SQL query against UDF output registered in the canvas:

```json
{
  "type": "bar-chart",
  "props": {
    "sql": "SELECT neighborhood AS label, COUNT(*) AS value FROM {{listings}} GROUP BY 1 ORDER BY 2 DESC LIMIT 10",
    "title": "Listings by neighborhood"
  }
}
```

- `{{udf_name}}` — references the DataFrame output of a UDF named `udf_name`.
- `$param_name` — substitutes the current value of a canvas parameter.

---

## Canvas parameter sync

Interactive components (inputs, dropdowns, sliders, buttons) can broadcast their current value to all UDFs on the canvas that have a matching parameter name by setting the `param` prop:

```json
{
  "type": "input",
  "props": {
    "label": "City filter",
    "param": "city"
  }
}
```

Any UDF with a `city` parameter will re-run with the new value when the user types in this input.

---

## UDF parameters in share / widget links

> **IMPORTANT — you MUST do this before calling `generate_widget_link`.**
>
> Whenever a widget SQL prop references a UDF (e.g. `SELECT … FROM {{my_udf}}`), that UDF runs on the canvas at render time. If the UDF has **required** parameters (i.e. no default value), the canvas will error unless those values are present in the share URL query string.
>
> **Required workflow for every UDF referenced in SQL:**
>
> 1. **Inspect the UDF** — read the UDF source and identify its parameter list (name, type, default value).
> 2. **Collect all required params** — a parameter is required when it has no default value. Also collect any optional params whose default is unlikely to produce useful output (e.g. `limit: int = 0`).
> 3. **Pass them via `params`** — supply every required (and any relevant optional) parameter as a key/value pair in the `params` argument of `generate_widget_link`. Do **not** embed them only in the widget JSON.
>
> **Do not skip step 1.** You cannot know which params are required without reading the UDF. Guessing or omitting required params will cause the visualisation to fail silently or show an error on the canvas.

When using `generate_widget_link`, supply required UDF parameters via the tool's `params` argument (a flat object). The tool appends them after `widget=...`:

```
https://www.fused.io/share/{share_token}?widget={...}&param1=42
```

**Example:** UDF `udf1` requires `param1: int`. The MCP call shape is:

```json
{
  "share_token": "<token>",
  "widget_json": { "type": "div", "props": {}, "children": [] },
  "params": { "param1": 42 }
}
```

---

## Layout and styling

Use `div` as a flex container:

```json
{
  "type": "div",
  "props": { "style": "display: flex; gap: 16px; padding: 16px" },
  "children": [
    { "type": "big-number", "props": { ... } },
    { "type": "bar-chart",  "props": { ... } }
  ]
}
```

Any component accepts a `style` prop with a plain CSS string for overrides.

---

## Workflow

1. Read this guide for an overview of the widget system.
2. Call `get_widget_schema` with the component type you want to use to get the exact props schema. Pass `"all"` to list every available component type with a short description.
3. **Inspect every UDF you plan to reference in SQL** — read the UDF source. Identify all parameters, note which ones are required (no default), and decide on concrete values for them. **You must complete this step before calling `generate_widget_link`.**
4. Build the widget JSON according to the schema and guidelines above, writing SQL props that reference UDFs via `{{udf_name}}`.
5. Call `generate_widget_link` with the canvas share token, the widget JSON, and all required (plus any relevant optional) UDF params in `params`.

In MCP Apps-capable hosts (Claude, ChatGPT, VS Code, Goose) the widget is rendered inline as an iframe automatically — no need to open a browser or copy a long URL.

---

## MCP tools reference

### `get_widget_schema`

```
get_widget_schema(component_type: str) -> dict
```

Returns the JSON Schema for the requested component's props, together with its `description` and `hasChildren` flag. Pass `"all"` to list every available component type with a short description.

### `generate_widget_link`

```
generate_widget_link(
  share_token: str,
  widget_json: str | dict,
  params: str | dict | None = None,
) -> ToolResult | str
```

Validates the widget JSON against the component schemas and — if valid — constructs the share URL:

```
https://www.fused.io/share/{share_token}?widget={url-encoded-json}[&key=value...]
```

Optional `params` is merged into the query string after `widget` (e.g. `param1=42&region=east`). Accepts either a plain dict or a JSON string (e.g. `'{"param1": 42}'`). Use this for **required UDF parameters** and other canvas query bindings — missing required UDF args often causes runtime errors on the canvas.

On success: the URL is returned and rendered inline as an iframe in Apps-capable hosts.
On failure: plain string listing the validation errors.

---

## Example: multi-chart dashboard

```json
{
  "type": "div",
  "props": { "style": "display: flex; flex-direction: column; gap: 24px; padding: 16px" },
  "children": [
    {
      "type": "div",
      "props": { "style": "display: flex; gap: 16px" },
      "children": [
        {
          "type": "big-number",
          "props": {
            "sql": "SELECT COUNT(*) AS value FROM {{listings}}",
            "label": "Total listings"
          }
        },
        {
          "type": "big-number",
          "props": {
            "sql": "SELECT ROUND(AVG(price), 2) AS value FROM {{listings}}",
            "label": "Avg price"
          }
        }
      ]
    },
    {
      "type": "bar-chart",
      "props": {
        "sql": "SELECT neighborhood AS label, COUNT(*) AS value FROM {{listings}} GROUP BY 1 ORDER BY 2 DESC LIMIT 10",
        "title": "Listings by neighborhood"
      }
    },
    {
      "type": "table",
      "props": {
        "sql": "SELECT id, neighborhood, price, room_type FROM {{listings}} ORDER BY price DESC LIMIT 20",
        "title": "Top 20 listings by price"
      }
    }
  ]
}
```

---

## Available components

Call `get_widget_schema("all")` to get the current catalog of available component types. Common ones include:

| Type | Description |
|---|---|
| `div` | Flex container for layout — the only component that wraps others |
| `text` | Static markdown or plain text |
| `big-number` | Single prominent metric with a label |
| `bar-chart` | Vertical or horizontal bar chart |
| `line-chart` | Time series or ordered line chart |
| `table` | Scrollable data table |
| `map` | Interactive map layer |
| `input` | Text input that syncs to a canvas parameter |
| `select` | Dropdown that syncs to a canvas parameter |
| `slider` | Numeric range slider that syncs to a canvas parameter |

Use `get_widget_schema("<type>")` for the exact props schema of any component before building with it.
