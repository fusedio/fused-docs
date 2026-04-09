import React, { useEffect, useRef } from "react";

/**
 * Wrapper around <iframe> that prevents the browser from scrolling the
 * parent page to the iframe when the embedded content loads and steals focus.
 */
export default function CanvasIframe({ src, width = "100%", height = "500px", style, title, ...rest }) {
  const iframeRef = useRef(null);

  useEffect(() => {
    const iframe = iframeRef.current;
    if (!iframe) return;

    // Capture scroll position before the iframe can steal it
    const scrollX = window.scrollX;
    const scrollY = window.scrollY;

    const handleLoad = () => {
      // Restore scroll position in the next frame to override any browser auto-scroll
      requestAnimationFrame(() => {
        window.scrollTo(scrollX, scrollY);
      });
    };

    iframe.addEventListener("load", handleLoad);
    return () => iframe.removeEventListener("load", handleLoad);
  }, [src]);

  return (
    <iframe
      ref={iframeRef}
      src={src}
      width={width}
      height={height}
      style={style}
      title={title || src}
      {...rest}
    />
  );
}
