import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

export default defineConfig({
  plugins: [react()],
  server: {
    port: 5173,
    proxy: {
      // send /api/* to Flask
      "/api": "http://localhost:5001"
    }
  }
});
