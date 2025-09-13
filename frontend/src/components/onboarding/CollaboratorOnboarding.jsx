// frontend/src/components/onboarding/CollaboratorOnboarding.jsx

import { useNavigate } from "react-router-dom"

export default function CollaboratorOnboarding() {
  const navigate = useNavigate()

  /**
   * Renders onboarding experience for collaborator persona.
   * Introduces shared workflows, task visibility, and communication tools.
   *
   * Strategic Role:
   * - Aligns contributors with project goals and step-level responsibilities.
   * - Scalable for external teams, assistants, and cross-functional roles.
   * - Extensible for analytics, permissions, and branded experiences.
   */
  const handleContinue = () => {
    navigate("/dashboard")
  }

  return (
    <div className="p-6 bg-white dark:bg-gray-900 rounded shadow max-w-2xl mx-auto">
      <h1 className="text-2xl font-bold mb-4 text-gray-900 dark:text-white">Welcome, Collaborator 🤝</h1>
      <p className="mb-4 text-gray-700 dark:text-gray-300">
        RelayPoint helps you stay aligned with producers and artists by surfacing shared workflows, assigned tasks, and real-time updates.
      </p>

      <ul className="list-disc pl-5 mb-6 text-gray-700 dark:text-gray-300">
        <li>Access shared workflows and view assigned steps</li>
        <li>Upload assets and leave comments on deliverables</li>
        <li>Receive notifications and track project milestones</li>
      </ul>

      <button
        onClick={handleContinue}
        className="bg-indigo-600 text-white px-4 py-2 rounded hover:bg-indigo-700"
      >
        Join the Project
      </button>
    </div>
  )
}
