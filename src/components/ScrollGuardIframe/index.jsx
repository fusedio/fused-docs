import React, { useRef, useState } from "react";
import styles from "./styles.module.css";

const VIDEO_HOSTS = /(^|\.)(youtube\.com|youtube-nocookie\.com|youtu\.be|loom\.com|vimeo\.com)$/;

function isVideo(src) {
  try {
    return VIDEO_HOSTS.test(new URL(src).hostname);
  } catch {
    return false;
  }
}

export function ClickToInteract({ onActivate }) {
  const [active, setActive] = useState(false);

  if (active) {
    return null;
  }

  return (
    <button
      type="button"
      className={styles.overlay}
      aria-label="Click to interact with the embedded content"
      onClick={() => {
        setActive(true);
        onActivate?.();
      }}
    >
      <span className={styles.hint}>Click to interact</span>
    </button>
  );
}

export default function ScrollGuardIframe({ style, ...props }) {
  const iframeRef = useRef(null);

  if (isVideo(props.src)) {
    return <iframe style={style} {...props} />;
  }

  const { margin, marginTop, marginBottom, maxWidth, ...iframeStyle } = style || {};

  return (
    <div
      className={styles.wrapper}
      style={{ margin, marginTop, marginBottom, maxWidth, borderRadius: iframeStyle.borderRadius }}
    >
      <iframe ref={iframeRef} style={{ ...iframeStyle, display: "block" }} {...props} />
      <ClickToInteract onActivate={() => iframeRef.current?.focus()} />
    </div>
  );
}
