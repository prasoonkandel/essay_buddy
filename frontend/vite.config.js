import { defineConfig, loadEnv } from "vite";

export default defineConfig(({ mode }) => {
  const env = loadEnv(mode, process.cwd(), "");

  return {
    define: {
      "import.meta.env.API_BASE_URL": JSON.stringify(env.API_BASE_URL),
    },
  };
});
