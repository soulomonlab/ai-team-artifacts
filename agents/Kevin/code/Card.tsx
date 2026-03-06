import React from 'react';

export interface CardProps {
  title: string;
  subtitle?: string;
  onClick?: () => void;
  children?: React.ReactNode;
}

export const Card: React.FC<CardProps> = ({ title, subtitle, onClick, children }) => {
  return (
    <article
      role={onClick ? 'button' : 'article'}
      onClick={onClick}
      tabIndex={0}
      className="w-full bg-white rounded-lg shadow-sm p-4 mb-3 focus:outline-none focus:ring-2 focus:ring-blue-300"
      aria-label={title}
    >
      <div className="flex items-start justify-between">
        <div>
          <h2 className="text-sm font-medium text-gray-900">{title}</h2>
          {subtitle && <p className="text-xs text-gray-500 mt-1">{subtitle}</p>}
        </div>
      </div>
      {children && <div className="mt-3">{children}</div>}
    </article>
  );
};

export default Card;
