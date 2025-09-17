import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import { fileURLToPath, URL } from 'node:url'

export default defineConfig({
  plugins: [vue()],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url)), // @ 指向 src
    },
  },
  server: {
    port: 5173,
    proxy: {
      '/api': 'http://localhost:5000'  // 所有 /api 请求代理到后端
    }
  }
})
