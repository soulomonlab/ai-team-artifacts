import React from 'react';

export interface QuickActionProps {
  icon?: React.ReactNode;
  title: string;
  subtitle?: string;
  onClick?: () => void;
  badge?: string | number;
  className?: string;
}

export const QuickAction: React.FC<QuickActionProps> = ({ icon, title, subtitle, onClick, badge, className = '' }) => {
  return (
    <button
      type="button"
      onClick={onClick}
      className={`w-full flex items-center gap-3 p-3 rounded-md border bg-white hover:shadow-sm ${className}`}
    >
      <div className="w-10 h-10 flex items-center justify-center rounded-md bg-gray-100">{icon}</div>
      <div className="flex-1 text-left">
        <div className="text-sm font-medium">{title}</div>
        {subtitle && <div className="text-xs text-gray-500">{subtitle}</div>}
      </div>
      {badge !== undefined && (
        <div className="text-xs bg-blue-100 text-blue-800 px-2 py-1 rounded-full">{badge}</div>
      )}
    </button>
  );
};

export default QuickAction;
