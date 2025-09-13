// frontend/src/components/TriggerWorkflow.jsx

import { useState } from "react"

export default function TriggerWorkflow({ workflowId }) {
  const [status, setStatus] = useState(null)
  const [loading, setLoading] = useState(false)

  /**
   * Sends a request to backend to execute a workflow by ID.
   * Updates UI with status feedback and handles errors gracefully.
   *
   * Strategic Role:
   * - Connects user action to backend automation.
   * - Enables real-time feedback and collaborative execution.
   * - Scalable for analytics, monetization, and async workflows.
   */
  const handleTrigger = async () => {
    setLoading(true)
    setStatus(null)

    try {
      const response = await fetch(`http://localhost:8000/api/v1/workflows/${workflowId}/run`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${localStorage.getItem("access_token")}`,
        },
      })

      const data = await response.json()
      if (!response.ok) throw new Error(data.detail || "Workflow execution failed")

      setStatus("Workflow completed successfully")
    } catch (err) {
      setStatus(`Error: ${err.message}`)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="p-4 bg-white dark:bg-gray-900 rounded shadow">
      <button
        onClick={handleTrigger}
        disabled={loading}
        className="bg-green-600 text-white px-4 py-2 rounded hover:bg-green-700"
      >
        {loading ? "Running..." : "Run Workflow"}
      </button>
      {status && <p className="mt-2 text-sm text-gray-700 dark:text-gray-300">{status}</p>}
    </div>
  )
}
