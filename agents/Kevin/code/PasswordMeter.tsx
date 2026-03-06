import React, { useMemo } from 'react';

export interface PasswordMeterProps {
  password: string;
  minLength?: number;
}

export const PasswordMeter: React.FC<PasswordMeterProps> = ({ password, minLength = 8 }) => {
  const score = useMemo(() => {
    let s = 0;
    if (password.length >= minLength) s += 1;
    if (/[A-Z]/.test(password)) s += 1;
    if (/[0-9]/.test(password)) s += 1;
    if (/[^A-Za-z0-9]/.test(password)) s += 1;
    return Math.min(s, 4);
  }, [password, minLength]);

  const labels = ['Too weak', 'Weak', 'Okay', 'Strong', 'Excellent'];
  const colors = ['bg-red-500', 'bg-orange-400', 'bg-yellow-400', 'bg-green-400', 'bg-green-600'];

  return (
    <div className="flex flex-col gap-1">
      <div className="w-full h-2 bg-gray-200 rounded flex overflow-hidden">
        <div className={`h-full ${colors[score]} transition-width duration-200`} style={{ width: `${(score / 4) * 100}%` }} />
      </div>
      <div className="flex justify-between text-xs text-gray-600">
        <span>{labels[score]}</span>
        <span>{password.length}/{minLength}</span>
      </div>
    </div>
  );
};

export default PasswordMeter;
