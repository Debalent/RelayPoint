// frontend/src/components/Dashboard.jsx
// RelayPoint — Premium Enterprise Dashboard

import React, { useState, useEffect } from 'react'
import ForecastCardWeb from './hospitality/ForecastCardWeb'

/* ── Inline SVG icons ────────────────────────────────────────────────────────── */
const Ico = {
  Check: () => (
    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round">
      <polyline points="20 6 9 17 4 12"/>
    </svg>
  ),
  Clock: () => (
    <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/>
    </svg>
  ),
  Alert: () => (
    <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"/>
      <line x1="12" y1="9" x2="12" y2="13"/><line x1="12" y1="17" x2="12.01" y2="17"/>
    </svg>
  ),
  Trend: () => (
    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <polyline points="23 6 13.5 15.5 8.5 10.5 1 18"/><polyline points="17 6 23 6 23 12"/>
    </svg>
  ),
  Tasks: () => (
    <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <path d="M9 11l3 3L22 4"/><path d="M21 12v7a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11"/>
    </svg>
  ),
  Star: () => (
    <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor" stroke="none">
      <polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/>
    </svg>
  ),
  Refresh: () => (
    <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <polyline points="23 4 23 10 17 10"/><polyline points="1 20 1 14 7 14"/>
      <path d="M3.51 9a9 9 0 0 1 14.85-3.36L23 10M1 14l4.64 4.36A9 9 0 0 0 20.49 15"/>
    </svg>
  ),
  Dot: ({ color }) => (
    <svg width="8" height="8" viewBox="0 0 8 8"><circle cx="4" cy="4" r="4" fill={color} /></svg>
  ),
}

/* ── KPI Metrics data ────────────────────────────────────────────────────────── */
const KPI_METRICS = [
  {
    id: 'tasks',
    label: 'Tasks Completed Today',
    value: '47',
    delta: '+12%',
    positive: true,
    icon: '✓',
    iconBg: 'rgba(16,185,129,0.15)',
    iconColor: '#10b981',
    accent: 'linear-gradient(135deg, #10b981, #059669)',
    sub: '8 still pending',
  },
  {
    id: 'rooms',
    label: 'Rooms Ready',
    value: '84%',
    delta: '+6pts',
    positive: true,
    icon: '🏨',
    iconBg: 'rgba(16,128,208,0.15)',
    iconColor: 'var(--rp-indigo)',
    accent: 'linear-gradient(135deg, #003080, #1080D0)',
    sub: '136 / 162 rooms',
  },
  {
    id: 'response',
    label: 'Avg Response Time',
    value: '4.2m',
    delta: '-1.8m',
    positive: true,
    icon: '⚡',
    iconBg: 'rgba(245,158,11,0.15)',
    iconColor: '#f59e0b',
    accent: 'linear-gradient(135deg, #f59e0b, #d97706)',
    sub: 'vs 6.0m last week',
  },
  {
    id: 'score',
    label: 'Guest Satisfaction',
    value: '4.8',
    delta: '+0.2',
    positive: true,
    icon: '★',
    iconBg: 'rgba(236,72,153,0.12)',
    iconColor: '#ec4899',
    accent: 'linear-gradient(135deg, #ec4899, #db2777)',
    sub: 'Based on 38 reviews',
  },
]

/* ── Recent tasks ──────────────────────────────────────────────────────────── */
const RECENT_TASKS = [
  { id: 1, title: 'Deep clean Room 412 — checkout',   dept: 'Housekeeping', priority: 'urgent',  status: 'in-progress', ago: '5m ago' },
  { id: 2, title: 'Fix AC unit in Room 308',           dept: 'Maintenance',  priority: 'high',    status: 'pending',     ago: '12m ago' },
  { id: 3, title: 'Extra towels to Room 220',          dept: 'Housekeeping', priority: 'medium',  status: 'completed',   ago: '18m ago' },
  { id: 4, title: 'Table 7 reservation — dietary req', dept: 'F&B',          priority: 'medium',  status: 'pending',     ago: '24m ago' },
  { id: 5, title: 'Lost & found: laptop bag lobby',    dept: 'Front Desk',   priority: 'low',     status: 'completed',   ago: '31m ago' },
  { id: 6, title: 'VIP arrival prep — Suite 604',      dept: 'Front Desk',   priority: 'urgent',  status: 'in-progress', ago: '45m ago' },
]

/* ── Department health ─────────────────────────────────────────────────────── */
const DEPT_HEALTH = [
  { name: 'Housekeeping', pct: 88, active: 12, color: '#1080D0' },
  { name: 'Maintenance',  pct: 72, active: 5,  color: '#f59e0b' },
  { name: 'F&B',          pct: 95, active: 18, color: '#10b981' },
  { name: 'Front Desk',   pct: 91, active: 8,  color: '#2DB580' },
]

/* ── Alerts ────────────────────────────────────────────────────────────────── */
const ALERTS = [
  { id: 1, msg: 'Room 308 AC — escalated 2×. Maintenance dispatch needed.', level: 'danger',  time: '2m ago' },
  { id: 2, msg: 'Suite 604 VIP arrival in 45 min. Pre-arrival checklist unconfirmed.', level: 'warning', time: '8m ago' },
  { id: 3, msg: 'Forecasted occupancy spike Fri–Sun. Recommend +4 HK staff.', level: 'info',   time: '1h ago' },
]

/* ── Priority badge config ─────────────────────────────────────────────────── */
const PRIORITY_CFG = {
  urgent: { cls: 'rp-badge--danger',   label: 'Urgent' },
  high:   { cls: 'rp-badge--warning',  label: 'High' },
  medium: { cls: 'rp-badge--info',     label: 'Medium' },
  low:    { cls: 'rp-badge--neutral',  label: 'Low' },
}

const STATUS_CFG = {
  'in-progress': { color: '#1080D0', label: 'In Progress' },
  'pending':     { color: '#f59e0b', label: 'Pending' },
  'completed':   { color: '#10b981', label: 'Done' },
}

const LEVEL_CLS = {
  danger:  'rp-badge--danger',
  warning: 'rp-badge--warning',
  info:    'rp-badge--info',
}

/* ═══════════════════════════════════════════════════════════════════════════
   Dashboard Component
   ═══════════════════════════════════════════════════════════════════════════ */
export default function Dashboard({ onNavigate }) {
  const [time, setTime] = useState(new Date())
  const [activeTab, setActiveTab] = useState('tasks')

  // Live clock
  useEffect(() => {
    const t = setInterval(() => setTime(new Date()), 30000)
    return () => clearInterval(t)
  }, [])

  const fmtTime = time.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
  const fmtDate = time.toLocaleDateString([], { weekday: 'long', month: 'long', day: 'numeric' })

  return (
    <div className="animate-fadeInUp">

      {/* ── Page header ──────────────────────────────────────────────────── */}
      <div className="rp-page-header">
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', flexWrap: 'wrap', gap: 'var(--space-4)' }}>
          <div>
            <div className="rp-breadcrumb">
              <span>Feb 22, 2026</span>
              <span>·</span>
              <span style={{ color: '#10b981' }}>
                <span className="rp-dot pulse" style={{ background: '#10b981', marginRight: 4 }} />
                All systems operational
              </span>
            </div>
            <h1 style={{ marginBottom: 'var(--space-1)' }}>Good afternoon, Hotel Manager 👋</h1>
            <p style={{ margin: 0 }}>Here's your property overview for today — <strong style={{ color: 'var(--rp-text-primary)' }}>{fmtDate} · {fmtTime}</strong></p>
          </div>
          <div style={{ display: 'flex', gap: 'var(--space-3)', flexWrap: 'wrap' }}>
            <button className="rp-btn rp-btn--secondary rp-btn--sm">
              <Ico.Refresh /> Refresh
            </button>
            <button className="rp-btn rp-btn--primary rp-btn--sm" onClick={() => onNavigate?.('tasks')}>
              View all tasks →
            </button>
          </div>
        </div>
      </div>

      {/* ── Alerts banner ────────────────────────────────────────────────── */}
      {ALERTS.length > 0 && (
        <div style={{ display: 'flex', flexDirection: 'column', gap: 'var(--space-2)', marginBottom: 'var(--space-6)' }}>
          {ALERTS.map(a => (
            <div key={a.id} style={{
              display: 'flex', alignItems: 'center', gap: 'var(--space-3)',
              padding: 'var(--space-3) var(--space-5)',
              borderRadius: 'var(--r-lg)',
              background: a.level === 'danger'  ? 'rgba(239,68,68,0.08)'   :
                          a.level === 'warning' ? 'rgba(245,158,11,0.08)'  : 'rgba(99,102,241,0.08)',
              border: `1px solid ${a.level === 'danger' ? 'rgba(239,68,68,0.2)' : a.level === 'warning' ? 'rgba(245,158,11,0.2)' : 'rgba(99,102,241,0.2)'}`,
              fontSize: '0.875rem',
            }}>
              <span className={`rp-badge ${LEVEL_CLS[a.level]}`} style={{ fontSize: '0.65rem', whiteSpace: 'nowrap' }}>
                {a.level.toUpperCase()}
              </span>
              <span style={{ flex: 1, color: 'var(--rp-text-secondary)' }}>{a.msg}</span>
              <span className="text-xs" style={{ color: 'var(--rp-text-muted)', whiteSpace: 'nowrap' }}>{a.time}</span>
            </div>
          ))}
        </div>
      )}

      {/* ── KPI Cards ────────────────────────────────────────────────────── */}
      <div className="stagger-children" style={{ display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: 'var(--space-5)', marginBottom: 'var(--space-8)' }}>
        {KPI_METRICS.map(m => (
          <div key={m.id} className="rp-stat-card" style={{ '--card-accent': m.accent }}>
            <div style={{
              width: 44, height: 44, borderRadius: 'var(--r-lg)',
              background: m.iconBg, display: 'flex', alignItems: 'center', justifyContent: 'center',
              fontSize: '1.25rem', marginBottom: 'var(--space-4)', color: m.iconColor,
            }}>
              {m.icon}
            </div>
            <div className="rp-stat-card__value">{m.value}</div>
            <div className="rp-stat-card__label" style={{ marginBottom: 'var(--space-2)' }}>{m.label}</div>
            <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
              <span className={`rp-stat-card__delta${m.positive ? '' : ' negative'}`}>
                <Ico.Trend /> {m.delta} vs last week
              </span>
            </div>
            <div style={{ marginTop: 'var(--space-2)', fontSize: '0.75rem', color: 'var(--rp-text-muted)' }}>{m.sub}</div>
          </div>
        ))}
      </div>

      {/* ── Main content grid ────────────────────────────────────────────── */}
      <div style={{ display: 'grid', gridTemplateColumns: '1fr 320px', gap: 'var(--space-6)', marginBottom: 'var(--space-6)' }}>

        {/* Left: Tasks panel */}
        <div className="rp-card">
          <div className="rp-card__header">
            <div style={{ display: 'flex', alignItems: 'center', gap: 'var(--space-3)' }}>
              <div style={{
                width: 32, height: 32, background: 'rgba(99,102,241,0.15)',
                borderRadius: 'var(--r-md)', display: 'flex', alignItems: 'center',
                justifyContent: 'center', color: 'var(--rp-indigo)',
              }}><Ico.Tasks /></div>
              <div>
                <div className="fw-700" style={{ color: 'var(--rp-text-primary)' }}>Live Task Feed</div>
                <div className="text-xs" style={{ color: 'var(--rp-text-muted)' }}>Updates every 30 seconds</div>
              </div>
            </div>
            <div style={{ display: 'flex', gap: 'var(--space-2)' }}>
              {['tasks', 'alerts'].map(tab => (
                <button
                  key={tab}
                  onClick={() => setActiveTab(tab)}
                  className="rp-btn rp-btn--sm"
                  style={{
                    background: activeTab === tab ? 'rgba(99,102,241,0.15)' : 'transparent',
                    color: activeTab === tab ? 'var(--rp-indigo)' : 'var(--rp-text-muted)',
                    border: activeTab === tab ? '1px solid rgba(99,102,241,0.3)' : '1px solid transparent',
                    textTransform: 'capitalize',
                  }}
                >
                  {tab}
                </button>
              ))}
            </div>
          </div>
          <div className="rp-card__body" style={{ padding: 0 }}>
            <table className="rp-table">
              <thead>
                <tr>
                  <th>Task</th>
                  <th>Dept</th>
                  <th>Priority</th>
                  <th>Status</th>
                  <th>Time</th>
                </tr>
              </thead>
              <tbody>
                {RECENT_TASKS.map(task => {
                  const p = PRIORITY_CFG[task.priority]
                  const s = STATUS_CFG[task.status]
                  return (
                    <tr key={task.id} style={{ cursor: 'pointer' }}>
                      <td style={{ maxWidth: 220 }}>
                        <span className="truncate fw-500" style={{
                          display: 'block', color: 'var(--rp-text-primary)', fontSize: '0.875rem',
                        }}>{task.title}</span>
                      </td>
                      <td>
                        <span className="rp-badge rp-badge--neutral" style={{ fontSize: '0.65rem' }}>
                          {task.dept}
                        </span>
                      </td>
                      <td>
                        <span className={`rp-badge ${p.cls}`} style={{ fontSize: '0.65rem' }}>
                          {p.label}
                        </span>
                      </td>
                      <td>
                        <span style={{ display: 'flex', alignItems: 'center', gap: 5, fontSize: '0.8rem', color: s.color, fontWeight: 600 }}>
                          <Ico.Dot color={s.color} />
                          {s.label}
                        </span>
                      </td>
                      <td>
                        <span className="text-xs" style={{ color: 'var(--rp-text-muted)', display: 'flex', alignItems: 'center', gap: 3 }}>
                          <Ico.Clock />{task.ago}
                        </span>
                      </td>
                    </tr>
                  )
                })}
              </tbody>
            </table>
          </div>
          <div className="rp-card__footer" style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
            <span className="text-xs" style={{ color: 'var(--rp-text-muted)' }}>Showing 6 of 55 active tasks</span>
            <button
              className="rp-btn rp-btn--ghost rp-btn--sm"
              onClick={() => onNavigate?.('tasks')}
            >
              View all tasks →
            </button>
          </div>
        </div>

        {/* Right: Dept health + sidebar panels */}
        <div style={{ display: 'flex', flexDirection: 'column', gap: 'var(--space-5)' }}>

          {/* Department Health */}
          <div className="rp-card">
            <div className="rp-card__header">
              <div className="fw-700" style={{ color: 'var(--rp-text-primary)', fontSize: '0.9rem' }}>Department Health</div>
              <span className="rp-badge rp-badge--success">
                <span className="rp-dot pulse" />
                Live
              </span>
            </div>
            <div className="rp-card__body">
              {DEPT_HEALTH.map(d => (
                <div key={d.name} style={{ marginBottom: 'var(--space-4)' }}>
                  <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: 'var(--space-1)' }}>
                    <span className="text-sm fw-500" style={{ color: 'var(--rp-text-primary)' }}>{d.name}</span>
                    <div style={{ display: 'flex', alignItems: 'center', gap: 'var(--space-3)' }}>
                      <span className="text-xs" style={{ color: 'var(--rp-text-muted)' }}>{d.active} active</span>
                      <span className="fw-700 text-sm" style={{ color: d.color }}>{d.pct}%</span>
                    </div>
                  </div>
                  <div className="rp-progress">
                    <div className="rp-progress__fill" style={{
                      width: `${d.pct}%`,
                      background: d.color,
                    }} />
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Quick actions */}
          <div className="rp-card">
            <div className="rp-card__header">
              <div className="fw-700" style={{ color: 'var(--rp-text-primary)', fontSize: '0.9rem' }}>Quick Actions</div>
            </div>
            <div className="rp-card__body" style={{ display: 'flex', flexDirection: 'column', gap: 'var(--space-2)' }}>
              {[
                { label: 'Create Task', icon: '➕', color: 'var(--rp-indigo)' },
                { label: 'Trigger Alert',    icon: '🚨', color: '#ef4444' },
                { label: 'Shift Handoff',    icon: '🔄', color: '#06b6d4' },
                { label: 'Send Broadcast',   icon: '📢', color: '#f59e0b' },
              ].map(a => (
                <button key={a.label} className="rp-btn rp-btn--secondary rp-btn--full" style={{
                  justifyContent: 'flex-start', gap: 'var(--space-3)', fontSize: '0.875rem',
                }}>
                  <span style={{ fontSize: '1rem' }}>{a.icon}</span>
                  {a.label}
                </button>
              ))}
            </div>
          </div>
        </div>
      </div>

      {/* ── Forecast row ─────────────────────────────────────────────────── */}
      <div>
        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: 'var(--space-4)' }}>
          <div>
            <h3 style={{ margin: 0 }}>7-Day Staff Forecast</h3>
            <p style={{ margin: 0, fontSize: '0.875rem' }}>AI-generated staffing recommendations based on occupancy predictions</p>
          </div>
          <button className="rp-btn rp-btn--ghost rp-btn--sm" onClick={() => onNavigate?.('forecast')}>
            Full forecast →
          </button>
        </div>
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(2, 1fr)', gap: 'var(--space-5)' }}>
          <ForecastCardWeb propertyId={1} role="housekeeping" />
          <ForecastCardWeb propertyId={1} role="maintenance" />
        </div>
      </div>

    </div>
  )
}
