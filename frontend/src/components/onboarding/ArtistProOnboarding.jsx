// frontend/src/components/onboarding/ArtistProOnboarding.jsx

import { useNavigate } from "react-router-dom"
import { useEffect } from "react"

export default function ArtistProOnboarding() {
  const navigate = useNavigate()

  /**
   * Artist Pro onboarding flow for premium-tier users.
   * Strategic Role:
   * - Unlocks advanced features and collaboration tools.
   * - Reinforces value of Pro-tier investment.
   * - Scalable for branded onboarding and media-rich environments.
   */
  useEffect(() => {
    // Optional: log onboarding start event
  }, [])

  const handleContinue = () => {
    navigate("/dashboard")
  }

  return (
    <div className="max-w-3xl mx-auto p-6 bg-white dark:bg-gray-900 rounded shadow">
      <h1 className="text-2xl font-bold mb-4 text-gray-900 dark:text-white">Welcome to Artist Pro 🚀</h1>
      <p className="text-gray-700 dark:text-gray-300 mb-6">
        You’ve unlocked the full creative suite—designed for professional artists who collaborate, monetize, and scale.
        Let’s walk through what’s now at your fingertips.
      </p>

      <ul className="list-disc pl-6 text-gray-700 dark:text-gray-300 mb-6">
        <li>Unlimited workflows and collaborators</li>
        <li>Advanced analytics and audit visibility</li>
        <li>Media sync, branded dashboards, and export tools</li>
        <li>Governance scorecard and investor-ready reporting</li>
      </ul>

      <button
        onClick={handleContinue}
        className="px-4 py-2 bg-green-600 text-white rounded hover:bg-green-700"
      >
        Launch Dashboard
      </button>

      <div className="mt-6 text-sm text-gray-500 dark:text-gray-400">
        Need help getting started?{" "}
        <a href="/admin/manual" className="text-green-600 hover:underline">
          View the Admin Manual
        </a>{" "}
        or explore workflow templates.
      </div>
    </div>
  )
}
