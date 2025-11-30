<template>
  <div class="hospital-info">
    <h1>医院信息管理</h1>
    <p>修改本院的基础资料</p>
    
    <form @submit.prevent="saveHospitalInfo" class="info-form">
      <div class="form-group">
        <label for="name">医院名称:</label>
        <input 
          type="text" 
          id="name" 
          v-model="hospitalInfo.name" 
          required
        />
      </div>
      
      <div class="form-group">
        <label for="address">地址:</label>
        <input 
          type="text" 
          id="address" 
          v-model="hospitalInfo.address" 
          required
        />
      </div>
      
      <div class="form-group">
        <label for="phone">电话:</label>
        <input 
          type="text" 
          id="phone" 
          v-model="hospitalInfo.phone" 
        />
      </div>
      
      <div class="form-group">
        <label for="email">邮箱:</label>
        <input 
          type="email" 
          id="email" 
          v-model="hospitalInfo.email" 
        />
      </div>
      
      <div class="form-group">
        <label for="description">医院简介 (富文本):</label>
        <textarea 
          id="description" 
          v-model="hospitalInfo.description" 
          rows="6"
          placeholder="请输入医院简介..."
        ></textarea>
      </div>
      
      <div class="form-group">
        <label>医院等级:</label>
        <div class="read-only-field">
          {{ hospitalInfo.level_name || '未设置' }}
        </div>
      </div>
      
      <div class="form-actions">
        <button type="submit" :disabled="loading" class="save-btn">
          {{ loading ? '保存中...' : '保存信息' }}
        </button>
      </div>
    </form>
  </div>
</template>

<script>
import api from '@/services/api';
import { useHospitalStore } from '@/stores/hospital';
import { useAuthStore } from '@/stores/auth';

export default {
  name: 'HospitalInfoView',
  data() {
    return {
      hospitalInfo: {
        id: null,
        name: '',
        address: '',
        phone: '',
        email: '',
        description: '',
        level_name: ''
      },
      loading: false,
      hospitalStore: useHospitalStore(),
      authStore: useAuthStore()
    };
  },
  async created() {
    // Get hospital ID from user's profile in a real app
    // For now, we'll use a mock ID
    await this.loadHospitalInfo();
  },
  methods: {
    async loadHospitalInfo() {
      this.loading = true;
      try {
        // In a real app, we would get the hospital ID from the authenticated user's profile
        // For this example, we'll use a mock hospital ID
        const hospitalId = this.authStore.user?.hospital_id || 1;
        
        const response = await api.hospital.getHospitalById(hospitalId);
        this.hospitalInfo = {
          ...response.data.data,
          level_name: response.data.data.level?.name || response.data.data.level_name
        };
      } catch (error) {
        console.error('Error loading hospital info:', error);
        // In a real app, show a user-friendly error message
      } finally {
        this.loading = false;
      }
    },
    async saveHospitalInfo() {
      this.loading = true;
      try {
        await api.hospital.updateHospital(this.hospitalInfo.id, {
          name: this.hospitalInfo.name,
          address: this.hospitalInfo.address,
          phone: this.hospitalInfo.phone,
          email: this.hospitalInfo.email,
          description: this.hospitalInfo.description
        });
        
        // Update the hospital store
        this.hospitalStore.currentHospital = { ...this.hospitalInfo };
        
        alert('医院信息已保存！');
      } catch (error) {
        console.error('Error saving hospital info:', error);
        alert('保存失败，请重试');
      } finally {
        this.loading = false;
      }
    }
  }
};
</script>

<style scoped>
.hospital-info {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
}

.info-form {
  background: #f8f9fa;
  padding: 20px;
  border-radius: 8px;
  margin-top: 20px;
}

.form-group {
  margin-bottom: 20px;
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

.read-only-field {
  padding: 8px 12px;
  background-color: #e9ecef;
  border: 1px solid #ddd;
  border-radius: 4px;
}

.form-actions {
  text-align: center;
  margin-top: 30px;
}

.save-btn {
  padding: 10px 30px;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 16px;
}

.save-btn:disabled {
  background-color: #6c757d;
  cursor: not-allowed;
}
</style>