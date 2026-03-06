import React from 'react';

interface StrengthResult {
  score: number; // 0-4
  label: string;
}

interface PasswordStrengthProps {
  password: string;
}

function calculateStrength(password: string): StrengthResult {
  let score = 0;
  if (password.length >= 8) score++;
  if (/[A-Z]/.test(password)) score++;
  if (/[0-9]/.test(password)) score++;
  if (/[^A-Za-z0-9]/.test(password)) score++;

  const labels = ['Very weak', 'Weak', 'Okay', 'Good', 'Strong'];
  return { score: Math.max(0, Math.min(4, score)), label: labels[Math.max(0, Math.min(4, score))] };
}

export const PasswordStrength: React.FC<PasswordStrengthProps> = ({ password }) => {
  const { score, label } = calculateStrength(password);
  const colors = ['bg-red-400', 'bg-red-300', 'bg-yellow-300', 'bg-green-300', 'bg-green-500'];

  return (
    <div aria-live="polite" className="mt-2">
      <div className="flex space-x-1 h-2">
        {Array.from({ length: 5 }).map((_, i) => (
          <div key={i} className={`flex-1 rounded ${i <= score - 1 ? colors[score] : 'bg-gray-200'}`} />
        ))}
      </div>
      <div className="text-xs text-gray-600 mt-1">{label}</div>
    </div>
  );
};

export default PasswordStrength;
