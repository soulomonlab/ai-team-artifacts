import React from 'react';

export interface FABProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  icon: React.ReactNode;
  label?: string;
}

export const FAB: React.FC<FABProps> = ({ icon, label = '', className = '', ...rest }) => {
  return (
    <button
      className={`fixed right-4 bottom-6 z-50 inline-flex items-center justify-center rounded-full shadow-lg h-14 w-14 bg-primary-600 text-white hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-offset-2 ${className}`}
      aria-label={label || 'Primary action'}
      {...rest}
    >
      {icon}
    </button>
  );
};

export default FAB;
