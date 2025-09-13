// frontend/src/components/dashboards/ArtistDashboard.jsx

import { useEffect, useState } from "react"
import StepStatus from "../WorkflowStatus"

export default function ArtistDashboard() {
  const [assignedSteps, setAssignedSteps] = useState([])

  /**
   * Renders dashboard for artist persona.
   * Surfaces assigned workflow steps, deadlines, and upload status.
   *
   * Strategic Role:
   * - Powers deliverable tracking and creative accountability.
   * - Scalable for multi-project views, version control, and notifications.
   * - Extensible for asset uploads, feedback loops, and monetization triggers.
   */
  useEffect(() => {
    const fetchAssignedSteps = async () => {
      try {
        const response = await fetch("http://localhost:8000/api/v1/steps/assigned", {
          headers: {
            Authorization: `Bearer ${localStorage.getItem("access_token")}`,
          },
        })
        const data = await response.json()
        setAssignedSteps(data.steps || [])
      } catch (err) {
        console.error("Failed to fetch assigned steps:", err)
      }
    }

    fetchAssignedSteps()
  }, [])

  return (
    <div className="p-6 bg-white dark:bg-gray-900 rounded shadow max-w-5xl mx-auto">
      <h1 className="text-2xl font-bold mb-6 text-gray-900 dark:text-white">Artist Dashboard 🎤</h1>

      {assignedSteps.length === 0 ? (
        <p className="text-gray-600 dark:text-gray-400">No tasks assigned yet. Waiting on producer input.</p>
      ) : (
        assignedSteps.map((step) => (
          <div key={step.id} className="mb-6 border-b pb-4">
            <h2 className="text-xl font-semibold text-gray-800 dark:text-gray-200">{step.name}</h2>
            <StepStatus workflowId={step.workflow_id} />
            {/* Future: Add upload button, feedback thread, version history */}
          </div>
        ))
      )}
    </div>
  )
}
