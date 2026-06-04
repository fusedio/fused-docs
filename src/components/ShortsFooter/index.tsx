import React, { useEffect, useRef } from "react";
import styles from "./styles.module.css";

const BEEHIIV_FORM_ID = "4d460bb7-ac79-4cef-a7ee-c014bc5f62eb";

const SHOW_NEWSLETTER = true;
const SHOW_CONNECT_AGENT = false;

function BeehiivForm(): JSX.Element {
  const containerRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const container = containerRef.current;
    if (!container) return;
    const script = document.createElement("script");
    script.src = "https://subscribe-forms.beehiiv.com/v3/loader.js";
    script.async = true;
    script.setAttribute("data-beehiiv-form", BEEHIIV_FORM_ID);
    container.appendChild(script);
    return () => { container.innerHTML = ""; };
  }, []);

  return <div ref={containerRef} className={styles.beehiivEmbed} />;
}

export default function ShortsFooter(): JSX.Element {
  return (
    <div className={styles.footer}>
      <hr className={styles.divider} />

      {SHOW_NEWSLETTER && (
        <div className={styles.subscribeSection}>
          <h3 className={styles.subscribeHeading}>Get new shorts in your inbox</h3>
          <p className={styles.subscribeSubtext}>
            Short posts on building Fused without writing a single line of code.
          </p>
          <BeehiivForm />
        </div>
      )}

      {SHOW_CONNECT_AGENT && (
        <div className={styles.connectSection}>
          <h4 className={styles.connectHeading}>Connect your agent</h4>
          <div className={styles.cards}>
            <div className={`${styles.card} ${styles.cardDisabled}`}>
              <div className={styles.cardLabel}>
                Fused skill{" "}
                <span className={styles.comingSoon}>coming soon</span>
              </div>
              <div className={styles.cardDesc}>
                Install in Claude to get latest shorts in agent context
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
