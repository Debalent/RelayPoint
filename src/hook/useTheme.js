import { useState, useEffect } from 'react';

// Key under which we persist user choice in localStorage
const THEME_KEY = 'themePreference';

/**
 * Custom React hook to initialize, persist, and apply light/dark theme.
 * Investors care: clean separation of concerns, easy to extend (e.g. add new palettes).
 */
export function useTheme() {
  // Initialize state from localStorage or OS preference
  const [theme, setTheme] = useState(() => {
    const stored = localStorage.getItem(THEME_KEY);
    if (stored) {
      // If user has chosen before, use that
      return stored;
    }
    // Otherwise, fallback to system color scheme
    return (
      window.matchMedia &&
      window.matchMedia('(prefers-color-scheme: dark)').matches
    )
      ? 'dark'
      : 'light';
  });

  // Side-effect: apply the theme class and persist choice
  useEffect(() => {
    const root = document.documentElement;         // target the <html> element
    if (theme === 'dark') {
      root.classList.add('dark');                  // tells Tailwind to switch to dark mode
    } else {
      root.classList.remove('dark');               // revert to light mode
    }
    localStorage.setItem(THEME_KEY, theme);        // persist for future visits
  }, [theme]);

  // Return current theme and setter so components can toggle
  return [theme, setTheme];
}
