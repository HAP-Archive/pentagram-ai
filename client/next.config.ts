import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  logging: {
    fetches: {
      hmrRefreshes: true,
      fullUrl: true,
    }
  }
};

export default nextConfig;
