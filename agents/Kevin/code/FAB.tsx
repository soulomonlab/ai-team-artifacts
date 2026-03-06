import React from 'react';

export interface FABProps {
  onClick: () => void;
  ariaLabel?: string;
}

export const FAB: React.FC<FABProps> = ({ onClick, ariaLabel = 'primary-action' }) => {
  return (
    <button
      aria-label={ariaLabel}
      onClick={onClick}
      className="fixed bottom-6 right-6 w-14 h-14 rounded-full bg-indigo-600 text-white shadow-lg flex items-center justify-center hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-indigo-500"
    >
      <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className="feather feather-plus">
        <line x1="12" y1="5" x2="12" y2="19"></line>
        <line x1="5" y1="12" x2="19" y2="12"></line>
      </svg>
    </button>
  );
};

export default FAB;
