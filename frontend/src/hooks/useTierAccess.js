// frontend/src/hooks/useTierAccess.js

import { useEffect, useState } from "react"

export default function useTierAccess(requiredTier = "pro") {
  const [hasAccess, setHasAccess] = useState(false)

  /**
   * Checks if the current user meets the required tier.
   * Powers feature gating across components.
   *
   * Strategic Role:
   * - Enables monetization logic and upsell prompts.
   * - Scalable for multi-tier platforms and role-based UX.
   * - Extensible for usage caps, trial logic, and upgrade nudges.
   */
  useEffect(() => {
    const userData = JSON.parse(localStorage.getItem("user_profile"))
    const tierOrder = ["free", "pro", "enterprise"]

    if (userData?.tier) {
      const userTierIndex = tierOrder.indexOf(userData.tier)
      const requiredTierIndex = tierOrder.indexOf(requiredTier)
      setHasAccess(userTierIndex >= requiredTierIndex)
    }
  }, [requiredTier])

  return hasAccess
}
