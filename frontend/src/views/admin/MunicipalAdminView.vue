<template>
  <div class="municipal-admin">
    <h1>市政管理员后台</h1>
    <p>欢迎，{{ user?.name || '市政管理员' }}！</p>
    
    <div class="admin-menu">
      <router-link to="/municipal-admin/hospitals" class="menu-item">
        <h3>医院管理</h3>
        <p>增删改医院信息</p>
      </router-link>
      
      <router-link to="/municipal-admin/departments" class="menu-item">
        <h3>标准科室库管理</h3>
        <p>维护全市统一的科室列表</p>
      </router-link>
      
      <router-link to="/municipal-admin/resources" class="menu-item">
        <h3>全市医院资源总览</h3>
        <p>查看全市医院资源数据大屏</p>
      </router-link>
      
      <router-link to="/municipal-admin/staff" class="menu-item">
        <h3>全市人员统计</h3>
        <p>查看各医院人员分布</p>
      </router-link>
      
      <router-link to="/municipal-admin/events" class="menu-item">
        <h3>突发事件管理</h3>
        <p>管理全市突发事件</p>
      </router-link>
      
      <router-link to="/municipal-admin/levels" class="menu-item">
        <h3>等级设置管理</h3>
        <p>管理医院等级库</p>
      </router-link>
    </div>
  </div>
</template>

<script>
import { useAuthStore } from '@/stores/auth';

export default {
  name: 'MunicipalAdminView',
  computed: {
    authStore() {
      return useAuthStore();
    },
    user() {
      return this.authStore.user;
    }
  },
  created() {
    // Check if user is authenticated and has correct role
    this.authStore.checkAuth();
    if (!this.authStore.isAuthenticated || this.authStore.user?.role !== 'municipal_admin') {
      // Redirect to login in a real app
      console.log('Access denied: Municipal admin access required');
    }
  }
};
</script>

<style scoped>
.municipal-admin {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

.admin-menu {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 20px;
  margin-top: 30px;
}

.menu-item {
  display: block;
  padding: 20px;
  border: 1px solid #ddd;
  border-radius: 8px;
  text-decoration: none;
  color: #333;
  transition: box-shadow 0.3s;
}

.menu-item:hover {
  box-shadow: 0 4px 8px rgba(0,0,0,0.1);
}

.menu-item h3 {
  margin-top: 0;
  color: #007bff;
}
</style>