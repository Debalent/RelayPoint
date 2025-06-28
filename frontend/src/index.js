// frontend/src/index.js

import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App'
import './index.css'        // Tailwind base + utilities
import reportWebVitals from './reportWebVitals'

// --- Theme init: apply saved/system preference before React mounts ---
;(function () {
  const THEME_KEY = 'themePreference'
  const root = document.documentElement

  // 1. Check localStorage
  const saved = localStorage.getItem(THEME_KEY)
  if (saved === 'dark') {
    root.classList.add('dark')
  } else if (saved === 'light') {
    root.classList.remove('dark')
  } else {
    // 2. Fallback to system preference
    const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches
    root.classList.toggle('dark', prefersDark)
  }
})()

// --- React entrypoint ---
const root = ReactDOM.createRoot(document.getElementById('root'))
root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
)

// (Optional) performance tracking
reportWebVitals()
