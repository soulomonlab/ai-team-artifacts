import React from 'react';
import { tokens } from './designTokens';

export interface PrimaryButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  label: string;
  loading?: boolean;
}

export const PrimaryButton: React.FC<PrimaryButtonProps> = ({ label, loading, disabled, ...rest }) => {
  const isDisabled = disabled || loading;
  return (
    <button
      {...rest}
      disabled={isDisabled}
      style={{
        background: isDisabled ? '#93C5FD' : tokens.colors.primary,
        color: '#FFFFFF',
        border: 'none',
        padding: `${tokens.spacing.sm}px ${tokens.spacing.lg}px`,
        borderRadius: tokens.radius.sm,
        fontSize: tokens.typography.scale.md,
        fontFamily: tokens.typography.fontFamily,
        opacity: isDisabled ? 0.8 : 1,
        cursor: isDisabled ? 'not-allowed' : 'pointer',
      }}
      aria-busy={loading}
    >
      {loading ? 'Loading...' : label}
    </button>
  );
};

export default PrimaryButton;
