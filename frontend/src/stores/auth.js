import { defineStore } from 'pinia';

export const useAuthStore = defineStore('auth', {
  state: () => ({
    user: null,
    token: localStorage.getItem('token') || null,
    isAuthenticated: false
  }),

  actions: {
    login(credentials) {
      // In a real app, you would make an API call here
      // For now, we'll simulate login success
      this.token = 'fake-jwt-token';
      this.isAuthenticated = true;
      this.user = credentials;
      localStorage.setItem('token', this.token);
      return Promise.resolve({ token: this.token });
    },

    logout() {
      this.token = null;
      this.isAuthenticated = false;
      this.user = null;
      localStorage.removeItem('token');
      localStorage.removeItem('user');
    },

    checkAuth() {
      const token = localStorage.getItem('token');
      if (token) {
        this.token = token;
        this.isAuthenticated = true;
        // In a real app, you would verify the token with an API call
      }
    }
  }
});