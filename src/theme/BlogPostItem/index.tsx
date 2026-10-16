import React from "react";
import BlogPostItem from "@theme-original/BlogPostItem";
import type BlogPostItemType from "@theme/BlogPostItem";
import type { WrapperProps } from "@docusaurus/types";
import { useBlogPost } from "@docusaurus/plugin-content-blog/client";
import LLMShareButton from "@site/src/components/LLMShareButton";

type Props = WrapperProps<typeof BlogPostItemType>;

export default function BlogPostItemWrapper(props: Props): JSX.Element {
  const { isBlogPostPage } = useBlogPost();
  return (
    <>
      {isBlogPostPage && (
        <div style={{ display: "flex", justifyContent: "flex-end", marginBottom: "0.5rem" }}>
          <LLMShareButton />
        </div>
      )}
      <BlogPostItem {...props} />
    </>
  );
}
