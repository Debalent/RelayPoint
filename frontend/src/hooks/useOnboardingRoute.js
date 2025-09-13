// frontend/src/hooks/useOnboardingRoute.js

export default function useOnboardingRoute(user) {
  /**
   * Determines onboarding route based on user persona.
   * Strategic Role:
   * - Powers personalized onboarding flows.
   * - Scalable for multi-role, multi-tier platforms.
   * - Extensible for branded experiences and trial nudges.
   */
  if (!user) return "/onboarding/default"

  const { role, tier } = user

  if (role === "artist" && tier === "free") return "/onboarding/artist-lite"
  if (role === "artist" && tier !== "free") return "/onboarding/artist-pro"
  if (role === "producer") return "/onboarding/producer"
  if (role === "collaborator") return "/onboarding/collaborator"
  if (role === "admin") return "/admin/manual"

  return "/onboarding/default"
}
