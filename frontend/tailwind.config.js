/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        primary: {
          DEFAULT: '#102A43',
          dark: '#0B1C2D',
          light: '#243B53',
        },
        secondary: {
          DEFAULT: '#247BA0',
          dark: '#1A5A75',
          light: '#3AA5D8',
        },
        accent: {
          DEFAULT: '#20B2AA',
          dark: '#147D77',
          light: '#48D1CC',
        },
        surface: {
          bg: '#F4F8FB',
          card: '#FFFFFF',
          muted: '#E2E8F0',
        },
        status: {
          success: '#2E9D72',
          warning: '#E9A23B',
          emergency: '#D64545',
        }
      },
      fontFamily: {
        sans: ['Plus Jakarta Sans', 'Inter', 'system-ui', 'sans-serif'],
      }
    },
  },
  plugins: [],
}
