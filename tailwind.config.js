/** @type {import('tailwindcss').Config} */
let primaryBase = ''
module.exports = {
  content: [
    './flaskr/templates/**/*.html'
  ],
  theme: {
    fontFamily: {
      'jk-marugo': ['jk-marugo', 'ui-sans-serif', 'system-ui',],
      'kaiso': ['kaiso', 'ui-sans-serif', 'system-ui',],
    },
    extend: {
      colors: {
        primary: {
          white: '#faf5ff',
          light: '#e9d5ff',
          pale: '#c084fc',
          mid: '#9333ea',
          strong: '#7e22ce',
          dark: '#6b21a8',
          deep: '#6b21a8',
        }
      }
    },
  },
  plugins: [],
}
