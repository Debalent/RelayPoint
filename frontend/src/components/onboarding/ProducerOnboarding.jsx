// frontend/src/components/onboarding/ProducerOnboarding.jsx

import { useNavigate } from "react-router-dom"

export default function ProducerOnboarding() {
  const navigate = useNavigate()

  /**
   * Renders onboarding experience for producer persona.
   * Introduces workflow tools, monetization features, and collaboration setup.
   *
   * Strategic Role:
   * - Accelerates activation for high-value users.
   * - Scalable for branded flows, tiered access, and feature discovery.
   * - Extensible for analytics, upsells, and personalized dashboards.
   */
  const handleContinue = () => {
    navigate("/dashboard")
  }

  return (
    <div className="p-6 bg-white dark:bg-gray-900 rounded shadow max-w-2xl mx-auto">
      <h1 className="text-2xl font-bold mb-4 text-gray-900 dark:text-white">Welcome, Producer 🎧</h1>
      <p className="mb-4 text-gray-700 dark:text-gray-300">
        RelayPoint is built to help you automate your creative workflows, collaborate with artists, and monetize your production process.
      </p>

      <ul className="list-disc pl-5 mb-6 text-gray-700 dark:text-gray-300">
        <li>Create modular workflows for beats, stems, and deliverables</li>
        <li>Invite collaborators and assign step-level ownership</li>
        <li>Trigger monetization events and track completion analytics</li>
      </ul>

      <button
        onClick={handleContinue}
        className="bg-green-600 text-white px-4 py-2 rounded hover:bg-green-700"
      >
        Get Started
      </button>
    </div>
  )
}
