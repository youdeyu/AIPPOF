/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{vue,js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        // 深色渐变主题色（参考YouTube Dubbing风格）
        'primary-dark': '#2C2A4A',     // 深紫
        'primary-blue': '#1A3A52',     // 深蓝
        'accent-purple': '#7C3AED',    // 紫色高亮
        'glass-bg': 'rgba(255, 255, 255, 0.05)',
        'glass-border': 'rgba(255, 255, 255, 0.1)',
      },
      backgroundImage: {
        'gradient-main': 'linear-gradient(135deg, #2C2A4A 0%, #1A3A52 100%)',
        'gradient-card': 'linear-gradient(135deg, rgba(124, 58, 237, 0.1) 0%, rgba(26, 58, 82, 0.1) 100%)',
      },
      backdropBlur: {
        'xs': '2px',
      },
      borderRadius: {
        'card': '16px',
      },
      boxShadow: {
        'glass': '0 8px 32px 0 rgba(31, 38, 135, 0.37)',
        'glow': '0 0 20px rgba(124, 58, 237, 0.5)',
      },
    },
  },
  plugins: [],
}
