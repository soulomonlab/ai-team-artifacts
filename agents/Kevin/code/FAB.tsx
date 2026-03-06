import React from 'react';
import { tokens } from './designTokens';

export interface FABProps {
  onClick: () => void;
  ariaLabel?: string;
}

export const FAB: React.FC<FABProps> = ({ onClick, ariaLabel = 'Primary action' }) => {
  const size = 56;
  return (
    <button
      onClick={onClick}
      aria-label={ariaLabel}
      style={{
        position: 'fixed',
        right: tokens.spacing.md,
        bottom: tokens.spacing.md,
        width: size,
        height: size,
        borderRadius: '50%',
        background: tokens.colors.primary,
        color: '#fff',
        border: 'none',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        boxShadow: '0 6px 16px rgba(37,99,235,0.24)',
        cursor: 'pointer',
      }}
    >
      <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" aria-hidden>
        <path d="M12 5v14M5 12h14" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" />
      </svg>
    </button>
  );
};

export default FAB;
