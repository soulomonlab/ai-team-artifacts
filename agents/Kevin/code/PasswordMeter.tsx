import React from 'react';

interface Props {
  password: string;
}

const scorePassword = (password: string) => {
  let score = 0;
  if (!password) return 0;
  if (password.length >= 8) score += 1;
  if (/[A-Z]/.test(password)) score += 1;
  if (/[0-9]/.test(password)) score += 1;
  if (/[^A-Za-z0-9]/.test(password)) score += 1;
  if (password.length >= 12) score += 1;
  return score; // 0..5
};

export const PasswordMeter: React.FC<Props> = ({ password }) => {
  const score = scorePassword(password);
  const pct = (score / 5) * 100;
  const color = score <= 1 ? 'bg-red-500' : score <= 3 ? 'bg-yellow-400' : 'bg-green-500';

  return (
    <div aria-hidden className="w-full">
      <div className="h-2 w-full bg-gray-200 rounded overflow-hidden">
        <div className={`${color} h-2`} style={{ width: `${pct}%` }} />
      </div>
      <div className="mt-1 text-xs text-gray-600">{['Too weak', 'Weak', 'Okay', 'Strong', 'Very strong'][Math.max(0, score - 1)]}</div>
    </div>
  );
};

export default PasswordMeter;
