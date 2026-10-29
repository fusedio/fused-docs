function walk(node) {
  if (node.type === "mdxJsxFlowElement" && node.name === "iframe") {
    node.name = "ScrollGuardIframe";
  }
  if (node.children) {
    node.children.forEach(walk);
  }
}

module.exports = function iframeScrollGuard() {
  return (tree) => walk(tree);
};
