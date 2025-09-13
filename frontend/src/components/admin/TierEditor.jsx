// frontend/src/components/admin/TierEditor.jsx

import { useState } from "react"

export default function TierEditor({ userId, currentTier }) {
  const [tier, setTier] = useState(currentTier)
  const [status, setStatus] = useState(null)

  /**
   * Renders a dropdown for editing a user's pricing tier.
   * Sends updates to backend and reflects changes in Admin Console.
   *
   * Strategic Role:
   * - Powers monetization workflows and tiered access control.
   * - Scalable for multi-tenant orgs, usage-based pricing, and upgrade flows.
   * - Extensible for audit logging, billing hooks, and investor dashboards.
   */
  const handleTierChange = async (e) => {
    const newTier = e.target.value
    setTier(newTier)
    setStatus(null)

    try {
      const response = await fetch(`http://localhost:8000/api/v1/admin/users/${userId}/tier`, {
        method: "PUT",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${localStorage.getItem("access_token")}`,
        },
        body: JSON.stringify({ tier: newTier }),
      })

      const data = await response.json()
      if (!response.ok) throw new Error(data.detail || "Failed to update tier")

      setStatus(`Tier updated to ${newTier}`)
    } catch (err) {
      setStatus(`Error: ${err.message}`)
    }
  }

  return (
    <div className="mb-4">
      <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Pricing Tier</label>
      <select value={tier} onChange={handleTierChange} className="p-2 border rounded w-full">
        <option value="free">Free</option>
        <option value="pro">Pro</option>
        <option value="enterprise">Enterprise</option>
      </select>
      {status && <p className="mt-2 text-sm text-gray-600 dark:text-gray-400">{status}</p>}
    </div>
  )
}
