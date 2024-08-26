import React from "react";
import clsx from "clsx";
import Layout from "@theme/Layout";
import BlogSidebar from "@theme/BlogSidebar";
import Link from "@docusaurus/Link";

import type { Props } from "@theme/BlogLayout";

export default function BlogLayout(props: Props): JSX.Element {
  const { sidebar, toc, children, ...layoutProps } = props;
  const hasSidebar = sidebar && sidebar.items.length > 0;

  return (
    <Layout {...layoutProps}>
      <div className="container margin-vert--lg">
        <div className="row">
          <BlogSidebar sidebar={sidebar} />
          <main
            className={clsx("col", {
              "col--7": hasSidebar,
              "col--9 col--offset-1": !hasSidebar,
            })}
          >
            {children}
          </main>

          {toc && (
            <div className="col col--2">
              <h4>Jump to section</h4>
              {toc} <br></br>
              <Link to={"/blog"}>↰ Back to blog</Link>
            </div>
          )}
        </div>
      </div>
    </Layout>
  );
}
