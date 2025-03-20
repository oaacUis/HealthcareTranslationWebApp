/** @type {import('next').NextConfig} */
const nextConfig = {
    reactStrictMode: true,
    env: {
      NEXT_PUBLIC_API_BASE_URL: "http://localhost:8000", // Cambiar en producción
    },
  };
  
  module.exports = nextConfig;
  