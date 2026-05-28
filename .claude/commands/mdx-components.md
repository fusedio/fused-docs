# MDX components — fused-docs

Reference for every component and pattern available in fused-docs MDX files.

---

## Admonitions (Docusaurus built-in)

Use `:::type` fenced blocks. Always add a blank line before and after.

```md
:::note
Use for neutral supplementary info — something helpful but not critical.
:::

:::tip
Use for recommended approaches, shortcuts, or best practices.
:::

:::info
Use for context or background that readers might want but don't need.
:::

:::warning
Use when the reader might do something that causes data loss, a failed job, or unexpected behaviour.
:::

:::danger
Reserved for irreversible actions (deleting data, revoking tokens, etc.).
:::
```

**Rule:** Don't stack multiple admonitions back to back — if you need two, the content probably belongs in the body prose instead.

---

## Custom components

### `<Tag>`

Coloured inline label. Use for status badges (Experimental, Beta, Deprecated).

```mdx
import Tag from '@site/src/components/Tag';

<Tag color="#f0a500">Experimental</Tag>
<Tag color="#e53e3e" fontColor="#fff">Deprecated</Tag>
```

### `<CellOutput>`

Renders a notebook-style output cell below a code block.

```mdx
import CellOutput from "@site/src/components/CellOutput.jsx";

```python
df.head()
```
<CellOutput>
{/* paste rendered output here */}
</CellOutput>
```

### `<LazyReactPlayer>`

Embeds a video (YouTube, Loom, etc.) with lazy loading.

```mdx
import LazyReactPlayer from "@site/src/components/LazyReactPlayer.jsx";

<LazyReactPlayer url="https://youtu.be/..." />
```

### `<ClickZoomImage>`

Makes an image clickable to zoom. Use for screenshots that need detail.

```mdx
import ClickZoomImage from "@site/src/components/ClickZoomImage.tsx";

<ClickZoomImage src="/img/path/to/image.png" alt="Description" />
```

### `<Tabs>` / `<TabItem>`

Use for showing the same thing in multiple languages or environments.

```mdx
import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

<Tabs>
  <TabItem value="python" label="Python">
    ```python
    fused.run(...)
    ```
  </TabItem>
  <TabItem value="cli" label="CLI">
    ```bash
    fused run ...
    ```
  </TabItem>
</Tabs>
```

**Rule:** Tabs are for equivalent alternatives only — not for sequential steps.

### `<Details>`

Collapsible section. Use for optional deep-dives that most readers can skip.

```mdx
import Details from '@theme/MDXComponents/Details';

<Details>
<summary>How this works under the hood</summary>

Content here...

</Details>
```

---

## Code blocks

Always specify the language. Use `showLineNumbers` for multi-step examples. Use `// highlight-next-line` to call out a key line.

```md
```python showLineNumbers
@fused.udf
def udf(bbox):
    import geopandas as gpd
    # highlight-next-line
    return gpd.read_file(...)
```
```

For CLI commands, use `bash`. For output, use `text` or `console`.

---

## Frontmatter fields used in this repo

```yaml
---
title: Page title          # shown in browser tab and OG
sidebar_label: Short label # shown in sidebar (use if title is long)
sidebar_position: 3        # controls order within the section
toc_max_heading_level: 4   # default is 3; use 4 for API reference pages
unlisted: true             # hides from sidebar but keeps the URL live
---
```
