import React from 'react';
import logoFile from '../../assets/relaypoint-logo.png';
import iconFile from '../../assets/relaypoint-icon.png';

/**
 * Logo component for RelayPoint.
 *
 * Props:
 *   variant  - 'full' (default) shows the full logo wordmark
 *              'icon' shows just the app icon (square, for collapsed sidebars)
 *   height   - CSS height string, default '36px'
 *   style    - additional inline styles
 *
 * The logo is displayed inside a white pill container so it reads clearly
 * on any background (dark navy UI or light pages).
 */
export default function Logo({ variant = 'full', height = '36px', style = {}, className = '' }) {
  const src = variant === 'icon' ? iconFile : logoFile;
  const alt = 'RelayPoint';

  return (
    <span
      className={`rp-logo-wrap ${className}`}
      style={{
        display: 'inline-flex',
        alignItems: 'center',
        justifyContent: 'center',
        background: 'linear-gradient(90deg, #4A90E2, #9013FE)',
        borderRadius: variant === 'icon' ? '12px' : '10px',
        padding: variant === 'icon' ? '6px' : '6px 12px',
        boxShadow: '0 4px 6px rgba(0, 0, 0, 0.1)',
        ...style,
      }}
    >
      <img
        src={src}
        alt={alt}
        style={{ height, objectFit: 'contain' }}
        loading="eager"
        draggable={false}
      />
    </span>
  );
}
