<template>
  <div class="hospital-staff-view">
    <div class="page-header">
      <h2>🏥 本院医护人员管理</h2>
      <button class="btn-primary" @click="showAddModal = true">
        + 录用员工
      </button>
    </div>

    <div class="table-container card">
      <table>
        <thead>
          <tr>
            <th>姓名</th>
            <th>工号</th>
            <th>职称 (Title)</th>
            <th>本院身份 (Employment)</th>
            <th>操作</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="hs in staffList" :key="hs.id">
            <td><strong>{{ hs.staff.name }}</strong></td>
            <td>{{ hs.staff.staff_id }}</td>
            <td>{{ hs.staff.title }}</td>
            <td>
              <span class="status-tag">{{ hs.employment_type }}</span>
            </td>
            <td>
              <button class="btn-link" @click="goToDetail(hs.staff.staff_id)">完整档案</button>

              <button class="btn-link delete" @click="removeStaff(hs.id)">解聘</button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <div v-if="showAddModal" class="modal-overlay">
      <div class="modal-content">
        <h3>录用新员工</h3>
        <p class="hint">请输入基本信息以建立档案并录用。</p>

        <form @submit.prevent="handleCreate">
           <div class="form-group">
             <label>员工姓名</label>
             <input v-model="form.name" required placeholder="例如：张三">
           </div>
           <div class="form-group">
             <label>职称</label>
             <input v-model="form.title" placeholder="例如：主治医师">
           </div>
           <div class="form-group">
             <label>联系电话</label>
             <input v-model="form.phone" placeholder="请输入电话">
           </div>
           <div class="form-group">
             <label>性别</label>
             <select v-model="form.gender">
               <option>男</option>
               <option>女</option>
             </select>
           </div>
           <div class="form-group">
             <label>本院雇佣类型</label>
             <select v-model="form.employment_type">
               <option>全职</option>
               <option>兼职</option>
               <option>外聘</option>
             </select>
           </div>
           <div class="actions">
             <button type="button" @click="showAddModal = false">取消</button>
             <button type="submit" class="btn-primary">确认录用</button>
           </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
import api from '@/services/api';

export default {
  name: 'HospitalStaffView',
  data() {
    return {
      staffList: [],
      showAddModal: false,
      form: {
        name: '',
        title: '',
        phone: '',
        gender: '男',
        employment_type: '全职'
      }
    };
  },
  mounted() {
    this.fetchData();
  },
  methods: {
    async fetchData() {
      try {
        // 获取本院员工 (HospitalStaff 列表)
        const res = await api.staff.getHospitalStaffs();
        // 兼容分页和不分页的返回结构
        this.staffList = Array.isArray(res.data) ? res.data : (res.data.results || []);
      } catch (err) {
        console.error("加载列表失败", err);
      }
    },
    goToDetail(staffId) {
      // 这里的 staffId 现在应该是 1001, 1002 等整数，不再是 undefined
      console.log("Viewing staff:", staffId);
      this.$router.push(`/staff/${staffId}`);
    },
    async removeStaff(hospitalStaffId) {
      if(!confirm('确定要解除该员工与本院的聘用关系吗？')) return;
      try {
        await api.staff.deleteHospitalStaff(hospitalStaffId);
        this.fetchData();
      } catch (err) {
        alert("删除失败: " + err.message);
      }
    },
    async handleCreate() {
      try {
        // 调用之前的复合创建接口
        await api.staff.createHospitalStaff(this.form);
        this.showAddModal = false;
        // 重置表单
        this.form = { name: '', title: '', phone: '', gender: '男', employment_type: '全职' };
        this.fetchData();
      } catch(e) {
        console.error(e);
        const msg = e.response?.data?.detail || e.message;
        alert('操作失败: ' + msg);
      }
    }
  }
}
</script>

<style scoped>
.hospital-staff-view {
  padding: 20px;
  max-width: 1200px;
  margin: 0 auto;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
}

.page-header h2 {
  margin: 0;
  color: #2c3e50;
}

.card {
  background: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 12px rgba(0,0,0,0.05);
  overflow: hidden;
}

table {
  width: 100%;
  border-collapse: collapse;
}

th {
  background: #f8f9fa;
  padding: 16px;
  text-align: left;
  font-weight: 600;
  color: #555;
  border-bottom: 2px solid #eee;
}

td {
  padding: 16px;
  border-bottom: 1px solid #eee;
  color: #333;
}

tr:last-child td {
  border-bottom: none;
}

tr:hover {
  background-color: #fafafa;
}

.status-tag {
  background: #e8f5e9;
  color: #2e7d32;
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 12px;
  font-weight: 500;
}

.btn-primary {
  background-color: #3498db;
  color: white;
  border: none;
  padding: 10px 20px;
  border-radius: 6px;
  cursor: pointer;
  font-weight: 500;
}

.btn-primary:hover {
  background-color: #2980b9;
}

.btn-link {
  background: none;
  border: none;
  color: #3498db;
  cursor: pointer;
  margin-right: 12px;
  font-size: 14px;
}

.btn-link:hover {
  text-decoration: underline;
}

.btn-link.delete {
  color: #e74c3c;
}

/* 模态框样式 */
.modal-overlay {
  position: fixed;
  top: 0; left: 0; right: 0; bottom: 0;
  background: rgba(0,0,0,0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.modal-content {
  background: white;
  padding: 30px;
  border-radius: 12px;
  width: 400px;
  max-width: 90%;
  box-shadow: 0 4px 20px rgba(0,0,0,0.15);
}

.modal-content h3 {
  margin-top: 0;
  color: #2c3e50;
}

.hint {
  color: #7f8c8d;
  font-size: 13px;
  margin-bottom: 20px;
}

.form-group {
  margin-bottom: 16px;
}

.form-group label {
  display: block;
  margin-bottom: 6px;
  font-weight: 500;
  color: #34495e;
}

.form-group input, .form-group select {
  width: 100%;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 6px;
  font-size: 14px;
  box-sizing: border-box;
}

.form-group input:focus, .form-group select:focus {
  border-color: #3498db;
  outline: none;
}

.actions {
  margin-top: 24px;
  text-align: right;
  display: flex;
  justify-content: flex-end;
  gap: 12px;
}

.actions button[type="button"] {
  background: #f1f2f6;
  color: #2c3e50;
  border: 1px solid #dcdde1;
  padding: 10px 20px;
  border-radius: 6px;
  cursor: pointer;
}
</style>