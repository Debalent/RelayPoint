// frontend/src/App.jsx

import React from 'react'
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom'
import ThemeToggle from './components/ThemeToggle'
import Logo from './components/Logo'
import LoginForm from './components/LoginForm'
import Dashboard from './components/Dashboard' // You’ll create this next
import useAuth from './hooks/useAuth'
import './index.css' // Tailwind styles

export default function App() {
  const { isAuthenticated } = useAuth()

  return (
    <Router>
      <div className="min-h-screen bg-white dark:bg-gray-900 transition-colors">
        <header className="flex items-center justify-between p-4">
          <Logo className="h-12 w-auto" />
          <ThemeToggle />
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
