// frontend/src/components/admin/GovernanceScorecard.jsx

import { useEffect, useState } from "react"

export default function GovernanceScorecard({ orgId }) {
  const [scorecard, setScorecard] = useState(null)

  /**
   * Displays governance maturity score and breakdown.
   * Strategic Role:
   * - Powers admin coaching, investor dashboards, and org benchmarking.
   * - Scalable for multi-tenant platforms and role-based segmentation.
   * - Extensible for alerts, export, and score history.
   */
  useEffect(() => {
    const fetchScorecard = async () => {
      try {
        const response = await fetch(`http://localhost:8000/api/v1/admin/orgs/${orgId}/governance-score`, {
          headers: {
            Authorization: `Bearer ${localStorage.getItem("access_token")}`,
          },
        })
        const data = await response.json()
        setScorecard(data)
      } catch (err) {
        console.error("Failed to fetch governance scorecard:", err)
      }
    }

    fetchScorecard()
  }, [orgId])

  if (!scorecard) return <p className="text-gray-600 dark:text-gray-400">Loading scorecard...</p>

  const { score, breakdown } = scorecard

  return (
    <div className="p-6 bg-white dark:bg-gray-900 rounded shadow max-w-4xl mx-auto">
      <h2 className="text-xl font-bold mb-4 text-gray-900 dark:text-white">Governance Scorecard 🧭</h2>
      <p className="text-gray-700 dark:text-gray-300 mb-4">
        Your organization’s governance maturity score is <strong>{score}/100</strong>. Here's how it's calculated:
      </p>

      <ul className="list-disc pl-6 text-gray-700 dark:text-gray-300 mb-6 space-y-2">
        <li><strong>Workflow Coverage:</strong> {breakdown.workflowCoverage} active workflows</li>
        <li><strong>Audit Events:</strong> {breakdown.auditEvents} logged actions</li>
        <li><strong>Role Clarity:</strong> {breakdown.roleClarity} users with defined roles</li>
        <li><strong>Collaboration Density:</strong> {breakdown.collaborationDensity} shared actions</li>
        <li><strong>Governance Hygiene:</strong> {breakdown.hygieneEvents} cleanup actions</li>
      </ul>

      <div className="text-sm text-gray-500 dark:text-gray-400">
        Want to improve your score?{" "}
        <a href="/admin/manual" className="text-blue-600 hover:underline">
          View governance best practices
        </a>{" "}
        or schedule a workflow audit.
      </div>
    </div>
  )
}
