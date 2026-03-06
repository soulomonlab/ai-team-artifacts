import React from 'react';

export interface ListItemCardProps {
  title: string;
  subtitle?: string;
  avatar?: React.ReactNode;
  onClick?: () => void;
  metadata?: string;
  className?: string;
}

export const ListItemCard: React.FC<ListItemCardProps> = ({ title, subtitle, avatar, onClick, metadata, className = '' }) => {
  return (
    <div
      role={onClick ? 'button' : undefined}
      tabIndex={onClick ? 0 : undefined}
      onClick={onClick}
      onKeyDown={(e) => (e.key === 'Enter' || e.key === ' ') && onClick && onClick()}
      className={`flex items-center gap-3 p-3 rounded-md border bg-white ${onClick ? 'hover:shadow-sm cursor-pointer' : ''} ${className}`}
    >
      <div className="w-10 h-10 rounded-full overflow-hidden bg-gray-100 flex items-center justify-center">{avatar}</div>
      <div className="flex-1">
        <div className="text-sm font-medium">{title}</div>
        {subtitle && <div className="text-xs text-gray-500">{subtitle}</div>}
      </div>
      {metadata && <div className="text-xs text-gray-400">{metadata}</div>}
    </div>
  );
};

export default ListItemCard;
