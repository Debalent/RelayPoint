// frontend/src/App.jsx
// RelayPoint Web Shell — Premium enterprise layout

import React, { useState } from 'react'
import './index.css'   // ← design system (was missing — this was root cause of unstyled UI)
import './App.css'
import LoginForm from './components/LoginForm'
import Dashboard from './components/Dashboard'
import Sidebar, { IconMenu } from './components/Sidebar'
import useAuth from './hooks/useAuth'

// Search icon
function IconSearch() {
  return (
    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/>
    </svg>
  )
}

// Bell icon
function IconBell() {
  return (
    <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <path d="M18 8A6 6 0 0 0 6 8c0 7-3 9-3 9h18s-3-2-3-9"/>
      <path d="M13.73 21a2 2 0 0 1-3.46 0"/>
    </svg>
  )
}

// Plus icon
function IconPlus() {
  return (
    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round">
      <line x1="12" y1="5" x2="12" y2="19"/><line x1="5" y1="12" x2="19" y2="12"/>
    </svg>
  )
}

const PAGE_TITLES = {
  dashboard:    'Dashboard',
  tasks:        'Task Board',
  workflows:    'Workflows',
  forecast:     'Staff Forecasting',
  staff:        'Staff Management',
  alerts:       'Alerts & Notifications',
  analytics:    'Analytics',
  reports:      'Reports',
  integrations: 'Integrations',
  settings:     'Settings',
}

export default function App() {
  const { isAuthenticated, logout, token } = useAuth()
  const [activeSection, setActiveSection] = useState('dashboard')
  const [sidebarCollapsed, setSidebarCollapsed] = useState(false)
  const [mobileSidebarOpen, setMobileSidebarOpen] = useState(false)

  // ── Not authenticated → show login ──────────────────────────────────────
  if (!isAuthenticated) {
    return <LoginForm />
  }

  // ── Authenticated app shell ───────────────────────────────────────────────
  return (
    <div className="rp-layout">
      {/* Mobile overlay */}
      {mobileSidebarOpen && (
        <div
          onClick={() => setMobileSidebarOpen(false)}
          style={{
            position: 'fixed', inset: 0, background: 'rgba(0,0,0,0.6)',
            zIndex: 199, backdropFilter: 'blur(4px)',
          }}
        />
      )}

      {/* Sidebar */}
      <Sidebar
        activeSection={activeSection}
        onNavigate={(id) => { setActiveSection(id); setMobileSidebarOpen(false) }}
        onLogout={logout}
        userEmail={null}
        collapsed={sidebarCollapsed}
        onToggleCollapse={() => setSidebarCollapsed(v => !v)}
        className={mobileSidebarOpen ? 'mobile-open' : ''}
      />

      {/* Main area */}
      <div className={`rp-main${sidebarCollapsed ? ' sidebar-collapsed' : ''}`}>

        {/* Topbar */}
        <header className="rp-topbar">
          {/* Mobile hamburger */}
          <button
            className="rp-icon-btn"
            onClick={() => setMobileSidebarOpen(v => !v)}
            style={{ display: 'none' }}
            aria-label="Toggle menu"
          >
            <IconMenu />
          </button>

          {/* Page breadcrumb */}
          <div style={{ display: 'flex', alignItems: 'center', gap: 'var(--space-3)' }}>
            <span style={{ color: 'var(--rp-text-muted)', fontSize: '0.8rem' }}>RelayPoint</span>
            <span style={{ color: 'var(--rp-text-muted)', fontSize: '0.7rem' }}>›</span>
            <span style={{ color: 'var(--rp-text-primary)', fontSize: '0.875rem', fontWeight: 600 }}>
              {PAGE_TITLES[activeSection] || 'Dashboard'}
            </span>
          </div>

          {/* Search */}
          <div className="rp-topbar__search">
            <span style={{ color: 'var(--rp-text-muted)', display: 'flex' }}>
              <IconSearch />
            </span>
            <input type="text" placeholder="Search tasks, workflows…" />
            <kbd style={{
              fontSize: '0.65rem', color: 'var(--rp-text-muted)',
              background: 'rgba(255,255,255,0.06)', padding: '2px 5px',
              borderRadius: '4px', border: '1px solid var(--rp-border)',
              fontFamily: 'inherit',
            }}>⌘K</kbd>
          </div>

          {/* Actions */}
          <div className="rp-topbar__actions">
            <button className="rp-btn rp-btn--primary rp-btn--sm">
              <IconPlus /> New Task
            </button>
            <div className="rp-notif-bell">
              <button className="rp-icon-btn" aria-label="Notifications">
                <IconBell />
              </button>
              <span className="rp-notif-badge">3</span>
            </div>
            <div className="rp-avatar" style={{ cursor: 'pointer', width: 32, height: 32, flexShrink: 0 }}>
              HS
            </div>
          </div>
        </header>

        {/* Page content */}
        <main className="rp-content">
          {activeSection === 'dashboard' && <Dashboard onNavigate={setActiveSection} />}
          {activeSection !== 'dashboard' && (
            <PlaceholderPage section={activeSection} />
          )}
        </main>

      </div>
    </div>
  )
}

// Placeholder for sections not yet built
function PlaceholderPage({ section }) {
  return (
    <div className="animate-fadeInUp">
      <div className="rp-page-header">
        <h1>{PAGE_TITLES[section] || section}</h1>
        <p style={{ marginTop: 'var(--space-2)' }}>
          This module is coming soon. Configure it via Settings.
        </p>
      </div>
      <div className="rp-card">
        <div className="rp-card__body" style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', minHeight: 240 }}>
          <div style={{ textAlign: 'center' }}>
            <div style={{
              width: 64, height: 64, borderRadius: 'var(--r-xl)',
              background: 'var(--rp-gradient-card)', border: '1px solid var(--rp-border)',
              display: 'flex', alignItems: 'center', justifyContent: 'center',
              fontSize: '1.75rem', margin: '0 auto var(--space-4)',
            }}>🚀</div>
            <div className="fw-700" style={{ fontSize: '1.125rem', marginBottom: 'var(--space-2)' }}>
              {PAGE_TITLES[section]} Coming Soon
            </div>
            <p style={{ maxWidth: 360 }}>
              This module is under active development for the RelayPoint pilot program.
            </p>
          </div>
        </div>
      </div>
    </div>
  )
}
