<template>
  <div class="staff-detail-page">
    <div class="header">
      <button class="back-btn" @click="$router.go(-1)">← 返回列表</button>
      <h1>员工详细档案</h1>
    </div>

    <div v-if="loading" class="loading">加载中...</div>

    <div v-else-if="staff" class="content-wrapper">
      <div class="profile-card">
        <div class="avatar-placeholder">{{ staff.name[0] }}</div>
        <div class="basic-info">
          <h2>{{ staff.name }} <span class="gender-badge" :class="staff.gender">{{ staff.gender }}</span></h2>
          <p class="staff-id">工号: {{ staff.staff_id }}</p>
          <div class="tags">
            <span class="tag title">{{ staff.title || '暂无职称' }}</span>
            <span class="tag date">入职: {{ staff.hire_date || '未记录' }}</span>
          </div>
          <div class="contact">
            📞 {{ staff.phone || '无联系方式' }}
          </div>
        </div>
      </div>

      <div class="grid-layout">
        <div class="section-card">
          <h3>🏥 执业关系 (Hospital Affiliations)</h3>
          <ul class="list">
            <li v-for="(h, index) in staff.hospital_employments" :key="index" class="list-item">
              <span class="item-name">{{ h.hospital.name }}</span>
              <span class="item-status">{{ h.employment_type || '普通在职' }}</span>
            </li>
            <li v-if="staff.hospital_employments.length === 0" class="empty">暂无执业记录</li>
          </ul>
        </div>

        <div class="section-card">
          <h3>🩺 科室岗位 (Department Roles)</h3>
          <ul class="list">
            <li v-for="(d, index) in staff.dept_assignments" :key="index" class="list-item">
              <span class="item-name">{{ d.dept.dept_name }}</span>
              <span class="item-role">{{ d.role_in_dept || '科员' }}</span>
            </li>
            <li v-if="staff.dept_assignments.length === 0" class="empty">暂无科室分配</li>
          </ul>
        </div>
      </div>
    </div>

    <div v-else class="error">未找到该员工信息</div>
  </div>
</template>

<script>
import api from '@/services/api';

export default {
  name: 'StaffDetailView',
  data() {
    return {
      staff: null,
      loading: true
    };
  },
  async created() {
    // 从路由参数获取 ID
    const staffId = this.$route.params.id;
    if (staffId) {
      await this.loadDetail(staffId);
    }
  },
  methods: {
    async loadDetail(id) {
      try {
        this.loading = true;
        // 调用后端 retrieve 接口，因为我们修改了 ViewSet，现在它会返回全量数据
        const res = await api.staff.getStaff(id); // 需确保 api.js 中有 getStaff(id) 方法
        this.staff = res.data;
      } catch (err) {
        console.error(err);
        alert('获取详情失败');
      } finally {
        this.loading = false;
      }
    }
  }
};
</script>

<style scoped>
.staff-detail-page {
  max-width: 900px;
  margin: 30px auto;
  padding: 0 20px;
}
.header {
  display: flex;
  align-items: center;
  gap: 20px;
  margin-bottom: 30px;
}
.back-btn {
  padding: 8px 16px;
  background: white;
  border: 1px solid #ddd;
  border-radius: 4px;
  cursor: pointer;
}
.back-btn:hover { background: #f5f5f5; }

/* 个人卡片 */
.profile-card {
  background: white;
  padding: 30px;
  border-radius: 12px;
  box-shadow: 0 4px 20px rgba(0,0,0,0.05);
  display: flex;
  gap: 30px;
  align-items: center;
  margin-bottom: 30px;
}
.avatar-placeholder {
  width: 80px; height: 80px;
  background: #3498db;
  color: white;
  font-size: 32px;
  display: flex; align-items: center; justify-content: center;
  border-radius: 50%;
  font-weight: bold;
}
.basic-info h2 { margin: 0 0 10px 0; display: flex; align-items: center; gap: 10px; }
.gender-badge { font-size: 14px; padding: 2px 8px; border-radius: 4px; background: #eee; font-weight: normal;}
.gender-badge.男 { background: #e3f2fd; color: #1976d2; }
.gender-badge.女 { background: #fce4ec; color: #c2185b; }
.staff-id { color: #666; margin: 0 0 15px 0; }
.tags { display: flex; gap: 10px; margin-bottom: 15px; }
.tag { padding: 4px 12px; border-radius: 20px; font-size: 13px; }
.tag.title { background: #e8f5e9; color: #2e7d32; font-weight: bold; }
.tag.date { background: #f5f5f5; color: #666; }
.contact { font-size: 16px; color: #333; }

/* 栅格布局 */
.grid-layout {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 20px;
}
.section-card {
  background: white;
  padding: 20px;
  border-radius: 8px;
  border: 1px solid #eee;
}
.section-card h3 {
  margin-top: 0;
  border-bottom: 2px solid #f0f0f0;
  padding-bottom: 10px;
  font-size: 16px;
  color: #2c3e50;
}
.list { list-style: none; padding: 0; margin: 0; }
.list-item {
  display: flex;
  justify-content: space-between;
  padding: 12px 0;
  border-bottom: 1px solid #f9f9f9;
}
.list-item:last-child { border-bottom: none; }
.item-name { font-weight: 500; }
.item-status, .item-role { color: #666; font-size: 14px; background: #fafafa; padding: 2px 8px; border-radius: 4px; }
.empty { color: #999; font-style: italic; padding: 10px 0; }
</style>