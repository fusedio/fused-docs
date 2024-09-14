import React from "react";
import clsx from "clsx";
import Translate from "@docusaurus/Translate";
import Link from "@docusaurus/Link";
import Image from "@theme/IdealImage";
import Heading from "@theme/Heading";
// import { useDocsSidebar } from "@docusaurus/theme-common";
import { useCurrentSidebarCategory } from "@docusaurus/theme-common";
// import useDocsSidebar from '@docusaurus/plugin-content-docs/client'; // Corrected import for sidebar access
// import {useDocsSidebar} from '@docusaurus/theme-common/internal';

const Playgrounds = [
  {
    name: "📦 CodeSandbox",
    image:
      "https://fused-magic.s3.us-west-2.amazonaws.com/thumbnails/udfs-staging/Fused_Logo.png",
    url: "https://docusaurus.new/codesandbox",
    urlTS: "https://docusaurus.new/codesandbox-ts",
    description: (
      <Translate id="playground.codesandbox.description">
        CodeSandbox is an online code editor and development environment that
        allows developers to create, share and collaborate on web development
        projects in a browser-based environment
      </Translate>
    ),
  },
  {
    name: " 123 test",
    image:
      "https://fused-magic.s3.us-west-2.amazonaws.com/thumbnails/udfs-staging/Fused_Logo.png",
    url: "https://docusaurus.new/codesandbox",
    urlTS: "https://docusaurus.new/codesandbox-ts",
    description: (
      <Translate id="playground.codesandbox.description">Co...</Translate>
    ),
  },
  {
    name: "⚡ StackBlitz 🆕",
    image:
      "https://fused-magic.s3.us-west-2.amazonaws.com/thumbnails/udfs-staging/Fused_Logo.png",
    url: "https://docusaurus.new/stackblitz",
    urlTS: "https://docusaurus.new/stackblitz-ts",
    description: (
      <Translate
        id="playground.stackblitz.description"
        values={{
          webContainersLink: (
            <Link href="https://blog.stackblitz.com/posts/introducing-webcontainers/">
              WebContainers
            </Link>
          ),
        }}
      >
        {
          "StackBlitz uses a novel {webContainersLink} technology to run Docusaurus directly in your browser."
        }
      </Translate>
    ),
  },
];

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
  // const sidebar = useDocsSidebar();
  console.log("!! sidebar");
  console.log(sidebar);
  const items = sidebar.items || [];
  return (
    <div className="row">
      {items.map(
        (item, index) => (
          console.log("!! item", item),
          (<PlaygroundCard key={index} {...item.customProps} />)
        ),
      )}
    </div>
  );
}
