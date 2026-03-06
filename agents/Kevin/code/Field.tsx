import React from 'react';

export interface FieldProps extends React.InputHTMLAttributes<HTMLInputElement> {
  label?: string;
  error?: string | null;
  id?: string;
  hint?: string;
}

export const Field: React.FC<FieldProps> = ({ label, error, id, hint, ...inputProps }) => {
  const inputId = id || `field-${Math.random().toString(36).slice(2, 9)}`;

  return (
    <div className="flex flex-col gap-1">
      {label && (
        <label htmlFor={inputId} className="text-sm font-medium text-gray-700">
          {label}
        </label>
      )}
      <input
        id={inputId}
        {...inputProps}
        className={`px-3 py-2 rounded-md border focus:outline-none focus:ring-2 focus:ring-blue-400 ${error ? 'border-red-500' : 'border-gray-200'} `}
        aria-invalid={!!error}
        aria-describedby={error ? `${inputId}-error` : hint ? `${inputId}-hint` : undefined}
      />
      {hint && !error && (
        <p id={`${inputId}-hint`} className="text-xs text-gray-500">
          {hint}
        </p>
      )}
      {error && (
        <p id={`${inputId}-error`} className="text-xs text-red-600">
          {error}
        </p>
      )}
    </div>
  );
};

export default Field;
