import React from "react";
import styles from "./styles.module.css";

// Set to true to show sections when ready
const SHOW_NEWSLETTER = false;
const SHOW_CONNECT_AGENT = false;

export default function ShortsFooter(): JSX.Element {
  return (
    <div className={styles.footer}>
      <hr className={styles.divider} />

      {SHOW_NEWSLETTER && (
        <div className={styles.subscribeSection}>
          <h3 className={styles.subscribeHeading}>Get new shorts in your inbox</h3>
          <p className={styles.subscribeSubtext}>
            Short dispatches from Fused as we build toward zero-code data workflows.
          </p>
          {/* BEEHIIV_EMBED_HERE */}
          <div className={styles.embedPlaceholder}>
            Newsletter embed — paste Beehiiv code here
          </div>
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
