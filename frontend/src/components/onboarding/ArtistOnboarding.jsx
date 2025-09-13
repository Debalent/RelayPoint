// frontend/src/components/onboarding/ArtistOnboarding.jsx

import { useNavigate } from "react-router-dom"

export default function ArtistOnboarding() {
  const navigate = useNavigate()

  /**
   * Renders onboarding experience for artist persona.
   * Introduces collaboration tools, step-level ownership, and delivery tracking.
   *
   * Strategic Role:
   * - Accelerates activation for creative contributors.
   * - Scalable for branded flows, role-based dashboards, and monetization triggers.
   * - Extensible for analytics, upsells, and personalized UX.
   */
  const handleContinue = () => {
    navigate("/dashboard")
  }

  return (
    <div className="p-6 bg-white dark:bg-gray-900 rounded shadow max-w-2xl mx-auto">
      <h1 className="text-2xl font-bold mb-4 text-gray-900 dark:text-white">Welcome, Artist 🎨</h1>
      <p className="mb-4 text-gray-700 dark:text-gray-300">
        RelayPoint helps you collaborate with producers, track your deliverables, and stay aligned on creative workflows.
      </p>

      <ul className="list-disc pl-5 mb-6 text-gray-700 dark:text-gray-300">
        <li>View and complete assigned workflow steps</li>
        <li>Upload stems, vocals, and assets with version control</li>
        <li>Receive notifications and track project progress</li>
      </ul>

      <button
        onClick={handleContinue}
        className="bg-purple-600 text-white px-4 py-2 rounded hover:bg-purple-700"
      >
        Enter Studio
      </button>
    </div>
  )
}
