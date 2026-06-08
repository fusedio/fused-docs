import React from "react";
import type { WidgetSchemaFile } from "@site/src/components/WidgetSchemaDocs";
import WidgetSchemaDocs from "@site/src/components/WidgetSchemaDocs";

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
  return <WidgetSchemaDocs schema={schema} />;
}
