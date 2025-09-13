// frontend/src/components/analytics/CollaborationHeatmap.jsx

import { useEffect, useState } from "react"
import { HeatMapGrid } from "react-grid-heatmap"

export default function CollaborationHeatmap() {
  const [matrix, setMatrix] = useState({})
  const [userIds, setUserIds] = useState([])

  /**
   * Renders a heatmap of user-to-user collaboration frequency.
   * Strategic Role:
   * - Powers team analytics, silo detection, and upgrade targeting.
   * - Scalable for multi-tenant orgs and role segmentation.
   * - Extensible for governance scorecards and anomaly detection.
   */
  useEffect(() => {
    const fetchMatrix = async () => {
      try {
        const response = await fetch("http://localhost:8000/api/v1/admin/collaboration-matrix", {
          headers: {
            Authorization: `Bearer ${localStorage.getItem("access_token")}`,
          },
        })
        const data = await response.json()
        setMatrix(data.matrix || {})
        setUserIds(data.user_ids || [])
      } catch (err) {
        console.error("Failed to fetch collaboration matrix:", err)
      }
    }

    fetchMatrix()
  }, [])

  const getHeatmapData = () => {
    return userIds.map((rowId) =>
      userIds.map((colId) => {
        const pair = [rowId, colId].sort()
        const key = `${pair[0]}-${pair[1]}`
        return matrix[key] || 0
      })
    )
  }

  return (
    <div className="p-6 bg-white dark:bg-gray-900 rounded shadow max-w-6xl mx-auto">
      <h1 className="text-2xl font-bold mb-6 text-gray-900 dark:text-white">Collaboration Heatmap 🔥</h1>
      {userIds.length === 0 ? (
        <p className="text-gray-600 dark:text-gray-400">No collaboration data available.</p>
      ) : (
        <HeatMapGrid
          data={getHeatmapData()}
          xLabels={userIds}
          yLabels={userIds}
          cellRender={(value) => value && `${value}`}
          cellStyle={(value) => ({
            background: `rgba(59, 130, 246, ${value / 10})`,
            fontSize: "0.8rem",
            color: value > 5 ? "white" : "black",
          })}
        />
      )}
    </div>
  )
}
