<template>
  <div class="resource-overview">
    <h1>📊 全市医疗资源总览</h1>

    <div class="overview-cards">
      <div class="card blue">
        <div class="label">🏥 总医院数</div>
        <div class="value">{{ dashboard.total_hospitals }}</div>
      </div>
      <div class="card green">
        <div class="label">🛏️ 全市床位总数</div>
        <div class="value">{{ dashboard.total_beds }}</div>
        <div class="sub">ICU床位: {{ dashboard.icu_beds }}</div>
      </div>
      <div class="card orange">
        <div class="label">🩺 设备总数</div>
        <div class="value">{{ dashboard.total_devices }}</div>
      </div>
      <div class="card purple">
        <div class="label">🚪 诊室总数</div>
        <div class="value">{{ dashboard.total_rooms }}</div>
      </div>
    </div>

    <div class="filter-bar">
      <div class="filter-item">
        <label>行政区：</label>
        <select v-model="filters.district" @change="loadRankData">
          <option value="">全部</option>
          <option v-for="d in districts" :key="d.district_id" :value="d.district_id">
            {{ d.district_name }}
          </option>
        </select>
      </div>
      <div class="filter-item">
        <label>医院等级：</label>
        <select v-model="filters.level" @change="loadRankData">
          <option value="">全部</option>
          <option v-for="l in levels" :key="l.level_id" :value="l.level_id">
            {{ l.level_name }}
          </option>
        </select>
      </div>
      <button class="reset-btn" @click="resetFilters">重置筛选</button>
    </div>

    <div class="table-section">
      <h3>🏥 资源分布明细</h3>
      <table>
        <thead>
          <tr>
            <th>医院名称</th>
            <th>行政区</th>
            <th>等级</th>
            <th>总床位</th>
            <th>ICU/设备/诊室</th>
            <th>资源紧张度</th>
            <th>操作</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="item in rankData" :key="item.hospital_id">
            <td>{{ item.name }}</td>
            <td>{{ item.district }}</td>
            <td>
              <span class="tag level-tag">{{ item.level }}</span>
            </td>
            <td class="font-bold">{{ item.bed_total }}</td>
            <td class="resource-detail">
              <span>设备: {{ item.device_count }}</span>
              <span>诊室: {{ item.room_count }}</span>
            </td>
            <td>
              <span :class="['status-badge', item.stress]">
                {{ getStressLabel(item.stress) }}
              </span>
            </td>
            <td>
              <button class="view-btn" @click="$router.push(`/hospital/${item.hospital_id}`)">
                查看详情
              </button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script>
import api from '@/services/api';

export default {
  name: 'ResourceOverviewView',
  data() {
    return {
      dashboard: {
        total_hospitals: 0,
        total_beds: 0,
        icu_beds: 0,
        total_devices: 0,
        total_rooms: 0
      },
      rankData: [],
      districts: [],
      levels: [],
      filters: {
        district: '',
        level: ''
      }
    };
  },
  async created() {
    await this.loadDashboard();
    await this.loadOptions();
    await this.loadRankData();
  },
  methods: {
    async loadDashboard() {
      try {
        const res = await api.statistics.getDashboard();
        this.dashboard = res.data.data;
      } catch (err) {
        console.error("加载总览失败", err);
      }
    },
    async loadOptions() {
      // 加载筛选下拉框的选项
      const dRes = await api.district.getAllDistricts();
      this.districts = dRes.data.data || dRes.data;

      const lRes = await api.hospitalLevel.getAllLevels();
      this.levels = lRes.data.data || lRes.data;
    },
    async loadRankData() {
      try {
        const res = await api.statistics.getHospitalRank(this.filters);
        this.rankData = res.data.data;
        console.log(this.rankData);
      } catch (err) {
        console.error("加载列表失败", err);
      }
    },
    resetFilters() {
      this.filters.district = '';
      this.filters.level = '';
      this.loadRankData();
    },
    getStressLabel(status) {
      const map = {
        high: '🔴 紧张',
        medium: '🟠 适中',
        normal: '🟢 充足'
      };
      return map[status] || status;
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

/* 卡片样式 */
.overview-cards {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 20px;
  margin-bottom: 30px;
}
.card {
  background: white;
  padding: 20px;
  border-radius: 10px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
  text-align: center;
}
.card .label { font-size: 14px; color: #666; margin-bottom: 10px; }
.card .value { font-size: 28px; font-weight: bold; color: #333; }
.card .sub { font-size: 12px; color: #888; margin-top: 5px; }

.blue { border-top: 4px solid #007bff; }
.green { border-top: 4px solid #28a745; }
.orange { border-top: 4px solid #fd7e14; }
.purple { border-top: 4px solid #6f42c1; }

/* 筛选区 */
.filter-bar {
  background: white;
  padding: 15px;
  border-radius: 8px;
  margin-bottom: 20px;
  display: flex;
  gap: 20px;
  align-items: center;
}
.filter-item label { margin-right: 10px; font-weight: bold; }
.filter-item select { padding: 5px 10px; border: 1px solid #ddd; border-radius: 4px; }
.reset-btn { padding: 5px 15px; background: #f8f9fa; border: 1px solid #ddd; cursor: pointer; }

/* 表格区 */
.table-section { background: white; padding: 20px; border-radius: 8px; }
table { width: 100%; border-collapse: collapse; margin-top: 15px; }
th { background: #f8f9fa; text-align: left; padding: 12px; border-bottom: 2px solid #eee; }
td { padding: 12px; border-bottom: 1px solid #eee; color: #555; }

.tag { padding: 2px 8px; border-radius: 12px; font-size: 12px; background: #e9ecef; color: #495057; }
.resource-detail { font-size: 13px; color: #666; display: flex; flex-direction: column; gap: 4px; }
.font-bold { font-weight: bold; color: #333; }

/* 状态徽章 */
.status-badge { padding: 4px 8px; border-radius: 4px; font-size: 12px; font-weight: bold; }
.status-badge.high { background: #ffebee; color: #c62828; }
.status-badge.medium { background: #fff3e0; color: #ef6c00; }
.status-badge.normal { background: #e8f5e9; color: #2e7d32; }

.view-btn { background: none; border: 1px solid #007bff; color: #007bff; padding: 4px 10px; border-radius: 4px; cursor: pointer; }
.view-btn:hover { background: #007bff; color: white; }
</style>