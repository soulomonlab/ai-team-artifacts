import React from 'react';

export interface CardProps extends React.HTMLAttributes<HTMLDivElement> {
  title?: string;
  children: React.ReactNode;
}

export const Card: React.FC<CardProps> = ({ title, children, className = '', ...rest }) => {
  return (
    <div className={`bg-white shadow-md rounded-lg p-6 ${className}`} {...rest}>
      {title && <h3 className="text-lg font-semibold mb-4">{title}</h3>}
      <div>{children}</div>
    </div>
  );
};

export default Card;
