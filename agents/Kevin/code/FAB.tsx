import React from 'react';

export interface FABProps {
  onClick: () => void;
  label?: string;
}

export const FAB: React.FC<FABProps> = ({ onClick, label = '+' }) => {
  return (
    <button
      aria-label={label}
      onClick={onClick}
      className="fixed bottom-6 right-6 w-14 h-14 rounded-full bg-blue-600 text-white shadow-lg flex items-center justify-center focus:outline-none focus:ring-2 focus:ring-blue-300"
    >
      <span className="text-2xl">{label}</span>
    </button>
  );
};

export default FAB;
