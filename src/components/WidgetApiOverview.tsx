import Link from "@docusaurus/Link";
import React from "react";
import type { WidgetSchemaFile } from "@site/src/components/WidgetSchemaDocs";
import {
  WIDGET_CATEGORIES,
  widgetLabel,
} from "@site/src/lib/widget-api-labels";

const schemaContext = require.context(
  "../../static/widget-schema",
  false,
  /\.json$/,
);

type WidgetEntry = {
  slug: string;
  schema: WidgetSchemaFile;
};

function loadAllWidgets(): WidgetEntry[] {
  return schemaContext
    .keys()
    .map((key) => key.replace("./", "").replace(/\.json$/, ""))
    .sort()
    .map((slug) => ({
      slug,
      schema: schemaContext(`./${slug}.json`) as WidgetSchemaFile,
    }));
}

function WidgetTable({
  slugs,
  widgets,
}: {
  slugs: string[];
  widgets: WidgetEntry[];
}): React.ReactElement {
  const rows = slugs
    .map((slug) => widgets.find((w) => w.slug === slug))
    .filter((w): w is WidgetEntry => Boolean(w));

  return (
    <table>
      <thead>
        <tr>
          <th>Type</th>
          <th>Component</th>
        </tr>
      </thead>
      <tbody>
        {rows.map(({ slug }) => (
          <tr key={slug}>
            <td>
              <code>{slug}</code>
            </td>
            <td>
              <Link to={`/widget-api/${slug}`}>{widgetLabel(slug)}</Link>
            </td>
          </tr>
        ))}
      </tbody>
    </table>
  );
}

export default function WidgetApiOverview(): React.ReactElement {
  const widgets = loadAllWidgets();
  const categorized = new Set(Object.values(WIDGET_CATEGORIES).flat());
  const other = widgets
    .map((w) => w.slug)
    .filter((slug) => !categorized.has(slug));

  return (
    <>
      <p>
        Reference documentation for every Fused canvas widget type. Each page is
        generated from the widget JSON Schema and lists all supported{" "}
        <code>props</code>.
      </p>
      <p>
        For conceptual guides and examples, see the{" "}
        <Link to="/guide/data-input-outputs/import-connection/widgets">
          Widgets guide
        </Link>
        .
      </p>
      <h2>Widget structure</h2>
      <pre>
        <code>{`{
  "type": "<widget-type>",
  "props": { }
}`}</code>
      </pre>
      <p>
        Raw schema files are also available under{" "}
        <code>/widget-schema/&lt;type&gt;.json</code> (for example,{" "}
        <a href="/widget-schema/button.json">
          <code>/widget-schema/button.json</code>
        </a>
        ).
      </p>
      <h2>Input widgets</h2>
      <WidgetTable slugs={WIDGET_CATEGORIES.Input} widgets={widgets} />
      <h2>Output widgets</h2>
      <WidgetTable slugs={WIDGET_CATEGORIES.Output} widgets={widgets} />
      <h2>Utility widgets</h2>
      <WidgetTable slugs={WIDGET_CATEGORIES.Utility} widgets={widgets} />
      {other.length > 0 ? (
        <>
          <h2>Other</h2>
          <WidgetTable slugs={other} widgets={widgets} />
        </>
      ) : null}
    </>
  );
}
