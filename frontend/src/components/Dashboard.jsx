// frontend/src/components/Dashboard.jsx

import React from 'react'
import useAuth from '../hooks/useAuth'
import ForecastCardWeb from './hospitality/ForecastCardWeb'
import ForecastAdmin from './hospitality/ForecastAdmin'
export default function Dashboard() {
  const { logout } = useAuth()

  return (
    <div className="max-w-3xl mx-auto p-6 bg-white dark:bg-gray-800 rounded shadow">
      <h1 className="text-2xl font-bold mb-4 text-gray-900 dark:text-white">
        Welcome to RelayPoint
      </h1>
      <p className="text-gray-700 dark:text-gray-300 mb-6">
        This is your secure dashboard. Future modules will include automation workflows,
        real-time collaboration, and user analytics.
      </p>

      {/* Forecast card integration */}
      <div className="mb-6">
        <ForecastCardWeb propertyId={1} role={'housekeeping'} />
      </div>

      {/* Admin models (visible to admins) */}
      <div className="mb-6">
        <ForecastAdmin />
      </div>

      <button
        onClick={logout}
        className="bg-red-600 text-white px-4 py-2 rounded hover:bg-red-700"
      >
        Log Out
      </button>
    </div>
  )
}
