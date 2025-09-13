// frontend/src/components/admin/TierAnalytics.jsx

import { useEffect, useState } from "react"
import { Pie, Line } from "react-chartjs-2"
import { Chart as ChartJS, ArcElement, CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend } from "chart.js"

ChartJS.register(ArcElement, CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend)

export default function TierAnalytics() {
  const [users, setUsers] = useState([])

  /**
   * Visualizes tier distribution and upgrade velocity.
   * Powers monetization dashboards and investor snapshots.
   *
   * Strategic Role:
   * - Reveals adoption trends and monetization signals.
   * - Scalable for multi-tenant orgs and tiered feature access.
   * - Extensible for churn risk, trial conversion, and upsell targeting.
   */
  useEffect(() => {
    const fetchUsers = async () => {
      try {
        const response = await fetch("http://localhost:8000/api/v1/admin/users", {
          headers: {
            Authorization: `Bearer ${localStorage.getItem("access_token")}`,
          },
        })
        const data = await response.json()
        setUsers(data.users || [])
      } catch (err) {
        console.error("Failed to fetch users:", err)
      }
    }

    fetchUsers()
  }, [])

  const getTierCounts = () => {
    const counts = { free: 0, pro: 0, enterprise: 0 }
    users.forEach((user) => {
      if (counts[user.tier] !== undefined) {
        counts[user.tier] += 1
      }
    })
    return {
      labels: ["Free", "Pro", "Enterprise"],
      datasets: [
        {
          data: [counts.free, counts.pro, counts.enterprise],
          backgroundColor: ["#f59e0b", "#3b82f6", "#10b981"],
        },
      ],
    }
  }

  const getUpgradeVelocity = () => {
    const upgradesByDay = {}
    users.forEach((user) => {
      if (user.tier !== "free" && user.upgraded_at) {
        const date = new Date(user.upgraded_at).toLocaleDateString()
        upgradesByDay[date] = (upgradesByDay[date] || 0) + 1
      }
    })
    return {
      labels: Object.keys(upgradesByDay),
      datasets: [
        {
          label: "Upgrades",
          data: Object.values(upgradesByDay),
          borderColor: "#3b82f6",
          backgroundColor: "#bfdbfe",
          fill: true,
        },
      ],
    }
  }

  return (
    <div className="p-6 bg-white dark:bg-gray-900 rounded shadow max-w-5xl mx-auto">
      <h1 className="text-2xl font-bold mb-6 text-gray-900 dark:text-white">Tier Analytics 💸</h1>

      <div className="space-y-10">
        <div>
          <h2 className="text-lg font-semibold mb-2 text-gray-800 dark:text-gray-200">Tier Distribution</h2>
          <Pie data={getTierCounts()} />
        </div>

        <div>
          <h2 className="text-lg font-semibold mb-2 text-gray-800 dark:text-gray-200">Upgrade Velocity</h2>
          <Line data={getUpgradeVelocity()} />
        </div>
      </div>
    </div>
  )
}
