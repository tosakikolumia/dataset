<template>
  <nav class="navbar">
    <div class="nav-container">
      <router-link to="/" class="nav-logo">
        城市医疗管理系统
      </router-link>
      
      <div class="nav-menu" :class="{ active: isMenuActive }">
        <router-link to="/" class="nav-link">首页</router-link>
        <router-link to="/hospitals" class="nav-link">医院列表</router-link>
        
        <template v-if="authStore.isAuthenticated">
          <template v-if="userRole === 'hospital_admin'">
            <router-link to="/hospital-admin" class="nav-link">医院管理</router-link>
          </template>
          <template v-else-if="userRole === 'municipal_admin'">
            <router-link to="/municipal-admin" class="nav-link">市政管理</router-link>
          </template>
          <button @click="handleLogout" class="logout-btn">退出登录</button>
        </template>
        <template v-else>
          <router-link to="/login" class="nav-link login-link">登录</router-link>
        </template>
      </div>
      
      <div class="hamburger" @click="toggleMenu">
        <span class="bar"></span>
        <span class="bar"></span>
        <span class="bar"></span>
      </div>
    </div>
  </nav>
</template>

<script>
import { useAuthStore } from '@/stores/auth';
import { useRouter } from 'vue-router';

export default {
  name: 'Navbar',
  data() {
    return {
      isMenuActive: false,
      authStore: useAuthStore(),
      router: useRouter()
    };
  },
  computed: {
    userRole() {
      return this.authStore.user?.role;
    }
  },
  methods: {
    toggleMenu() {
      this.isMenuActive = !this.isMenuActive;
    },
    handleLogout() {
      this.authStore.logout();
      this.router.push('/');
    }
  }
};
</script>

<style scoped>
.navbar {
  background-color: #343a40;
  color: white;
  height: 60px;
  display: flex;
  justify-content: center;
  align-items: center;
  font-size: 1.2rem;
  position: sticky;
  top: 0;
  z-index: 999;
}

.nav-container {
  width: 100%;
  max-width: 1200px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 20px;
}

.nav-logo {
  color: #fff;
  display: flex;
  align-items: center;
  cursor: pointer;
  text-decoration: none;
  font-weight: bold;
  font-size: 1.5rem;
}

.nav-menu {
  display: flex;
  align-items: center;
  gap: 2rem;
}

.nav-link {
  color: #fff;
  text-decoration: none;
  transition: 0.3s ease-in-out;
}

.nav-link:hover {
  color: #007bff;
}

.login-link {
  background-color: #007bff;
  padding: 8px 16px;
  border-radius: 4px;
}

.logout-btn {
  background-color: #dc3545;
  color: white;
  border: none;
  padding: 8px 16px;
  border-radius: 4px;
  cursor: pointer;
}

.hamburger {
  display: none;
  flex-direction: column;
  cursor: pointer;
}

.bar {
  width: 25px;
  height: 3px;
  margin: 3px 0;
  transition: 0.3s;
  background-color: #fff;
}

@media screen and (max-width: 768px) {
  .nav-menu {
    position: fixed;
    left: -100%;
    top: 60px;
    flex-direction: column;
    background-color: #343a40;
    width: 100%;
    text-align: center;
    transition: 0.3s;
    box-shadow: 0 10px 27px rgba(0, 0, 0, 0.05);
    padding: 20px 0;
  }

  .nav-menu.active {
    left: 0;
  }

  .hamburger {
    display: flex;
  }
}
</style>