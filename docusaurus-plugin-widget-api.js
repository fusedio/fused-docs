/**
 * Generates widget API doc pages from static/widget-schema/*.json at build time.
 * Runs before the docs plugin loads content (register in plugins[] before presets).
 */
const fs = require("fs");
const path = require("path");

const SCHEMA_DIR = path.join(__dirname, "static/widget-schema");
const DOCS_DIR = path.join(__dirname, "docs/widget-api");

const LABEL_OVERRIDES = {
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

function widgetLabel(slug) {
  if (LABEL_OVERRIDES[slug]) return LABEL_OVERRIDES[slug];
  return slug
    .split("-")
    .map((p) => p.charAt(0).toUpperCase() + p.slice(1))
    .join(" ");
}

function generateWidgetMdx(slug) {
  const label = widgetLabel(slug);
  return `---
id: ${slug}
title: ${label}
sidebar_label: ${label}
---

import WidgetSchemaPage from '@site/src/components/WidgetSchemaPage';

<WidgetSchemaPage slug="${slug}" />
`;
}

function syncWidgetApiDocs() {
  if (!fs.existsSync(DOCS_DIR)) {
    fs.mkdirSync(DOCS_DIR, { recursive: true });
  }

  const schemas = fs
    .readdirSync(SCHEMA_DIR)
    .filter((f) => f.endsWith(".json"))
    .map((f) => f.replace(/\.json$/, ""));

  const expected = new Set(schemas.map((s) => `${s}.mdx`));

  for (const file of fs.readdirSync(DOCS_DIR)) {
    if (file === "overview.mdx") continue;
    if (file.endsWith(".mdx") && !expected.has(file)) {
      fs.unlinkSync(path.join(DOCS_DIR, file));
    }
  }

  for (const slug of schemas) {
    fs.writeFileSync(
      path.join(DOCS_DIR, `${slug}.mdx`),
      generateWidgetMdx(slug),
    );
  }
}

module.exports = function widgetApiPlugin() {
  return {
    name: "docusaurus-plugin-widget-api",
    loadContent() {
      syncWidgetApiDocs();
      return null;
    },
  };
};
