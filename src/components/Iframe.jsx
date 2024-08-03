import React, { useEffect, useRef } from "react";
import { DEFAULT_APP_REQUIREMENTS } from "../app-iframe/requirements";

const URL = "https://staging.fused.io/workbench#app/s/aH4sIAAAAAAAAAw3JMQoCMRAF0KuEqRSWPUBKCy9gaSyG5C8EkkmcmRQi3t0tH%2B9LeRRQpNrnUA%2FmCu6temA7kSSJ%2BV7lGJdENzYEnjO0wQUl2MoZZsdq7bMnutJGiveqig5xo%2Fh8bVTtfv4jKyAUXRd%2Bf156J2R1AAAA";

export default function Iframe({
  id = "iframe-1",
  code,
  url = URL,
  requirements = DEFAULT_APP_REQUIREMENTS, // Hardcode common requirements, unless specified otherwise
  visible = true,
  mainPage = false,
}) {
  const containerRef = useRef(null);

  function syncIframeToContainer(boundingClientRect, iframe) {
    iframe.style.display = "block";
    iframe.style.left = `${boundingClientRect.left + window.scrollX}px`;
    iframe.style.top = `${boundingClientRect.top + window.scrollY}px`;
    iframe.style.width = `${boundingClientRect.width}px`;
    iframe.style.height = `${boundingClientRect.height}px`;
  }

  useEffect(() => {
    let iframe = null;
    let resizeObserver = null;
    let intersectionObserver = null;
    if (!document.getElementById("magic-iframe-" + id)) {
      iframe = document.createElement("iframe");
      iframe.src = url;
      iframe.height = "1050px";
      iframe.width = "100%";
      iframe.scrolling = "no";
      iframe.id = "magic-iframe-" + id;
      document.body.appendChild(iframe);
    } else {
      iframe = document.getElementById("magic-iframe-" + id);
    }

    iframe.style.position = "absolute";

    function sendMessage() {
      iframe.contentWindow.postMessage(
        {
          appRunner: {
            code,
            enabled: true,
            requirements,
          },
        },
        "*"
      );
    }

    function sendMessageWhenReady(event) {
      if (event.data === "appRunnerListener:ready") {
        sendMessage();
      }
    }
    if (!mainPage) {
      sendMessage();

      window.addEventListener("message", sendMessageWhenReady);
    }

    if (visible) {
      const boundingClientRect = containerRef.current.getBoundingClientRect();
      iframe.style.display = "block";
      syncIframeToContainer(boundingClientRect, iframe);

      intersectionObserver = new IntersectionObserver((entries) => {
        for (const entry of entries) {
          if (entry.isIntersecting) {
            const iframe = document.getElementById("magic-iframe-" + id);
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
            const iframe = document.getElementById("magic-iframe-" + id);
            if (iframe) {
              const boundingClientRect =
                containerRef.current.getBoundingClientRect();
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
        const iframe = document.getElementById("magic-iframe-" + id);
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
      if (!mainPage) {
        window.removeEventListener("message", sendMessageWhenReady);
      }
    };
  }, []);

  return (
    <div
      display={visible ? "block" : "none"}
      ref={containerRef}
      style={{
        width: "100%",
        height: "1050px",
      }}
    />
  );
}
