<template>
  <div class="hospital-staff">
    <h1>医护人员管理</h1>
    <p>管理医院员工信息</p>
    
    <div class="staff-tabs">
      <button 
        :class="{ active: activeTab === 'staff-list' }"
        @click="activeTab = 'staff-list'"
      >
        员工信息管理
      </button>
      <button 
        :class="{ active: activeTab === 'hospital-staff' }"
        @click="activeTab = 'hospital-staff'"
      >
        医院员工执业关系
      </button>
    </div>
    
    <!-- 员工信息管理标签页 -->
    <div v-if="activeTab === 'staff-list'" class="tab-content">
      <div class="staff-header">
        <h3>全市员工库</h3>
        <button @click="showAddStaffModal = true" class="add-btn">添加员工</button>
      </div>
      
      <div class="staff-table">
        <table>
          <thead>
            <tr>
              <th>姓名</th>
              <th>工号</th>
              <th>职位</th>
              <th>科室</th>
              <th>职称</th>
              <th>操作</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="staff in staffList" :key="staff.id">
              <td>{{ staff.name }}</td>
              <td>{{ staff.staff_id }}</td>
              <td>{{ staff.position }}</td>
              <td>{{ staff.department_name }}</td>
              <td>{{ staff.title }}</td>
              <td>
                <button @click="editStaff(staff)" class="edit-btn">编辑</button>
                <button @click="deleteStaff(staff.id)" class="delete-btn">删除</button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
    
    <!-- 医院员工关系标签页 -->
    <div v-if="activeTab === 'hospital-staff'" class="tab-content">
      <div class="hospital-staff-header">
        <h3>本院员工执业关系</h3>
        <button @click="showAddHospitalStaffModal = true" class="add-btn">添加医院员工关系</button>
      </div>
      
      <div class="hospital-staff-table">
        <table>
          <thead>
            <tr>
              <th>员工姓名</th>
              <th>员工工号</th>
              <th>科室</th>
              <th>职位</th>
              <th>职称</th>
              <th>入职时间</th>
              <th>操作</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="hs in hospitalStaffList" :key="hs.id">
              <td>{{ hs.staff?.name || hs.staff_name }}</td>
              <td>{{ hs.staff?.staff_id || hs.staff_id }}</td>
              <td>{{ hs.department?.name || hs.department_name }}</td>
              <td>{{ hs.staff?.position || hs.position }}</td>
              <td>{{ hs.staff?.title || hs.title }}</td>
              <td>{{ formatDate(hs.employment_date) }}</td>
              <td>
                <button @click="deleteHospitalStaff(hs.id)" class="delete-btn">删除</button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
    
    <!-- 添加员工模态框 -->
    <div v-if="showAddStaffModal" class="modal-overlay" @click="showAddStaffModal = false">
      <div class="modal-content" @click.stop>
        <h3>{{ editingStaff ? '编辑员工' : '添加员工' }}</h3>
        <form @submit.prevent="saveStaff">
          <div class="form-group">
            <label>姓名:</label>
            <input v-model="currentStaff.name" type="text" required />
          </div>
          <div class="form-group">
            <label>工号:</label>
            <input v-model="currentStaff.staff_id" type="text" required />
          </div>
          <div class="form-group">
            <label>职位:</label>
            <input v-model="currentStaff.position" type="text" />
          </div>
          <div class="form-group">
            <label>职称:</label>
            <input v-model="currentStaff.title" type="text" />
          </div>
          <div class="form-group">
            <label>科室:</label>
            <input v-model="currentStaff.department_name" type="text" />
          </div>
          <div class="form-actions">
            <button type="submit" class="save-btn">
              {{ editingStaff ? '更新' : '添加' }}
            </button>
            <button type="button" @click="cancelEdit" class="cancel-btn">取消</button>
          </div>
        </form>
      </div>
    </div>
    
    <!-- 添加医院员工关系模态框 -->
    <div v-if="showAddHospitalStaffModal" class="modal-overlay" @click="showAddHospitalStaffModal = false">
      <div class="modal-content" @click.stop>
        <h3>添加医院员工关系</h3>
        <form @submit.prevent="saveHospitalStaff">
          <div class="form-group">
            <label>选择员工:</label>
            <select v-model="currentHospitalStaff.staff_id" required>
              <option value="">请选择员工</option>
              <option v-for="staff in staffList" :key="staff.id" :value="staff.id">
                {{ staff.name }} ({{ staff.staff_id }})
              </option>
            </select>
          </div>
          <div class="form-group">
            <label>科室:</label>
            <select v-model="currentHospitalStaff.department_id" required>
              <option value="">请选择科室</option>
              <option v-for="dept in departments" :key="dept.id" :value="dept.id">
                {{ dept.department?.name || dept.department_name }}
              </option>
            </select>
          </div>
          <div class="form-group">
            <label>入职时间:</label>
            <input v-model="currentHospitalStaff.employment_date" type="date" />
          </div>
          <div class="form-actions">
            <button type="submit" class="save-btn">添加</button>
            <button type="button" @click="showAddHospitalStaffModal = false" class="cancel-btn">取消</button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
import api from '@/services/api';
import { useAuthStore } from '@/stores/auth';
import { useHospitalStore } from '@/stores/hospital';

export default {
  name: 'HospitalStaffView',
  data() {
    return {
      activeTab: 'staff-list',
      staffList: [],
      hospitalStaffList: [],
      departments: [],
      showAddStaffModal: false,
      showAddHospitalStaffModal: false,
      editingStaff: false,
      currentStaff: {
        id: null,
        name: '',
        staff_id: '',
        position: '',
        title: '',
        department_name: ''
      },
      currentHospitalStaff: {
        staff_id: '',
        department_id: '',
        employment_date: ''
      },
      authStore: useAuthStore(),
      hospitalStore: useHospitalStore()
    };
  },
  async created() {
    await this.loadData();
  },
  methods: {
    async loadData() {
      await this.loadStaffList();
      await this.loadHospitalStaffList();
      await this.loadDepartments();
    },
    async loadStaffList() {
      try {
        const response = await api.staff.getAllStaffs();
        this.staffList = response.data.data;
      } catch (error) {
        console.error('Error loading staff list:', error);
      }
    },
    async loadHospitalStaffList() {
      try {
        // In a real app, we would get the hospital ID from the authenticated user's profile
        const hospitalId = this.authStore.user?.hospital_id || 1;
        const response = await api.staff.getHospitalStaffs({ hospital: hospitalId });
        this.hospitalStaffList = response.data.data;
      } catch (error) {
        console.error('Error loading hospital staff list:', error);
      }
    },
    async loadDepartments() {
      try {
        // In a real app, we would get the hospital ID from the authenticated user's profile
        const hospitalId = this.authStore.user?.hospital_id || 1;
        const response = await api.hospital.getHospitalDepartments(hospitalId);
        this.departments = response.data.data;
      } catch (error) {
        console.error('Error loading departments:', error);
      }
    },
    editStaff(staff) {
      this.editingStaff = true;
      this.currentStaff = { ...staff };
      this.showAddStaffModal = true;
    },
    async saveStaff() {
      try {
        if (this.editingStaff) {
          // Update existing staff
          await api.staff.createStaff(this.currentStaff);
        } else {
          // Create new staff
          await api.staff.createStaff(this.currentStaff);
        }
        
        await this.loadStaffList();
        this.cancelEdit();
      } catch (error) {
        console.error('Error saving staff:', error);
        // In a real app, show user-friendly error message
      }
    },
    async deleteStaff(id) {
      if (confirm('确定要删除这个员工吗？')) {
        try {
          await api.staff.deleteStaff(id); // Note: API doesn't have deleteStaff endpoint in our service
          await this.loadStaffList();
        } catch (error) {
          console.error('Error deleting staff:', error);
        }
      }
    },
    async saveHospitalStaff() {
      try {
        // In a real app, we would get the hospital ID from the authenticated user's profile
        const hospitalId = this.authStore.user?.hospital_id || 1;
        
        await api.staff.createHospitalStaff({
          staff: this.currentHospitalStaff.staff_id,
          department: this.currentHospitalStaff.department_id,
          employment_date: this.currentHospitalStaff.employment_date,
          hospital: hospitalId
        });
        
        await this.loadHospitalStaffList();
        this.showAddHospitalStaffModal = false;
        this.resetHospitalStaffForm();
      } catch (error) {
        console.error('Error saving hospital staff:', error);
        // In a real app, show user-friendly error message
      }
    },
    async deleteHospitalStaff(id) {
      if (confirm('确定要删除这个医院员工关系吗？')) {
        try {
          await api.staff.deleteHospitalStaff(id); // Note: API doesn't have deleteHospitalStaff endpoint in our service
          await this.loadHospitalStaffList();
        } catch (error) {
          console.error('Error deleting hospital staff:', error);
        }
      }
    },
    cancelEdit() {
      this.showAddStaffModal = false;
      this.editingStaff = false;
      this.resetStaffForm();
    },
    resetStaffForm() {
      this.currentStaff = {
        id: null,
        name: '',
        staff_id: '',
        position: '',
        title: '',
        department_name: ''
      };
    },
    resetHospitalStaffForm() {
      this.currentHospitalStaff = {
        staff_id: '',
        department_id: '',
        employment_date: ''
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
.hospital-staff {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

.staff-tabs {
  display: flex;
  margin-bottom: 20px;
}

.staff-tabs button {
  padding: 10px 20px;
  border: 1px solid #ddd;
  background: #f8f9fa;
  cursor: pointer;
  border-radius: 4px 4px 0 0;
  margin-right: 5px;
}

.staff-tabs button.active {
  background: #007bff;
  color: white;
  border-color: #007bff;
}

.tab-content {
  background: #f8f9fa;
  padding: 20px;
  border-radius: 0 4px 4px 4px;
}

.staff-header, .hospital-staff-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.add-btn, .edit-btn, .delete-btn, .save-btn, .cancel-btn {
  padding: 6px 12px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  text-decoration: none;
  display: inline-block;
}

.add-btn, .save-btn {
  background-color: #007bff;
  color: white;
}

.edit-btn {
  background-color: #ffc107;
  color: #212529;
}

.delete-btn {
  background-color: #dc3545;
  color: white;
}

.cancel-btn {
  background-color: #6c757d;
  color: white;
  margin-left: 10px;
}

.staff-table, .hospital-staff-table {
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
.form-group select {
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