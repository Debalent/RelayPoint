// frontend/src/App.jsx

import React from 'react'
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom'
import ThemeToggle from './components/ThemeToggle'     // Enables user personalization (light/dark mode)
import Logo from './components/Logo'                   // Auto-switches branding assets based on theme
import LoginForm from './components/LoginForm'         // Entry point for authentication flow
import Dashboard from './components/Dashboard'         // Protected route for authenticated users
import useAuth from './hooks/useAuth'                  // Custom hook for managing auth state
import './index.css'                                   // Tailwind CSS integration for responsive theming

export default function App() {
  const { isAuthenticated } = useAuth()                // Checks if user has valid session token

  return (
    <Router>
      <div className="min-h-screen bg-white dark:bg-gray-900 transition-colors">
        <header className="flex items-center justify-between p-4">
          <Logo className="h-12 w-auto" />             {/* Brand visibility and theme responsiveness */}
          <ThemeToggle />                              {/* UX enhancement: user-controlled theming */}
        </header>

        <main className="p-4">
          <Routes>
            <Route path="/login" element={<LoginForm />} />
            <Route
              path="/dashboard"
              element={
                isAuthenticated ? <Dashboard /> : <Navigate to="/login" replace />
              }
            />
            <Route path="*" element={<Navigate to="/login" replace />} />
          </Routes>
        </main>
      </div>
    </Router>
  )
}
