<template>
  <div class="hospital-admin">
    <h1>医院管理员后台</h1>
    <p>欢迎，{{ user?.name || '管理员' }}！</p>
    
    <div class="admin-menu">
      <router-link to="/hospital-admin/info" class="menu-item">
        <h3>医院信息管理</h3>
        <p>修改本院的基础资料</p>
      </router-link>
      
      <router-link to="/hospital-admin/resources" class="menu-item">
        <h3>科室资源管理</h3>
        <p>管理床位数、设备等资源</p>
      </router-link>
      
      <router-link to="/hospital-admin/staff" class="menu-item">
        <h3>医护人员管理</h3>
        <p>管理医院员工信息</p>
      </router-link>
      
      <router-link to="/hospital-admin/events" class="menu-item">
        <h3>突发事件响应</h3>
        <p>上报/参与突发事件</p>
      </router-link>
      
      <router-link to="/hospital-admin/scores" class="menu-item">
        <h3>医院评分上报</h3>
        <p>提交自评结果</p>
      </router-link>
    </div>
  </div>
</template>

<script>
import { useAuthStore } from '@/stores/auth';

export default {
  name: 'HospitalAdminView',
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
    if (!this.authStore.isAuthenticated || this.authStore.user?.role !== 'hospital_admin') {
      // Redirect to login in a real app
      console.log('Access denied: Hospital admin access required');
    }
  }
};
</script>

<style scoped>
.hospital-admin {
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