// frontend/src/components/admin/AuditLogViewer.jsx

import { useEffect, useState } from "react"

export default function AuditLogViewer() {
  const [logs, setLogs] = useState([])

  /**
   * Renders audit log entries for admin oversight.
   * Surfaces role changes with timestamps and attribution.
   *
   * Strategic Role:
   * - Powers transparency, compliance, and enterprise governance.
   * - Scalable for multi-tenant orgs, export tools, and behavioral analytics.
   * - Extensible for filtering, search, and UI surfacing in investor dashboards.
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

  return (
    <div className="p-6 bg-white dark:bg-gray-900 rounded shadow max-w-5xl mx-auto">
      <h1 className="text-2xl font-bold mb-6 text-gray-900 dark:text-white">Audit Log Viewer 📜</h1>

      {logs.length === 0 ? (
        <p className="text-gray-600 dark:text-gray-400">No audit entries found.</p>
      ) : (
        <ul className="space-y-4">
          {logs.map((log) => (
            <li key={log.id} className="border-b pb-2 text-gray-700 dark:text-gray-300">
              <strong>{log.timestamp}</strong>: Admin <em>{log.admin_id}</em> changed user <em>{log.user_id}</em> role from <code>{log.old_value}</code> to <code>{log.new_value}</code>
            </li>
          ))}
        </ul>
      )}
    </div>
  )
}
