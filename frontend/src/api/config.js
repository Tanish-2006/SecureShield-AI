const config = {
  API_BASE_URL: import.meta.env.VITE_API_URL
    || import.meta.env.VITE_API_BASE_URL
    || (import.meta.env.PROD
      ? "/api"
      : import.meta.env.VITE_API_BASE_URL),
  REQUEST_TIMEOUT: parseInt(import.meta.env.VITE_API_TIMEOUT || "30000", 10),
};

export default config;
