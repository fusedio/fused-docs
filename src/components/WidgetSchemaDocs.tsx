import CodeBlock from "@theme/CodeBlock";
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

// Fenced code block pattern — captured so split() keeps it in the array.
const CODE_FENCE_RE = /(```[\w]*\n[\s\S]*?```)/g;
const CODE_FENCE_MATCH_RE = /^```([\w]*)\n([\s\S]*?)```$/;

function MarkdownDescription({ text }: { text: string }): React.ReactElement {
  const segments = text.split(CODE_FENCE_RE);
  const elements: React.ReactElement[] = [];
  let key = 0;

  for (const segment of segments) {
    const codeMatch = segment.match(CODE_FENCE_MATCH_RE);
    if (codeMatch) {
      const lang = codeMatch[1] || "text";
      const code = codeMatch[2].trimEnd();
      elements.push(
        <CodeBlock key={key++} language={lang}>
          {code}
        </CodeBlock>,
      );
      continue;
    }
    for (const para of segment.split(/\n\n+/)) {
      const trimmed = para.trim();
      if (!trimmed) continue;
      if (trimmed.startsWith("## ")) {
        elements.push(<h3 key={key++}>{trimmed.slice(3)}</h3>);
      } else if (trimmed.startsWith("# ")) {
        elements.push(<h2 key={key++}>{trimmed.slice(2)}</h2>);
      } else {
        elements.push(<p key={key++}>{trimmed}</p>);
      }
    }
  }

  return <>{elements}</>;
}

export default function WidgetSchemaDocs({
  schema,
}: Props): React.ReactElement {
  const widgetType = schema.type;
  const schemaDescription = (schema.propsSchema as { description?: string })
    .description;
  // Strip description before passing to JSONSchemaViewer — we render it
  // ourselves above the props table to support markdown formatting.
  const propsSchemaForViewer = Object.fromEntries(
    Object.entries(schema.propsSchema).filter(([k]) => k !== "description"),
  );

  return (
    <div className="widget-schema-docs">
      <p>
        <strong>Type:</strong> <code>{widgetType}</code>
      </p>
      {schema.description ? <p>{schema.description}</p> : null}
      <p>
        <strong>Supports children:</strong> {schema.hasChildren ? "Yes" : "No"}
      </p>
      {schemaDescription ? (
        <MarkdownDescription text={schemaDescription} />
      ) : null}
      <p>
        Every widget is defined as{" "}
        <code>{`{ "type": "${widgetType}", "props": { ... } }`}</code>. The
        properties below describe the <code>props</code> object.
      </p>
      <h2>Props</h2>
      <JSONSchemaViewer
        schema={propsSchemaForViewer}
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
