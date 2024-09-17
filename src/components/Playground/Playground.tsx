import React from "react";
import clsx from "clsx";
import Link from "@docusaurus/Link";
import Image from "@theme/IdealImage";
import Heading from "@theme/Heading";
import { useCurrentSidebarCategory } from "@docusaurus/theme-common";

interface Props {
  name: string;
  image: string;
  url: string;
  urlTS: string;
  description: JSX.Element;
}

function PlaygroundCard({ name, image, url, urlTS, description }: Props) {
  image =
    "https://fused-magic.s3.us-west-2.amazonaws.com/thumbnails/udfs-staging/Fused_Logo.png";

  return (
    <div className="col col--6 margin-bottom--lg" style={{ display: "flex" }}>
      <div
        className={clsx(
          "card cardContainer_node_modules-@docusaurus-theme-classic-lib-theme-DocCard-styles-module",
        )}
      >
        <Link to={url}>
          <div className={clsx("card__image")}>
            <Image img={image} alt={`${name}'s image`} />
          </div>
          <div className="card__body playground-card-body">
            <Heading as="h3">{name}</Heading>
            <p>{description}</p>
          </div>
        </Link>
      </div>
    </div>
  );
}

export function PlaygroundCardsRow(): JSX.Element {
  const sidebar = useCurrentSidebarCategory();
  const items = sidebar.items || [];
  return (
    <div className="row">
      {items.map((item, index) => (
        // customProps is the sidebar_custom_props frontmatter https://github.com/facebook/docusaurus/pull/6619/commits/23237bb1538ec02e71bcc58f6fcaabf56caaec87
        <PlaygroundCard key={index} {...item.customProps} />
      ))}
    </div>
  );
}
