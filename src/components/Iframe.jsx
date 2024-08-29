import React, { useEffect, useRef } from "react";
import { DEFAULT_APP_REQUIREMENTS } from "../app-iframe/requirements";
import { gzip } from "pako";
import { u8aToBase64 } from "../../utils/buffer";

const URL_PREFIX = "https://staging.fused.io/workbench#app/s/a";
const APP_SHARE_PREFIX = "#app/s/a";

export default function Iframe({
  id = "iframe-1",
  code,
  url = URL_PREFIX,
  requirements = DEFAULT_APP_REQUIREMENTS, // Hardcode common requirements, unless specified otherwise
  visible = true,
  height = "500px",
  useResizer = true, // set to false to work around nodes causing this to move around after the effect runs
}) {
  const containerRef = useRef(null);

  function syncIframeToContainer(boundingClientRect, iframe) {
    iframe.style.display = "block";
    iframe.style.left = `${boundingClientRect.left + window.scrollX}px`;
    iframe.style.top = `${boundingClientRect.top + window.scrollY}px`;
    iframe.style.width = `${boundingClientRect.width}px`;
    iframe.style.height = `${boundingClientRect.height}px`;
  }

  function createIframeDefaultUrl() {
    // build url hash with code and requirements
    const newUrl = new URL(url);
    const payload = JSON.stringify({
      code: code,
      requirements: requirements,
      isFullScreen: true,
    });
    // Note: for very small strings (say <= 500 bytes), it will be less efficient to gzip them
    const gzipped = gzip(payload);
    const base64 = u8aToBase64(gzipped);

    newUrl.hash = `${APP_SHARE_PREFIX}${encodeURIComponent(base64)}`;
    return newUrl.toString();
  }

  useEffect(() => {
    if (!useResizer) {
      return;
    }

    let iframe = null;
    let resizeObserver = null;
    let intersectionObserver = null;
    if (!document.getElementById("magic-" + id)) {
      // end build url hash with code and requirements
      iframe = document.createElement("iframe");
      iframe.src = createIframeDefaultUrl();
      iframe.height = height;
      iframe.width = "100%";
      iframe.scrolling = "no";
      iframe.id = "magic-" + id;

      document.body.appendChild(iframe);
    } else {
      iframe = document.getElementById("magic-" + id);
      const targetOrigin = new URL(url).origin;
      function sendMessage() {
        iframe.contentWindow.postMessage(
          {
            appRunner: {
              code,
              enabled: true,
              requirements,
            },
          },
          targetOrigin
        );
      }
      if (visible) {
        sendMessage();
      }
    }

    iframe.style.position = "absolute";

    if (visible) {
      const boundingClientRect = containerRef.current?.getBoundingClientRect();
      iframe.style.display = "block";
      syncIframeToContainer(boundingClientRect, iframe);

      intersectionObserver = new IntersectionObserver((entries) => {
        for (const entry of entries) {
          if (entry.isIntersecting) {
            const iframe = document.getElementById("magic-" + id);
            if (iframe) {
              const boundingClientRect = entry.boundingClientRect;
              syncIframeToContainer(boundingClientRect, iframe);
            }
          }
        }
      });

      intersectionObserver.observe(containerRef.current);

      resizeObserver = new ResizeObserver((entries) => {
        for (const entry of entries) {
          if (entry.contentBoxSize) {
            const iframe = document.getElementById("magic-" + id);
            if (iframe) {
              const boundingClientRect =
                containerRef?.current?.getBoundingClientRect();
              syncIframeToContainer(boundingClientRect, iframe);
            }
          }
        }
      });

      resizeObserver.observe(containerRef.current);
    } else {
      iframe.style.left = "-10000px";
      iframe.style.top = "-10000px";
      iframe.style.width = "0px";
      iframe.style.height = "0px";
      iframe.style.display = "none";
    }

    return () => {
      if (visible) {
        const iframe = document.getElementById("magic-" + id);

        if (iframe) {
          iframe.style.left = "-10000px";
          iframe.style.top = "-10000px";
          iframe.style.width = "0px";
          iframe.style.height = "0px";
          iframe.style.display = "none";
        }

        resizeObserver.disconnect();
        intersectionObserver.disconnect();
      }
    };
  }, [useResizer]);

  const defaultIframe = useResizer ? undefined : <iframe
    src={createIframeDefaultUrl()}
    height={height}
    width={"100%"}
    scrolling={"no"}
  />;

  return (
    <div
      display={visible ? "block" : "none"}
      ref={containerRef}
      style={{
        width: "100%",
        height,
      }}
    >{defaultIframe}</div>
  );
}
