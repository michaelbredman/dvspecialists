/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ['./*.html', './resources/**/*.html'],
  theme: {
    extend: {
      colors: {
        teal: { light: '#53cfd6', DEFAULT: '#026766' },
        brand: { orange: '#f3651a', 'orange-lt': '#ffa360', cream: '#fcedbf' }
      }
    }
  },
  plugins: [],
}
