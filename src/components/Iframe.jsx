import React, { useEffect, useRef } from "react";

export default function Iframe({ id, url }) {
  const containerRef = useRef(null);

  useEffect(() => {
    let iframe = null;
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

    const boundingClientRect = containerRef.current.getBoundingClientRect();
    iframe.style.position = "absolute";
    iframe.style.left = `${boundingClientRect.left + window.scrollX}px`;
    iframe.style.top = `${boundingClientRect.top + window.scrollY}px`;
    iframe.style.width = `${boundingClientRect.width}px`;
    iframe.style.height = `${boundingClientRect.height}px`;
    iframe.style.display = "block";

    // const resizeObserver = new ResizeObserver((entries) => {
    //   for (const entry of entries) {
    //     if (entry.contentBoxSize) {
    //       const iframe = document.getElementById("magic-iframe-" + id);
    //       if (iframe) {
    //         const boundingClientRect =
    //           containerRef.current.getBoundingClientRect();
    //         iframe.style.left = `${boundingClientRect.left + window.scrollX}px`;
    //         iframe.style.top = `${boundingClientRect.top + window.scrollY}px`;
    //         iframe.style.width = `${entry.contentRect.width}px`;
    //         iframe.style.height = `${entry.contentRect.height}px`;
    //       }
    //     }
    //   }
    // });

    // resizeObserver.observe(containerRef.current);

    return () => {
      const iframe = document.getElementById("magic-iframe-" + id);
      if (iframe) {
        iframe.style.left = "-10000px";
        iframe.style.top = "-10000px";
        iframe.style.width = "0px";
        iframe.style.height = "0px";
        iframe.style.display = "none";
      }
      // resizeObserver.disconnect();
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
