import React, { useState, useEffect } from "react";
import Iframe from "@site/src/components/Iframe";
import DEFAULT_APP_CODE from "@site/src/app-iframe/python/default.py";
import BrowserOnly from "@docusaurus/BrowserOnly";
import ExecutionEnvironment from "@docusaurus/ExecutionEnvironment";

// Swizzling (wrapping) the Root component since it never unmounts
// This wrapper mounts MAX_IFRAMES_PER_PAGE iframes on the page
// so that when we go to a page with visible iframes, it's already loaded

// Modify MAX_IFRAMES_PER_PAGE to the number of iframes that need to be preloaded
// Add PATHS_WITH_THREE_IFRAMES etc. if needed
// Modify checkIfPathContainsIframe function for additional iframes

const PATHS_WITH_ONE_IFRAME = [
  "/user-guide/transform/geospatial/buffer/",
  "/user-guide/transform/geospatial/point-in-polygon/",
  "/user-guide/transform/geospatial/raster-h3/",
  "/user-guide/transform/geospatial/zonal_stats/",
  "/workbench/app-builder/",
  "/user-guide/quickstart/",
];

const PATHS_WITH_TWO_IFRAMES = [];

const MAX_IFRAMES_PER_PAGE = 2;

function checkIfPathContainsIframe(index, path) {
  if (index <= 1) {
    return PATHS_WITH_ONE_IFRAME.includes(path);
  }
  if (index <= 2) {
    return PATHS_WITH_TWO_IFRAMES.includes(path);
  }
}

function RootIframeComponent() {
  const [iframesHaveLoaded, setIframesHaveLoaded] = useState(false);

  useEffect(() => {
    setIframesHaveLoaded(true);
  });

  function currentPathContainsIframe(index) {
    if (!ExecutionEnvironment.canUseDOM) {
      return true;
    }
    checkIfPathContainsIframe(index, window.location.pathname);
  }

  return (
    <>
      {iframesHaveLoaded
        ? null
        : Array.from({ length: MAX_IFRAMES_PER_PAGE }).map((_, index) => {
            return currentPathContainsIframe(index + 1) ? null : (
              <Iframe
                key={index + 1}
                id={`iframe-${index + 1}`}
                code={DEFAULT_APP_CODE}
                requirements={[
                  "/pyarrow/pyarrow-17.0.0-cp312-cp312-pyodide_2024_0_wasm32.whl",
                  "micropip",
                  "pyodide-unix-timezones", // needed by pyarrow
                  "geopandas",
                  "requests",
                  "xarray",
                  "yarl",
                  // Commonly used in product:
                  "pydeck",
                ]}
                visible={false}
              />
            );
          })}
    </>
  );
}

export default function Root({ children }) {
  return (
    <>
      {children}
      <BrowserOnly>
        {() => {
          return <RootIframeComponent />;
        }}
      </BrowserOnly>
    </>
  );
}
