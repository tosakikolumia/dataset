<template>
  <div class="department-management">
    <h1>标准科室库管理</h1>
    <p>用于维护全市统一的科室列表</p>
    
    <div class="management-header">
      <h3>科室列表</h3>
      <button @click="showAddDepartmentModal = true" class="add-btn">新增科室</button>
    </div>
    
    <div class="departments-table">
      <table>
        <thead>
          <tr>
            <th>科室名称</th>
            <th>描述</th>
            <th>创建时间</th>
            <th>操作</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="department in departments" :key="department.id">
            <td>{{ department.name }}</td>
            <td>{{ department.description || '无描述' }}</td>
            <td>{{ formatDate(department.created_at) }}</td>
            <td>
              <button @click="deleteDepartment(department.id)" class="delete-btn">删除</button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
    
    <!-- 添加科室模态框 -->
    <div v-if="showAddDepartmentModal" class="modal-overlay" @click="showAddDepartmentModal = false">
      <div class="modal-content" @click.stop>
        <h3>新增科室</h3>
        <form @submit.prevent="addDepartment">
          <div class="form-group">
            <label>科室名称:</label>
            <input v-model="newDepartment.name" type="text" required />
          </div>
          <div class="form-group">
            <label>描述:</label>
            <textarea 
              v-model="newDepartment.description" 
              rows="3"
              placeholder="请输入科室描述..."
            ></textarea>
          </div>
          <div class="form-actions">
            <button type="submit" class="add-btn">添加科室</button>
            <button type="button" @click="cancelAdd" class="cancel-btn">取消</button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
import api from '@/services/api';

export default {
  name: 'DepartmentManagementView',
  data() {
    return {
      departments: [],
      showAddDepartmentModal: false,
      newDepartment: {
        name: '',
        description: ''
      }
    };
  },
  async created() {
    await this.loadDepartments();
  },
  methods: {
    async loadDepartments() {
      try {
        const response = await api.department.getAllDepartments();
        this.departments = response.data.data;
      } catch (error) {
        console.error('Error loading departments:', error);
      }
    },
    async addDepartment() {
      try {
        await api.department.createDepartment(this.newDepartment);
        await this.loadDepartments();
        this.cancelAdd();
      } catch (error) {
        console.error('Error adding department:', error);
        // In a real app, show user-friendly error message
      }
    },
    async deleteDepartment(id) {
      if (confirm('确定要删除这个科室吗？删除后将影响所有关联的医院科室信息！')) {
        try {
          await api.department.deleteDepartment(id);
          await this.loadDepartments();
        } catch (error) {
          console.error('Error deleting department:', error);
        }
      }
    },
    cancelAdd() {
      this.showAddDepartmentModal = false;
      this.newDepartment = {
        name: '',
        description: ''
      };
    },
    formatDate(dateString) {
      if (!dateString) return '未设置';
      const date = new Date(dateString);
      return date.toLocaleDateString('zh-CN');
    }
  }
};
</script>

<style scoped>
.department-management {
  max-width: 1000px;
  margin: 0 auto;
  padding: 20px;
}

.management-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.add-btn, .delete-btn, .cancel-btn {
  padding: 6px 12px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  text-decoration: none;
  display: inline-block;
}

.add-btn {
  background-color: #007bff;
  color: white;
}

.delete-btn, .cancel-btn {
  background-color: #dc3545;
  color: white;
  margin-left: 10px;
}

.departments-table {
  overflow-x: auto;
}

table {
  width: 100%;
  border-collapse: collapse;
}

th, td {
  padding: 12px;
  text-align: left;
  border-bottom: 1px solid #ddd;
}

th {
  background-color: #f8f9fa;
  font-weight: bold;
}

.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.modal-content {
  background: white;
  padding: 20px;
  border-radius: 8px;
  width: 500px;
  max-width: 90%;
}

.form-group {
  margin-bottom: 15px;
}

.form-group label {
  display: block;
  margin-bottom: 5px;
  font-weight: bold;
}

.form-group input,
.form-group textarea {
  width: 100%;
  padding: 8px 12px;
  border: 1px solid #ddd;
  border-radius: 4px;
  box-sizing: border-box;
}

.form-actions {
  text-align: right;
  margin-top: 20px;
}
</style>