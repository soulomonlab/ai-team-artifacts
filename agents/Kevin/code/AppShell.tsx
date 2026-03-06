import React from 'react';

export interface AppShellProps {
  header?: React.ReactNode;
  footer?: React.ReactNode;
  children: React.ReactNode;
}

export const AppShell: React.FC<AppShellProps> = ({ header, footer, children }) => {
  return (
    <div className="min-h-screen bg-gray-50 text-gray-900">
      {header}
      <main className="max-w-3xl mx-auto px-4 py-6">{children}</main>
      {footer}
    </div>
  );
};

export default AppShell;
