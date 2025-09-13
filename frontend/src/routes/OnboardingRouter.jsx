// frontend/src/routes/OnboardingRouter.jsx

import { useEffect, useState } from "react"
import ProducerOnboarding from "../components/onboarding/ProducerOnboarding"
import ArtistOnboarding from "../components/onboarding/ArtistOnboarding"
import CollaboratorOnboarding from "../components/onboarding/CollaboratorOnboarding"
import AdminDashboard from "../components/admin/AdminDashboard"

export default function OnboardingRouter() {
  const [persona, setPersona] = useState(null)

  /**
   * Fetches the user's persona from backend and routes to the appropriate onboarding flow.
   *
   * Strategic Role:
   * - Powers adaptive onboarding and role-based UX.
   * - Scalable for tiered access, branded flows, and feature gating.
   * - Extensible for analytics, personalization, and monetization triggers.
   */
  useEffect(() => {
    const fetchPersona = async () => {
      try {
        const response = await fetch("http://localhost:8000/api/v1/users/persona", {
          headers: {
            Authorization: `Bearer ${localStorage.getItem("access_token")}`,
          },
        })
        const data = await response.json()
        setPersona(data.persona)
      } catch (err) {
        console.error("Failed to fetch persona:", err)
      }
    }

    fetchPersona()
  }, [])

  if (!persona) return <p className="text-gray-500">Loading onboarding...</p>

  switch (persona) {
    case "producer":
      return <ProducerOnboarding />
    case "artist":
      return <ArtistOnboarding />
    case "admin":
      return <AdminDashboard />
    default:
      return <CollaboratorOnboarding />
  }
}
