// frontend/src/components/admin/GovernanceAnalytics.jsx

import { useEffect, useState } from "react"
import { Line, Bar } from "react-chartjs-2"
import { Chart as ChartJS, CategoryScale, LinearScale, PointElement, LineElement, BarElement, Title, Tooltip, Legend } from "chart.js"

ChartJS.register(CategoryScale, LinearScale, PointElement, LineElement, BarElement, Title, Tooltip, Legend)

export default function GovernanceAnalytics() {
  const [auditData, setAuditData] = useState([])

  /**
   * Fetches audit logs and visualizes governance activity.
   * Charts login frequency, role change velocity, and workflow edit trends.
   *
   * Strategic Role:
   * - Powers investor dashboards, behavioral analytics, and governance maturity.
   * - Scalable for multi-tenant orgs, persona segmentation, and anomaly detection.
   * - Extensible for heatmaps, leaderboards, and exportable insights.
   */
  useEffect(() => {
    const fetchAuditLogs = async () => {
      try {
        const response = await fetch("http://localhost:8000/api/v1/admin/audit-logs", {
          headers: {
            Authorization: `Bearer ${localStorage.getItem("access_token")}`,
          },
        })
        const data = await response.json()
        setAuditData(data.logs || [])
      } catch (err) {
        console.error("Failed to fetch audit logs:", err)
      }
    }

    fetchAuditLogs()
  }, [])

  // 🧠 Transform audit logs into chart-ready datasets
  const getEventCountsByDay = (actionType) => {
    const counts = {}
    auditData
      .filter((log) => log.action === actionType)
      .forEach((log) => {
        const date = new Date(log.timestamp).toLocaleDateString()
        counts[date] = (counts[date] || 0) + 1
      })
    return {
      labels: Object.keys(counts),
      datasets: [
        {
          label: `${actionType} events`,
          data: Object.values(counts),
          backgroundColor: "#3b82f6",
          borderColor: "#2563eb",
          fill: false,
        },
      ],
    }
  }

  return (
    <div className="p-6 bg-white dark:bg-gray-900 rounded shadow max-w-6xl mx-auto">
      <h1 className="text-2xl font-bold mb-6 text-gray-900 dark:text-white">Governance Analytics 📊</h1>

      <div className="space-y-10">
        <div>
          <h2 className="text-lg font-semibold mb-2 text-gray-800 dark:text-gray-200">Login Frequency</h2>
          <Bar data={getEventCountsByDay("login")} />
        </div>

        <div>
          <h2 className="text-lg font-semibold mb-2 text-gray-800 dark:text-gray-200">Role Change Velocity</h2>
          <Line data={getEventCountsByDay("role_change")} />
        </div>

        <div>
          <h2 className="text-lg font-semibold mb-2 text-gray-800 dark:text-gray-200">Workflow Edit Trends</h2>
          <Line data={getEventCountsByDay("workflow_edit")} />
        </div>
      </div>
    </div>
  )
}
