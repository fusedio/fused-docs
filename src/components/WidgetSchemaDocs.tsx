import JSONSchemaViewer from "@theme/JSONSchemaViewer";
import React from "react";

export type WidgetSchemaFile = {
  type: string;
  description: string;
  hasChildren: boolean;
  propsSchema: Record<string, unknown>;
};

type Props = {
  schema: WidgetSchemaFile;
};

function titleCase(slug: string): string {
  return slug
    .split("-")
    .map((part) => part.charAt(0).toUpperCase() + part.slice(1))
    .join(" ");
}

export default function WidgetSchemaDocs({
  schema,
}: Props): React.ReactElement {
  const widgetType = schema.type;

  return (
    <div className="widget-schema-docs">
      <p>
        <strong>Type:</strong> <code>{widgetType}</code>
      </p>
      {schema.description ? <p>{schema.description}</p> : null}
      <p>
        <strong>Supports children:</strong> {schema.hasChildren ? "Yes" : "No"}
      </p>
      <p>
        Every widget is defined as{" "}
        <code>{`{ "type": "${widgetType}", "props": { ... } }`}</code>. The
        properties below describe the <code>props</code> object.
      </p>
      <h2>Props</h2>
      <JSONSchemaViewer
        schema={schema.propsSchema}
        viewerOptions={{
          defaultExpandDepth: 1,
          showExamples: true,
        }}
      />
      <h2>Raw schema</h2>
      <p>
        Download the full schema file:{" "}
        <a href={`/widget-schema/${widgetType}.json`}>
          <code>/widget-schema/{widgetType}.json</code>
        </a>
      </p>
    </div>
  );
}

export { titleCase };
