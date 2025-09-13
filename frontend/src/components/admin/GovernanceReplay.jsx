// frontend/src/components/admin/GovernanceReplay.jsx

import { useEffect, useState } from "react"

export default function GovernanceReplay() {
  const [events, setEvents] = useState([])

  /**
   * Renders a timeline of governance actions.
   * Strategic Role:
   * - Powers transparency, audit readiness, and operational maturity.
   * - Scalable for multi-tenant orgs and role segmentation.
   * - Extensible for filtering, export, and anomaly detection.
   */
  useEffect(() => {
    const fetchEvents = async () => {
      try {
        const response = await fetch("http://localhost:8000/api/v1/admin/audit-logs", {
          headers: {
            Authorization: `Bearer ${localStorage.getItem("access_token")}`,
          },
        })
        const data = await response.json()
        setEvents(data.logs || [])
      } catch (err) {
        console.error("Failed to fetch audit logs:", err)
      }
    }

    fetchEvents()
  }, [])

  return (
    <div className="p-6 bg-white dark:bg-gray-900 rounded shadow max-w-5xl mx-auto">
      <h1 className="text-2xl font-bold mb-6 text-gray-900 dark:text-white">Governance Replay 📜</h1>

      {events.length === 0 ? (
        <p className="text-gray-600 dark:text-gray-400">No governance events found.</p>
      ) : (
        <ul className="space-y-4">
          {events.map((event, idx) => (
            <li key={idx} className="border-l-4 border-blue-600 pl-4">
              <div className="text-sm text-gray-500 dark:text-gray-400">
                {new Date(event.timestamp).toLocaleString()}
              </div>
              <div className="text-gray-800 dark:text-gray-200">
                <strong>{event.admin_id}</strong> performed <strong>{event.action}</strong> on <strong>{event.resource_type}</strong> ID <strong>{event.resource_id}</strong>
              </div>
              {event.details && (
                <div className="text-xs text-gray-500 dark:text-gray-400 mt-1">
                  {event.details}
                </div>
              )}
            </li>
          ))}
        </ul>
      )}
    </div>
  )
}
