// frontend/src/components/feedback/SafetyScoreDashboard.jsx

import { useEffect, useState } from "react"

export default function SafetyScoreDashboard({ workflowId }) {
  const [scores, setScores] = useState(null)

  /**
   * Displays aggregated psychological safety scores for a workflow.
   * Strategic Role:
   * - Powers team health dashboards, onboarding refinement, and contributor coaching.
   * - Scalable for org benchmarking, role segmentation, and alert triggers.
   * - Extensible for scorecards, trend lines, and improvement prompts.
   */
  useEffect(() => {
    const fetchScores = async () => {
      try {
        const response = await fetch(`/api/v1/workflows/${workflowId}/safety-scores`, {
          headers: {
            Authorization: `Bearer ${localStorage.getItem("access_token")}`,
          },
        })
        const data = await response.json()
        setScores(data)
      } catch (err) {
        console.error("Failed to fetch safety scores:", err)
      }
    }

    fetchScores()
  }, [workflowId])

  if (!scores) return <p className="text-gray-600 dark:text-gray-400">Loading safety metrics...</p>

  const { clarity, trust, collaboration, count } = scores

  return (
    <div className="p-6 bg-white dark:bg-gray-900 rounded shadow max-w-xl mx-auto">
      <h2 className="text-xl font-bold mb-4 text-gray-900 dark:text-white">Team Health Metrics 🧠</h2>
      <p className="text-sm text-gray-700 dark:text-gray-300 mb-4">
        Based on <strong>{count}</strong> feedback submissions, here’s how contributors rate this workflow:
      </p>

      <ul className="space-y-2 text-gray-800 dark:text-gray-200">
        <li><strong>Clarity:</strong> {clarity ?? "N/A"} / 5</li>
        <li><strong>Trust:</strong> {trust ?? "N/A"} / 5</li>
        <li><strong>Collaboration:</strong> {collaboration ?? "N/A"} / 5</li>
      </ul>

      <div className="mt-4 text-xs text-gray-500 dark:text-gray-400">
        Want to improve these scores?{" "}
        <a href="/cookbook/persona-routing" className="text-blue-600 hover:underline">
          Explore onboarding strategies
        </a>{" "}
        or{" "}
        <a href="/admin/manual" className="text-blue-600 hover:underline">
          review governance best practices
        </a>.
      </div>
    </div>
  )
}
