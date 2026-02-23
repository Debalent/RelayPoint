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
        background: 'rgba(255,255,255,0.96)',
        borderRadius: variant === 'icon' ? '10px' : '8px',
        padding: variant === 'icon' ? '4px' : '4px 10px',
        boxShadow: '0 1px 4px rgba(0,0,0,0.18)',
        ...style,
      }}
    >
      <img
        src={src}
        alt={alt}
        style={{ height, width: 'auto', display: 'block' }}
        loading="eager"
        draggable={false}
      />
    </span>
  );
}
