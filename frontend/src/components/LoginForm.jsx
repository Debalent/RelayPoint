// frontend/src/components/LoginForm.jsx
// RelayPoint — Elite Login Page with Demo Mode

import { useState } from 'react'
import useAuth from '../hooks/useAuth'

/* ── Injected keyframes & component-scoped styles ───────────────────────────── */
const INJECTED_CSS = `
  @keyframes rp-spin    { to { transform: rotate(360deg); } }
  @keyframes rp-floatA  { 0%,100%{transform:translate(0,0) scale(1);opacity:.7;} 50%{transform:translate(30px,-20px) scale(1.08);opacity:1;} }
  @keyframes rp-floatB  { 0%,100%{transform:translate(0,0);opacity:.5;} 50%{transform:translate(-20px,30px) scale(1.1);opacity:.85;} }
  @keyframes rp-slideUp { from{opacity:0;transform:translateY(24px);} to{opacity:1;transform:translateY(0);} }
  @keyframes rp-pulseDot{ 0%,100%{transform:scale(1);opacity:1;} 50%{transform:scale(.75);opacity:.5;} }
  @keyframes rp-shine   { 0%{background-position:-200% center;} to{background-position:200% center;} }
  @keyframes rp-borderPulse { 0%,100%{box-shadow:0 0 0 0 rgba(16,128,208,0);} 50%{box-shadow:0 0 0 3px rgba(16,128,208,.35);} }
  .rpl-demo-btn {
    display:flex;align-items:center;justify-content:center;gap:8px;
    width:100%;padding:14px 24px;
    background:linear-gradient(135deg,rgba(16,128,208,.15),rgba(45,181,128,.12));
    border:1px solid rgba(16,128,208,.35);border-radius:10px;
    color:#60c4ff;font-size:.9375rem;font-weight:600;font-family:inherit;
    cursor:pointer;transition:all .18s ease;
    animation:rp-borderPulse 3s ease-in-out infinite;
  }
  .rpl-demo-btn:hover:not(:disabled) {
    background:linear-gradient(135deg,rgba(16,128,208,.3),rgba(45,181,128,.22));
    border-color:rgba(16,128,208,.8);color:#fff;
    transform:translateY(-2px);box-shadow:0 8px 32px rgba(16,128,208,.35);
    animation:none;
  }
  .rpl-demo-btn:disabled { opacity:.55;cursor:not-allowed;animation:none; }
  .rpl-input {
    background:rgba(255,255,255,.05);border:1px solid rgba(255,255,255,.1);
    border-radius:10px;padding:13px 16px 13px 44px;
    color:#f0f6ff;font-family:inherit;font-size:.9375rem;
    width:100%;outline:none;transition:all .18s ease;-webkit-appearance:none;
  }
  .rpl-input::-webkit-input-placeholder{color:rgba(255,255,255,.3);}
  .rpl-input::placeholder{color:rgba(255,255,255,.3);}
  .rpl-input:hover{border-color:rgba(255,255,255,.2);}
  .rpl-input:focus{border-color:#1080D0;background:rgba(16,128,208,.1);box-shadow:0 0 0 3px rgba(16,128,208,.2);}
  .rpl-primary-btn {
    display:flex;align-items:center;justify-content:center;gap:8px;
    width:100%;padding:14px 24px;
    background:linear-gradient(90deg,#003080,#1080D0,#2DB580,#1080D0,#003080);
    background-size:300% auto;
    border:none;border-radius:10px;
    color:#fff;font-size:.9375rem;font-weight:700;font-family:inherit;
    cursor:pointer;transition:transform .18s ease,box-shadow .18s ease;
    box-shadow:0 4px 20px rgba(16,128,208,.5);
    animation:rp-shine 6s linear infinite;
  }
  .rpl-primary-btn:hover:not(:disabled){transform:translateY(-2px);box-shadow:0 8px 32px rgba(16,128,208,.65);}
  .rpl-primary-btn:active:not(:disabled){transform:translateY(0);}
  .rpl-primary-btn:disabled{opacity:.45;cursor:not-allowed;animation:none;}
  .rpl-sso-btn {
    display:flex;align-items:center;justify-content:center;gap:10px;
    width:100%;padding:13px 24px;
    background:rgba(255,255,255,.05);border:1px solid rgba(255,255,255,.1);
    border-radius:10px;color:#c8d8ec;font-size:.9375rem;font-weight:500;font-family:inherit;
    cursor:pointer;transition:all .18s ease;
  }
  .rpl-sso-btn:hover{background:rgba(255,255,255,.1);border-color:rgba(255,255,255,.2);color:#fff;}
  .rpl-stat-card {
    background:rgba(255,255,255,.05);border:1px solid rgba(255,255,255,.09);
    backdrop-filter:blur(12px);border-radius:14px;padding:16px;text-align:center;
    transition:all .18s ease;
  }
  .rpl-stat-card:hover{background:rgba(255,255,255,.08);border-color:rgba(16,128,208,.35);transform:translateY(-2px);}
  .rpl-feature-tick {
    width:22px;height:22px;border-radius:50%;flex-shrink:0;
    background:rgba(16,128,208,.18);border:1px solid rgba(16,128,208,.35);
    display:flex;align-items:center;justify-content:center;color:#60c4ff;
  }
  .rpl-pw-toggle { position:absolute;right:12px;top:50%;transform:translateY(-50%);background:none;border:none;color:rgba(255,255,255,.3);cursor:pointer;padding:4px;display:flex;transition:color .15s; }
  .rpl-pw-toggle:hover{color:rgba(255,255,255,.7);}
`

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

/* ── Data ───────────────────────────────────────────────────────────────────── */
const FEATURES = [
  'Real-time coordination across all hotel departments',
  'AI-powered staff forecasting & smart scheduling',
  'Seamless Cloudbeds & PMS two-way integration',
  'Live escalation routing with priority intelligence',
]

const HERO_STATS = [
  { value: '92%', label: 'Task completion rate' },
  { value: '3.2×', label: 'Faster resolution' },
  { value: '40min', label: 'Saved per staff/day' },
]

/* ═════════════════════════════════════════════════════════════════════════════
   LoginForm Component
   ═════════════════════════════════════════════════════════════════════════════ */
export default function LoginForm() {
  const [email, setEmail]             = useState('')
  const [password, setPassword]       = useState('')
  const [showPassword, setShowPass]   = useState(false)
  const [error, setError]             = useState('')
  const [loading, setLoading]         = useState(false)
  const [demoLoading, setDemoLoading] = useState(false)
  const { login } = useAuth()

  /* ── Real API login ───────────────────────────────────────────────────── */
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

  /* ── Demo bypass (no backend needed) ─────────────────────────────────── */
  const handleDemo = async () => {
    setDemoLoading(true)
    await new Promise(r => setTimeout(r, 800)) // brief loading UX
    login('demo-token-relaypoint-preview')
  }

  /* ── Shared style objects ────────────────────────────────────────────────── */
  const bg = { position:'absolute', borderRadius:'50%', pointerEvents:'none', filter:'blur(2px)' }

  return (
    <>
      <style>{INJECTED_CSS}</style>
      <style>{`
        @keyframes spin { to { transform: rotate(360deg); } }
        .hero-bg-orb-1 {
          position: absolute; border-radius: 50%; filter: blur(80px); pointer-events: none; z-index: 0;
          width: 480px; height: 480px; top: -80px; right: -60px;
          background: radial-gradient(circle, rgba(16,128,208,0.22) 0%, transparent 68%);
          animation: rp-floatA 12s ease-in-out infinite;
        }
        .hero-bg-orb-2 {
          position: absolute; border-radius: 50%; filter: blur(60px); pointer-events: none; z-index: 0;
          width: 360px; height: 360px; bottom: -80px; left: -60px;
          background: radial-gradient(circle, rgba(45,181,128,0.18) 0%, transparent 68%);
          animation: rp-floatB 16s ease-in-out infinite 2s;
        }
        .hero-bg-grid {
          position: absolute; inset: 0; z-index: 0; opacity: 0.03; pointer-events: none;
          background-image: linear-gradient(rgba(255,255,255,0.5) 1px, transparent 1px),
                            linear-gradient(90deg, rgba(255,255,255,0.5) 1px, transparent 1px);
          background-size: 48px 48px;
        }
        .input-icon-left {
          position: absolute; left: 14px; top: 50%; transform: translateY(-50%);
          color: rgba(255,255,255,0.3); display: flex; pointer-events: none;
        }
      `}</style>

      <div className="rp-login-page">

        {/* ── Hero/brand panel ────────────────────────────────────────────── */}
        <div className="rp-login-hero">
          <div className="hero-bg-grid" />
          <div className="hero-bg-orb-1" />
          <div className="hero-bg-orb-2" />

          {/* Logo */}
          <div style={{ position: 'relative', zIndex: 1 }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: 12, marginBottom: 64 }}>
              <div style={{
                width: 44, height: 44, borderRadius: 12, flexShrink: 0,
                background: 'linear-gradient(135deg, #003080 0%, #1080D0 55%, #2DB580 100%)',
                display: 'flex', alignItems: 'center', justifyContent: 'center',
                fontFamily: "'Plus Jakarta Sans', sans-serif",
                fontWeight: 900, fontSize: '1.2rem', color: '#fff',
                boxShadow: '0 4px 24px rgba(16,128,208,0.5)',
              }}>R</div>
              <div>
                <div style={{
                  fontFamily: "'Plus Jakarta Sans', 'Inter', sans-serif",
                  fontWeight: 800, fontSize: '1.25rem', letterSpacing: '-0.03em',
                  background: 'linear-gradient(90deg, #f0f6ff, #60c4ff)',
                  WebkitBackgroundClip: 'text', WebkitTextFillColor: 'transparent', backgroundClip: 'text',
                }}>RelayPoint</div>
                <div style={{ fontSize: '0.65rem', color: 'rgba(255,255,255,0.35)', letterSpacing: '0.12em', textTransform: 'uppercase' }}>
                  Hospitality OS
                </div>
              </div>
            </div>

            {/* Headline */}
            <h1 style={{
              fontFamily: "'Plus Jakarta Sans', sans-serif",
              fontWeight: 800, fontSize: 'clamp(2rem, 3.5vw, 2.8rem)',
              lineHeight: 1.1, letterSpacing: '-0.03em',
              color: '#f0f6ff', margin: '0 0 20px',
            }}>
              Every team in sync.{' '}
              <span style={{
                background: 'linear-gradient(90deg, #60c4ff, #2DB580)',
                WebkitBackgroundClip: 'text', WebkitTextFillColor: 'transparent', backgroundClip: 'text',
              }}>Every guest delighted.</span>
            </h1>
            <p style={{ fontSize: '1.0625rem', color: 'rgba(240,246,255,0.6)', maxWidth: 440, lineHeight: 1.75, margin: '0 0 40px' }}>
              AI-powered workflow automation that keeps housekeeping, maintenance, F&amp;B and front desk perfectly coordinated — in real time.
            </p>

            {/* Features list */}
            <div style={{ display: 'flex', flexDirection: 'column', gap: 12, marginBottom: 48 }}>
              {FEATURES.map((f, i) => (
                <div key={i} style={{ display: 'flex', alignItems: 'center', gap: 12 }}>
                  <span className="rpl-feature-tick"><IconCheck /></span>
                  <span style={{ fontSize: '0.9rem', color: 'rgba(240,246,255,0.65)' }}>{f}</span>
                </div>
              ))}
            </div>
          </div>

          {/* Testimonial + Stats */}
          <div style={{ position: 'relative', zIndex: 1 }}>
            <div style={{
              background: 'rgba(255,255,255,0.04)', border: '1px solid rgba(255,255,255,0.08)',
              backdropFilter: 'blur(16px)', borderRadius: 16, padding: 24, marginBottom: 24,
            }}>
              <p style={{ fontSize: '0.9375rem', fontStyle: 'italic', color: 'rgba(240,246,255,0.7)', lineHeight: 1.75, marginBottom: 16 }}>
                "RelayPoint cut our room-ready time by 22 minutes and virtually eliminated missed escalations. Our TripAdvisor score jumped a full point in 6 weeks."
              </p>
              <div style={{ display: 'flex', alignItems: 'center', gap: 12 }}>
                <div style={{ width: 36, height: 36, borderRadius: '50%', background: 'linear-gradient(135deg, #f59e0b, #d97706)', display: 'flex', alignItems: 'center', justifyContent: 'center', fontWeight: 700, fontSize: '0.8rem', color: '#fff', flexShrink: 0 }}>AK</div>
                <div>
                  <div style={{ fontWeight: 600, fontSize: '0.875rem', color: '#f0f6ff' }}>Andrea K.</div>
                  <div style={{ fontSize: '0.75rem', color: 'rgba(255,255,255,0.4)' }}>GM, Embassy Suites Chicago</div>
                </div>
                <div style={{ marginLeft: 'auto', display: 'flex', gap: 2 }}>
                  {[...Array(5)].map((_, i) => <span key={i} style={{ color: '#f59e0b', fontSize: '0.875rem' }}>★</span>)}
                </div>
              </div>
            </div>
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: 12 }}>
              {HERO_STATS.map((s, i) => (
                <div key={i} className="rpl-stat-card">
                  <div style={{ fontFamily: "'Plus Jakarta Sans', sans-serif", fontWeight: 800, fontSize: '1.6rem', letterSpacing: '-0.04em', background: 'linear-gradient(90deg, #60c4ff, #2DB580)', WebkitBackgroundClip: 'text', WebkitTextFillColor: 'transparent', backgroundClip: 'text', marginBottom: 4 }}>{s.value}</div>
                  <div style={{ fontSize: '0.7rem', color: 'rgba(255,255,255,0.45)', lineHeight: 1.3 }}>{s.label}</div>
                </div>
              ))}
            </div>
          </div>
        </div>

        {/* ── FORM PANEL ────────────────────────────────────────────────── */}
        <div className="rp-login-form-panel" style={{ animation: 'rp-slideUp 0.5s ease forwards' }}>
          <div style={{ maxWidth: 380, width: '100%', margin: '0 auto', position: 'relative', zIndex: 1 }}>

            {/* Header */}
            <div style={{ marginBottom: 36 }}>
              <div style={{
                display: 'inline-flex', alignItems: 'center', gap: 6,
                background: 'rgba(16,185,129,0.12)', border: '1px solid rgba(16,185,129,0.25)',
                borderRadius: 99, padding: '4px 12px',
                fontSize: '0.75rem', fontWeight: 600, color: '#34d399',
                marginBottom: 16,
              }}>
                <span style={{ width: 6, height: 6, borderRadius: '50%', background: '#34d399', animation: 'rp-pulseDot 2s ease-in-out infinite' }} />
                Pilot Program Active
              </div>
              <h2 style={{
                fontFamily: "'Plus Jakarta Sans', sans-serif",
                fontWeight: 800, fontSize: 'clamp(1.5rem, 2.5vw, 1.875rem)',
                letterSpacing: '-0.025em', color: '#f0f6ff', margin: '0 0 8px',
              }}>Welcome back</h2>
              <p style={{ fontSize: '0.9375rem', color: 'rgba(240,246,255,0.5)', margin: 0 }}>Sign in to your RelayPoint workspace.</p>
            </div>

            {/* ── Demo CTA ─────────────────────────────────────────────── */}
            <button
              type="button"
              className="rpl-demo-btn"
              onClick={handleDemo}
              disabled={demoLoading}
              style={{ marginBottom: 24 }}
            >
              {demoLoading ? <><IconSpinner /> Loading demo…</> : <>▶ Preview Live Demo — no login needed</>}
            </button>

            {/* Divider */}
            <div style={{ display: 'flex', alignItems: 'center', gap: 12, marginBottom: 24 }}>
              <div style={{ flex: 1, height: 1, background: 'rgba(255,255,255,0.07)' }} />
              <span style={{ fontSize: '0.75rem', color: 'rgba(255,255,255,0.3)' }}>or sign in with your account</span>
              <div style={{ flex: 1, height: 1, background: 'rgba(255,255,255,0.07)' }} />
            </div>

            {/* ── Form ─────────────────────────────────────────────────── */}
            <form onSubmit={handleLogin}>
              {/* Email */}
              <div style={{ marginBottom: 20 }}>
                <label style={{ display: 'block', fontSize: '0.75rem', fontWeight: 600, color: 'rgba(240,246,255,0.5)', textTransform: 'uppercase', letterSpacing: '0.07em', marginBottom: 6 }} htmlFor="rp-email">Email address</label>
                <div style={{ position: 'relative' }}>
                  <span className="input-icon-left"><IconMail /></span>
                  <input
                    id="rp-email"
                    type="email"
                    className="rpl-input"
                    placeholder="you@hotel.com"
                    value={email}
                    onChange={e => setEmail(e.target.value)}
                    required
                    autoComplete="email"
                  />
                </div>
              </div>

              {/* Password */}
              <div style={{ marginBottom: 20 }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 6 }}>
                  <label style={{ fontSize: '0.75rem', fontWeight: 600, color: 'rgba(240,246,255,0.5)', textTransform: 'uppercase', letterSpacing: '0.07em' }} htmlFor="rp-password">Password</label>
                  <a href="#" style={{ fontSize: '0.8rem', color: '#1080D0', fontWeight: 500, textDecoration: 'none' }}>Forgot password?</a>
                </div>
                <div style={{ position: 'relative' }}>
                  <span className="input-icon-left"><IconLock /></span>
                  <input
                    id="rp-password"
                    type={showPassword ? 'text' : 'password'}
                    className="rpl-input"
                    placeholder="••••••••"
                    value={password}
                    onChange={e => setPassword(e.target.value)}
                    required
                    autoComplete="current-password"
                    style={{ paddingRight: 44 }}
                  />
                  <button type="button" className="rpl-pw-toggle" onClick={() => setShowPass(v => !v)} aria-label="Toggle password visibility">
                    <IconEye off={showPassword} />
                  </button>
                </div>
              </div>

              {/* Error */}
              {error && (
                <div style={{
                  background: 'rgba(239,68,68,0.1)', border: '1px solid rgba(239,68,68,0.25)',
                  borderRadius: 10, padding: '12px 16px', marginBottom: 16,
                  fontSize: '0.875rem', color: '#f87171',
                  display: 'flex', alignItems: 'center', gap: 8,
                }}>
                  <span>⚠</span> {error}
                </div>
              )}

              {/* Submit */}
              <button type="submit" className="rpl-primary-btn" disabled={loading} style={{ marginBottom: 16 }}>
                {loading ? <><IconSpinner /> Signing in…</> : <>Sign in <IconArrowRight /></>}
              </button>

              {/* Divider */}
              <div style={{ display: 'flex', alignItems: 'center', gap: 12, margin: '16px 0' }}>
                <div style={{ flex: 1, height: 1, background: 'rgba(255,255,255,0.07)' }} />
                <span style={{ fontSize: '0.75rem', color: 'rgba(255,255,255,0.3)' }}>OR</span>
                <div style={{ flex: 1, height: 1, background: 'rgba(255,255,255,0.07)' }} />
              </div>

              {/* SSO */}
              <button type="button" className="rpl-sso-btn">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor">
                  <path d="M12 0C5.37 0 0 5.37 0 12c0 5.31 3.435 9.795 8.205 11.385.6.105.825-.255.825-.57 0-.285-.015-1.23-.015-2.235-3.015.555-3.795-.735-4.035-1.41-.135-.345-.72-1.41-1.23-1.695-.42-.225-1.02-.78-.015-.795.945-.015 1.62.87 1.845 1.23 1.08 1.815 2.805 1.305 3.495.99.105-.78.42-1.305.765-1.605-2.67-.3-5.46-1.335-5.46-5.925 0-1.305.465-2.385 1.23-3.225-.12-.3-.54-1.53.12-3.18 0 0 1.005-.315 3.3 1.23.96-.27 1.98-.405 3-.405s2.04.135 3 .405c2.295-1.56 3.3-1.23 3.3-1.23.66 1.65.24 2.88.12 3.18.765.84 1.23 1.905 1.23 3.225 0 4.605-2.805 5.625-5.475 5.925.435.375.81 1.095.81 2.22 0 1.605-.015 2.895-.015 3.3 0 .315.225.69.825.57A12.02 12.02 0 0 0 24 12c0-6.63-5.37-12-12-12z"/>
                </svg>
                Continue with SSO / GitHub
              </button>
            </form>

            <p style={{ fontSize: '0.75rem', textAlign: 'center', color: 'rgba(240,246,255,0.3)', lineHeight: 1.7, marginTop: 24 }}>
              By signing in, you agree to RelayPoint's{' '}
              <a href="#" style={{ color: '#1080D0' }}>Terms of Service</a> and{' '}
              <a href="#" style={{ color: '#1080D0' }}>Privacy Policy</a>.<br />
              Protected by 256-bit TLS encryption.
            </p>
          </div>
        </div>
      </div>
    </>
  )
}
