// frontend/src/App.jsx
import React from 'react'
import ThemeToggle from './components/ThemeToggle'
import Logo from './components/Logo'
import './index.css'    // make sure Tailwind styles are loaded

export default function App() {
  return (
    <div className="min-h-screen bg-white dark:bg-gray-900 transition-colors">
      <header className="flex items-center justify-between p-4">
        <Logo className="h-12 w-auto" />
        <ThemeToggle />
      </header>
      <main className="p-4">
        {/* Your routed pages or content go here */}
      </main>
    </div>
  )
}
