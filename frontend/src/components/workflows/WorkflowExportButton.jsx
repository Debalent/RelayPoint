// frontend/src/components/workflows/WorkflowExportButton.jsx

export default function WorkflowExportButton({ workflowId }) {
  /**
   * Triggers export of a workflow as a reusable JSON template.
   * Strategic Role:
   * - Powers modular reuse, onboarding acceleration, and investor demos.
   * - Scalable for template libraries, branded exports, and tiered access.
   */
  const handleExport = async () => {
    try {
      const response = await fetch(`http://localhost:8000/api/v1/admin/workflow/${workflowId}/export`, {
        headers: {
          Authorization: `Bearer ${localStorage.getItem("access_token")}`,
        },
      })

      const blob = await response.blob()
      const url = window.URL.createObjectURL(blob)
      const link = document.createElement("a")
      link.href = url
      link.download = `workflow-${workflowId}-template.json`
      document.body.appendChild(link)
      link.click()
      link.remove()
    } catch (err) {
      console.error("Export failed:", err)
    }
  }

  return (
    <button
      onClick={handleExport}
      className="px-3 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 text-sm"
    >
      Export as Template
    </button>
  )
}
