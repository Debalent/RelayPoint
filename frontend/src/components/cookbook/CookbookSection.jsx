// frontend/src/components/cookbook/CookbookSection.jsx

import { useEffect, useState } from "react"
import { useParams } from "react-router-dom"

export default function CookbookSection() {
  const { sectionId } = useParams()
  const [section, setSection] = useState(null)

  /**
   * Renders a cookbook section with strategy notes and code snippets.
   * Strategic Role:
   * - Powers developer onboarding, analogical learning, and framework reuse.
   * - Scalable for markdown rendering, contributor mode, and public docs.
   * - Extensible for search, tagging, and export logic.
   */
  useEffect(() => {
    const fetchSection = async () => {
      try {
        const response = await fetch(`/static/cookbook/${sectionId}.json`)
        const data = await response.json()
        setSection(data)
      } catch (err) {
        console.error("Failed to load cookbook section:", err)
      }
    }

    fetchSection()
  }, [sectionId])

  if (!section) return <p className="text-gray-600 dark:text-gray-400">Loading section...</p>

  return (
    <div className="p-6 bg-white dark:bg-gray-900 rounded shadow max-w-4xl mx-auto">
      <h1 className="text-2xl font-bold mb-4 text-gray-900 dark:text-white">{section.title} 📘</h1>
      <p className="text-gray-700 dark:text-gray-300 mb-6">{section.description}</p>

      {section.examples?.map((example, idx) => (
        <div key={idx} className="mb-6">
          <h2 className="text-lg font-semibold text-gray-800 dark:text-gray-200">{example.title}</h2>
          <p className="text-sm text-gray-600 dark:text-gray-400 mb-2">{example.analogy}</p>
          <pre className="bg-gray-100 dark:bg-gray-800 p-4 rounded text-sm overflow-x-auto">
            <code>{example.code}</code>
          </pre>
          <p className="text-xs text-gray-500 dark:text-gray-400 mt-1">{example.notes}</p>
        </div>
      ))}
    </div>
  )
}
