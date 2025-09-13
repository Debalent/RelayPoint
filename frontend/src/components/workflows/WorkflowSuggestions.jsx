// frontend/src/components/workflows/WorkflowSuggestions.jsx

import { useEffect, useState } from "react"

export default function WorkflowSuggestions({ userId }) {
  const [suggestions, setSuggestions] = useState([])

  /**
   * Displays AI-powered workflow suggestions based on user behavior.
   * Strategic Role:
   * - Powers smart onboarding, template reuse, and upgrade nudges.
   * - Scalable for role-based suggestions, tier awareness, and media sync.
   * - Extensible for quick-start buttons, preview cards, and persona routing.
   */
  useEffect(() => {
    const fetchSuggestions = async () => {
      try {
        const response = await fetch(`http://localhost:8000/api/v1/admin/users/${userId}/suggestions`, {
          headers: {
            Authorization: `Bearer ${localStorage.getItem("access_token")}`,
          },
        })
        const data = await response.json()
        setSuggestions(data || [])
      } catch (err) {
        console.error("Failed to fetch workflow suggestions:", err)
      }
    }

    fetchSuggestions()
  }, [userId])

  return (
    <div className="p-6 bg-white dark:bg-gray-900 rounded shadow max-w-4xl mx-auto">
      <h2 className="text-xl font-bold mb-4 text-gray-900 dark:text-white">Suggested Workflows 🤖</h2>

      {suggestions.length === 0 ? (
        <p className="text-gray-600 dark:text-gray-400">No suggestions available yet.</p>
      ) : (
        <ul className="space-y-4">
          {suggestions.map((wf) => (
            <li key={wf.id} className="border p-4 rounded bg-gray-50 dark:bg-gray-800">
              <h3 className="text-lg font-semibold text-gray-800 dark:text-gray-200">{wf.name}</h3>
              <p className="text-sm text-gray-600 dark:text-gray-400 mb-2">{wf.description}</p>
              <ul className="list-disc pl-5 text-sm text-gray-700 dark:text-gray-300">
                {wf.steps.map((step, idx) => (
                  <li key={idx}>{step}</li>
                ))}
              </ul>
              <button className="mt-3 px-3 py-1 bg-blue-600 text-white rounded hover:bg-blue-700 text-sm">
                Start This Workflow
              </button>
            </li>
          ))}
        </ul>
      )}
    </div>
  )
}
