import React, { useEffect, useRef } from "react";
import { DEFAULT_APP_REQUIREMENTS } from "../app-iframe/requirements";
import { gzip } from "pako";
import { u8aToBase64 } from "../../utils/buffer";
import { useMemo } from 'react';


const URL_PREFIX = "https://www.fused.io/workbench/apps#app/s/a";
const APP_SHARE_PREFIX = "#app/s/a";
const SEND_EXTRA_TIMES = 10;

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
    if (boundingClientRect) {
      iframe.style.display = "block";
      iframe.style.position = "relative";
      iframe.style.left = "0";
      iframe.style.top = "0";
      iframe.style.width = "100%";
      iframe.style.height = "100%";
    }
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
      iframe.style.position = "relative";

      containerRef.current.appendChild(iframe);
    } else {
      iframe = document.getElementById("magic-" + id);
      const targetOrigin = new URL(url).origin;
      const nonce = `docs-${Math.random()}`;
      function sendMessage() {
        iframe.contentWindow.postMessage(
          {
            appRunner: {
              code,
              enabled: true,
              requirements,
              nonce,
            },
          },
          targetOrigin,
        );
      }

      if (visible) {
        sendMessage();

        for (let i = 0; i < SEND_EXTRA_TIMES; i++) {
          setTimeout(sendMessage, 1000 * i);
        }
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

  const defaultIframe = useResizer
    ? undefined
    : useMemo(() => {
        return (
          <iframe
            src={createIframeDefaultUrl()}
            height={height}
            width={"100%"}
            scrolling={"no"}
          />
        );
      }, [height]);

  return (
    <div
      display={visible ? "block" : "none"}
      ref={containerRef}
      style={{
        width: "100%",
        height,
      }}
    >
      {defaultIframe}
    </div>
  );
}
