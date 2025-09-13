// frontend/src/routes/DashboardRouter.jsx

import { useEffect, useState } from "react"
import ProducerDashboard from "../components/dashboards/ProducerDashboard"
import ArtistDashboard from "../components/dashboards/ArtistDashboard"
import CollaboratorDashboard from "../components/dashboards/CollaboratorDashboard"
import AdminDashboard from "../components/admin/AdminDashboard"

export default function DashboardRouter() {
  const [persona, setPersona] = useState(null)

  /**
   * Routes user to the appropriate dashboard based on their persona.
   * Powers personalized UX, feature access, and strategic visibility.
   *
   * Strategic Role:
   * - Aligns dashboard content with user goals and responsibilities.
   * - Scalable for multi-tenant orgs, tiered pricing, and branded layouts.
   * - Extensible for analytics, upsells, and role-based modules.
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

  if (!persona) return <p className="text-gray-500">Loading dashboard...</p>

  switch (persona) {
    case "producer":
      return <ProducerDashboard />
    case "artist":
      return <ArtistDashboard />
    case "admin":
      return <AdminDashboard />
    default:
      return <CollaboratorDashboard />
  }
}
