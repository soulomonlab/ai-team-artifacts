import React from 'react';

interface Props {
  icon?: React.ReactNode;
  label: string;
  onClick?: () => void;
  className?: string;
}

export const QuickAction: React.FC<Props> = ({ icon, label, onClick, className = '' }) => {
  return (
    <button
      type="button"
      onClick={onClick}
      className={`flex items-center gap-3 rounded-md border px-3 py-2 text-sm bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-1 ${className}`}
    >
      {icon && <span className="w-5 h-5 flex-none">{icon}</span>}
      <span className="truncate">{label}</span>
    </button>
  );
};

export default QuickAction;
