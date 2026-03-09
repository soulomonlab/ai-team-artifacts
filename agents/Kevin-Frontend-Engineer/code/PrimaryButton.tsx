import React from 'react';

export interface PrimaryButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  label: string;
  variant?: 'solid' | 'outline';
}

export const PrimaryButton: React.FC<PrimaryButtonProps> = ({ label, variant = 'solid', className = '', disabled, ...rest }) => {
  const base = 'inline-flex items-center justify-center rounded-md font-medium focus:outline-none focus:ring-2 focus:ring-offset-2';
  const solid = 'bg-primary-600 text-white hover:bg-primary-700 disabled:opacity-50';
  const outline = 'border border-primary-600 text-primary-600 hover:bg-primary-50 disabled:opacity-50';

  const classes = `${base} ${variant === 'solid' ? solid : outline} ${className}`;

  return (
    <button className={classes} disabled={disabled} aria-disabled={disabled} {...rest}>
      {label}
    </button>
  );
};

export default PrimaryButton;
