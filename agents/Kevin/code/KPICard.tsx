import React from 'react';

interface Props {
  title: string;
  value: string | number;
  unit?: string;
  delta?: number | null; // percent
  subtitle?: string;
  onClick?: () => void;
  className?: string;
}

export const KPICard: React.FC<Props> = ({ title, value, unit, delta, subtitle, onClick, className = '' }) => {
  const deltaLabel = delta === null || delta === undefined ? null : `${delta > 0 ? '+' : ''}${delta}%`;
  const deltaColor = delta === null || delta === undefined ? 'text-gray-500' : delta >= 0 ? 'text-green-600' : 'text-red-600';

  return (
    <div
      role="button"
      tabIndex={0}
      onClick={onClick}
      onKeyDown={(e) => (e.key === 'Enter' || e.key === ' ') && onClick && onClick()}
      className={`rounded-lg border p-4 bg-white shadow-sm focus:outline-none focus:ring-2 focus:ring-offset-1 ${className}`}
    >
      <div className="flex items-baseline justify-between gap-2">
        <div>
          <div className="text-xs text-gray-500">{title}</div>
          <div className="text-2xl font-semibold">
            {value}
            {unit && <span className="text-sm font-medium ml-1">{unit}</span>}
          </div>
        </div>
        {deltaLabel && <div className={`text-sm font-medium ${deltaColor}`}>{deltaLabel}</div>}
      </div>
      {subtitle && <div className="mt-2 text-xs text-gray-500">{subtitle}</div>}
    </div>
  );
};

export default KPICard;
