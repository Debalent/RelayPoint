// frontend/src/components/dashboards/ProducerDashboard.jsx

import { useEffect, useState } from "react"
import TriggerWorkflow from "../TriggerWorkflow"
import WorkflowStatus from "../WorkflowStatus"

export default function ProducerDashboard() {
  const [workflows, setWorkflows] = useState([])

  /**
   * Renders dashboard for producer persona.
   * Surfaces workflow tools, collaborator status, and monetization triggers.
   *
   * Strategic Role:
   * - Powers creative automation and team orchestration.
   * - Scalable for multi-project views, analytics, and upsell modules.
   * - Extensible for asset tracking, revenue insights, and branded UX.
   */
  useEffect(() => {
    const fetchWorkflows = async () => {
      try {
        const response = await fetch("http://localhost:8000/api/v1/workflows", {
          headers: {
            Authorization: `Bearer ${localStorage.getItem("access_token")}`,
          },
        })
        const data = await response.json()
        setWorkflows(data.workflows || [])
      } catch (err) {
        console.error("Failed to fetch workflows:", err)
      }
    }

    fetchWorkflows()
  }, [])

  return (
    <div className="p-6 bg-white dark:bg-gray-900 rounded shadow max-w-5xl mx-auto">
      <h1 className="text-2xl font-bold mb-6 text-gray-900 dark:text-white">Producer Dashboard 🎚️</h1>

      {workflows.length === 0 ? (
        <p className="text-gray-600 dark:text-gray-400">No workflows yet. Start by creating one!</p>
      ) : (
        workflows.map((workflow) => (
          <div key={workflow.id} className="mb-6 border-b pb-4">
            <h2 className="text-xl font-semibold text-gray-800 dark:text-gray-200">{workflow.name}</h2>
            <TriggerWorkflow workflowId={workflow.id} />
            <WorkflowStatus workflowId={workflow.id} />
          </div>
        ))
      )}
    </div>
  )
}
