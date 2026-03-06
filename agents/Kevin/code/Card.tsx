import React from 'react';
import { tokens } from './designTokens';

export interface CardProps {
  title: string;
  subtitle?: string;
  children?: React.ReactNode;
  onClick?: () => void;
}

export const Card: React.FC<CardProps> = ({ title, subtitle, children, onClick }) => {
  return (
    <div
      role={onClick ? 'button' : undefined}
      onClick={onClick}
      tabIndex={onClick ? 0 : undefined}
      style={{
        background: tokens.colors.surface,
        borderRadius: tokens.radius.md,
        padding: tokens.spacing.md,
        boxShadow: '0 1px 2px rgba(0,0,0,0.06)',
        marginBottom: tokens.spacing.sm,
        cursor: onClick ? 'pointer' : 'default',
      }}
    >
      <div style={{ fontSize: tokens.typography.scale.lg, fontWeight: 600 }}>{title}</div>
      {subtitle && (
        <div style={{ fontSize: tokens.typography.scale.sm, color: tokens.colors.muted }}>{subtitle}</div>
      )}
      {children}
    </div>
  );
};

export default Card;
