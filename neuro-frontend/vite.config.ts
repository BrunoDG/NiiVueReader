import { defineConfig } from "vite";
import vue from "@vitejs/plugin-vue";
import path from "path";

export default defineConfig({
  plugins: [vue()],
  resolve: {
    alias: {
      "@": path.resolve(__dirname, "./src"),
      buffer: "buffer", // Adiciona o alias para o módulo buffer
    },
  },
  define: {
    global: "globalThis", // Emula o objeto global no navegador
  },
});
