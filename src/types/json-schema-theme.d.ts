declare module "@theme/JSONSchemaViewer" {
  import type { ComponentType } from "react";

  type JSONSchemaViewerProps = {
    schema: Record<string, unknown>;
    viewerOptions?: {
      defaultExpandDepth?: number;
      showExamples?: boolean;
    };
    resolverOptions?: Record<string, unknown>;
  };

  const JSONSchemaViewer: ComponentType<JSONSchemaViewerProps>;
  export default JSONSchemaViewer;
}
