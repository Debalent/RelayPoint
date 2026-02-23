// frontend/src/components/hospitality/ForecastCardWeb.jsx
// Premium 7-day staffing forecast card with visual bar chart

import React, { useEffect, useState } from 'react'

/* ── Icon helpers ─────────────────────────────────────────────────────────── */
function IconEdit() {
  return (
    <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"/>
      <path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"/>
    </svg>
  )
}
function IconSave() {
  return (
    <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <polyline points="20 6 9 17 4 12"/>
    </svg>
  )
}
function IconX() {
  return (
    <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/>
    </svg>
  )
}
function IconSpinner() {
  return (
    <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5"
      strokeLinecap="round" strokeLinejoin="round"
      style={{ animation: 'rp-spin 0.8s linear infinite' }}>
      <path d="M12 2v4M12 18v4M4.93 4.93l2.83 2.83M16.24 16.24l2.83 2.83M2 12h4M18 12h4M4.93 19.07l2.83-2.83M16.24 7.76l2.83-2.83"/>
    </svg>
  )
}

/* ── Role config ──────────────────────────────────────────────────────────── */
const ROLE_META = {
  housekeeping: { label: 'Housekeeping', icon: '🧹', color: '#1080D0', bg: 'rgba(16,128,208,0.13)' },
  maintenance:  { label: 'Maintenance',  icon: '🔧', color: '#f59e0b', bg: 'rgba(245,158,11,0.12)' },
  'f&b':        { label: 'F&B',          icon: '🍽️', color: '#10b981', bg: 'rgba(16,185,129,0.12)' },
  'front-desk': { label: 'Front Desk',   icon: '🏨', color: '#2DB580', bg: 'rgba(45,181,128,0.12)'  },
}

/* ── Utility ──────────────────────────────────────────────────────────────── */
function shortDate(iso) {
  const d = new Date(iso)
  return d.toLocaleDateString([], { weekday: 'short', month: 'short', day: 'numeric' })
}

function shortDay(iso) {
  const d = new Date(iso)
  return d.toLocaleDateString([], { weekday: 'short' })
}

function isToday(iso) {
  const d = new Date(iso)
  const now = new Date()
  return d.toDateString() === now.toDateString()
}

/* ── Skeleton bar ─────────────────────────────────────────────────────────── */
function SkeletonRow() {
  return (
    <div style={{ display: 'flex', alignItems: 'center', gap: 12, padding: '8px 0' }}>
      <div className="rp-skeleton" style={{ width: 36, height: 16, borderRadius: 4 }} />
      <div className="rp-skeleton" style={{ flex: 1, height: 28, borderRadius: 6 }} />
      <div className="rp-skeleton" style={{ width: 28, height: 16, borderRadius: 4 }} />
    </div>
  )
}

/* ═══════════════════════════════════════════════════════════════════════════
   ForecastCardWeb Component
   ═══════════════════════════════════════════════════════════════════════════ */
export default function ForecastCardWeb({ propertyId = 1, role = 'housekeeping' }) {
  const [predictions, setPredictions]     = useState([])
  const [loading, setLoading]             = useState(false)
  const [selectedDate, setSelectedDate]   = useState(null)
  const [overrideValue, setOverrideValue] = useState('')
  const [saving, setSaving]               = useState(false)
  const [saveMsg, setSaveMsg]             = useState('')

  const meta = ROLE_META[role] || ROLE_META.housekeeping

  useEffect(() => { fetchForecast() }, [propertyId, role])

  async function fetchForecast() {
    setLoading(true)
    const today = new Date().toISOString().slice(0, 10)
    try {
      const res = await fetch(
        `/api/v1/forecast/forecast?property_id=${propertyId}&start_date=${today}&horizon=7&role=${role}`
      )
      const data = await res.json()
      setPredictions(data.predictions || [])
    } catch (_) {
      // Use demo data when API is unavailable
      setPredictions(generateDemo())
    }
    setLoading(false)
  }

  function generateDemo() {
    const today = new Date()
    return Array.from({ length: 7 }, (_, i) => {
      const d = new Date(today)
      d.setDate(today.getDate() + i)
      const base = role === 'housekeeping' ? 18 : role === 'maintenance' ? 6 : 12
      const noise = Math.round((Math.random() - 0.5) * 4)
      const predicted = base + noise + (i === 1 || i === 2 ? 4 : 0) // weekend spike
      return {
        date: d.toISOString().slice(0, 10),
        predicted,
        lower:  predicted - Math.round(2 + Math.random() * 2),
        upper:  predicted + Math.round(2 + Math.random() * 2),
        override: null,
      }
    })
  }

  async function saveOverride() {
    if (!selectedDate) return
    setSaving(true)
    setSaveMsg('')
    const payload = {
      property_id: propertyId,
      role,
      date: selectedDate,
      override_value: Number(overrideValue),
    }
    try {
      await fetch('/api/v1/forecast/override', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload),
      })
      setPredictions(p =>
        p.map(pt => pt.date === selectedDate ? { ...pt, predicted: Number(overrideValue), override: Number(overrideValue) } : pt)
      )
      setSaveMsg('Saved!')
      setTimeout(() => { setSelectedDate(null); setOverrideValue(''); setSaveMsg('') }, 1200)
    } catch (_) {
      // Optimistic update for demo
      setPredictions(p =>
        p.map(pt => pt.date === selectedDate ? { ...pt, predicted: Number(overrideValue), override: Number(overrideValue) } : pt)
      )
      setSaveMsg('Saved (demo)')
      setTimeout(() => { setSelectedDate(null); setOverrideValue(''); setSaveMsg('') }, 1200)
    }
    setSaving(false)
  }

  const maxVal = predictions.length ? Math.max(...predictions.map(p => p.upper)) : 1
  const avgPredicted = predictions.length
    ? Math.round(predictions.reduce((s, p) => s + p.predicted, 0) / predictions.length)
    : 0

  return (
    <>
      <style>{`@keyframes rp-spin { to { transform: rotate(360deg); } }`}</style>

      <div className="rp-card" style={{ overflow: 'visible' }}>

        {/* Header */}
        <div className="rp-card__header">
          <div style={{ display: 'flex', alignItems: 'center', gap: 'var(--space-3)' }}>
            <div style={{
              width: 36, height: 36, borderRadius: 'var(--r-md)',
              background: meta.bg, display: 'flex', alignItems: 'center',
              justifyContent: 'center', fontSize: '1.1rem',
            }}>
              {meta.icon}
            </div>
            <div>
              <div className="fw-700" style={{ color: 'var(--rp-text-primary)', fontSize: '0.9375rem' }}>
                {meta.label} Forecast
              </div>
              <div className="text-xs" style={{ color: 'var(--rp-text-muted)' }}>
                7-day AI staffing prediction
              </div>
            </div>
          </div>
          <div style={{ display: 'flex', alignItems: 'center', gap: 'var(--space-3)' }}>
            {!loading && predictions.length > 0 && (
              <div style={{ textAlign: 'right' }}>
                <div style={{
                  fontFamily: 'var(--font-display)', fontWeight: 800, fontSize: '1.5rem',
                  letterSpacing: '-0.04em', color: meta.color, lineHeight: 1,
                }}>
                  {avgPredicted}
                </div>
                <div className="text-xs" style={{ color: 'var(--rp-text-muted)' }}>avg/day</div>
              </div>
            )}
            <button
              className="rp-icon-btn"
              onClick={fetchForecast}
              title="Refresh forecast"
              style={{ cursor: 'pointer' }}
            >
              {loading ? <IconSpinner /> : (
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                  <polyline points="23 4 23 10 17 10"/><polyline points="1 20 1 14 7 14"/>
                  <path d="M3.51 9a9 9 0 0 1 14.85-3.36L23 10M1 14l4.64 4.36A9 9 0 0 0 20.49 15"/>
                </svg>
              )}
            </button>
          </div>
        </div>

        {/* Chart body */}
        <div className="rp-card__body">
          {loading ? (
            <div>
              {[...Array(7)].map((_, i) => <SkeletonRow key={i} />)}
            </div>
          ) : predictions.length === 0 ? (
            <div style={{ textAlign: 'center', padding: 'var(--space-8)', color: 'var(--rp-text-muted)' }}>
              No forecast data available
            </div>
          ) : (
            <div style={{ display: 'flex', flexDirection: 'column', gap: 'var(--space-2)' }}>
              {predictions.map(item => {
                const fillPct   = (item.predicted / maxVal) * 100
                const lowerPct  = (item.lower / maxVal) * 100
                const upperPct  = (item.upper / maxVal) * 100
                const today     = isToday(item.date)
                const isEditing = selectedDate === item.date
                const hasOvr    = item.override != null

                return (
                  <div
                    key={item.date}
                    style={{
                      display: 'grid',
                      gridTemplateColumns: '52px 1fr 36px 28px',
                      alignItems: 'center',
                      gap: 8,
                      padding: '6px 0',
                      borderRadius: 'var(--r-sm)',
                    }}
                  >
                    {/* Day label */}
                    <div style={{ textAlign: 'right' }}>
                      <div style={{
                        fontSize: '0.75rem',
                        fontWeight: today ? 700 : 500,
                        color: today ? meta.color : 'var(--rp-text-secondary)',
                      }}>
                        {shortDay(item.date)}
                      </div>
                      {today && (
                        <div style={{ fontSize: '0.55rem', color: meta.color, fontWeight: 700, textTransform: 'uppercase', letterSpacing: '0.05em' }}>
                          TODAY
                        </div>
                      )}
                    </div>

                    {/* Bar */}
                    <div style={{ position: 'relative' }}>
                      {/* Range background */}
                      <div style={{
                        position: 'absolute',
                        left: `${lowerPct}%`,
                        width: `${upperPct - lowerPct}%`,
                        top: 0, bottom: 0,
                        background: `${meta.color}22`,
                        borderRadius: 4,
                      }} />
                      {/* Predicted fill */}
                      <div style={{
                        height: 28,
                        background: today ? meta.color : `${meta.color}88`,
                        borderRadius: 4,
                        width: `${fillPct}%`,
                        position: 'relative',
                        transition: 'width 0.5s ease',
                        boxShadow: today ? `0 2px 8px ${meta.color}44` : 'none',
                      }} />
                    </div>

                    {/* Value */}
                    {isEditing ? (
                      <input
                        type="number"
                        value={overrideValue}
                        onChange={e => setOverrideValue(e.target.value)}
                        style={{
                          width: 52, background: 'rgba(99,102,241,0.12)',
                          border: '1px solid var(--rp-indigo)', borderRadius: 6,
                          color: 'var(--rp-text-primary)', fontSize: '0.8rem',
                          padding: '3px 6px', outline: 'none', fontFamily: 'inherit',
                          textAlign: 'center',
                        }}
                        autoFocus
                        min={1}
                      />
                    ) : (
                      <div style={{
                        textAlign: 'center', fontSize: '0.8rem', fontWeight: 700,
                        color: hasOvr ? '#f59e0b' : today ? 'var(--rp-text-primary)' : 'var(--rp-text-secondary)',
                      }}>
                        {Math.round(item.predicted)}
                        {hasOvr && <span style={{ fontSize: '0.55rem', display: 'block', color: '#f59e0b' }}>OVR</span>}
                      </div>
                    )}

                    {/* Action button */}
                    {isEditing ? (
                      <div style={{ display: 'flex', flexDirection: 'column', gap: 2 }}>
                        <button
                          onClick={saveOverride}
                          disabled={saving}
                          title="Save override"
                          style={{
                            width: 24, height: 24, borderRadius: 4, background: 'rgba(16,185,129,0.2)',
                            border: '1px solid rgba(16,185,129,0.3)', cursor: 'pointer',
                            display: 'flex', alignItems: 'center', justifyContent: 'center',
                            color: '#10b981',
                          }}
                        >
                          {saving ? <IconSpinner /> : <IconSave />}
                        </button>
                        <button
                          onClick={() => { setSelectedDate(null); setOverrideValue('') }}
                          title="Cancel"
                          style={{
                            width: 24, height: 24, borderRadius: 4, background: 'rgba(239,68,68,0.12)',
                            border: '1px solid rgba(239,68,68,0.2)', cursor: 'pointer',
                            display: 'flex', alignItems: 'center', justifyContent: 'center',
                            color: '#ef4444',
                          }}
                        >
                          <IconX />
                        </button>
                      </div>
                    ) : (
                      <button
                        onClick={() => { setSelectedDate(item.date); setOverrideValue(Math.round(item.predicted)) }}
                        title="Override prediction"
                        style={{
                          width: 24, height: 24, borderRadius: 4, background: 'var(--rp-bg-glass)',
                          border: '1px solid var(--rp-border)', cursor: 'pointer',
                          display: 'flex', alignItems: 'center', justifyContent: 'center',
                          color: 'var(--rp-text-muted)', transition: 'all var(--t-fast)',
                        }}
                        onMouseEnter={e => { e.currentTarget.style.color = 'var(--rp-indigo)'; e.currentTarget.style.borderColor = 'rgba(99,102,241,0.4)' }}
                        onMouseLeave={e => { e.currentTarget.style.color = 'var(--rp-text-muted)'; e.currentTarget.style.borderColor = 'var(--rp-border)' }}
                      >
                        <IconEdit />
                      </button>
                    )}
                  </div>
                )
              })}
            </div>
          )}

          {/* Save feedback */}
          {saveMsg && (
            <div style={{
              marginTop: 'var(--space-3)', padding: 'var(--space-2) var(--space-3)',
              background: 'rgba(16,185,129,0.1)', border: '1px solid rgba(16,185,129,0.2)',
              borderRadius: 'var(--r-md)', fontSize: '0.8rem', color: '#10b981',
              display: 'flex', alignItems: 'center', gap: 6,
            }}>
              ✓ {saveMsg}
            </div>
          )}
        </div>

        {/* Footer */}
        <div className="rp-card__footer" style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: 'var(--space-4)' }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: 5 }}>
              <div style={{ width: 28, height: 8, borderRadius: 4, background: meta.color }} />
              <span className="text-xs" style={{ color: 'var(--rp-text-muted)' }}>Predicted</span>
            </div>
            <div style={{ display: 'flex', alignItems: 'center', gap: 5 }}>
              <div style={{ width: 28, height: 8, borderRadius: 4, background: `${meta.color}33` }} />
              <span className="text-xs" style={{ color: 'var(--rp-text-muted)' }}>Range</span>
            </div>
          </div>
          <div style={{ display: 'flex', alignItems: 'center', gap: 5 }}>
            <div style={{ width: 6, height: 6, borderRadius: 50, background: '#f59e0b' }} />
            <span className="text-xs" style={{ color: 'var(--rp-text-muted)' }}>Override active</span>
          </div>
        </div>
      </div>
    </>
  )
}