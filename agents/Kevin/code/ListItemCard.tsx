import React from 'react';

interface Props {
  title: string;
  subtitle?: string;
  avatar?: React.ReactNode;
  onClick?: () => void;
  rightAccessory?: React.ReactNode;
  className?: string;
}

export const ListItemCard: React.FC<Props> = ({ title, subtitle, avatar, onClick, rightAccessory, className = '' }) => {
  return (
    <div
      role={onClick ? 'button' : undefined}
      tabIndex={onClick ? 0 : undefined}
      onClick={onClick}
      onKeyDown={(e) => (onClick && (e.key === 'Enter' || e.key === ' ')) && onClick()}
      className={`flex items-center gap-3 rounded-md p-3 border bg-white ${className}`}
    >
      {avatar && <div className="w-10 h-10 rounded-full overflow-hidden flex-none">{avatar}</div>}
      <div className="flex-1 min-w-0">
        <div className="text-sm font-medium truncate">{title}</div>
        {subtitle && <div className="text-xs text-gray-500 truncate">{subtitle}</div>}
      </div>
      {rightAccessory && <div className="flex-none ml-2">{rightAccessory}</div>}
    </div>
  );
};

export default ListItemCard;
