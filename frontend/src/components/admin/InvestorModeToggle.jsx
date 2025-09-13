// frontend/src/components/admin/InvestorModeToggle.jsx

import { useState } from "react"

export default function InvestorModeToggle({ onToggle }) {
  const [enabled, setEnabled] = useState(false)

  /**
   * Toggles investor mode to filter dashboard for strategic metrics.
   * Strategic Role:
   * - Powers investor demos, pitch decks, and strategic reviews.
   * - Scalable for metric presets, export logic, and tiered visibility.
   * - Extensible for PDF snapshots, embedded views, and VC links.
   */
  const handleToggle = () => {
    const newState = !enabled
    setEnabled(newState)
    onToggle(newState)
  }

  return (
    <div className="flex items-center space-x-3 mb-6">
      <label className="text-sm font-medium text-gray-800 dark:text-gray-200">Investor Mode</label>
      <button
        onClick={handleToggle}
        className={`px-3 py-1 rounded text-sm ${
          enabled ? "bg-green-600 text-white" : "bg-gray-300 text-gray-800"
        }`}
      >
        {enabled ? "Enabled" : "Disabled"}
      </button>
    </div>
  )
}
