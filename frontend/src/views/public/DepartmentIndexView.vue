<template>
  <div class="dept-index">
    <div class="header">
      <h1>按科室找医院</h1>
      <p class="subtitle">选择您需要就诊的科室，查看全市开设该科室的医院</p>
    </div>

    <div class="dept-section">
      <div v-if="loadingDepts" class="loading">加载科室库...</div>
      <div v-else class="dept-tags">
        <button
          v-for="dept in departments"
          :key="dept.dept_id"
          :class="['tag', { active: selectedDeptId === dept.dept_id }]"
          @click="selectDepartment(dept)"
        >
          {{ dept.dept_name }}
        </button>
      </div>
    </div>

    <div v-if="selectedDeptId" class="results-section">
      <div class="results-header">
        <h2>{{ selectedDeptName }}</h2>
        <span class="count-badge">共找到 {{ hospitals.length }} 家医院</span>
      </div>

      <div v-if="loadingHospitals" class="loading">正在查询医院资源...</div>

      <div v-else-if="hospitals.length === 0" class="empty-state">
        暂无医院开设此科室
      </div>

      <div v-else class="hospital-grid">
        <div
          v-for="hospital in hospitals"
          :key="hospital.hospital_id"
          class="hospital-card"
          @click="goToHospital(hospital.hospital_id)"
        >
          <div class="card-header">
            <h3>{{ hospital.name }}</h3>
            <span class="level-tag">{{ hospital.level_name }}</span>
          </div>
          <p class="address">📍 {{ hospital.address }}</p>
          <div class="card-footer">
            <span class="view-btn">查看详情 →</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import api from '@/services/api';

export default {
  name: 'DepartmentIndexView',
  data() {
    return {
      departments: [],
      hospitals: [],
      selectedDeptId: null,
      selectedDeptName: '',
      loadingDepts: false,
      loadingHospitals: false
    };
  },
  async created() {
    await this.fetchAllDepartments();
  },
  methods: {
    // 获取所有标准科室
    async fetchAllDepartments() {
      this.loadingDepts = true;
      try {
        const res = await api.department.getAllDepartments();
        // 兼容 DRF 默认的分页格式 (results) 或 列表格式
        this.departments = Array.isArray(res.data) ? res.data : (res.data.results || []);
      } catch (error) {
        console.error("获取科室失败", error);
      } finally {
        this.loadingDepts = false;
      }
    },

    // 选中科室 -> 查医院
    async selectDepartment(dept) {
      if (this.selectedDeptId === dept.dept_id) return;

      this.selectedDeptId = dept.dept_id;
      this.selectedDeptName = dept.dept_name;
      this.hospitals = []; // 清空旧结果
      this.loadingHospitals = true;

      try {
        // 调用我们刚才修改的 searchHospitals 接口
        const res = await api.public.searchHospitals({
          department: this.selectedDeptId
        });

        if (res.data.code === 0) {
          this.hospitals = res.data.data;
        }
      } catch (error) {
        console.error("查询医院失败", error);
      } finally {
        this.loadingHospitals = false;
      }
    },

    // 跳转详情
    goToHospital(id) {
      this.$router.push(`/hospital/${id}`);
    }
  }
};
</script>

<style scoped>
.dept-index {
  max-width: 1200px;
  margin: 0 auto;
  padding: 30px 20px;
}

.header {
  text-align: center;
  margin-bottom: 30px;
}

.subtitle {
  color: #666;
  margin-top: 10px;
}

/* 科室标签样式 */
.dept-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
  justify-content: center;
  margin-bottom: 40px;
}

.tag {
  padding: 10px 20px;
  background-color: #f0f2f5;
  border: 1px solid #e1e4e8;
  border-radius: 20px;
  cursor: pointer;
  transition: all 0.3s;
  font-size: 1rem;
  color: #333;
}

.tag:hover {
  border-color: #4CAF50;
  color: #4CAF50;
}

.tag.active {
  background-color: #4CAF50;
  color: white;
  border-color: #4CAF50;
  box-shadow: 0 4px 10px rgba(76, 175, 80, 0.3);
}

/* 结果区域样式 */
.results-section {
  animation: fadeIn 0.5s ease;
}

.results-header {
  border-left: 5px solid #4CAF50;
  padding-left: 15px;
  margin-bottom: 20px;
  display: flex;
  align-items: center;
  gap: 15px;
}

.count-badge {
  background: #e8f5e9;
  color: #2e7d32;
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 0.85rem;
  font-weight: bold;
}

.hospital-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 20px;
}

.hospital-card {
  background: white;
  border: 1px solid #eee;
  border-radius: 8px;
  padding: 20px;
  cursor: pointer;
  transition: transform 0.2s, box-shadow 0.2s;
}

.hospital-card:hover {
  transform: translateY(-3px);
  box-shadow: 0 8px 15px rgba(0,0,0,0.1);
  border-color: #a5d6a7;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 10px;
}

.card-header h3 {
  margin: 0;
  font-size: 1.1rem;
  color: #2c3e50;
}

.level-tag {
  background: #fff3e0;
  color: #f57c00;
  font-size: 0.8rem;
  padding: 2px 6px;
  border-radius: 4px;
  white-space: nowrap;
}

.address {
  color: #666;
  font-size: 0.9rem;
  margin-bottom: 15px;
  min-height: 40px; /* 保持卡片高度一致 */
}

.view-btn {
  color: #4CAF50;
  font-size: 0.9rem;
  font-weight: bold;
}

.empty-state {
  text-align: center;
  padding: 40px;
  color: #999;
  background: #f9f9f9;
  border-radius: 8px;
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}
</style>