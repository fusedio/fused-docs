import { ThemeClassNames } from "@docusaurus/theme-common";

const SKIPPED_TAGS = new Set(["SCRIPT", "STYLE", "NOSCRIPT", "NAV", "SUMMARY"]);

const BLOCK_TAGS = new Set([
  "P", "DIV", "SECTION", "HEADER", "FOOTER", "MAIN", "ARTICLE", "ASIDE", "FIGURE", "FIGCAPTION",
  "UL", "OL", "DL", "DT", "DD", "PRE", "TABLE", "BLOCKQUOTE", "HR", "DETAILS", "IFRAME", "VIDEO",
  "H1", "H2", "H3", "H4", "H5", "H6",
]);

const joinBlocks = (parts: string[], separator = "\n\n") => parts.filter(Boolean).join(separator);

const wrap = (mark: string, text = "") => (text ? `${mark}${text}${mark}` : "");

function inline(node: Node): string {
  if (node.nodeType === Node.TEXT_NODE) return (node.textContent ?? "").replace(/\s+/g, " ");
  if (!(node instanceof HTMLElement) || SKIPPED_TAGS.has(node.tagName) || node.classList.contains("hash-link")) {
    return "";
  }
  const text = () => Array.from(node.childNodes).map(inline).join("");
  switch (node.tagName) {
    case "A": {
      const label = text().replace(/\s+/g, " ").trim();
      const href = (node as HTMLAnchorElement).href;
      return href && label ? `[${label}](${href})` : label;
    }
    case "STRONG":
    case "B":
      return wrap("**", text().trim());
    case "EM":
    case "I":
      return wrap("_", text().trim());
    case "CODE":
      return `\`${node.textContent ?? ""}\``;
    case "BR":
      return "\n";
    case "IMG": {
      const img = node as HTMLImageElement;
      return img.src ? `![${img.alt}](${img.src})` : "";
    }
    case "BUTTON":
      return Array.from(node.querySelectorAll("img")).map(inline).join(" ");
    default:
      return BLOCK_TAGS.has(node.tagName) ? ` ${text()} ` : text();
  }
}

function blocks(parent: Element, separator = "\n\n"): string {
  const out: string[] = [];
  let run = "";
  const flush = () => {
    out.push(run.replace(/[ \t]+\n/g, "\n").trim());
    run = "";
  };
  parent.childNodes.forEach((child) => {
    if (child instanceof HTMLElement && BLOCK_TAGS.has(child.tagName)) {
      flush();
      out.push(block(child).trim());
    } else {
      run += inline(child);
    }
  });
  flush();
  return joinBlocks(out, separator);
}

function quote(text: string): string {
  return text.split("\n").map((line) => (line ? `> ${line}` : ">")).join("\n");
}

function codeBlock(el: HTMLElement): string {
  const pre = el.tagName === "PRE" ? el : el.querySelector("pre");
  if (!pre) return "";
  const lang = /language-([\w-]+)/.exec(`${el.className} ${pre.className}`)?.[1] ?? "";
  const lines = pre.querySelectorAll(".token-line");
  const code = lines.length
    ? Array.from(lines).map((l) => l.textContent ?? "").join("\n")
    : pre.textContent ?? "";
  const fence = "`".repeat(Math.max(3, ...(code.match(/`+/g) ?? []).map((run) => run.length + 1)));
  return `${fence}${lang}\n${code.replace(/\n+$/, "")}\n${fence}`;
}

function list(el: HTMLElement, ordered: boolean): string {
  const start = ordered ? (el as HTMLOListElement).start || 1 : 1;
  return Array.from(el.querySelectorAll(":scope > li"))
    .map((li, i) => {
      const marker = ordered ? `${start + i}. ` : "- ";
      const separator = li.querySelectorAll(":scope > p").length > 1 ? "\n\n" : "\n";
      const indent = " ".repeat(marker.length);
      return marker + blocks(li, separator).split("\n").map((line, j) => (j && line ? indent + line : line)).join("\n");
    })
    .join("\n");
}

function table(el: HTMLElement): string {
  const rows = Array.from(el.querySelectorAll("tr")).map((tr) =>
    Array.from(tr.children).map((cell) => inline(cell).trim().replace(/\s*\n\s*/g, " ").replace(/\|/g, "\\|")),
  );
  if (!rows.length) return "";
  const divider = rows[0].map(() => "---");
  return [rows[0], divider, ...rows.slice(1)].map((r) => `| ${r.join(" | ")} |`).join("\n");
}

function tabs(el: HTMLElement): string {
  const labels = Array.from(el.querySelectorAll(':scope > [role="tablist"] > [role="tab"]')).map(
    (t) => t.textContent?.trim() ?? "",
  );
  const panels = Array.from(el.querySelectorAll(':scope > div > [role="tabpanel"]'));
  return joinBlocks(panels.map((panel, i) => joinBlocks([wrap("**", labels[i]), blocks(panel)])));
}

function block(el: HTMLElement): string {
  const heading = el.tagName.match(/^H([1-6])$/);
  if (heading) return `${"#".repeat(Number(heading[1]))} ${inline(el).trim()}`;
  if (el.tagName === "PRE" || el.classList.contains(ThemeClassNames.common.codeBlock)) return codeBlock(el);
  if (el.classList.contains(ThemeClassNames.tabs.container)) return tabs(el);
  if (el.classList.contains(ThemeClassNames.common.admonition)) {
    const title = el.querySelector('[class*="admonitionHeading"]')?.textContent?.trim() ?? "";
    const content = el.querySelector('[class*="admonitionContent"]');
    return quote(joinBlocks([`**${title}**`, content ? blocks(content) : ""]));
  }
  switch (el.tagName) {
    case "P":
      return inline(el).trim();
    case "UL":
      return list(el, false);
    case "OL":
      return list(el, true);
    case "TABLE":
      return table(el);
    case "BLOCKQUOTE":
      return quote(blocks(el));
    case "HR":
      return "---";
    case "DETAILS": {
      const summary = el.querySelector("summary");
      const title = summary ? Array.from(summary.childNodes).map(inline).join("").trim() : "";
      return joinBlocks([wrap("**", title), blocks(el)]);
    }
    case "IFRAME": {
      const frame = el as HTMLIFrameElement;
      return frame.src ? `[${frame.title || "Embedded content"}](${frame.src})` : "";
    }
    case "VIDEO": {
      const src = (el as HTMLVideoElement).currentSrc || el.querySelector("source")?.src;
      return src ? `[Video](${src})` : "";
    }
    default:
      return blocks(el);
  }
}

export default function pageToMarkdown(): string {
  try {
    const article = document.querySelector("article");
    const body = article?.querySelector(".markdown");
    if (!article || !body) return "";
    const title = article.querySelector("h1");
    const heading = title && !body.contains(title) ? `# ${title.textContent?.trim() ?? ""}` : "";
    return `${joinBlocks([heading, blocks(body)]).trim()}\n`;
  } catch {
    return "";
  }
}
