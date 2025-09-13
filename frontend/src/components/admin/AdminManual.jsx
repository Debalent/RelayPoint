// frontend/src/components/admin/AdminManual.jsx

import { useState } from "react"

export default function AdminManual() {
  const [activeSection, setActiveSection] = useState("overview")

  const sections = {
    overview: {
      title: "🧭 Overview & Access",
      content: `
        The Admin Console provides governance, user management, and workflow oversight.
        Only users with the 'admin' role can access this panel.
        Use the sidebar to navigate between modules like Users, Workflows, Audit Logs, and Analytics.
      `
    },
    users: {
      title: "👥 User Management",
      content: `
        - View all users via the Users tab.
        - Edit roles using the Role Editor dropdown.
        - Role changes are logged in the Audit Log Viewer.
        - Future: Invite users with preset roles and onboarding flows.
      `
    },
    workflows: {
      title: "📂 Workflow Oversight",
      content: `
        - Monitor total workflows, completion rates, and active projects.
        - Edit workflow metadata (e.g. name, steps) via the Workflow Editor.
        - All edits are logged for governance and analytics.
      `
    },
    audit: {
      title: "📜 Audit Logs",
      content: `
        - View all governance events: role changes, workflow edits, logins, and permission updates.
        - Filter logs by date, action type, or user ID.
        - Export logs as CSV for compliance or investor reporting.
      `
    },
    login: {
      title: "🔐 Login Activity",
      content: `
        - Track who accessed the system and when.
        - Login events are logged automatically after authentication.
        - Future: Add IP, device, and geo metadata for deeper insight.
      `
    },
    permissions: {
      title: "🔑 Permissions",
      content: `
        - Admins can grant or revoke access to resources.
        - Permission changes are logged with resource and role metadata.
        - Future: Add permission history viewer and alerts for risky changes.
      `
    },
    reporting: {
      title: "📊 Reporting & Analytics",
      content: `
        - Export audit logs with presets like 'Investor Snapshot' or 'Compliance Summary'.
        - Visualize governance trends with charts and heatmaps.
        - Future: Add dashboards for role velocity, login frequency, and workflow adoption.
      `
    },
    support: {
      title: "🛠 Troubleshooting & Support",
      content: `
        - Common issues: role update failures, missing audit logs, login errors.
        - Check browser console or network tab for API errors.
        - Contact support or submit feedback via the Help tab (coming soon).
      `
    }
  }

  return (
    <div className="p-6 bg-white dark:bg-gray-900 rounded shadow max-w-5xl mx-auto">
      <h1 className="text-2xl font-bold mb-6 text-gray-900 dark:text-white">Admin Manual 📘</h1>

      <div className="flex flex-wrap gap-2 mb-4">
        {Object.keys(sections).map((key) => (
          <button
            key={key}
            onClick={() => setActiveSection(key)}
            className={`px-3 py-2 rounded text-sm font-medium ${
              activeSection === key ? "bg-blue-600 text-white" : "bg-gray-200 dark:bg-gray-700 text-gray-800 dark:text-gray-200"
            }`}
          >
            {sections[key].title}
          </button>
        ))}
      </div>

      <div className="bg-gray-50 dark:bg-gray-800 p-4 rounded text-gray-700 dark:text-gray-300 whitespace-pre-line">
        {sections[activeSection].content}
      </div>
    </div>
  )
}
