<template>
  <div class="home">
    <h1>城市医疗公共服务门户</h1>
    <div class="search-section">
      <input 
        v-model="searchKeyword" 
        type="text" 
        placeholder="搜索医院名称..." 
        @keyup.enter="searchHospitals"
      />
      <button @click="searchHospitals">搜索</button>
    </div>
    
    <div class="quick-links">
      <h2>快捷入口</h2>
      <div class="links">
        <router-link to="/hospitals" class="link">医院查询</router-link>
        <a href="#" class="link">急诊服务</a>
        <a href="#" class="link">疫情信息</a>
        <a href="#" class="link">突发事件公告</a>
      </div>
    </div>
    
    <div class="recommended-hospitals">
      <h2>推荐医院</h2>
      <div v-if="hospitals.length > 0" class="hospital-list">
        <div 
          v-for="hospital in hospitals" 
          :key="hospital.id" 
          class="hospital-card"
          @click="goToHospitalDetail(hospital.id)"
        >
          <h3>{{ hospital.name }}</h3>
          <p>{{ hospital.address }}</p>
          <p>评分: {{ hospital.rating || '暂无评分' }}</p>
        </div>
      </div>
      <div v-else class="no-hospitals">暂无医院数据</div>
    </div>
  </div>
</template>

<script>
import { useHospitalStore } from '@/stores/hospital';
import { useRouter } from 'vue-router';

export default {
  name: 'HomeView',
  data() {
    return {
      searchKeyword: '',
      hospitalStore: useHospitalStore(),
      router: useRouter()
    };
  },
  computed: {
    hospitals() {
      return this.hospitalStore.hospitals.slice(0, 5); // Show only first 5 as recommendations
    }
  },
  async created() {
    // Load some hospitals for recommendations
    await this.hospitalStore.fetchHospitals();
  },
  methods: {
    async searchHospitals() {
      await this.hospitalStore.fetchHospitals({ name: this.searchKeyword });
    },
    goToHospitalDetail(id) {
      this.router.push(`/hospital/${id}`);
    }
  }
};
</script>

<style scoped>
.home {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

.search-section {
  margin: 30px 0;
  text-align: center;
}

.search-section input {
  padding: 10px;
  width: 300px;
  margin-right: 10px;
  border: 1px solid #ddd;
  border-radius: 4px;
}

.search-section button {
  padding: 10px 20px;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.quick-links .links {
  display: flex;
  justify-content: space-around;
  flex-wrap: wrap;
  margin: 20px 0;
}

.link {
  display: inline-block;
  padding: 15px;
  margin: 10px;
  background-color: #f8f9fa;
  border: 1px solid #dee2e6;
  border-radius: 4px;
  text-decoration: none;
  color: #007bff;
  min-width: 120px;
}

.hospital-list {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  gap: 20px;
  margin-top: 20px;
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

.no-hospitals {
  text-align: center;
  padding: 40px;
  color: #666;
}
</style>