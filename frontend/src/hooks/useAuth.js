// frontend/src/hooks/useAuth.js

import { useState, useEffect } from "react"

/**
 * Custom hook for managing authentication state across the app.
 * Centralizes token logic for login persistence, logout handling, and access control.
 * Scalable for future role-based permissions, session expiry checks, and multi-user support.
 */
export default function useAuth() {
  const [token, setToken] = useState(null)

  // On initial load, check if token exists in localStorage
  useEffect(() => {
    const storedToken = localStorage.getItem("access_token")
    if (storedToken) setToken(storedToken)
  }, [])

  // Save token to localStorage and update state
  const login = (newToken) => {
    localStorage.setItem("access_token", newToken)
    setToken(newToken)
  }

  // Clear token from localStorage and reset state
  const logout = () => {
    localStorage.removeItem("access_token")
    setToken(null)
  }

  return {
    token,               // Raw token value for API requests
    login,               // Function to initiate session
    logout,              // Function to terminate session
    isAuthenticated: !!token // Boolean flag for route protection
  }
}
