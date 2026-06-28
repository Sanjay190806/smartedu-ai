import type { Config } from "tailwindcss";

export default {
  darkMode: ["class"],
  content: ["./index.html", "./src/**/*.{ts,tsx}"],
  theme: {
    extend: {
      fontFamily: {
        sans: ["Inter", "ui-sans-serif", "system-ui", "sans-serif"],
      },
      colors: {
        border: "hsl(var(--border))",
        input: "hsl(var(--input))",
        ring: "hsl(var(--ring))",
        background: "hsl(var(--background))",
        foreground: "hsl(var(--foreground))",
        primary: {
          DEFAULT: "hsl(var(--primary))",
          foreground: "hsl(var(--primary-foreground))",
        },
        muted: {
          DEFAULT: "hsl(var(--muted))",
          foreground: "hsl(var(--muted-foreground))",
        },
        card: {
          DEFAULT: "hsl(var(--card))",
          foreground: "hsl(var(--card-foreground))",
        },
        surface: {
          DEFAULT: "hsl(var(--surface))",
          strong: "hsl(var(--surface-strong))",
        },
        "accent-cyan": "hsl(var(--accent-cyan))",
        "accent-violet": "hsl(var(--accent-violet))",
        success: "hsl(var(--success))",
        warning: "hsl(var(--warning))",
        danger: "hsl(var(--danger))",
      },
      boxShadow: {
        glow: "0 20px 80px rgba(14, 165, 233, 0.18)",
        "inner-glow": "inset 0 1px 0 rgba(255,255,255,0.10)",
      },
      backgroundImage: {
        "mesh-dark": "radial-gradient(circle at top left, rgba(56,189,248,0.20), transparent 28rem), radial-gradient(circle at 80% 10%, rgba(168,85,247,0.16), transparent 26rem)",
        "mesh-light": "radial-gradient(circle at top left, rgba(14,116,144,0.12), transparent 28rem), radial-gradient(circle at 80% 10%, rgba(124,58,237,0.10), transparent 26rem)",
      },
    },
  },
  plugins: [],
} satisfies Config;
