// frontend/src/components/tiers/UpgradeNudgeBanner.jsx

import { useEffect, useState } from "react"

export default function UpgradeNudgeBanner({ userId }) {
  const [shouldNudge, setShouldNudge] = useState(false)

  /**
   * Displays upgrade prompt when user hits Pro-level behavior.
   * Strategic Role:
   * - Powers trial conversion and tier awareness.
   * - Scalable for persona-specific nudges and usage thresholds.
   * - Extensible for banners, modals, and email triggers.
   */
  useEffect(() => {
    const checkNudge = async () => {
      try {
        const response = await fetch(`http://localhost:8000/api/v1/admin/users/${userId}/upgrade-nudge`, {
          headers: {
            Authorization: `Bearer ${localStorage.getItem("access_token")}`,
          },
        })
        const data = await response.json()
        setShouldNudge(data.should_nudge || false)
      } catch (err) {
        console.error("Failed to check upgrade nudge:", err)
      }
    }

    checkNudge()
  }, [userId])

  if (!shouldNudge) return null

  return (
    <div className="bg-yellow-100 border-l-4 border-yellow-500 text-yellow-900 p-4 mb-4 rounded">
      <p className="font-semibold">You're pushing the limits of the Free tier 🚀</p>
      <p className="text-sm">
        You’ve created multiple workflows and collaborated extensively. Unlock full access with Pro—advanced analytics, unlimited workflows, and media sync.
      </p>
      <a
        href="/upgrade"
        className="inline-block mt-2 px-3 py-1 bg-yellow-600 text-white rounded hover:bg-yellow-700 text-sm"
      >
        Upgrade to Pro
      </a>
    </div>
  )
}
