// frontend/src/components/admin/AuditLogFilter.jsx

import { useState } from "react"

export default function AuditLogFilter({ onFilter }) {
  const [startDate, setStartDate] = useState("")
  const [endDate, setEndDate] = useState("")
  const [action, setAction] = useState("")
  const [userId, setUserId] = useState("")

  /**
   * Renders filter controls for audit log viewer.
   * Supports date range, action type, and user-specific queries.
   *
   * Strategic Role:
   * - Powers governance analytics and behavioral segmentation.
   * - Scalable for multi-tenant orgs, export presets, and investor dashboards.
   * - Extensible for persona filters, search, and audit visualizations.
   */
  const handleSubmit = (e) => {
    e.preventDefault()
    onFilter({ startDate, endDate, action, userId })
  }

  return (
    <form onSubmit={handleSubmit} className="mb-6 space-y-4">
      <div>
        <label className="block text-sm font-medium text-gray-700 dark:text-gray-300">Start Date</label>
        <input type="date" value={startDate} onChange={(e) => setStartDate(e.target.value)} className="p-2 border rounded w-full" />
      </div>

      <div>
        <label className="block text-sm font-medium text-gray-700 dark:text-gray-300">End Date</label>
        <input type="date" value={endDate} onChange={(e) => setEndDate(e.target.value)} className="p-2 border rounded w-full" />
      </div>

      <div>
        <label className="block text-sm font-medium text-gray-700 dark:text-gray-300">Action Type</label>
        <select value={action} onChange={(e) => setAction(e.target.value)} className="p-2 border rounded w-full">
          <option value="">All</option>
          <option value="role_change">Role Change</option>
          {/* Future: login, workflow_edit, permission_update */}
        </select>
      </div>

      <div>
        <label className="block text-sm font-medium text-gray-700 dark:text-gray-300">User ID</label>
        <input type="text" value={userId} onChange={(e) => setUserId(e.target.value)} className="p-2 border rounded w-full" />
      </div>

      <button type="submit" className="bg-green-600 text-white px-4 py-2 rounded hover:bg-green-700">
        Apply Filters
      </button>
    </form>
  )
}
