import React from "react";
import type { WidgetSchemaFile } from "@site/src/components/WidgetSchemaDocs";
import WidgetSchemaDocs from "@site/src/components/WidgetSchemaDocs";
import { widgetLabel } from "@site/src/lib/widget-api-labels";

const schemaContext = require.context(
  "../../static/widget-schema",
  false,
  /\.json$/,
);

function loadSchema(slug: string): WidgetSchemaFile {
  return schemaContext(`./${slug}.json`) as WidgetSchemaFile;
}

type Props = {
  slug: string;
};

export default function WidgetSchemaPage({ slug }: Props): React.ReactElement {
  const schema = loadSchema(slug);
  const title = widgetLabel(slug);

  return (
    <>
      <h1>{title}</h1>
      <WidgetSchemaDocs schema={schema} />
    </>
  );
}
