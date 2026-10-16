import React from "react";
import Layout from "@theme/Layout";
import Link from "@docusaurus/Link";

import type { Props } from "@theme/BlogLayout";

export default function BlogLayout(props: Props): JSX.Element {
  const { sidebar, toc, children, ...layoutProps } = props;

  return (
    <Layout {...layoutProps}>
      <div className="container margin-vert--lg">
        <div className="row ">
          <main className="col">
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
