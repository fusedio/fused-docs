import React from "react";
import Layout from "@theme/Layout";
import Link from "@docusaurus/Link";
import { useLocation } from "@docusaurus/router";
import LLMShareButton from "@site/src/components/LLMShareButton";

import type { Props } from "@theme/BlogLayout";

export default function BlogLayout(props: Props): JSX.Element {
  const { sidebar, toc, children, ...layoutProps } = props;
  const { pathname } = useLocation();

  // Don't show on list pages (/blog, /shorts, /blog/page/N, /shorts/page/N)
  const isListPage = /^\/(blog|shorts)(\/page\/\d+)?\/?$/.test(pathname);

  return (
    <Layout {...layoutProps}>
      <div className="container margin-vert--lg">
        <div className="row ">
          <main className="col">
            {!isListPage && (
              <div style={{ display: "flex", justifyContent: "flex-end", marginBottom: "0.5rem" }}>
                <LLMShareButton />
              </div>
            )}
            {children}
          </main>

          {toc && (
            <div className="col col--2">
              <h4>Jump to section</h4>
              {toc} <br></br>
              <Link to={"/blog"}>← Back to blog</Link>
            </div>
          )}
        </div>
      </div>
    </Layout>
  );
}
