import React, { PropsWithChildren } from 'react';

interface CardProps {
  className?: string;
  'aria-label'?: string;
}

export const Card: React.FC<PropsWithChildren<CardProps>> = ({ children, className = '', ...rest }) => {
  return (
    <div
      role="region"
      {...rest}
      className={`bg-white shadow-md rounded-lg p-6 border border-gray-100 ${className}`}
    >
      {children}
    </div>
  );
};

export default Card;
