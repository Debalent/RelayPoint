// frontend/src/components/admin/LoginActivityViewer.jsx

import { useEffect, useState } from "react"

export default function LoginActivityViewer() {
  const [logs, setLogs] = useState([])

  /**
   * Renders login events from the audit log.
   * Shows who accessed the system and when.
   *
   * Strategic Role:
   * - Powers security audits, usage analytics, and compliance tracking.
   * - Scalable for multi-tenant orgs, anomaly detection, and investor dashboards.
   * - Extensible for IP metadata, device info, and geo-fencing.
   */
  useEffect(() => {
    const fetchLogs = async () => {
      try {
        const response = await fetch("http://localhost:8000/api/v1/admin/audit-logs?action=login", {
          headers: {
            Authorization: `Bearer ${localStorage.getItem("access_token")}`,
          },
        })
        const data = await response.json()
        setLogs(data.logs || [])
      } catch (err) {
        console.error("Failed to fetch login logs:", err)
      }
    }

    fetchLogs()
  }, [])

  return (
    <div className="p-6 bg-white dark:bg-gray-900 rounded shadow max-w-4xl mx-auto">
      <h2 className="text-xl font-bold mb-4 text-gray-900 dark:text-white">Login Activity 📍</h2>
      {logs.length === 0 ? (
        <p className="text-gray-600 dark:text-gray-400">No login activity found.</p>
      ) : (
        <ul className="space-y-3">
          {logs.map((log) => (
            <li key={log.id} className="border-b pb-2 text-gray-700 dark:text-gray-300">
              <strong>{log.timestamp}</strong>: User <em>{log.user_id}</em> logged in successfully
            </li>
          ))}
        </ul>
      )}
    </div>
  )
}
