// frontend/src/components/admin/AuditLogExportButton.jsx

export default function AuditLogExportButton() {
  /**
   * Triggers CSV download of audit logs from backend.
   * Connects governance data to investor reporting and compliance workflows.
   *
   * Strategic Role:
   * - Powers exportability of role changes and admin actions.
   * - Scalable for enterprise audits, investor decks, and multi-tenant orgs.
   * - Extensible for time filters, persona segmentation, and external integrations.
   */
  const handleExport = async () => {
    try {
      const response = await fetch("http://localhost:8000/api/v1/admin/audit-logs/export", {
        headers: {
          Authorization: `Bearer ${localStorage.getItem("access_token")}`,
        },
      })

      if (!response.ok) throw new Error("Export failed")

      const blob = await response.blob()
      const url = window.URL.createObjectURL(blob)
      const link = document.createElement("a")
      link.href = url
      link.download = "audit_logs.csv"
      document.body.appendChild(link)
      link.click()
      document.body.removeChild(link)
    } catch (err) {
      console.error("Audit log export error:", err)
    }
  }

  return (
    <button
      onClick={handleExport}
      className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700"
    >
      Download Audit Logs
    </button>
  )
}
