import { defineStore } from 'pinia';
import api from '@/services/api';

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
        const response = await api.post('/public/search_hospital/', filters);
        this.hospitals = response.data.data;
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
        const response = await api.get(`/hospitals/${id}/`);
        this.currentHospital = response.data.data;
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
        const response = await api.get(`/hospitals/${hospitalId}/departments/`);
        this.hospitalDepartments = response.data.data;
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
        const response = await api.get(`/hospitals/${hospitalId}/scores/`);
        this.hospitalScores = response.data.data;
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
        const response = await api.get(`/hospitals/${hospitalId}/events/`);
        this.hospitalEvents = response.data.data;
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