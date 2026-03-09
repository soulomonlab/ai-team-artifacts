import React from 'react';

interface AppShellProps {
  children: React.ReactNode;
  title?: string;
  onBack?: () => void;
}

export const AppShell: React.FC<AppShellProps> = ({ children, title, onBack }) => {
  return (
    <div className="min-h-screen bg-gray-50 text-gray-900">
      <header className="sticky top-0 bg-white border-b border-gray-200 z-40">
        <div className="max-w-2xl mx-auto px-4 py-3 flex items-center gap-3">
          {onBack && (
            <button onClick={onBack} aria-label="Back" className="p-2 rounded-md">
              {/* simple chevron */}
              <svg width="20" height="20" viewBox="0 0 20 20" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M12 15L7 10L12 5" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" />
              </svg>
            </button>
          )}
          <h1 className="text-lg font-semibold">{title || 'App'}</h1>
        </div>
      </header>

      <main className="max-w-2xl mx-auto px-4 py-6">{children}</main>

      <footer className="fixed bottom-0 left-0 right-0 bg-white border-t border-gray-200 md:hidden">
        <div className="max-w-2xl mx-auto px-4 py-2 flex justify-between">
          <button className="p-2">Home</button>
          <button className="p-2">Search</button>
          <button className="p-2">Profile</button>
        </div>
      </footer>
    </div>
  );
};

export default AppShell;
