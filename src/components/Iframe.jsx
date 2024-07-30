import React, { useEffect, useRef } from "react";

export default function Iframe({ id, url, code, requirements }) {
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

    // intersection observer
    const intersectionObserver = new IntersectionObserver((entries) => {
      for (const entry of entries) {
        console.log("intersection observer entry", entry);
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
