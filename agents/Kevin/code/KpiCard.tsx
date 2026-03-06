import React from 'react';

export interface KpiCardProps {
  title: string;
  value: string | number;
  delta?: string | number | null;
  trend?: 'up' | 'down' | 'neutral';
  description?: string;
  onClick?: () => void;
  className?: string;
}

export const KpiCard: React.FC<KpiCardProps> = ({ title, value, delta, trend = 'neutral', description, onClick, className = '' }) => {
  const trendColor = trend === 'up' ? 'text-green-600' : trend === 'down' ? 'text-red-600' : 'text-gray-500';

  return (
    <div
      role="button"
      tabIndex={0}
      onClick={onClick}
      onKeyDown={(e) => (e.key === 'Enter' || e.key === ' ') && onClick && onClick()}
      className={`p-4 rounded-lg shadow-sm bg-white border ${className}`}
    >
      <div className="flex items-center justify-between">
        <h3 className="text-sm text-gray-600">{title}</h3>
        {delta !== undefined && (
          <div className={`text-xs font-medium ${trendColor}`} aria-hidden>
            {trend === 'up' && '▲'}{trend === 'down' && '▼'} {delta}
          </div>
        )}
      </div>
      <div className="mt-2 flex items-baseline gap-2">
        <span className="text-2xl font-semibold">{value}</span>
        {description && <span className="text-xs text-gray-500">{description}</span>}
      </div>
    </div>
  );
};

export default KpiCard;
