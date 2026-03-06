// Design tokens for the MVP (mobile-first)
// Used by frontend components. Keep tokens simple and framework-agnostic.

export const tokens = {
  colors: {
    primary: '#2563EB', // blue-600
    primaryHover: '#1D4ED8',
    background: '#F9FAFB', // gray-50
    surface: '#FFFFFF', // card background
    muted: '#6B7280',
    danger: '#DC2626',
  },
  spacing: {
    xs: 4,
    sm: 8,
    md: 16,
    lg: 24,
    xl: 32,
  },
  radius: {
    sm: 6,
    md: 10,
    lg: 14,
  },
  typography: {
    fontFamily: "Inter, ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, 'Helvetica Neue', Arial",
    base: 16,
    scale: {
      xs: 12,
      sm: 14,
      md: 16,
      lg: 20,
      xl: 24,
    },
  },
};
