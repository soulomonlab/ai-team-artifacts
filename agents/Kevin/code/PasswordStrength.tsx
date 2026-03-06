import React from 'react';

export type Strength = { score: number; label: string; color: string };

function calculateStrength(password: string): Strength {
  let score = 0;
  if (password.length >= 8) score++;
  if (/[A-Z]/.test(password)) score++;
  if (/[0-9]/.test(password)) score++;
  if (/[^A-Za-z0-9]/.test(password)) score++;

  if (score <= 1) return { score, label: 'Weak', color: 'bg-red-500' };
  if (score === 2) return { score, label: 'Fair', color: 'bg-yellow-400' };
  if (score === 3) return { score, label: 'Good', color: 'bg-green-400' };
  return { score, label: 'Strong', color: 'bg-green-600' };
}

export const PasswordStrength: React.FC<{ password: string }> = ({ password }) => {
  const s = calculateStrength(password);
  const pct = Math.min(100, (s.score / 4) * 100);
  return (
    <div aria-live="polite" className="mt-2">
      <div className="w-full bg-gray-200 h-2 rounded">
        <div className={`${s.color} h-2 rounded`} style={{ width: `${pct}%` }} />
      </div>
      <div className="mt-1 text-sm text-gray-600">Strength: {s.label}</div>
    </div>
  );
};

export default PasswordStrength;
