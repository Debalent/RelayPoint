// frontend/src/components/admin/RoleEditor.jsx

import { useState } from "react"

export default function RoleEditor({ userId, currentRole }) {
  const [role, setRole] = useState(currentRole)
  const [status, setStatus] = useState(null)

  /**
   * Renders a dropdown for editing a user's role.
   * Sends updates to backend and reflects changes in Admin Console.
   *
   * Strategic Role:
   * - Powers governance and team configuration.
   * - Scalable for multi-tenant orgs, branded flows, and onboarding logic.
   * - Extensible for audit logs, tier management, and behavioral segmentation.
   */
  const handleRoleChange = async (e) => {
    const newRole = e.target.value
    setRole(newRole)
    setStatus(null)

    try {
      const response = await fetch(`http://localhost:8000/api/v1/admin/users/${userId}/role`, {
        method: "PUT",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${localStorage.getItem("access_token")}`,
        },
        body: JSON.stringify({ role: newRole }),
      })

      const data = await response.json()
      if (!response.ok) throw new Error(data.detail || "Failed to update role")

      setStatus(`Role updated to ${newRole}`)
    } catch (err) {
      setStatus(`Error: ${err.message}`)
    }
  }

  return (
    <div className="mb-4">
      <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Role</label>
      <select value={role} onChange={handleRoleChange} className="p-2 border rounded w-full">
        <option value="producer">Producer</option>
        <option value="artist">Artist</option>
        <option value="collaborator">Collaborator</option>
        <option value="admin">Admin</option>
      </select>
      {status && <p className="mt-2 text-sm text-gray-600 dark:text-gray-400">{status}</p>}
    </div>
  )
}
