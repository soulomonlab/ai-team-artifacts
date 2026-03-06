import React from 'react';

export interface OAuthButtonProps {
  provider: 'google' | 'apple' | 'github' | string;
  onClick?: () => void;
  label?: string;
  disabled?: boolean;
  className?: string;
}

const providerStyles: Record<string, { bg: string; text: string }> = {
  google: { bg: 'bg-white', text: 'text-gray-800' },
  apple: { bg: 'bg-black', text: 'text-white' },
  github: { bg: 'bg-gray-900', text: 'text-white' },
};

export const OAuthButton: React.FC<OAuthButtonProps> = ({
  provider,
  onClick,
  label,
  disabled = false,
  className = '',
}) => {
  const styles = providerStyles[provider] || { bg: 'bg-gray-100', text: 'text-gray-800' };
  return (
    <button
      type="button"
      aria-label={`Sign up with ${provider}`}
      onClick={onClick}
      disabled={disabled}
      className={`flex items-center justify-center gap-3 px-4 py-2 rounded-md shadow-sm border ${styles.bg} ${styles.text} ${disabled ? 'opacity-50 cursor-not-allowed' : 'hover:scale-101'} ${className}`}
    >
      <span className="w-5 h-5 flex items-center justify-center" aria-hidden>
        {/* Simple provider icons (svg placeholders) */}
        {provider === 'google' && (
          <svg width="18" height="18" viewBox="0 0 48 48" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M44 24c0-1.6-.1-3.1-.4-4.6H24v8.7h11.9c-.5 2.7-2 5-4.2 6.5v5.5h6.8C41.6 37.9 44 31.5 44 24z" fill="#4285F4" />
          </svg>
        )}
        {provider === 'apple' && (
          <svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor" xmlns="http://www.w3.org/2000/svg">
            <path d="M16.365 1.43c-.94.056-2.08.64-2.77 1.38-.6.66-1.14 1.73-.95 2.77 1.04.07 2.1-.53 2.77-1.35.6-.73 1.02-1.8.95-2.82zM12.5 6.5c-2.94 0-4.96 1.95-6.28 1.95-1.34 0-3.01-1.87-5.06-1.87-2.3 0-4 2.3-4 5.5 0 3.5 2.3 8.34 6.06 12.23 1.97 1.86 3.96 3.96 6.84 3.96 2.9 0 3.62-1.35 6.77-1.35 3.18 0 4.11 1.35 6.77 1.35 2.97 0 4.67-1.96 6.37-3.82C29.9 19.63 32 14.12 32 10c0-4.87-3.99-7.5-7.5-7.5C21.5 2.5 16.5 6.5 12.5 6.5z" />
          </svg>
        )}
        {provider !== 'google' && provider !== 'apple' && provider !== 'github' && <span className="text-xs">{provider[0]?.toUpperCase()}</span>}
      </span>
      <span className="text-sm font-medium">{label || `Continue with ${provider}`}</span>
    </button>
  );
};

export default OAuthButton;
