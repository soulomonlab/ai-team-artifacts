import React from 'react';
import { tokens } from './designTokens';

export interface HeaderProps {
  title: string;
  onBack?: () => void;
}

export const Header: React.FC<HeaderProps> = ({ title, onBack }) => {
  return (
    <div style={{
      display: 'flex',
      alignItems: 'center',
      gap: tokens.spacing.sm,
    }}>
      {onBack && (
        <button onClick={onBack} aria-label="Back" style={{
          background: 'transparent',
          border: 'none',
          fontSize: tokens.typography.scale.md,
          cursor: 'pointer',
        }}>←</button>
      )}
      <h1 style={{ fontSize: tokens.typography.scale.lg, margin: 0 }}>{title}</h1>
    </div>
  );
};

export default Header;
