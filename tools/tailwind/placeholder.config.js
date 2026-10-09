// Placeholder used by `npm run build:css` until design/01-foundations/tailwind.config.js exists.
// Keep the real config in the same shape: plain Tailwind 3, CommonJS, theme only, so it can be
// reused in the Expo/NativeWind app later (add `presets: [require('nativewind/preset')]` there).
/** @type {import('tailwindcss').Config} */
module.exports = {
  theme: {
    extend: {
      fontFamily: {
        sans: ['"Inter Variable"', 'Inter', 'system-ui', 'sans-serif'],
      },
    },
  },
  plugins: [],
};
