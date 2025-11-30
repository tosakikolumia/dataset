<template>
  <div class="hospital-management">
    <h1>医院管理</h1>
    <p>市政管理员可对医院进行增删改操作</p>
    
    <div class="management-header">
      <h3>医院列表</h3>
      <button @click="showAddHospitalModal = true" class="add-btn">新增医院</button>
    </div>
    
    <div class="hospitals-table">
      <table>
        <thead>
          <tr>
            <th>医院名称</th>
            <th>地址</th>
            <th>电话</th>
            <th>等级</th>
            <th>成立时间</th>
            <th>操作</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="hospital in hospitals" :key="hospital.id">
            <td>{{ hospital.name }}</td>
            <td>{{ hospital.address }}</td>
            <td>{{ hospital.phone || '未设置' }}</td>
            <td>{{ hospital.level?.name || hospital.level_name || '未设置' }}</td>
            <td>{{ formatDate(hospital.establishment_date) }}</td>
            <td>
              <button @click="editHospital(hospital)" class="edit-btn">编辑</button>
              <button @click="deleteHospital(hospital.id)" class="delete-btn">删除</button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
    
    <!-- 添加/编辑医院模态框 -->
    <div v-if="showAddHospitalModal" class="modal-overlay" @click="showAddHospitalModal = false">
      <div class="modal-content" @click.stop>
        <h3>{{ editingHospital ? '编辑医院' : '新增医院' }}</h3>
        <form @submit.prevent="saveHospital">
          <div class="form-group">
            <label>医院名称:</label>
            <input v-model="currentHospital.name" type="text" required />
          </div>
          <div class="form-group">
            <label>地址:</label>
            <input v-model="currentHospital.address" type="text" required />
          </div>
          <div class="form-group">
            <label>电话:</label>
            <input v-model="currentHospital.phone" type="text" />
          </div>
          <div class="form-group">
            <label>邮箱:</label>
            <input v-model="currentHospital.email" type="email" />
          </div>
          <div class="form-group">
            <label>成立时间:</label>
            <input v-model="currentHospital.establishment_date" type="date" />
          </div>
          <div class="form-group">
            <label>医院等级:</label>
            <select v-model="currentHospital.level_id">
              <option value="">请选择等级</option>
              <option v-for="level in hospitalLevels" :key="level.id" :value="level.id">
                {{ level.name }}
              </option>
            </select>
          </div>
          <div class="form-group">
            <label>床位数:</label>
            <input v-model.number="currentHospital.bed_count" type="number" />
          </div>
          <div class="form-group">
            <label>简介:</label>
            <textarea 
              v-model="currentHospital.description" 
              rows="4"
              placeholder="请输入医院简介..."
            ></textarea>
          </div>
          <div class="form-actions">
            <button type="submit" class="save-btn">
              {{ editingHospital ? '更新' : '添加' }}
            </button>
            <button type="button" @click="cancelEdit" class="cancel-btn">取消</button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
import api from '@/services/api';

export default {
  name: 'HospitalManagementView',
  data() {
    return {
      hospitals: [],
      hospitalLevels: [],
      showAddHospitalModal: false,
      editingHospital: false,
      currentHospital: {
        id: null,
        name: '',
        address: '',
        phone: '',
        email: '',
        establishment_date: '',
        level_id: '',
        bed_count: null,
        description: ''
      }
    };
  },
  async created() {
    await this.loadData();
  },
  methods: {
    async loadData() {
      await this.loadHospitals();
      await this.loadHospitalLevels();
    },
    async loadHospitals() {
      try {
        const response = await api.hospital.getAllHospitals();
        this.hospitals = response.data.data;
      } catch (error) {
        console.error('Error loading hospitals:', error);
      }
    },
    async loadHospitalLevels() {
      try {
        const response = await api.hospitalLevel.getAllLevels();
        this.hospitalLevels = response.data.data;
      } catch (error) {
        console.error('Error loading hospital levels:', error);
      }
    },
    editHospital(hospital) {
      this.editingHospital = true;
      this.currentHospital = { ...hospital };
      // Handle level selection
      if (hospital.level) {
        this.currentHospital.level_id = hospital.level.id;
      } else if (hospital.level_id) {
        this.currentHospital.level_id = hospital.level_id;
      }
      this.showAddHospitalModal = true;
    },
    async saveHospital() {
      try {
        if (this.editingHospital) {
          await api.hospital.updateHospital(this.currentHospital.id, this.currentHospital);
        } else {
          await api.hospital.createHospital(this.currentHospital);
        }
        
        await this.loadHospitals();
        this.cancelEdit();
      } catch (error) {
        console.error('Error saving hospital:', error);
        // In a real app, show user-friendly error message
      }
    },
    async deleteHospital(id) {
      if (confirm('确定要删除这个医院吗？删除后将无法恢复！')) {
        try {
          await api.hospital.deleteHospital(id);
          await this.loadHospitals();
        } catch (error) {
          console.error('Error deleting hospital:', error);
        }
      }
    },
    cancelEdit() {
      this.showAddHospitalModal = false;
      this.editingHospital = false;
      this.resetHospitalForm();
    },
    resetHospitalForm() {
      this.currentHospital = {
        id: null,
        name: '',
        address: '',
        phone: '',
        email: '',
        establishment_date: '',
        level_id: '',
        bed_count: null,
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
.hospital-management {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

.management-header {
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

.delete-btn, .cancel-btn {
  background-color: #dc3545;
  color: white;
  margin-left: 10px;
}

.hospitals-table {
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
  width: 600px;
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
.form-group select,
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