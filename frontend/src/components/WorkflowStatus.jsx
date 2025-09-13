// frontend/src/components/WorkflowStatus.jsx

import { useEffect, useState } from "react"

export default function WorkflowStatus({ workflowId }) {
  const [steps, setSteps] = useState([])
  const [loading, setLoading] = useState(true)

  /**
   * Fetches workflow steps and their completion status from backend.
   * Displays real-time progress and enables future analytics or notifications.
   *
   * Strategic Role:
   * - Visualizes execution state for producers, collaborators, and admins.
   * - Scalable for dashboards, mobile views, and role-based insights.
   * - Extensible for analytics, alerts, and monetization tracking.
   */
  useEffect(() => {
    const fetchSteps = async () => {
      try {
        const response = await fetch(`http://localhost:8000/api/v1/workflows/${workflowId}/status`, {
          headers: {
            Authorization: `Bearer ${localStorage.getItem("access_token")}`,
          },
        })
        const data = await response.json()
        setSteps(data.steps || [])
      } catch (err) {
        console.error("Failed to fetch workflow status:", err)
      } finally {
        setLoading(false)
      }
    }

    fetchSteps()
  }, [workflowId])

  if (loading) return <p className="text-gray-500">Loading workflow status...</p>

  return (
    <div className="p-4 bg-white dark:bg-gray-900 rounded shadow">
      <h2 className="text-xl font-semibold mb-4 text-gray-900 dark:text-white">Workflow Progress</h2>
      <ul className="space-y-2">
        {steps.map((step) => (
          <li key={step.id} className="flex items-center justify-between">
            <span className="text-gray-800 dark:text-gray-200">{step.name}</span>
            <span className={`px-2 py-1 rounded text-sm ${
              step.is_complete ? "bg-green-600 text-white" : "bg-yellow-500 text-white"
            }`}>
              {step.is_complete ? "Complete" : "Pending"}
            </span>
          </li>
        ))}
      </ul>
    </div>
  )
}
