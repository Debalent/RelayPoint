// frontend/src/components/onboarding/ArtistLiteOnboarding.jsx

import { useNavigate } from "react-router-dom"
import { useEffect } from "react"

export default function ArtistLiteOnboarding() {
  const navigate = useNavigate()

  /**
   * Artist Lite onboarding flow for Free-tier users.
   * Strategic Role:
   * - Accelerates activation with role-specific guidance.
   * - Plants upgrade nudges for Pro-tier features.
   * - Scalable for branded onboarding and trial conversion.
   */
  useEffect(() => {
    // Optional: log onboarding start event
  }, [])

  const handleContinue = () => {
    navigate("/dashboard")
  }

  return (
    <div className="max-w-3xl mx-auto p-6 bg-white dark:bg-gray-900 rounded shadow">
      <h1 className="text-2xl font-bold mb-4 text-gray-900 dark:text-white">Welcome, Artist 🎨</h1>
      <p className="text-gray-700 dark:text-gray-300 mb-6">
        You’re on the Free tier, which gives you access to basic workflow tools and limited collaboration.
        Upgrade to Pro anytime to unlock advanced analytics, media sync, and multi-role routing.
      </p>

      <ul className="list-disc pl-6 text-gray-700 dark:text-gray-300 mb-6">
        <li>Create up to 3 workflows</li>
        <li>Invite 1 collaborator per workflow</li>
        <li>Access basic dashboard and audit logs</li>
      </ul>

      <button
        onClick={handleContinue}
        className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700"
      >
        Continue to Dashboard
      </button>

      <div className="mt-6 text-sm text-gray-500 dark:text-gray-400">
        Want more power?{" "}
        <a href="/upgrade" className="text-blue-600 hover:underline">
          Upgrade to Pro
        </a>{" "}
        for full access.
      </div>
    </div>
  )
}
