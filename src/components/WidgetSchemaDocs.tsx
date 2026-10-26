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

const INLINE_RE = /(`[^`]+`|\*\*[^*]+\*\*|\[[^\]]+\]\([^)\s]+\))/g;
const LINK_RE = /^\[([^\]]+)\]\(([^)\s]+)\)$/;
const BULLET_RE = /^\s*[-*]\s+(.*)$/;
const NUMBERED_RE = /^\s*\d+\.\s+(.*)$/;

function renderInline(text: string): React.ReactNode[] {
  return text.split(INLINE_RE).map((part, i) => {
    if (part.startsWith("`") && part.endsWith("`") && part.length > 1) {
      return <code key={i}>{part.slice(1, -1)}</code>;
    }
    if (part.startsWith("**") && part.endsWith("**") && part.length > 3) {
      return <strong key={i}>{part.slice(2, -2)}</strong>;
    }
    const link = part.match(LINK_RE);
    if (link) {
      return (
        <a key={i} href={link[2]}>
          {link[1]}
        </a>
      );
    }
    return part;
  });
}

function InlineDescription({
  description,
}: {
  description: string;
}): React.ReactElement {
  return <>{renderInline(description)}</>;
}

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
    let paraBuf: string[] = [];
    let listItems: string[] = [];
    let listOrdered = false;
    const flushPara = () => {
      const t = paraBuf.join(" ").trim();
      if (t) elements.push(<p key={key++}>{renderInline(t)}</p>);
      paraBuf = [];
    };
    const flushList = () => {
      if (listItems.length) {
        const items = listItems.map((item, i) => (
          <li key={i}>{renderInline(item)}</li>
        ));
        elements.push(
          listOrdered ? <ol key={key++}>{items}</ol> : <ul key={key++}>{items}</ul>,
        );
      }
      listItems = [];
    };
    const flushAll = () => {
      flushPara();
      flushList();
    };
    for (const line of segment.split("\n")) {
      const bullet = line.match(BULLET_RE);
      const numbered = line.match(NUMBERED_RE);
      if (line.startsWith("## ")) {
        flushAll();
        elements.push(<h3 key={key++}>{renderInline(line.slice(3))}</h3>);
      } else if (line.startsWith("# ")) {
        flushAll();
        elements.push(<h2 key={key++}>{renderInline(line.slice(2))}</h2>);
      } else if (bullet || numbered) {
        flushPara();
        const ordered = Boolean(numbered);
        if (listItems.length && ordered !== listOrdered) flushList();
        listOrdered = ordered;
        listItems.push((bullet ?? numbered)![1].trim());
      } else if (line.trim() === "") {
        flushAll();
      } else if (listItems.length) {
        listItems[listItems.length - 1] += ` ${line.trim()}`;
      } else {
        paraBuf.push(line.trim());
      }
    }
    flushAll();
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
          DescriptionComponent: InlineDescription,
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
