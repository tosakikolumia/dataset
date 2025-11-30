<template>
  <div class="hospital-detail" v-if="hospital">
    <div class="hospital-header">
      <h1>{{ hospital.name }}</h1>
      <p class="address">{{ hospital.address }}</p>
      <p class="phone">电话: {{ hospital.phone || '暂无' }}</p>
      <p class="rating">评分: {{ hospital.rating || '暂无评分' }}</p>
    </div>
    
    <div class="tabs">
      <button 
        v-for="tab in tabs" 
        :key="tab.key"
        :class="{ active: activeTab === tab.key }"
        @click="changeTab(tab.key)"
      >
        {{ tab.title }}
      </button>
    </div>
    
    <div class="tab-content">
      <!-- 基础信息 -->
      <div v-if="activeTab === 'info'" class="tab-pane">
        <h3>医院简介</h3>
        <p>{{ hospital.description || '暂无简介' }}</p>
        
        <h3>详细信息</h3>
        <div class="info-grid">
          <div><strong>医院等级:</strong> {{ hospital.level_name || '未设置' }}</div>
          <div><strong>成立时间:</strong> {{ hospital.establishment_date || '未设置' }}</div>
          <div><strong>床位数:</strong> {{ hospital.bed_count || '未设置' }}</div>
          <div><strong>员工数:</strong> {{ hospital.staff_count || '未设置' }}</div>
        </div>
      </div>
      
      <!-- 科室信息 -->
      <div v-if="activeTab === 'departments'" class="tab-pane">
        <h3>科室列表</h3>
        <div v-if="departments.length > 0" class="departments-list">
          <div 
            v-for="dept in departments" 
            :key="dept.id" 
            class="department-item"
          >
            <h4>{{ dept.department?.name || dept.department_name }}</h4>
            <p>{{ dept.description || '暂无描述' }}</p>
          </div>
        </div>
        <div v-else class="no-data">暂无科室信息</div>
      </div>
      
      <!-- 评分记录 -->
      <div v-if="activeTab === 'scores'" class="tab-pane">
        <h3>医院评分记录</h3>
        <div v-if="scores.length > 0" class="scores-list">
          <div 
            v-for="score in scores" 
            :key="score.id" 
            class="score-item"
          >
            <h4>评分: {{ score.score }}/100</h4>
            <p><strong>检查日期:</strong> {{ formatDate(score.last_inspection_date) }}</p>
            <p><strong>检查内容:</strong> {{ score.inspection_content || '无' }}</p>
            <p><strong>备注:</strong> {{ score.remarks || '无' }}</p>
          </div>
        </div>
        <div v-else class="no-data">暂无评分记录</div>
      </div>
      
      <!-- 突发事件 -->
      <div v-if="activeTab === 'events'" class="tab-pane">
        <h3>参与的突发事件</h3>
        <div v-if="events.length > 0" class="events-list">
          <div 
            v-for="event in events" 
            :key="event.id" 
            class="event-item"
          >
            <h4>{{ event.title }}</h4>
            <p><strong>类型:</strong> {{ event.event_type || '未分类' }}</p>
            <p><strong>发生时间:</strong> {{ formatDate(event.occurrence_time) }}</p>
            <p><strong>状态:</strong> {{ event.status || '进行中' }}</p>
            <p><strong>描述:</strong> {{ event.description || '暂无描述' }}</p>
          </div>
        </div>
        <div v-else class="no-data">暂无突发事件记录</div>
      </div>
    </div>
  </div>
  
  <div v-else class="loading">加载中...</div>
</template>

<script>
import { useHospitalStore } from '@/stores/hospital';

export default {
  name: 'HospitalDetailView',
  props: ['id'],
  data() {
    return {
      hospitalStore: useHospitalStore(),
      activeTab: 'info',
      tabs: [
        { key: 'info', title: '医院信息' },
        { key: 'departments', title: '科室信息' },
        { key: 'scores', title: '医院评分' },
        { key: 'events', title: '突发事件' }
      ]
    };
  },
  computed: {
    hospital() {
      return this.hospitalStore.currentHospital;
    },
    departments() {
      return this.hospitalStore.hospitalDepartments;
    },
    scores() {
      return this.hospitalStore.hospitalScores;
    },
    events() {
      return this.hospitalStore.hospitalEvents;
    }
  },
  async created() {
    await this.loadHospitalData();
  },
  methods: {
    async loadHospitalData() {
      await this.hospitalStore.fetchHospitalById(this.id);
      await this.hospitalStore.fetchHospitalDepartments(this.id);
      await this.hospitalStore.fetchHospitalScores(this.id);
      await this.hospitalStore.fetchHospitalEvents(this.id);
    },
    changeTab(tabKey) {
      this.activeTab = tabKey;
    },
    formatDate(dateString) {
      if (!dateString) return '未设置';
      const date = new Date(dateString);
      return date.toLocaleDateString('zh-CN');
    }
  },
  watch: {
    id: {
      handler() {
        this.loadHospitalData();
      },
      immediate: true
    }
  }
};
</script>

<style scoped>
.hospital-detail {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

.hospital-header h1 {
  margin-bottom: 10px;
}

.address, .phone, .rating {
  margin: 5px 0;
  color: #666;
}

.tabs {
  display: flex;
  margin: 20px 0;
  border-bottom: 1px solid #ddd;
}

.tabs button {
  padding: 10px 20px;
  background: none;
  border: none;
  cursor: pointer;
  border-bottom: 3px solid transparent;
}

.tabs button.active {
  border-bottom-color: #007bff;
  color: #007bff;
}

.tab-content {
  padding: 20px 0;
}

.info-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 15px;
  margin-top: 20px;
}

.department-item, .score-item, .event-item {
  border: 1px solid #eee;
  padding: 15px;
  margin-bottom: 15px;
  border-radius: 4px;
}

.no-data {
  text-align: center;
  padding: 40px;
  color: #666;
}

.loading {
  text-align: center;
  padding: 40px;
  color: #666;
}
</style>