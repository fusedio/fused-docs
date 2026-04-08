import React, { useCallback, useEffect, useState } from "react";
import styles from "./ClickZoomImage.module.css";

type Props = {
  src: string;
  alt: string;
  className?: string;
};

function MagnifyIcon(): React.ReactElement {
  return (
    <svg
      className={styles.magnifySvg}
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      strokeWidth="2"
      strokeLinecap="round"
      strokeLinejoin="round"
      aria-hidden
    >
      <circle cx="11" cy="11" r="8" />
      <path d="m21 21-4.35-4.35" />
    </svg>
  );
}

/**
 * Inline image that opens a full-screen overlay on click (click backdrop or Escape to close).
 */
export default function ClickZoomImage({ src, alt, className }: Props): React.ReactElement {
  const [open, setOpen] = useState(false);

  const close = useCallback(() => setOpen(false), []);

  useEffect(() => {
    if (!open) return;
    const onKey = (e: KeyboardEvent) => {
      if (e.key === "Escape") close();
    };
    document.addEventListener("keydown", onKey);
    const prev = document.body.style.overflow;
    document.body.style.overflow = "hidden";
    return () => {
      document.removeEventListener("keydown", onKey);
      document.body.style.overflow = prev;
    };
  }, [open, close]);

  return (
    <>
      <button
        type="button"
        className={`${styles.thumb} ${className ?? ""}`}
        onClick={() => setOpen(true)}
        aria-haspopup="dialog"
        aria-expanded={open}
        aria-label={`Enlarge image: ${alt}`}
      >
        <span className={styles.thumbInner}>
          <img src={src} alt={alt} className={styles.thumbImg} />
          <span className={styles.zoomHint} aria-hidden="true">
            <MagnifyIcon />
          </span>
        </span>
      </button>
      {open ? (
        <div
          className={styles.overlay}
          role="dialog"
          aria-modal="true"
          aria-label={alt}
          onClick={close}
        >
          <img
            src={src}
            alt=""
            className={styles.full}
            onClick={(e) => e.stopPropagation()}
          />
        </div>
      ) : null}
    </>
  );
}
