<template>
  <div class="hospital-list">
    <h1>医院列表</h1>
    
    <div class="filters">
      <div class="filter-group">
        <label>地区:</label>
        <select v-model="filters.district">
          <option value="">全部</option>
          <!-- In a real app, these would come from an API -->
          <option value="1">市中心区</option>
          <option value="2">东城区</option>
          <option value="3">西城区</option>
          <option value="4">南城区</option>
          <option value="5">北城区</option>
        </select>
      </div>
      
      <div class="filter-group">
        <label>等级:</label>
        <select v-model="filters.level">
          <option value="">全部</option>
          <!-- In a real app, these would come from an API -->
          <option value="1">三级甲等</option>
          <option value="2">三级乙等</option>
          <option value="3">二级甲等</option>
          <option value="4">二级乙等</option>
          <option value="5">一级医院</option>
        </select>
      </div>
      
      <div class="filter-group">
        <label>医院类型:</label>
        <select v-model="filters.type">
          <option value="">全部</option>
          <option value="general">综合医院</option>
          <option value="specialized">专科医院</option>
          <option value="traditional">中医医院</option>
        </select>
      </div>
      
      <button @click="applyFilters" class="search-btn">搜索</button>
    </div>
    
    <div class="hospital-results">
      <div 
        v-for="hospital in hospitals" 
        :key="hospital.id" 
        class="hospital-card"
        @click="goToHospitalDetail(hospital.id)"
      >
        <h3>{{ hospital.name }}</h3>
        <p class="address">{{ hospital.address }}</p>
        <p class="rating">评分: {{ hospital.rating || '暂无评分' }}</p>
        <p class="level">{{ hospital.level_name || '未设置等级' }}</p>
      </div>
      
      <div v-if="hospitals.length === 0 && !loading" class="no-results">
        暂无匹配的医院
      </div>
      
      <div v-if="loading" class="loading">
        加载中...
      </div>
    </div>
  </div>
</template>

<script>
import { useHospitalStore } from '@/stores/hospital';
import { useRouter } from 'vue-router';

export default {
  name: 'HospitalListView',
  data() {
    return {
      filters: {
        district: '',
        level: '',
        name: ''
      },
      hospitalStore: useHospitalStore(),
      router: useRouter()
    };
  },
  computed: {
    hospitals() {
      return this.hospitalStore.hospitals;
    },
    loading() {
      return this.hospitalStore.loading;
    }
  },
  async created() {
    await this.hospitalStore.fetchHospitals();
  },
  methods: {
    async applyFilters() {
      await this.hospitalStore.fetchHospitals(this.filters);
    },
    goToHospitalDetail(id) {
      this.router.push(`/hospital/${id}`);
    }
  }
};
</script>

<style scoped>
.hospital-list {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

.filters {
  display: flex;
  gap: 20px;
  margin-bottom: 30px;
  flex-wrap: wrap;
  align-items: end;
}

.filter-group {
  display: flex;
  flex-direction: column;
}

.filter-group label {
  margin-bottom: 5px;
  font-weight: bold;
}

.filter-group select {
  padding: 8px;
  border: 1px solid #ddd;
  border-radius: 4px;
}

.search-btn {
  padding: 8px 15px;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  height: fit-content;
}

.hospital-results {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 20px;
}

.hospital-card {
  border: 1px solid #ddd;
  border-radius: 8px;
  padding: 15px;
  cursor: pointer;
  transition: box-shadow 0.3s;
}

.hospital-card:hover {
  box-shadow: 0 4px 8px rgba(0,0,0,0.1);
}

.address, .rating, .level {
  margin: 5px 0;
  color: #666;
}

.no-results {
  grid-column: 1 / -1;
  text-align: center;
  padding: 40px;
  color: #666;
}

.loading {
  grid-column: 1 / -1;
  text-align: center;
  padding: 40px;
  color: #666;
}
</style>