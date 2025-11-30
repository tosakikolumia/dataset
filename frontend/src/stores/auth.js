import { defineStore } from 'pinia';
import api from '@/services/api'; // 👈 引入我们封装好的 api

export const useAuthStore = defineStore('auth', {
  state: () => ({
    user: JSON.parse(localStorage.getItem('user')) || null, // 从缓存恢复用户信息
    token: localStorage.getItem('token') || null,
    isAuthenticated: !!localStorage.getItem('token'),
  }),

  actions: {
    async login(credentials) {
      try {
        // 1. 发送请求给 Django 后端
        // 注意：Django 的 SimpleJWT 默认只需要 username 和 password
        const response = await api.auth.login({
          username: credentials.username,
          password: credentials.password
        });

        // 2. 获取后端返回的 access token
        const { access, refresh } = response.data;
        this.token = access;
        this.isAuthenticated = true;

        // 3. 处理用户信息
        // 因为后端 Token 暂时不包含 role 信息，我们先暂时“信任”用户在登录页选的角色
        // (在真实企业开发中，这里应该再次调用 api.get('/me/') 来获取准确角色，但这对 0 基础有点难，先跳过)
        this.user = {
          username: credentials.username,
          role: credentials.role // 把用户选的角色存下来，用于路由跳转
        };

        // 4. 持久化存储到浏览器 (刷新页面不丢失)
        localStorage.setItem('token', access);
        localStorage.setItem('refresh', refresh); // 存 refresh token 备用
        localStorage.setItem('user', JSON.stringify(this.user));

        return Promise.resolve(response);
      } catch (error) {
        console.error('Login Failed:', error);
        return Promise.reject(error);
      }
    },

    logout() {
      this.token = null;
      this.isAuthenticated = false;
      this.user = null;
      localStorage.removeItem('token');
      localStorage.removeItem('refresh');
      localStorage.removeItem('user');
    },

    checkAuth() {
      const token = localStorage.getItem('token');
      if (token) {
        this.token = token;
        this.isAuthenticated = true;
      } else {
        this.logout();
      }
    }
  }
});