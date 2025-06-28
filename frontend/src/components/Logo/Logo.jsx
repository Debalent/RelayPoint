import React from 'react';
import { useTheme } from '../../hooks/useTheme';
// Import both versions of the logo
import lightLogo from '../../assets/relaypoint-logo-light.png';
import darkLogo from '../../assets/relaypoint-logo-dark.png';

/**
 * Logo component that switches
 * between light & dark assets based on theme.
 * Placed in header/navigation so it shows on every tab.
 */
export default function Logo({ className = 'h-10 w-auto' }) {
  const [theme] = useTheme();
  const isDark = theme === 'dark';

  return (
    <img
      src={isDark ? darkLogo : lightLogo}      // choose appropriate asset
      alt="RelayPoint Logo"
      className={className}                     // allow sizing via props
      loading="eager"                           // ensure logo loads immediately
    />
  );
}
