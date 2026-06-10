import type { Config } from "tailwindcss";

export default {
  content: ["./index.html", "./src/**/*.{ts,tsx}"],
  theme: {
    extend: {
      colors: {
        leaf: {
          50: "#f3faf5",
          100: "#e3f4e8",
          300: "#9dd9b0",
          500: "#3f9d63",
          600: "#2f8050",
          700: "#266641",
          900: "#16382a"
        }
      },
      fontFamily: {
        sans: ["Inter", "system-ui", "sans-serif"]
      }
    }
  },
  plugins: []
} satisfies Config;
