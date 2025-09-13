// frontend/src/components/feedback/SafetySignalForm.jsx

import { useState } from "react"

export default function SafetySignalForm({ workflowId }) {
  const [clarity, setClarity] = useState(3)
  const [trust, setTrust] = useState(3)
  const [collaboration, setCollaboration] = useState(3)
  const [submitted, setSubmitted] = useState(false)

  /**
   * Captures psychological safety signals for a workflow.
   * Strategic Role:
   * - Powers team health metrics, onboarding refinement, and contributor retention.
   * - Scalable for org benchmarking, role segmentation, and coaching prompts.
   * - Extensible for scorecards, alerts, and feedback loops.
   */
  const handleSubmit = async () => {
    try {
      await fetch(`/api/v1/workflows/${workflowId}/safety-signals`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${localStorage.getItem("access_token")}`,
        },
        body: JSON.stringify({ clarity, trust, collaboration }),
      })
      setSubmitted(true)
    } catch (err) {
      console.error("Failed to submit safety signals:", err)
    }
  }

  if (submitted) {
    return (
      <div className="bg-green-100 border-l-4 border-green-500 text-green-900 p-4 rounded">
        Thanks for your feedback! Your signal helps improve team health and workflow clarity.
      </div>
    )
  }

  return (
    <div className="p-6 bg-white dark:bg-gray-900 rounded shadow max-w-xl mx-auto">
      <h2 className="text-xl font-bold mb-4 text-gray-900 dark:text-white">Workflow Feedback 🧠</h2>
      <p className="text-sm text-gray-600 dark:text-gray-400 mb-4">
        Rate this workflow on clarity, trust, and collaboration. Your feedback helps improve team dynamics.
      </p>

      <div className="space-y-4">
        <RatingSlider label="Clarity of Instructions" value={clarity} onChange={setClarity} />
        <RatingSlider label="Trust in Team Roles" value={trust} onChange={setTrust} />
        <RatingSlider label="Collaboration Experience" value={collaboration} onChange={setCollaboration} />
      </div>

      <button
        onClick={handleSubmit}
        className="mt-6 px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 text-sm"
      >
        Submit Feedback
      </button>
    </div>
  )
}

function RatingSlider({ label, value, onChange }) {
  return (
    <div>
      <label className="block text-gray-800 dark:text-gray-200 mb-1">{label}</label>
      <input
        type="range"
        min="1"
        max="5"
        value={value}
        onChange={(e) => onChange(Number(e.target.value))}
        className="w-full"
      />
      <div className="text-xs text-gray-500 dark:text-gray-400 mt-1">Rating: {value}/5</div>
    </div>
  )
}
