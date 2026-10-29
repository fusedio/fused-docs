import React from "react";
import MDXComponents from "@theme-original/MDXComponents";
import ReactPlayer from "react-player";
import LazyReactPlayer from "@site/src/components/LazyReactPlayer";
import Tag from "@site/src/components/Tag";
import ClickZoomImage from "@site/src/components/ClickZoomImage";
import ScrollGuardIframe from "@site/src/components/ScrollGuardIframe";

export default {
  ...MDXComponents,
  LazyReactPlayer,
  ReactPlayer,
  Tag,
  ClickZoomImage,
  ScrollGuardIframe,
};
