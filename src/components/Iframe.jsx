import React, { useEffect, useRef } from "react";
import {DEFAULT_APP_REQUIREMENTS} from '../app-iframe/requirements'

const URL = "https://staging.fused.io/workbench#app/s/aH4sIAAAAAAAAA1XQPW%2FEIAwG4L9iMd1JUbJnrk7q3G5NB4c4iVW%2Bik3UU9X%2FXpIsd%2BAFeA2P%2BDU2TmR6wz7FrCCaCb1jBZS6GMIQRFsOc7wM5pgB6nhfWaAW%2FSTK7CkouhZeZ9D9wJMILgSYEmGWBpIjFIIlgtZaCaZoBRyGicMCac9erGP7BTEc57ciNIGLtQPHuNF13w0QcOMFlWDEmj3uqs%2Ft%2Fe3pOo3XAy3F2gp5ch9CgpTj6MhDxQuLPghJgSshFrvCxviAeWGxMU9go%2FclsN57WFWT9F03srbu3s17bjpjTxzTmEzfhTPtPyWm%2F%2FhsDMutOPdmM1EwveZCf%2F%2Bx8TCDjQEAAA%3D%3D"

// Hardcode common requirements, unless specified otherwise
export default function Iframe({ id, code, url=URL, requirements=DEFAULT_APP_REQUIREMENTS }) {
  const containerRef = useRef(null);

  function syncIframeToContainer(boundingClientRect, iframe) {
    iframe.style.left = `${boundingClientRect.left + window.scrollX}px`;
    iframe.style.top = `${boundingClientRect.top + window.scrollY}px`;
    iframe.style.width = `${boundingClientRect.width}px`;
    iframe.style.height = `${boundingClientRect.height}px`;
  }

  useEffect(() => {
    let iframe = null;
    if (!document.getElementById("magic-iframe")) {
      iframe = document.createElement("iframe");
      iframe.src = url;
      iframe.height = "1050px";
      iframe.width = "100%";
      iframe.scrolling = "no";
      iframe.id = "magic-iframe";
      document.body.appendChild(iframe);
    } else {
      iframe = document.getElementById("magic-iframe");
    }

    iframe.contentWindow.postMessage(
      {
        appRunner: {
          code,
          enabled: true,
          requirements,
        },
      },
      url
    );

    const boundingClientRect = containerRef.current.getBoundingClientRect();
    iframe.style.position = "absolute";
    iframe.style.display = "block";
    syncIframeToContainer(boundingClientRect, iframe);

    const intersectionObserver = new IntersectionObserver((entries) => {
      for (const entry of entries) {
        if (entry.isIntersecting) {
          const iframe = document.getElementById("magic-iframe");
          if (iframe) {
            const boundingClientRect = entry.boundingClientRect;
            syncIframeToContainer(boundingClientRect, iframe);
          }
        }
      }
    });

    intersectionObserver.observe(containerRef.current);

    const resizeObserver = new ResizeObserver((entries) => {
      for (const entry of entries) {
        if (entry.contentBoxSize) {
          const iframe = document.getElementById("magic-iframe");
          if (iframe) {
            const boundingClientRect =
              containerRef.current.getBoundingClientRect();
            syncIframeToContainer(boundingClientRect, iframe);
          }
        }
      }
    });

    resizeObserver.observe(containerRef.current);

    return () => {
      const iframe = document.getElementById("magic-iframe");
      if (iframe) {
        iframe.style.left = "-10000px";
        iframe.style.top = "-10000px";
        iframe.style.width = "0px";
        iframe.style.height = "0px";
        iframe.style.display = "none";
      }
      resizeObserver.disconnect();
      intersectionObserver.disconnect();
    };
  }, []);

  return (
    <div
      ref={containerRef}
      style={{
        width: "100%",
        height: "1050px",
      }}
    />
  );
}
