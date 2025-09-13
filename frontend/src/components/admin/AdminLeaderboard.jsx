// frontend/src/components/admin/AdminLeaderboard.jsx

import { useEffect, useState } from "react"

export default function AdminLeaderboard() {
  const [logs, setLogs] = useState([])
  const [leaderboard, setLeaderboard] = useState([])

  /**
   * Renders a leaderboard of admin governance activity.
   * Ranks admins by role changes, workflow edits, and permission updates.
   *
   * Strategic Role:
   * - Powers behavioral analytics, accountability, and platform oversight.
   * - Scalable for multi-tenant orgs, audit dashboards, and investor reporting.
   * - Extensible for time filters, persona segmentation, and export presets.
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
    const activityMap = {}

    logs.forEach((log) => {
      if (!log.admin_id) return
      if (!activityMap[log.admin_id]) {
        activityMap[log.admin_id] = { role_change: 0, workflow_edit: 0, permission_change: 0 }
      }
      if (activityMap[log.admin_id][log.action] !== undefined) {
        activityMap[log.admin_id][log.action] += 1
      }
    })

    const sorted = Object.entries(activityMap)
      .map(([adminId, actions]) => ({
        adminId,
        total: actions.role_change + actions.workflow_edit + actions.permission_change,
        ...actions,
      }))
      .sort((a, b) => b.total - a.total)

    setLeaderboard(sorted)
  }, [logs])

  return (
    <div className="p-6 bg-white dark:bg-gray-900 rounded shadow max-w-4xl mx-auto">
      <h1 className="text-2xl font-bold mb-6 text-gray-900 dark:text-white">Admin Leaderboard 🏆</h1>

      {leaderboard.length === 0 ? (
        <p className="text-gray-600 dark:text-gray-400">No admin activity found.</p>
      ) : (
        <table className="w-full text-left border-collapse">
          <thead>
            <tr className="bg-gray-100 dark:bg-gray-800 text-gray-700 dark:text-gray-300">
              <th className="p-2">Admin ID</th>
              <th className="p-2">Role Changes</th>
              <th className="p-2">Workflow Edits</th>
              <th className="p-2">Permission Changes</th>
              <th className="p-2">Total Actions</th>
            </tr>
          </thead>
          <tbody>
            {leaderboard.map((admin) => (
              <tr key={admin.adminId} className="border-b text-gray-800 dark:text-gray-200">
                <td className="p-2">{admin.adminId}</td>
                <td className="p-2">{admin.role_change}</td>
                <td className="p-2">{admin.workflow_edit}</td>
                <td className="p-2">{admin.permission_change}</td>
                <td className="p-2 font-semibold">{admin.total}</td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  )
}
