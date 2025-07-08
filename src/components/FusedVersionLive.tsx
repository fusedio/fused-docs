import React, { useState, useEffect } from 'react';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';

export default function FusedVersionLive(): JSX.Element {
  const { siteConfig } = useDocusaurusContext();
  const fallbackVersion = siteConfig.customFields?.fusedPyVersion as string;
  const [version, setVersion] = useState<string>(fallbackVersion || '1.20.1');
  const [loading, setLoading] = useState<boolean>(true);

  useEffect(() => {
    async function fetchVersion() {
      try {
        const response = await fetch('https://pypi.org/pypi/fused/json');
        const data = await response.json();
        setVersion(data.info.version);
      } catch (error) {
        console.warn('Failed to fetch version from PyPI, using fallback:', error);
        // Keep the fallback version
      } finally {
        setLoading(false);
      }
    }

    fetchVersion();
  }, []);

  if (loading) {
    return <span>{fallbackVersion || '1.20.1'}</span>;
  }

  return <span>{version}</span>;
} 