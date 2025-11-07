import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import { resolve } from 'path'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [vue()],
  resolve: {
    alias: {
      '@': resolve(__dirname, 'src')
    }
  },
  server: {
    port: 5173,
    host: '0.0.0.0', // 允许外部访问
    open: true,
    allowedHosts: [
      'aippof-0w0.lthero.com', // 您的域名
      'localhost',
      '.lthero.com' // 允许所有 lthero.com 子域名
    ],
    proxy: {
      '/api': {
        // ✅ 使用环境变量或默认本地地址
        // 生产环境：设置 VITE_API_URL=https://aippof-0w0.lthero.com/api
        // 开发环境：默认 http://localhost:8000
        target: process.env.VITE_API_URL || 'http://localhost:8000',
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/api/, '')
      }
    }
  },
  build: {
    outDir: 'dist',
    sourcemap: false,
    rollupOptions: {
      output: {
        manualChunks: {
          'vue-vendor': ['vue', 'vue-router', 'pinia'],
          'echarts-vendor': ['echarts', 'vue-echarts']
        }
      }
    }
  }
})
