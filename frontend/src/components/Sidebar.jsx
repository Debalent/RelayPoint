// frontend/src/components/Sidebar.jsx
// Premium collapsible sidebar navigation

import React, { useState } from 'react'

const NAV_ITEMS = [
  {
    section: 'Core',
    items: [
      { id: 'dashboard', label: 'Dashboard', icon: '⬛', badge: null },
      { id: 'tasks',     label: 'Task Board', icon: '◈',  badge: '12' },
      { id: 'workflows', label: 'Workflows',  icon: '⟳', badge: null },
    ],
  },
  {
    section: 'Operations',
    items: [
      { id: 'forecast',  label: 'Forecasting', icon: '📈', badge: null },
      { id: 'staff',     label: 'Staff Management', icon: '👥', badge: null },
      { id: 'alerts',    label: 'Alerts', icon: '🔔', badge: '3' },
    ],
  },
  {
    section: 'Insights',
    items: [
      { id: 'analytics', label: 'Analytics', icon: '◎', badge: null },
      { id: 'reports',   label: 'Reports',   icon: '📋', badge: null },
    ],
  },
  {
    section: 'Settings',
    items: [
      { id: 'integrations', label: 'Integrations', icon: '🔗', badge: null },
      { id: 'settings',     label: 'Settings',     icon: '⚙', badge: null },
    ],
  },
]

// SVG icon components for clean vector rendering
function IconDashboard() {
  return (
    <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <rect x="3" y="3" width="7" height="7"/><rect x="14" y="3" width="7" height="7"/>
      <rect x="14" y="14" width="7" height="7"/><rect x="3" y="14" width="7" height="7"/>
    </svg>
  )
}
function IconTasks() {
  return (
    <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <line x1="8" y1="6" x2="21" y2="6"/><line x1="8" y1="12" x2="21" y2="12"/>
      <line x1="8" y1="18" x2="21" y2="18"/><line x1="3" y1="6" x2="3.01" y2="6"/>
      <line x1="3" y1="12" x2="3.01" y2="12"/><line x1="3" y1="18" x2="3.01" y2="18"/>
    </svg>
  )
}
function IconWorkflow() {
  return (
    <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <circle cx="12" cy="5" r="3"/><path d="M12 8v8"/>
      <circle cx="7" cy="19" r="3"/><circle cx="17" cy="19" r="3"/>
      <path d="M12 16l-5 3"/><path d="M12 16l5 3"/>
    </svg>
  )
}
function IconForecast() {
  return (
    <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <polyline points="22 12 18 12 15 21 9 3 6 12 2 12"/>
    </svg>
  )
}
function IconStaff() {
  return (
    <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/>
      <circle cx="9" cy="7" r="4"/>
      <path d="M23 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/>
    </svg>
  )
}
function IconAlerts() {
  return (
    <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <path d="M18 8A6 6 0 0 0 6 8c0 7-3 9-3 9h18s-3-2-3-9"/>
      <path d="M13.73 21a2 2 0 0 1-3.46 0"/>
    </svg>
  )
}
function IconAnalytics() {
  return (
    <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <line x1="18" y1="20" x2="18" y2="10"/>
      <line x1="12" y1="20" x2="12" y2="4"/>
      <line x1="6" y1="20" x2="6" y2="14"/>
    </svg>
  )
}
function IconReports() {
  return (
    <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/>
      <polyline points="14 2 14 8 20 8"/><line x1="16" y1="13" x2="8" y2="13"/>
      <line x1="16" y1="17" x2="8" y2="17"/><polyline points="10 9 9 9 8 9"/>
    </svg>
  )
}
function IconIntegrations() {
  return (
    <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <path d="M10 13a5 5 0 0 0 7.54.54l3-3a5 5 0 0 0-7.07-7.07l-1.72 1.71"/>
      <path d="M14 11a5 5 0 0 0-7.54-.54l-3 3a5 5 0 0 0 7.07 7.07l1.71-1.71"/>
    </svg>
  )
}
function IconSettings() {
  return (
    <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <circle cx="12" cy="12" r="3"/>
      <path d="M19.07 4.93a10 10 0 0 1 0 14.14M4.93 4.93a10 10 0 0 0 0 14.14"/>
    </svg>
  )
}
function IconMenu() {
  return (
    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <line x1="3" y1="12" x2="21" y2="12"/><line x1="3" y1="6" x2="21" y2="6"/><line x1="3" y1="18" x2="21" y2="18"/>
    </svg>
  )
}
function IconChevron() {
  return (
    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <polyline points="15 18 9 12 15 6"/>
    </svg>
  )
}
function IconLogout() {
  return (
    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"/>
      <polyline points="16 17 21 12 16 7"/>
      <line x1="21" y1="12" x2="9" y2="12"/>
    </svg>
  )
}

const ICON_MAP = {
  dashboard:    <IconDashboard />,
  tasks:        <IconTasks />,
  workflows:    <IconWorkflow />,
  forecast:     <IconForecast />,
  staff:        <IconStaff />,
  alerts:       <IconAlerts />,
  analytics:    <IconAnalytics />,
  reports:      <IconReports />,
  integrations: <IconIntegrations />,
  settings:     <IconSettings />,
}

export default function Sidebar({ activeSection, onNavigate, onLogout, userEmail, collapsed, onToggleCollapse, className }) {
  const initials = userEmail
    ? userEmail.slice(0, 2).toUpperCase()
    : 'RP'

  return (
    <aside className={`rp-sidebar${collapsed ? ' collapsed' : ''}${className ? ' ' + className : ''}`}>
      {/* Logo */}
      <div className="rp-sidebar__logo">
        <div className="rp-logo-mark">R</div>
        {!collapsed && <span className="rp-logo-text">RelayPoint</span>}
      </div>

      {/* Navigation */}
      <nav className="rp-sidebar__nav">
        {NAV_ITEMS.map(({ section, items }) => (
          <div key={section} className="rp-nav-section">
            {!collapsed && (
              <div className="rp-nav-section__label">{section}</div>
            )}
            {items.map(item => (
              <button
                key={item.id}
                className={`rp-nav-item${activeSection === item.id ? ' active' : ''}`}
                onClick={() => onNavigate?.(item.id)}
                title={collapsed ? item.label : undefined}
                style={{
                  background: 'none',
                  border: 'none',
                  width: '100%',
                  textAlign: 'left',
                  cursor: 'pointer',
                  color: 'inherit',
                }}
              >
                <span className="rp-nav-item__icon">
                  {ICON_MAP[item.id]}
                </span>
                {!collapsed && (
                  <>
                    <span style={{ flex: 1 }}>{item.label}</span>
                    {item.badge && (
                      <span className="rp-nav-item__badge">{item.badge}</span>
                    )}
                  </>
                )}
              </button>
            ))}
          </div>
        ))}
      </nav>

      {/* Footer: user + collapse toggle */}
      <div className="rp-sidebar__footer">
        <div className="rp-user-chip">
          <div className="rp-avatar">{initials}</div>
          {!collapsed && (
            <div style={{ flex: 1, overflow: 'hidden' }}>
              <div className="truncate text-sm fw-600" style={{ color: 'var(--rp-text-primary)' }}>
                {userEmail || 'Hotel Manager'}
              </div>
              <div className="text-xs" style={{ color: 'var(--rp-text-muted)' }}>Admin</div>
            </div>
          )}
          {!collapsed && (
            <button
              className="rp-icon-btn"
              onClick={onLogout}
              title="Sign out"
              style={{ background: 'none', border: 'none', cursor: 'pointer', color: 'var(--rp-text-muted)' }}
            >
              <IconLogout />
            </button>
          )}
        </div>
        <button
          onClick={onToggleCollapse}
          style={{
            marginTop: '8px',
            width: '100%',
            display: 'flex',
            alignItems: 'center',
            justifyContent: collapsed ? 'center' : 'flex-end',
            padding: '6px',
            background: 'none',
            border: 'none',
            cursor: 'pointer',
            color: 'var(--rp-text-muted)',
            borderRadius: 'var(--r-sm)',
            transition: 'color var(--t-fast)',
          }}
          onMouseEnter={e => e.currentTarget.style.color = 'var(--rp-text-primary)'}
          onMouseLeave={e => e.currentTarget.style.color = 'var(--rp-text-muted)'}
          title={collapsed ? 'Expand sidebar' : 'Collapse sidebar'}
        >
          <span style={{ transform: collapsed ? 'rotate(180deg)' : 'none', display: 'flex' }}>
            <IconChevron />
          </span>
        </button>
      </div>
    </aside>
  )
}

export { IconMenu }
