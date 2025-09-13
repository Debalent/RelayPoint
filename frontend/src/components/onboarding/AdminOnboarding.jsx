// frontend/src/components/onboarding/AdminOnboarding.jsx

import { useNavigate } from "react-router-dom"

export default function AdminOnboarding() {
  const navigate = useNavigate()

  /**
   * Renders onboarding experience for admin persona.
   * Introduces user management, workflow oversight, and analytics tools.
   *
   * Strategic Role:
   * - Accelerates activation for platform managers and team leads.
   * - Scalable for enterprise orgs, multi-tenant setups, and compliance workflows.
   * - Extensible for audit logs, permissions, and strategic dashboards.
   */
  const handleContinue = () => {
    navigate("/admin/dashboard")
  }

  return (
    <div className="p-6 bg-white dark:bg-gray-900 rounded shadow max-w-2xl mx-auto">
      <h1 className="text-2xl font-bold mb-4 text-gray-900 dark:text-white">Welcome, Admin 🛠️</h1>
      <p className="mb-4 text-gray-700 dark:text-gray-300">
        RelayPoint gives you full visibility into user activity, workflow performance, and platform configuration.
      </p>

      <ul className="list-disc pl-5 mb-6 text-gray-700 dark:text-gray-300">
        <li>Manage users, roles, and permissions across teams</li>
        <li>Monitor workflow execution and completion rates</li>
        <li>Access analytics and audit logs for strategic oversight</li>
      </ul>

      <button
        onClick={handleContinue}
        className="bg-red-600 text-white px-4 py-2 rounded hover:bg-red-700"
      >
        Enter Admin Console
      </button>
    </div>
  )
}
