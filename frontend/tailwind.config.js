/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./src/**/*.{html,js,jsx}"], // fixed pattern  
  theme: {
    extend: {
      colors: {
        primary: "#A32033",
        primaryLight : "#7f1f2d",
      }
    },
  },
  plugins: [],
}

