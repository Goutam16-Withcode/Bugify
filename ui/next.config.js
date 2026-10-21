/** @type {import('next').NextConfig} */
const backendUrl = (process.env.BACKEND_API_URL || process.env.NEXT_PUBLIC_BACKEND_URL || 'https://bugify-5.onrender.com').replace(/\/+$/, '');

const nextConfig = {
  async rewrites() {
    return [
      {
        source: '/api/:path*',
        destination: `${backendUrl}/api/:path*`,
      },
    ];
  },
};

module.exports = nextConfig;

