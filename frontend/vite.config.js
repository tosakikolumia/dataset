import { fileURLToPath, URL } from 'node:url'
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [
    vue(),
  ],
  resolve: {
    alias: {
      // 关键配置：将 '@' 映射到 'src' 目录
      // 这是为了支持你在 Navbar.vue 中使用的 '@/stores/auth' 写法
      '@': fileURLToPath(new URL('./src', import.meta.url))
    }
  },
  server: {
    port: 5173, // 可选：指定开发服务器端口
    open: true  // 可选：启动时自动在浏览器打开
  }
})