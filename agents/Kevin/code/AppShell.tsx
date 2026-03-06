import React from 'react';
import type { ReactNode } from 'react';
import { tokens } from './designTokens';

interface AppShellProps {
  children: ReactNode;
  header?: ReactNode;
}

export const AppShell: React.FC<AppShellProps> = ({ children, header }) => {
  return (
    <div style={{
      fontFamily: tokens.typography.fontFamily,
      background: tokens.colors.background,
      minHeight: '100vh',
      padding: tokens.spacing.md,
      boxSizing: 'border-box',
    }}>
      <header style={{ marginBottom: tokens.spacing.md }}>
        {header}
      </header>
      <main>
        {children}
      </main>
    </div>
  );
};

export default AppShell;
