// frontend/src/components/NotificationPreferencesForm.jsx

import { useState, useEffect } from "react"

export default function NotificationPreferencesForm() {
  const [preferences, setPreferences] = useState({
    email_enabled: true,
    sms_enabled: false,
    in_app_enabled: true,
    frequency: "realtime",
    notify_on_step_complete: true,
    notify_on_project_update: true,
  })
  const [status, setStatus] = useState(null)

  /**
   * Renders a form for users to customize their notification preferences.
   * Sends updates to backend and provides feedback on save status.
   *
   * Strategic Role:
   * - Empowers users to control engagement and reduce alert fatigue.
   * - Scalable for role-based defaults, monetization tiers, and compliance.
   * - Extensible for analytics, branded messaging, and behavioral targeting.
   */
  const handleChange = (e) => {
    const { name, type, value, checked } = e.target
    setPreferences((prev) => ({
      ...prev,
      [name]: type === "checkbox" ? checked : value,
    }))
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    setStatus(null)

    try {
      const response = await fetch("http://localhost:8000/api/v1/notifications/preferences", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${localStorage.getItem("access_token")}`,
        },
        body: JSON.stringify(preferences),
      })

      const data = await response.json()
      if (!response.ok) throw new Error(data.detail || "Failed to save preferences")

      setStatus("Preferences updated successfully")
    } catch (err) {
      setStatus(`Error: ${err.message}`)
    }
  }

  return (
    <form onSubmit={handleSubmit} className="p-4 bg-white dark:bg-gray-900 rounded shadow max-w-lg mx-auto">
      <h2 className="text-xl font-semibold mb-4 text-gray-900 dark:text-white">Notification Preferences</h2>

      <label className="block mb-2">
        <input type="checkbox" name="email_enabled" checked={preferences.email_enabled} onChange={handleChange} />
        <span className="ml-2">Email Notifications</span>
      </label>

      <label className="block mb-2">
        <input type="checkbox" name="sms_enabled" checked={preferences.sms_enabled} onChange={handleChange} />
        <span className="ml-2">SMS Notifications</span>
      </label>

      <label className="block mb-2">
        <input type="checkbox" name="in_app_enabled" checked={preferences.in_app_enabled} onChange={handleChange} />
        <span className="ml-2">In-App Alerts</span>
      </label>

      <label className="block mb-4">
        <span className="block mb-1">Notification Frequency</span>
        <select name="frequency" value={preferences.frequency} onChange={handleChange} className="w-full p-2 border rounded">
          <option value="realtime">Real-Time</option>
          <option value="daily_digest">Daily Digest</option>
          <option value="weekly_summary">Weekly Summary</option>
        </select>
      </label>

      <label className="block mb-2">
        <input type="checkbox" name="notify_on_step_complete" checked={preferences.notify_on_step_complete} onChange={handleChange} />
        <span className="ml-2">Notify on Step Completion</span>
      </label>

      <label className="block mb-4">
        <input type="checkbox" name="notify_on_project_update" checked={preferences.notify_on_project_update} onChange={handleChange} />
        <span className="ml-2">Notify on Project Updates</span>
      </label>

      <button type="submit" className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700">
        Save Preferences
      </button>

      {status && <p className="mt-2 text-sm text-gray-700 dark:text-gray-300">{status}</p>}
    </form>
  )
}
