const LABEL_OVERRIDES: Record<string, string> = {
  "ai-chat": "AI Chat",
  "bar-chart": "Bar Chart",
  "code-editor": "Code Editor",
  "color-input": "Color Input",
  "datetime-input": "Datetime Input",
  "donut-chart": "Donut Chart",
  "fused-map": "Fused Map",
  "gallery-input": "Gallery Input",
  "heatmap-chart": "Heatmap Chart",
  "line-chart": "Line Chart",
  "map-bounds": "Map Bounds",
  "map-h3": "Map H3",
  "number-input": "Number Input",
  "pdf-gallery-viewer": "PDF Gallery Viewer",
  "scatter-chart": "Scatter Chart",
  "sql-runner": "SQL Runner",
  "sql-table": "SQL Table",
  "stacked-area-chart": "Stacked Area Chart",
  "stacked-bar-chart": "Stacked Bar Chart",
  "text-area": "Text Area",
  "text-input": "Text Input",
  "widget-builder": "Widget Builder",
};

export function widgetLabel(slug: string): string {
  if (LABEL_OVERRIDES[slug]) return LABEL_OVERRIDES[slug];
  return slug
    .split("-")
    .map((p) => p.charAt(0).toUpperCase() + p.slice(1))
    .join(" ");
}

export const WIDGET_CATEGORIES: Record<string, string[]> = {
  Input: [
    "slider",
    "text-input",
    "text-area",
    "number-input",
    "dropdown",
    "button",
    "color-input",
    "datetime-input",
    "code-editor",
    "form",
    "gallery-input",
    "camera-input",
    "map-bounds",
    "map-h3",
  ],
  Output: [
    "bar-chart",
    "line-chart",
    "stacked-bar-chart",
    "stacked-area-chart",
    "scatter-chart",
    "donut-chart",
    "heatmap-chart",
    "metric",
    "sql-table",
    "text",
    "image",
    "html",
    "iframe",
    "fused-map",
    "map",
    "pdf-gallery-viewer",
    "widget-builder",
  ],
  Utility: ["div", "sql-runner", "ai-chat", "transformer"],
};
