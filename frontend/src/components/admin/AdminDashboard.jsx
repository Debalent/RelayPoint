// frontend/src/components/admin/AdminDashboard.jsx

import { useEffect, useState } from "react"

export default function AdminDashboard() {
  const [users, setUsers] = useState([])
  const [workflowStats, setWorkflowStats] = useState({})

  /**
   * Renders dashboard for admin persona.
   * Surfaces user management, workflow analytics, and system health.
   *
   * Strategic Role:
   * - Powers governance, compliance, and strategic oversight.
   * - Scalable for multi-org setups, audit logs, and tiered access.
   * - Extensible for permissions, usage metrics, and monetization tracking.
   */
  useEffect(() => {
    const fetchAdminData = async () => {
      try {
        const [userRes, statsRes] = await Promise.all([
          fetch("http://localhost:8000/api/v1/admin/users", {
            headers: { Authorization: `Bearer ${localStorage.getItem("access_token")}` },
          }),
          fetch("http://localhost:8000/api/v1/admin/workflow-stats", {
            headers: { Authorization: `Bearer ${localStorage.getItem("access_token")}` },
          }),
        ])
        const usersData = await userRes.json()
        const statsData = await statsRes.json()
        setUsers(usersData.users || [])
        setWorkflowStats(statsData || {})
      } catch (err) {
        console.error("Failed to fetch admin data:", err)
      }
    }

    fetchAdminData()
  }, [])

  return (
    <div className="p-6 bg-white dark:bg-gray-900 rounded shadow max-w-6xl mx-auto">
      <h1 className="text-2xl font-bold mb-6 text-gray-900 dark:text-white">Admin Console 🛡️</h1>

      <section className="mb-8">
        <h2 className="text-xl font-semibold mb-2 text-gray-800 dark:text-gray-200">User Management</h2>
        <ul className="space-y-2">
          {users.map((user) => (
            <li key={user.id} className="border-b pb-2 text-gray-700 dark:text-gray-300">
              {user.email} — {user.role}
            </li>
          ))}
        </ul>
      </section>

      <section>
        <h2 className="text-xl font-semibold mb-2 text-gray-800 dark:text-gray-200">Workflow Analytics</h2>
        <p className="text-gray-700 dark:text-gray-300">Total Workflows: {workflowStats.total}</p>
        <p className="text-gray-700 dark:text-gray-300">Completion Rate: {workflowStats.completion_rate}%</p>
        <p className="text-gray-700 dark:text-gray-300">Active Projects: {workflowStats.active_projects}</p>
      </section>
    </div>
  )
}
