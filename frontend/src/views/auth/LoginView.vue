<template>
  <div class="login">
    <div class="login-container">
      <h2>城市医疗管理系统登录</h2>
      <form @submit.prevent="handleLogin" class="login-form">
        <div class="form-group">
          <label for="username">用户名:</label>
          <input 
            type="text" 
            id="username" 
            v-model="credentials.username" 
            required 
          />
        </div>
        
        <div class="form-group">
          <label for="password">密码:</label>
          <input 
            type="password" 
            id="password" 
            v-model="credentials.password" 
            required 
          />
        </div>
        
        <div class="form-group">
          <label for="role">角色:</label>
          <select id="role" v-model="credentials.role" required>
            <option value="">请选择角色</option>
            <option value="municipal_admin">市政管理员</option>
            <option value="hospital_admin">医院管理员</option>
            <option value="resident">居民（公众用户）</option>
          </select>
        </div>
        
        <button type="submit" :disabled="loading" class="login-btn">
          {{ loading ? '登录中...' : '登录' }}
        </button>
      </form>
      
      <div v-if="loginError" class="error-message">
        {{ loginError }}
      </div>
    </div>
  </div>
</template>

<script>
import { useAuthStore } from '@/stores/auth';
import { useRouter } from 'vue-router';

export default {
  name: 'LoginView',
  data() {
    return {
      credentials: {
        username: '',
        password: '',
        role: ''
      },
      loading: false,
      loginError: null,
      authStore: useAuthStore(),
      router: useRouter()
    };
  },
  methods: {
    async handleLogin() {
      this.loading = true;
      this.loginError = null;
      
      try {
        // In a real app, you would call the backend login API
        // For this example, we'll simulate authentication
        await this.authStore.login({
          ...this.credentials
        });
        
        // Redirect based on role
        if (this.credentials.role === 'hospital_admin') {
          this.router.push('/hospital-admin');
        } else if (this.credentials.role === 'municipal_admin') {
          this.router.push('/municipal-admin');
        } else {
          this.router.push('/');
        }
      } catch (error) {
        this.loginError = '登录失败，请检查用户名和密码';
        console.error('Login error:', error);
      } finally {
        this.loading = false;
      }
    }
  }
};
</script>

<style scoped>
.login {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background-color: #f8f9fa;
}

.login-container {
  background: white;
  padding: 30px;
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  width: 100%;
  max-width: 400px;
}

.login-container h2 {
  text-align: center;
  margin-bottom: 20px;
  color: #343a40;
}

.login-form {
  display: flex;
  flex-direction: column;
}

.form-group {
  margin-bottom: 15px;
}

.form-group label {
  display: block;
  margin-bottom: 5px;
  font-weight: bold;
  color: #495057;
}

.form-group input,
.form-group select {
  width: 100%;
  padding: 10px;
  border: 1px solid #ced4da;
  border-radius: 4px;
  box-sizing: border-box;
}

.login-btn {
  padding: 10px;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 16px;
}

.login-btn:disabled {
  background-color: #6c757d;
  cursor: not-allowed;
}

.error-message {
  margin-top: 15px;
  padding: 10px;
  background-color: #f8d7da;
  color: #721c24;
  border: 1px solid #f5c6cb;
  border-radius: 4px;
  text-align: center;
}
</style>