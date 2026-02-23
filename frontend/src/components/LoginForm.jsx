// frontend/src/components/LoginForm.jsx
// Premium split-screen login — RelayPoint

import { useState } from 'react'
import useAuth from '../hooks/useAuth'

/* ── SVG Icons ─────────────────────────────────────────────────────────────── */
function IconMail() {
  return (
    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"/>
      <polyline points="22,6 12,13 2,6"/>
    </svg>
  )
}
function IconLock() {
  return (
    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <rect x="3" y="11" width="18" height="11" rx="2" ry="2"/>
      <path d="M7 11V7a5 5 0 0 1 10 0v4"/>
    </svg>
  )
}
function IconEye({ off }) {
  return off ? (
    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <path d="M17.94 17.94A10.07 10.07 0 0 1 12 20c-7 0-11-8-11-8a18.45 18.45 0 0 1 5.06-5.94M9.9 4.24A9.12 9.12 0 0 1 12 4c7 0 11 8 11 8a18.5 18.5 0 0 1-2.16 3.19"/>
      <line x1="1" y1="1" x2="23" y2="23"/>
    </svg>
  ) : (
    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/>
      <circle cx="12" cy="12" r="3"/>
    </svg>
  )
}
function IconArrowRight() {
  return (
    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round">
      <line x1="5" y1="12" x2="19" y2="12"/>
      <polyline points="12 5 19 12 12 19"/>
    </svg>
  )
}
function IconCheck() {
  return (
    <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round">
      <polyline points="20 6 9 17 4 12"/>
    </svg>
  )
}
function IconSpinner() {
  return (
    <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round"
      style={{ animation: 'spin 0.8s linear infinite' }}>
      <path d="M12 2v4M12 18v4M4.93 4.93l2.83 2.83M16.24 16.24l2.83 2.83M2 12h4M18 12h4M4.93 19.07l2.83-2.83M16.24 7.76l2.83-2.83"/>
    </svg>
  )
}

/* ── Feature bullets for hero panel ────────────────────────────────────────── */
const FEATURES = [
  'Real-time task coordination across all departments',
  'AI-powered staff forecasting & scheduling',
  'Seamless Cloudbeds & PMS integration',
  'Live escalations with smart priority routing',
]

/* ── Stats for hero panel ───────────────────────────────────────────────────── */
const HERO_STATS = [
  { value: '92%', label: 'Task completion rate' },
  { value: '3.2×', label: 'Faster escalation resolution' },
  { value: '40min', label: 'Saved per staff member/day' },
]

/* ═════════════════════════════════════════════════════════════════════════════
   LoginForm Component
   ═════════════════════════════════════════════════════════════════════════════ */
export default function LoginForm() {
  const [email, setEmail]           = useState('')
  const [password, setPassword]     = useState('')
  const [showPassword, setShowPass] = useState(false)
  const [error, setError]           = useState('')
  const [loading, setLoading]       = useState(false)
  const { login } = useAuth()

  const handleLogin = async (e) => {
    e.preventDefault()
    setError('')
    setLoading(true)

    try {
      const response = await fetch('http://localhost:8000/api/v1/auth/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, password }),
      })
      const data = await response.json()
      if (!response.ok) throw new Error(data.detail || 'Login failed')
      login(data.access_token)
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  return (
    <>
      <style>{`
        @keyframes spin { to { transform: rotate(360deg); } }
        @keyframes gradFlow {
          0%,100% { background-position: 0% 50%; }
          50% { background-position: 100% 50%; }
        }
        .hero-bg-orb-1 {
          position: absolute; border-radius: 50%; filter: blur(80px); pointer-events: none; z-index: 0;
          width: 400px; height: 400px; top: -100px; right: -80px;
          background: radial-gradient(circle, rgba(99,102,241,0.25) 0%, transparent 70%);
          animation: pulse 8s ease-in-out infinite;
        }
        .hero-bg-orb-2 {
          position: absolute; border-radius: 50%; filter: blur(60px); pointer-events: none; z-index: 0;
          width: 300px; height: 300px; bottom: -80px; left: -60px;
          background: radial-gradient(circle, rgba(139,92,246,0.2) 0%, transparent 70%);
          animation: pulse 10s ease-in-out infinite 2s;
        }
        .hero-bg-grid {
          position: absolute; inset: 0; z-index: 0; opacity: 0.04; pointer-events: none;
          background-image: linear-gradient(var(--rp-border) 1px, transparent 1px),
                            linear-gradient(90deg, var(--rp-border) 1px, transparent 1px);
          background-size: 48px 48px;
        }
        @keyframes pulse {
          0%,100%{opacity:0.8;transform:scale(1);}
          50%{opacity:1;transform:scale(1.1);}
        }
        .input-icon-wrap {
          position: relative;
        }
        .input-icon-wrap .icon-left {
          position: absolute; left: 14px; top: 50%; transform: translateY(-50%);
          color: var(--rp-text-muted); display: flex; pointer-events: none;
        }
        .input-icon-wrap .rp-input {
          padding-left: 42px;
        }
        .input-icon-wrap .icon-right {
          position: absolute; right: 12px; top: 50%; transform: translateY(-50%);
          color: var(--rp-text-muted); display: flex; cursor: pointer;
          background: none; border: none; padding: 4px;
          transition: color var(--t-fast);
        }
        .input-icon-wrap .icon-right:hover { color: var(--rp-text-primary); }
      `}</style>

      <div className="rp-login-page">

        {/* ── Hero/brand panel ────────────────────────────────────────────── */}
        <div className="rp-login-hero">
          <div className="hero-bg-grid" />
          <div className="hero-bg-orb-1" />
          <div className="hero-bg-orb-2" />

          {/* Logo */}
          <div style={{ position: 'relative', zIndex: 1 }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: 'var(--space-3)', marginBottom: 'var(--space-12)' }}>
              <div className="rp-logo-mark" style={{ width: 44, height: 44, fontSize: '1.2rem' }}>R</div>
              <div>
                <div style={{
                  fontFamily: 'var(--font-display)', fontWeight: 800, fontSize: '1.25rem',
                  letterSpacing: '-0.03em',
                  background: 'var(--rp-gradient-brand)',
                  WebkitBackgroundClip: 'text', WebkitTextFillColor: 'transparent', backgroundClip: 'text',
                }}>RelayPoint</div>
                <div style={{ fontSize: '0.7rem', color: 'var(--rp-text-muted)', letterSpacing: '0.1em', textTransform: 'uppercase' }}>
                  Hospitality OS
                </div>
              </div>
            </div>

            {/* Headline */}
            <h1 style={{ marginBottom: 'var(--space-5)', maxWidth: 480, lineHeight: 1.1 }}>
              Every team in sync.{' '}
              <span style={{
                background: 'var(--rp-gradient-brand)',
                WebkitBackgroundClip: 'text', WebkitTextFillColor: 'transparent', backgroundClip: 'text',
              }}>Every guest delighted.</span>
            </h1>
            <p style={{ color: 'var(--rp-text-secondary)', fontSize: '1.0625rem', maxWidth: 440, marginBottom: 'var(--space-10)' }}>
              AI-powered workflow automation that keeps housekeeping, maintenance, F&amp;B and front desk perfectly coordinated — in real time.
            </p>

            {/* Features list */}
            <div style={{ display: 'flex', flexDirection: 'column', gap: 'var(--space-3)', marginBottom: 'var(--space-10)' }}>
              {FEATURES.map((f, i) => (
                <div key={i} style={{ display: 'flex', alignItems: 'center', gap: 'var(--space-3)' }}>
                  <span style={{
                    width: 22, height: 22, borderRadius: 'var(--r-full)',
                    background: 'rgba(99,102,241,0.18)',
                    border: '1px solid rgba(99,102,241,0.3)',
                    display: 'flex', alignItems: 'center', justifyContent: 'center',
                    flexShrink: 0, color: 'var(--rp-indigo)',
                  }}>
                    <IconCheck />
                  </span>
                  <span style={{ fontSize: '0.9rem', color: 'var(--rp-text-secondary)' }}>{f}</span>
                </div>
              ))}
            </div>
          </div>

          {/* Stats row */}
          <div style={{ position: 'relative', zIndex: 1 }}>
            {/* Testimonial card */}
            <div className="rp-login-testimonial" style={{ marginBottom: 'var(--space-6)' }}>
              <p style={{ fontSize: '0.9375rem', fontStyle: 'italic', color: 'var(--rp-text-secondary)', marginBottom: 'var(--space-4)', lineHeight: 1.7 }}>
                "RelayPoint cut our room-ready time by 22 minutes and virtually eliminated missed escalations. Our TripAdvisor score jumped a full point in 6 weeks."
              </p>
              <div style={{ display: 'flex', alignItems: 'center', gap: 'var(--space-3)' }}>
                <div className="rp-avatar" style={{ background: 'var(--rp-gradient-warm)' }}>AK</div>
                <div>
                  <div className="fw-600 text-sm" style={{ color: 'var(--rp-text-primary)' }}>Andrea K.</div>
                  <div className="text-xs" style={{ color: 'var(--rp-text-muted)' }}>GM, Embassy Suites Chicago</div>
                </div>
                <div style={{ marginLeft: 'auto', display: 'flex', gap: 2 }}>
                  {[...Array(5)].map((_, i) => (
                    <span key={i} style={{ color: '#f59e0b', fontSize: '0.875rem' }}>★</span>
                  ))}
                </div>
              </div>
            </div>

            {/* Metrics */}
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: 'var(--space-3)' }}>
              {HERO_STATS.map((s, i) => (
                <div key={i} style={{
                  background: 'var(--rp-bg-glass)', border: '1px solid var(--rp-border)',
                  borderRadius: 'var(--r-lg)', padding: 'var(--space-4)', textAlign: 'center',
                }}>
                  <div style={{
                    fontFamily: 'var(--font-display)', fontWeight: 800, fontSize: '1.5rem',
                    letterSpacing: '-0.03em',
                    background: 'var(--rp-gradient-brand)',
                    WebkitBackgroundClip: 'text', WebkitTextFillColor: 'transparent', backgroundClip: 'text',
                    marginBottom: 4,
                  }}>{s.value}</div>
                  <div style={{ fontSize: '0.7rem', color: 'var(--rp-text-muted)', lineHeight: 1.3 }}>{s.label}</div>
                </div>
              ))}
            </div>
          </div>
        </div>

        {/* ── Form panel ───────────────────────────────────────────────────── */}
        <div className="rp-login-form-panel animate-fadeInUp">
          <div style={{ maxWidth: 400, width: '100%', margin: '0 auto' }}>

            {/* Header */}
            <div style={{ marginBottom: 'var(--space-8)' }}>
              {/* Mobile logo */}
              <div style={{ display: 'none', alignItems: 'center', gap: 'var(--space-3)', marginBottom: 'var(--space-8)' }}
                id="mobile-logo">
                <div className="rp-logo-mark">R</div>
                <div style={{
                  fontFamily: 'var(--font-display)', fontWeight: 800, fontSize: '1.1rem',
                  background: 'var(--rp-gradient-brand)',
                  WebkitBackgroundClip: 'text', WebkitTextFillColor: 'transparent', backgroundClip: 'text',
                }}>RelayPoint</div>
              </div>

              <div style={{
                display: 'inline-flex', alignItems: 'center', gap: 6,
                background: 'rgba(16,185,129,0.1)', border: '1px solid rgba(16,185,129,0.2)',
                borderRadius: 'var(--r-full)', padding: '4px 12px',
                fontSize: '0.75rem', fontWeight: 600, color: '#10b981',
                marginBottom: 'var(--space-4)',
              }}>
                <span className="rp-dot pulse" style={{ background: '#10b981' }} />
                Pilot Program Active
              </div>
              <h2 style={{ marginBottom: 'var(--space-2)' }}>Welcome back</h2>
              <p>Sign in to your RelayPoint workspace.</p>
            </div>

            {/* Form */}
            <form onSubmit={handleLogin}>
              {/* Email */}
              <div className="rp-field">
                <label className="rp-label" htmlFor="rp-email">Email address</label>
                <div className="input-icon-wrap">
                  <span className="icon-left"><IconMail /></span>
                  <input
                    id="rp-email"
                    type="email"
                    className="rp-input"
                    placeholder="you@hotel.com"
                    value={email}
                    onChange={e => setEmail(e.target.value)}
                    required
                    autoComplete="email"
                    autoFocus
                  />
                </div>
              </div>

              {/* Password */}
              <div className="rp-field">
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                  <label className="rp-label" htmlFor="rp-password">Password</label>
                  <a href="#" style={{ fontSize: '0.75rem' }}>Forgot password?</a>
                </div>
                <div className="input-icon-wrap">
                  <span className="icon-left"><IconLock /></span>
                  <input
                    id="rp-password"
                    type={showPassword ? 'text' : 'password'}
                    className="rp-input"
                    placeholder="••••••••"
                    value={password}
                    onChange={e => setPassword(e.target.value)}
                    required
                    autoComplete="current-password"
                    style={{ paddingRight: 44 }}
                  />
                  <button type="button" className="icon-right" onClick={() => setShowPass(v => !v)}>
                    <IconEye off={showPassword} />
                  </button>
                </div>
              </div>

              {/* Error */}
              {error && (
                <div style={{
                  background: 'rgba(239,68,68,0.1)', border: '1px solid rgba(239,68,68,0.25)',
                  borderRadius: 'var(--r-md)', padding: 'var(--space-3) var(--space-4)',
                  marginBottom: 'var(--space-4)', fontSize: '0.875rem', color: '#ef4444',
                  display: 'flex', alignItems: 'center', gap: 'var(--space-2)',
                }}>
                  <span>⚠</span> {error}
                </div>
              )}

              {/* Submit */}
              <button
                type="submit"
                className="rp-btn rp-btn--primary rp-btn--lg rp-btn--full"
                disabled={loading}
                style={{ marginBottom: 'var(--space-4)' }}
              >
                {loading ? (
                  <><IconSpinner /> Signing in…</>
                ) : (
                  <>Sign in <IconArrowRight /></>
                )}
              </button>

              {/* Divider */}
              <div style={{ display: 'flex', alignItems: 'center', gap: 'var(--space-3)', marginBottom: 'var(--space-4)' }}>
                <hr className="rp-divider" style={{ flex: 1, margin: 0 }} />
                <span style={{ fontSize: '0.75rem', color: 'var(--rp-text-muted)', whiteSpace: 'nowrap' }}>OR</span>
                <hr className="rp-divider" style={{ flex: 1, margin: 0 }} />
              </div>

              {/* SSO */}
              <button
                type="button"
                className="rp-btn rp-btn--secondary rp-btn--full"
                style={{ marginBottom: 'var(--space-6)' }}
              >
                <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor">
                  <path d="M12 0C5.37 0 0 5.37 0 12c0 5.31 3.435 9.795 8.205 11.385.6.105.825-.255.825-.57 0-.285-.015-1.23-.015-2.235-3.015.555-3.795-.735-4.035-1.41-.135-.345-.72-1.41-1.23-1.695-.42-.225-1.02-.78-.015-.795.945-.015 1.62.87 1.845 1.23 1.08 1.815 2.805 1.305 3.495.99.105-.78.42-1.305.765-1.605-2.67-.3-5.46-1.335-5.46-5.925 0-1.305.465-2.385 1.23-3.225-.12-.3-.54-1.53.12-3.18 0 0 1.005-.315 3.3 1.23.96-.27 1.98-.405 3-.405s2.04.135 3 .405c2.295-1.56 3.3-1.23 3.3-1.23.66 1.65.24 2.88.12 3.18.765.84 1.23 1.905 1.23 3.225 0 4.605-2.805 5.625-5.475 5.925.435.375.81 1.095.81 2.22 0 1.605-.015 2.895-.015 3.3 0 .315.225.69.825.57A12.02 12.02 0 0 0 24 12c0-6.63-5.37-12-12-12z"/>
                </svg>
                Continue with SSO / GitHub
              </button>
            </form>

            {/* Footer note */}
            <p style={{ fontSize: '0.75rem', textAlign: 'center', color: 'var(--rp-text-muted)', lineHeight: 1.6 }}>
              By signing in, you agree to RelayPoint's{' '}
              <a href="#">Terms of Service</a> and{' '}
              <a href="#">Privacy Policy</a>.
              <br />Protected by 256-bit TLS encryption.
            </p>

          </div>
        </div>
      </div>
    </>
  )
}
