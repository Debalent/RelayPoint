// frontend/src/components/admin/GovernanceAlerts.jsx

import { useEffect, useState } from "react"

export default function GovernanceAlerts() {
  const [logs, setLogs] = useState([])
  const [alerts, setAlerts] = useState([])

  /**
   * Surfaces governance anomalies based on audit log patterns.
   * Flags permission spikes, login surges, and dormant account reactivation.
   *
   * Strategic Role:
   * - Powers proactive governance, security oversight, and investor confidence.
   * - Scalable for multi-tenant orgs, behavioral segmentation, and alert routing.
   * - Extensible for risk scoring, escalation workflows, and audit dashboards.
   */
  useEffect(() => {
    const fetchLogs = async () => {
      try {
        const response = await fetch("http://localhost:8000/api/v1/admin/audit-logs", {
          headers: {
            Authorization: `Bearer ${localStorage.getItem("access_token")}`,
          },
        })
        const data = await response.json()
        setLogs(data.logs || [])
      } catch (err) {
        console.error("Failed to fetch audit logs:", err)
      }
    }

    fetchLogs()
  }, [])

  useEffect(() => {
    const flagged = []

    // 🔍 Detect permission spikes
    const permissionChanges = logs.filter((log) => log.action === "permission_change")
    const permissionByAdmin = {}
    permissionChanges.forEach((log) => {
      permissionByAdmin[log.admin_id] = (permissionByAdmin[log.admin_id] || 0) + 1
    })
    Object.entries(permissionByAdmin).forEach(([adminId, count]) => {
      if (count > 10) {
        flagged.push(`⚠️ Admin ${adminId} made ${count} permission changes — possible overexposure or drift.`)
      }
    })

    // 🔍 Detect login surges
    const loginEvents = logs.filter((log) => log.action === "login")
    const loginByDay = {}
    loginEvents.forEach((log) => {
      const date = new Date(log.timestamp).toLocaleDateString()
      loginByDay[date] = (loginByDay[date] || 0) + 1
    })
    Object.entries(loginByDay).forEach(([date, count]) => {
      if (count > 50) {
        flagged.push(`⚠️ ${count} logins detected on ${date} — possible bot activity or campaign spike.`)
      }
    })

    // 🔍 Detect dormant reactivation
    const recentLogins = loginEvents.filter((log) => {
      const loginDate = new Date(log.timestamp)
      const now = new Date()
      const diffDays = (now - loginDate) / (1000 * 60 * 60 * 24)
      return diffDays < 7
    })
    const dormantUsers = recentLogins.filter((log) => {
      const userId = log.user_id
      const pastActivity = logs.filter((l) => l.user_id === userId && l.action !== "login")
      return pastActivity.length === 0
    })
    dormantUsers.forEach((log) => {
      flagged.push(`⚠️ Dormant user ${log.user_id} logged in — no prior activity detected.`)
    })

    setAlerts(flagged)
  }, [logs])

  return (
    <div className="p-6 bg-white dark:bg-gray-900 rounded shadow max-w-4xl mx-auto">
      <h1 className="text-2xl font-bold mb-6 text-gray-900 dark:text-white">Governance Alerts 🚨</h1>

      {alerts.length === 0 ? (
        <p className="text-gray-600 dark:text-gray-400">No anomalies detected.</p>
      ) : (
        <ul className="space-y-4 text-red-600 dark:text-red-400">
          {alerts.map((alert, idx) => (
            <li key={idx} className="border-b pb-2">{alert}</li>
          ))}
        </ul>
      )}
    </div>
  )
}
