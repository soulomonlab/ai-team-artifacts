// designTokens.ts
// Lightweight token bridge between design and Tailwind/CSS variables.
// Source of truth: output/design/core_flows_and_design_tokens.md (Maya)

export type ThemeTokens = {
  colorPrimary: string;
  colorOnPrimary: string;
  colorSurface: string;
  colorText: string;
  spacingBase: string; // e.g., "8px"
  radiusBase: string;
  fontFamilyBase: string;
};

// Implementation prefers CSS variables so designers can tweak tokens at runtime.
// Keep values minimal here; final values must be synced with design file.
export const tokens: ThemeTokens = {
  colorPrimary: "var(--color-primary, #2563EB)",
  colorOnPrimary: "var(--color-on-primary, #ffffff)",
  colorSurface: "var(--color-surface, #ffffff)",
  colorText: "var(--color-text, #0f172a)",
  spacingBase: "var(--spacing-base, 8px)",
  radiusBase: "var(--radius-base, 8px)",
  fontFamilyBase: "Inter, Roboto, system-ui, -apple-system, 'Helvetica Neue'",
};

// Decision: Use CSS variables for theming + Tailwind utility classes for layout.
// Pros: runtime theming, small bundle impact. Con: requires agreement with design tokens file.

export default tokens;
