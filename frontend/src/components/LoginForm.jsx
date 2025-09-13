// frontend/src/components/LoginForm.jsx

import { useState } from "react"
import useAuth from "../hooks/useAuth"

/**
 * LoginForm component handles user authentication via FastAPI backend.
 * Captures credentials, sends POST request, and stores access token on success.
 * Designed for extensibility—can support MFA, error analytics, and branded flows.
 */
export default function LoginForm() {
  const [email, setEmail] = useState("")
  const [password, setPassword] = useState("")
  const [error, setError] = useState("")
  const { login } = useAuth()

  const handleLogin = async (e) => {
    e.preventDefault()
    setError("")

    try {
      const response = await fetch("http://localhost:8000/api/v1/auth/login", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email, password }),
      })

      const data = await response.json()

      if (!response.ok) {
        throw new Error(data.detail || "Login failed")
      }

      login(data.access_token) // Store token for session persistence
    } catch (err) {
      setError(err.message)
    }
  }

  return (
    <form onSubmit={handleLogin} className="max-w-md mx-auto p-4 bg-white dark:bg-gray-900 rounded shadow">
      <h2 className="text-xl font-semibold mb-4 text-gray-900 dark:text-white">Login</h2>

      <input
        type="email"
        placeholder="Email"
        value={email}
        onChange={(e) => setEmail(e.target.value)}
        className="w-full mb-2 p-2 border rounded dark:bg-gray-800 dark:text-white"
        required
      />

      <input
        type="password"
        placeholder="Password"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
        className="w-full mb-2 p-2 border rounded dark:bg-gray-800 dark:text-white"
        required
      />

      {error && <p className="text-red-500 mb-2">{error}</p>}

      <button
        type="submit"
        className="w-full bg-blue-600 text-white py-2 rounded hover:bg-blue-700"
      >
        Log In
      </button>
    </form>
  )
}
