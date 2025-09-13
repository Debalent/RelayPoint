// frontend/src/components/NotificationCenter.jsx

import { useEffect, useState } from "react"

export default function NotificationCenter() {
  const [notifications, setNotifications] = useState([])

  /**
   * Fetches user-specific notifications from backend.
   * Displays alerts triggered by workflow events, system updates, or team activity.
   *
   * Strategic Role:
   * - Drives engagement and responsiveness across collaborative workflows.
   * - Scalable for role-based alerts, branded messaging, and real-time updates.
   * - Extensible for analytics, read receipts, and monetization triggers.
   */
  useEffect(() => {
    const fetchNotifications = async () => {
      try {
        const response = await fetch("http://localhost:8000/api/v1/notifications", {
          headers: {
            Authorization: `Bearer ${localStorage.getItem("access_token")}`,
          },
        })
        const data = await response.json()
        setNotifications(data.notifications || [])
      } catch (err) {
        console.error("Failed to fetch notifications:", err)
      }
    }

    fetchNotifications()
  }, [])

  return (
    <div className="p-4 bg-white dark:bg-gray-900 rounded shadow max-w-lg mx-auto">
      <h2 className="text-xl font-semibold mb-4 text-gray-900 dark:text-white">Notifications</h2>
      {notifications.length === 0 ? (
        <p className="text-gray-600 dark:text-gray-400">No new alerts.</p>
      ) : (
        <ul className="space-y-3">
          {notifications.map((note) => (
            <li key={note.id} className="border-b pb-2">
              <p className="text-gray-800 dark:text-gray-200">{note.message}</p>
              <p className="text-xs text-gray-500 dark:text-gray-400">{note.timestamp}</p>
            </li>
          ))}
        </ul>
      )}
    </div>
  )
}
