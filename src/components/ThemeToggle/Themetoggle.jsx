import React from 'react';
import { useTheme } from '../../hooks/useTheme';

/**
 * Sliding sun ↔ moon toggle component.
 * Investors appreciate: branded UI, a11y support, and smooth animation show polish.
 */
export default function ThemeToggle() {
  const [theme, setTheme] = useTheme();      // get current theme and setter
  const dark = theme === 'dark';             // boolean flag for dark mode

  return (
    <button
      aria-label="Toggle light and dark mode"
      role="switch"
      aria-checked={dark}                    // accessibility: communicates state
      onClick={() => setTheme(dark ? 'light' : 'dark')}  // flip theme on click
      className="
        relative
        w-14 h-8
        flex items-center
        bg-gray-300 dark:bg-gray-600         // background adapts to theme
        rounded-full
        p-1
        transition-colors duration-300
        focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500
      "
    >
      {/* Sliding knob */}
      <div
        className={`
          bg-white
          w-6 h-6
          rounded-full
          shadow-md
          transform transition-transform duration-300
          ${dark ? 'translate-x-6' : 'translate-x-0'}
        `}
      />

      {/* Sun icon (left) */}
      <div className="pointer-events-none absolute left-1 text-yellow-400 opacity-80">
        {!dark ? '☀️' : ''}
      </div>

      {/* Moon icon (right) */}
      <div className="pointer-events-none absolute right-1 text-indigo-200 opacity-80">
        {dark ? '🌙' : ''}
      </div>
    </button>
  );
}
