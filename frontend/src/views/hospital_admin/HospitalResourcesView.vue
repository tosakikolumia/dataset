<template>
  <div class="hospital-resources">
    <h1>科室资源管理</h1>
    <p>管理床位数、设备等资源</p>
    
    <div class="resources-container">
      <div class="departments-panel">
        <h3>科室列表</h3>
        <ul class="departments-list">
          <li 
            v-for="department in departments" 
            :key="department.id"
            :class="{ active: selectedDepartment?.id === department.id }"
            @click="selectDepartment(department)"
          >
            {{ department.department?.name || department.department_name }}
          </li>
        </ul>
      </div>
      
      <div class="resources-panel">
        <h3>资源详情 - {{ selectedDepartment?.department?.name || selectedDepartment?.department_name || '请选择科室' }}</h3>
        
        <div v-if="selectedDepartment" class="resources-form">
          <div class="form-row">
            <div class="form-group">
              <label>床位数:</label>
              <input 
                type="number" 
                v-model="selectedDepartment.bed_count" 
                @change="updateResource"
              />
            </div>
            
            <div class="form-group">
              <label>可用床位数:</label>
              <input 
                type="number" 
                v-model="selectedDepartment.available_bed_count" 
                @change="updateResource"
              />
            </div>
          </div>
          
          <div class="form-row">
            <div class="form-group">
              <label>ICU床位数:</label>
              <input 
                type="number" 
                v-model="selectedDepartment.icu_bed_count" 
                @change="updateResource"
              />
            </div>
            
            <div class="form-group">
              <label>可用ICU床位数:</label>
              <input 
                type="number" 
                v-model="selectedDepartment.available_icu_bed_count" 
                @change="updateResource"
              />
            </div>
          </div>
          
          <div class="form-group">
            <label>设备信息:</label>
            <textarea 
              v-model="selectedDepartment.equipment_info" 
              rows="4"
              @change="updateResource"
              placeholder="请输入设备信息，如：呼吸机5台，监护仪10台..."
            ></textarea>
          </div>
          
          <div class="form-group">
            <label>备注:</label>
            <textarea 
              v-model="selectedDepartment.remarks" 
              rows="3"
              @change="updateResource"
            ></textarea>
          </div>
        </div>
        
        <div v-else class="no-selection">
          请从左侧选择一个科室来管理其资源
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import api from '@/services/api';
import { useAuthStore } from '@/stores/auth';

export default {
  name: 'HospitalResourcesView',
  data() {
    return {
      departments: [],
      selectedDepartment: null,
      authStore: useAuthStore()
    };
  },
  async created() {
    await this.loadDepartments();
  },
  methods: {
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
    selectDepartment(department) {
      this.selectedDepartment = { ...department }; // Create a copy for editing
    },
    async updateResource() {
      if (!this.selectedDepartment) return;
      
      try {
        // Update the department resource
        await api.department.updateDepartmentResource(
          this.selectedDepartment.id, 
          {
            bed_count: this.selectedDepartment.bed_count,
            available_bed_count: this.selectedDepartment.available_bed_count,
            icu_bed_count: this.selectedDepartment.icu_bed_count,
            available_icu_bed_count: this.selectedDepartment.available_icu_bed_count,
            equipment_info: this.selectedDepartment.equipment_info,
            remarks: this.selectedDepartment.remarks
          }
        );
        
        // Update the local department list
        const index = this.departments.findIndex(d => d.id === this.selectedDepartment.id);
        if (index !== -1) {
          this.departments[index] = { ...this.selectedDepartment };
        }
        
        console.log('Resource updated successfully');
      } catch (error) {
        console.error('Error updating resource:', error);
        // In a real app, show user-friendly error message
      }
    }
  }
};
</script>

<style scoped>
.hospital-resources {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

.resources-container {
  display: flex;
  gap: 20px;
  margin-top: 20px;
}

.departments-panel {
  flex: 1;
  min-width: 200px;
}

.resources-panel {
  flex: 3;
  background: #f8f9fa;
  padding: 20px;
  border-radius: 8px;
}

.departments-list {
  list-style: none;
  padding: 0;
  margin: 0;
}

.departments-list li {
  padding: 10px;
  border: 1px solid #ddd;
  margin-bottom: 5px;
  cursor: pointer;
  border-radius: 4px;
}

.departments-list li:hover {
  background-color: #e9ecef;
}

.departments-list li.active {
  background-color: #007bff;
  color: white;
}

.resources-form {
  margin-top: 20px;
}

.form-row {
  display: flex;
  gap: 20px;
  margin-bottom: 15px;
}

.form-group {
  flex: 1;
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

.no-selection {
  text-align: center;
  padding: 40px;
  color: #666;
}
</style>