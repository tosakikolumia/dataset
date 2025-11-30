<template>
  <div class="resource-overview">
    <h1>全市医院资源总览</h1>
    <p>市政管理员查看全市医院资源数据大屏</p>
    
    <div class="overview-stats">
      <div class="stat-card">
        <h3>总医院数</h3>
        <p class="stat-value">{{ stats.totalHospitals }}</p>
      </div>
      
      <div class="stat-card">
        <h3>总床位数</h3>
        <p class="stat-value">{{ stats.totalBeds }}</p>
      </div>
      
      <div class="stat-card">
        <h3>总ICU床位</h3>
        <p class="stat-value">{{ stats.totalICUBeds }}</p>
      </div>
      
      <div class="stat-card">
        <h3>总设备数</h3>
        <p class="stat-value">{{ stats.totalEquipment }}</p>
      </div>
    </div>
    
    <div class="resources-section">
      <h2>各医院资源对比</h2>
      <div class="hospital-resources-list">
        <div 
          v-for="hospitalResource in hospitalResources" 
          :key="hospitalResource.id" 
          class="hospital-resource-card"
        >
          <h3>{{ hospitalResource.hospital?.name || hospitalResource.hospital_name }}</h3>
          <div class="resource-details">
            <div class="resource-item">
              <span>总床位:</span>
              <span>{{ hospitalResource.bed_count || 0 }}</span>
            </div>
            <div class="resource-item">
              <span>可用床位:</span>
              <span>{{ hospitalResource.available_bed_count || 0 }}</span>
            </div>
            <div class="resource-item">
              <span>ICU床位:</span>
              <span>{{ hospitalResource.icu_bed_count || 0 }}</span>
            </div>
            <div class="resource-item">
              <span>可用ICU床位:</span>
              <span>{{ hospitalResource.available_icu_bed_count || 0 }}</span>
            </div>
            <div class="resource-item full-width">
              <span>设备信息:</span>
              <span>{{ hospitalResource.equipment_info || '暂无信息' }}</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import api from '@/services/api';

export default {
  name: 'ResourceOverviewView',
  data() {
    return {
      hospitals: [],
      departmentResources: [],
      stats: {
        totalHospitals: 0,
        totalBeds: 0,
        totalICUBeds: 0,
        totalEquipment: 0
      },
      hospitalResources: []
    };
  },
  async created() {
    await this.loadData();
  },
  methods: {
    async loadData() {
      await Promise.all([
        this.loadHospitals(),
        this.loadDepartmentResources()
      ]);
      this.calculateStats();
      this.processHospitalResources();
    },
    async loadHospitals() {
      try {
        const response = await api.hospital.getAllHospitals();
        this.hospitals = response.data.data;
      } catch (error) {
        console.error('Error loading hospitals:', error);
      }
    },
    async loadDepartmentResources() {
      try {
        // Get all department resources
        const response = await api.department.getDepartmentResources({});
        this.departmentResources = response.data.data;
      } catch (error) {
        console.error('Error loading department resources:', error);
      }
    },
    calculateStats() {
      // Calculate total hospitals
      this.stats.totalHospitals = this.hospitals.length;
      
      // Calculate total beds and ICU beds from department resources
      this.stats.totalBeds = this.departmentResources.reduce((sum, res) => {
        return sum + (res.bed_count || 0);
      }, 0);
      
      this.stats.totalICUBeds = this.departmentResources.reduce((sum, res) => {
        return sum + (res.icu_bed_count || 0);
      }, 0);
      
      // For equipment, we'll count the resources that have equipment info
      this.stats.totalEquipment = this.departmentResources.filter(res => res.equipment_info).length;
    },
    processHospitalResources() {
      // Group department resources by hospital
      const grouped = {};
      
      this.departmentResources.forEach(resource => {
        const hospitalId = resource.hospital?.id || resource.hospital_id;
        if (!grouped[hospitalId]) {
          grouped[hospitalId] = {
            id: hospitalId,
            hospital: resource.hospital,
            hospital_name: resource.hospital?.name || resource.hospital_name,
            bed_count: 0,
            available_bed_count: 0,
            icu_bed_count: 0,
            available_icu_bed_count: 0,
            equipment_info: []
          };
        }
        
        // Add up the resources
        grouped[hospitalId].bed_count += resource.bed_count || 0;
        grouped[hospitalId].available_bed_count += resource.available_bed_count || 0;
        grouped[hospitalId].icu_bed_count += resource.icu_bed_count || 0;
        grouped[hospitalId].available_icu_bed_count += resource.available_icu_bed_count || 0;
        
        if (resource.equipment_info) {
          grouped[hospitalId].equipment_info.push(resource.equipment_info);
        }
      });
      
      this.hospitalResources = Object.values(grouped);
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
.resource-overview {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

.overview-stats {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 20px;
  margin-bottom: 30px;
}

.stat-card {
  background: #f8f9fa;
  padding: 20px;
  border-radius: 8px;
  text-align: center;
  border: 1px solid #dee2e6;
}

.stat-card h3 {
  margin: 0 0 10px 0;
  color: #495057;
}

.stat-value {
  font-size: 2em;
  font-weight: bold;
  color: #007bff;
  margin: 0;
}

.resources-section h2 {
  margin-bottom: 20px;
  color: #343a40;
}

.hospital-resources-list {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
  gap: 20px;
}

.hospital-resource-card {
  border: 1px solid #ddd;
  border-radius: 8px;
  padding: 15px;
  background: white;
}

.hospital-resource-card h3 {
  margin-top: 0;
  color: #007bff;
  border-bottom: 1px solid #eee;
  padding-bottom: 10px;
}

.resource-details {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 10px;
}

.resource-item {
  display: flex;
  justify-content: space-between;
  padding: 5px 0;
  border-bottom: 1px dashed #eee;
}

.resource-item.full-width {
  grid-column: 1 / -1;
}

.resource-item span:first-child {
  font-weight: bold;
  color: #495057;
}
</style>