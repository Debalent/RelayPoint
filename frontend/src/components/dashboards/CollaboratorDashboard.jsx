// frontend/src/components/dashboards/CollaboratorDashboard.jsx

import { useEffect, useState } from "react"
import StepStatus from "../WorkflowStatus"

export default function CollaboratorDashboard() {
  const [sharedSteps, setSharedSteps] = useState([])

  /**
   * Renders dashboard for collaborator persona.
   * Surfaces shared workflow steps, comments, and upload status.
   *
   * Strategic Role:
   * - Aligns contributors with project goals and step-level responsibilities.
   * - Scalable for external teams, assistants, and cross-functional roles.
   * - Extensible for asset uploads, feedback threads, and notification tracking.
   */
  useEffect(() => {
    const fetchSharedSteps = async () => {
      try {
        const response = await fetch("http://localhost:8000/api/v1/steps/shared", {
          headers: {
            Authorization: `Bearer ${localStorage.getItem("access_token")}`,
          },
        })
        const data = await response.json()
        setSharedSteps(data.steps || [])
      } catch (err) {
        console.error("Failed to fetch shared steps:", err)
      }
    }

    fetchSharedSteps()
  }, [])

  return (
    <div className="p-6 bg-white dark:bg-gray-900 rounded shadow max-w-5xl mx-auto">
      <h1 className="text-2xl font-bold mb-6 text-gray-900 dark:text-white">Collaborator Dashboard 🤝</h1>

      {sharedSteps.length === 0 ? (
        <p className="text-gray-600 dark:text-gray-400">No shared tasks yet. Waiting on producer or artist input.</p>
      ) : (
        sharedSteps.map((step) => (
          <div key={step.id} className="mb-6 border-b pb-4">
            <h2 className="text-xl font-semibold text-gray-800 dark:text-gray-200">{step.name}</h2>
            <StepStatus workflowId={step.workflow_id} />
            {/* Future: Add comment thread, upload button, read receipts */}
          </div>
        ))
      )}
    </div>
  )
}
