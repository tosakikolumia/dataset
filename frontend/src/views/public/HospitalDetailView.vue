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
      <div v-if="activeTab === 'info'" class="tab-pane">
        <h3>医院简介</h3>
        <p>{{ hospital.introduction || '暂无简介' }}</p>

        <h3>详细信息</h3>
        <div class="info-grid">
          <div><strong>医院等级:</strong> {{ hospital.level_name || '未设置' }}</div>

          <div><strong>成立时间:</strong> {{ formatYear(hospital.established_year) }}</div>

          <div><strong>床位数:</strong> {{ hospital.bed_total || '未设置' }}</div>

          <div><strong>日门诊量:</strong> {{ hospital.outpatient_capacity ? hospital.outpatient_capacity + ' 人次' : '未设置' }}</div>

          <div><strong>员工数:</strong> {{ hospital.staff_count || 0 }} 人</div>
        </div>
      </div>

      <div v-if="activeTab === 'departments'" class="tab-pane">
        <h3>科室列表</h3>
        <HospitalDepartmentList :hospitalId="hospital.hospital_id" />
      </div>

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
import HospitalDepartmentList from '@/components/HospitalDepartmentList.vue';
export default {
  name: 'HospitalDetailView',
  components: {HospitalDepartmentList},
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
      // 确保这里直接返回 store 中的对象，保持响应性
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
  updated() {
    // 调试日志：当组件更新时，在控制台输出当前数据，方便排查
    if (this.hospital) {
      console.log('HospitalDetailView updated:', {
        name: this.hospital.name,
        intro: this.hospital.introduction,
        year: this.hospital.established_year,
        bed: this.hospital.bed_total
      });
    }
  },
  methods: {
    async loadHospitalData() {
      if (this.id) {
        await this.hospitalStore.fetchHospitalById(this.id);
        await this.hospitalStore.fetchHospitalDepartments(this.id);
        await this.hospitalStore.fetchHospitalScores(this.id);
        await this.hospitalStore.fetchHospitalEvents(this.id);
      }
    },
    changeTab(tabKey) {
      this.activeTab = tabKey;
    },
    // ✅ 新增: 专门处理纯年份数字 (如 1985)
    formatYear(year) {
      if (!year) return '未设置';
      return year + '年';
    },
    // 处理完整日期字符串 (如 2023-10-01)
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