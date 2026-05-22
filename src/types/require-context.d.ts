interface RequireContext {
  keys(): string[];
  (id: string): unknown;
}

interface NodeRequire {
  context(
    directory: string,
    useSubdirectories?: boolean,
    regExp?: RegExp,
  ): RequireContext;
}
