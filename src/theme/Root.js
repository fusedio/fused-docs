import React, { useEffect } from "react";
import Iframe from "@site/src/components/Iframe";
import DEFAULT_APP_CODE from "@site/src/app-iframe/python/default.py";

// Swizzling (wrapping) the Root component since it never unmounts
// This wrapper mounts MAX_IFRAMES_PER_PAGE iframes on the page
// so that when we go to a page with visible iframes, it's already loaded
// Modify MAX_IFRAMES_PER_PAGE to the number of iframes that need to be preloaded

const PATHS_WITH_ONE_IFRAME = [
  "/basics/usecases/buffer/",
  "/basics/usecases/point-polygon/",
  "/basics/usecases/raster_to_h3/",
  "/basics/usecases/zonal_stats/",
];

const PATHS_WITH_TWO_IFRAMES = [];

const MAX_IFRAMES_PER_PAGE = 2;

export default function Root({ children }) {
  const [iframesHaveLoaded, setIframesHaveLoaded] = React.useState(false);

  useEffect(() => {
    setIframesHaveLoaded(true);
  });

  function currentPathContainsIframe(index) {
    if (index <= 1) {
      console.log("message secret ", PATHS_WITH_ONE_IFRAME.includes(window.location.pathname));
      return PATHS_WITH_ONE_IFRAME.includes(window.location.pathname);
    }
    if (index <= 2) {
      return PATHS_WITH_TWO_IFRAMES.includes(window.location.pathname);
    }
  }

  return (
    <>
      {children}
      {iframesHaveLoaded
        ? null
        : Array.from({ length: MAX_IFRAMES_PER_PAGE }).map((_, index) => {
            return currentPathContainsIframe(index + 1) ? null : (
              <Iframe
                key={index + 1}
                url={`https://staging.fused.io/workbench#app/s/aH4sIAAAAAAAAA21S246cMAz9lShP0DIUmKqVkJB600p9bt82K5QlnpmowaRJ6Axd7b%2FX4bIzUjdcbB8f28mBJ94NCnjNdW8HF9gRBitRSc%2FoPlolcE3g2NspgmhfsCvzhuiDA9kbHSLug8B4ffIh72R3glbJIAUqODAzSDWHCaa1QEZLHVhDvfJvhN452UOy4HE9Xd24BG3clILXzGgfEifxCElVpCl7w%2Fb0YPYKv4p8tDmx1dDPBpMPRaSnr%2FH3kX8v%2BGfBH4hUzUz2NkJf%2Foe%2B3kI37Z4XN12MgzA6pKMuypCuj%2BDo2BpDQiotcavRjiER%2FDt6IFElW3DBM9ZrbP9IM0JTZiQw2KZMqTfVnp0OJBn%2FeQLWjc4BhrWOac9i7RIRuztJF2b1afTNl9jyc79H6dqZmFzpGbs0m%2FYZm5pN14yRHVyz6UY9eMYd%2FB61g5524nl9z9%2FZSTo3nDe7Kz%2FmRV7sOrsvq%2FVtp0FpBW1VVO%2Fboj1L3%2B%2Br%2FHwy1G%2FN7UbUl13QPfwdEDwlXv7bdSj4EN0LTZETOTRuqVfQ%2FeIPGdf%2BbjTmR%2BcAkNcHaTw8%2FwM9w7JgDQMAAA%3D%3D`}
                id={`iframe-${index + 1}`}
                code={DEFAULT_APP_CODE}
                visible={false}
                mainPage={true} // i added two props here for testing
              />
            );
          })}
    </>
  );
}
