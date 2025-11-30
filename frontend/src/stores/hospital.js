import { defineStore } from 'pinia';
import api from '@/services/api'; // 这里导入的是你封装的服务对象

export const useHospitalStore = defineStore('hospital', {
  state: () => ({
    hospitals: [],
    currentHospital: null,
    hospitalDepartments: [],
    hospitalScores: [],
    hospitalEvents: [],
    loading: false
  }),

  actions: {
    async fetchHospitals(filters = {}) {
      this.loading = true;
      try {
        // ❌ 错误写法: await api.post('/public/search_hospital/', filters);
        // ✅ 正确写法: 调用 api.js 中定义的 public.searchHospitals 方法
        const response = await api.public.searchHospitals(filters);

        // 注意：根据后端返回格式，可能是 response.data.data 或者 response.data
        // 建议先 log 看一下结构，这里假设标准格式是 response.data
        this.hospitals = response.data.data || response.data;
        return response.data;
      } catch (error) {
        console.error('Error fetching hospitals:', error);
        throw error;
      } finally {
        this.loading = false;
      }
    },

    async fetchHospitalById(id) {
      this.loading = true;
      try {
        // ✅ 改用封装好的方法
        const response = await api.hospital.getHospitalById(id);
        this.currentHospital = response.data.data || response.data;
        return response.data;
      } catch (error) {
        console.error('Error fetching hospital:', error);
        throw error;
      } finally {
        this.loading = false;
      }
    },

    async fetchHospitalDepartments(hospitalId) {
      this.loading = true;
      try {
        // ✅ 改用封装好的方法
        const response = await api.hospital.getHospitalDepartments(hospitalId);
        this.hospitalDepartments = response.data.data || response.data;
        return response.data;
      } catch (error) {
        console.error('Error fetching hospital departments:', error);
        throw error;
      } finally {
        this.loading = false;
      }
    },

    async fetchHospitalScores(hospitalId) {
      this.loading = true;
      try {
        // ✅ 改用封装好的方法
        const response = await api.hospital.getHospitalScores(hospitalId);
        this.hospitalScores = response.data.data || response.data;
        return response.data;
      } catch (error) {
        console.error('Error fetching hospital scores:', error);
        throw error;
      } finally {
        this.loading = false;
      }
    },

    async fetchHospitalEvents(hospitalId) {
      this.loading = true;
      try {
        // ✅ 改用封装好的方法
        const response = await api.hospital.getHospitalEvents(hospitalId);
        this.hospitalEvents = response.data.data || response.data;
        return response.data;
      } catch (error) {
        console.error('Error fetching hospital events:', error);
        throw error;
      } finally {
        this.loading = false;
      }
    }
  }
});