<template>
  <div class="staff-statistics">
    <div class="header-section">
      <h1>医护人员规模与结构管理</h1>
      <p>全市医生、护士数量概览及职称结构分析</p>
    </div>

    <div class="stats-overview">
      <div class="stat-card doctor-card">
        <h3>医生总数</h3>
        <p class="stat-value">{{ stats.total_doctors }}</p>
        <span class="stat-label">Doctors</span>
      </div>

      <div class="stat-card nurse-card">
        <h3>护士总数</h3>
        <p class="stat-value">{{ stats.total_nurses }}</p>
        <span class="stat-label">Nurses</span>
      </div>

      <div class="stat-card other-card">
        <h3>其他人员</h3>
        <p class="stat-value">{{ stats.total_others }}</p>
        <span class="stat-label">Others</span>
      </div>

      <div class="stat-card total-card">
        <h3>全员总计</h3>
        <p class="stat-value">{{ stats.total_staff }}</p>
        <span class="stat-label">Total Staff</span>
      </div>
    </div>

    <div class="content-grid">
      <div class="panel title-structure">
        <h2>职称结构分布</h2>
        <div v-if="titleStructure.length > 0" class="structure-list">
          <div v-for="(item, index) in titleStructure" :key="index" class="structure-item">
            <div class="structure-info">
              <span class="structure-name">{{ item.title }}</span>
              <span class="structure-count">{{ item.count }}人</span>
            </div>
            <div class="progress-bg">
              <div
                class="progress-bar"
                :style="{ width: getPercentage(item.count) + '%' }"
                :class="getBarClass(item.title)"
              ></div>
            </div>
          </div>
        </div>
        <div v-else class="empty-state">暂无职称数据</div>
      </div>

      <div class="panel hospital-distribution">
        <h2>各医院人员分布</h2>
        <div class="hospital-list">
          <div
            v-for="hospital in hospitalDistribution"
            :key="hospital.hospital__hospital_id"
            class="hospital-item"
          >
            <div class="hospital-header">
              <h3>{{ hospital.hospital__name }}</h3>
              <span class="total-badge">总计: {{ hospital.total }}</span>
            </div>
            <div class="hospital-stats">
              <div class="sub-stat">
                <span class="dot doctor-dot"></span> 医生: {{ hospital.doctors_count }}
              </div>
              <div class="sub-stat">
                <span class="dot nurse-dot"></span> 护士: {{ hospital.nurses_count }}
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 新增环形图部分 -->
    <div class="panel chart-section">
      <h2>全市医院人员占比分析</h2>
      <div class="chart-container">
        <div ref="hospitalPieChart" class="pie-chart"></div>
        <div class="chart-legend">
          <div class="legend-item" v-for="(hospital, index) in hospitalDistribution" :key="index">
            <span class="legend-color" :style="{ backgroundColor: chartColors[index % chartColors.length] }"></span>
            <span class="legend-name">{{ hospital.hospital__name }}</span>
            <span class="legend-value">{{ hospital.total }}人 ({{ getHospitalPercentage(hospital.total) }}%)</span>
          </div>
        </div>
      </div>
    </div>

    <div class="panel staff-list-section">
      <div class="panel-header">
        <h2>人员明细表</h2>
        <button @click="loadData" class="refresh-btn">刷新数据</button>
      </div>
      <div class="table-container">
        <table>
          <thead>
            <tr>
              <th>姓名</th>
              <th>工号</th>
              <th>职称</th>
              <th>性别</th>
              <th>入职日期</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="staff in allStaff" :key="staff.staff_id">
              <td>{{ staff.name }}</td>
              <td>{{ staff.staff_id }}</td>
              <td>
                <span class="tag" :class="getBarClass(staff.title)">
                  {{ staff.title || '未定级' }}
                </span>
              </td>
              <td>{{ staff.gender || '-' }}</td>
              <td>{{ staff.hire_date || '-' }}</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script>
import api from '@/services/api';
import * as echarts from 'echarts';

export default {
  name: 'StaffStatisticsView',
  data() {
    return {
      stats: {
        total_staff: 0,
        total_doctors: 0,
        total_nurses: 0,
        total_others: 0
      },
      titleStructure: [],
      hospitalDistribution: [],
      allStaff: [],
      chartColors: [
        '#3498db', '#2ecc71', '#f39c12', '#e74c3c', '#9b59b6',
        '#1abc9c', '#34495e', '#16a085', '#27ae60', '#2980b9',
        '#8e44ad', '#f1c40f', '#e67e22', '#95a5a6', '#d35400'
      ],
      pieChart: null
    };
  },
  created() {
    this.loadData();
  },
  mounted() {
    window.addEventListener('resize', this.handleResize);
  },
  beforeUnmount() {
    window.removeEventListener('resize', this.handleResize);
    if (this.pieChart) {
      this.pieChart.dispose();
    }
  },
  methods: {
    async loadData() {
      try {
        // 并行请求统计数据和明细数据
        const [statsRes, listRes] = await Promise.all([
          api.staff.getStatistics(),
          api.staff.getAllStaffs()
        ]);

        // 处理统计数据
        const data = statsRes.data;
        this.stats = data.overview;
        this.titleStructure = data.title_structure;
        this.hospitalDistribution = data.hospital_distribution;

        // 处理列表数据
        this.allStaff = listRes.data.results || listRes.data;

        // 等待DOM更新后初始化图表
        this.$nextTick(() => {
          this.initPieChart();
        });

      } catch (error) {
        console.error('Failed to load staff data:', error);
        if (error.response && error.response.status === 401) {
          this.$router.push('/login');
        }
      }
    },
    initPieChart() {
      if (!this.$refs.hospitalPieChart) return;

      // 如果图表已存在，先销毁
      if (this.pieChart) {
        this.pieChart.dispose();
      }

      // 初始化图表
      this.pieChart = echarts.init(this.$refs.hospitalPieChart);

      // 准备图表数据
      const chartData = this.hospitalDistribution.map((hospital, index) => ({
        name: hospital.hospital__name,
        value: hospital.total,
        itemStyle: {
          color: this.chartColors[index % this.chartColors.length]
        }
      }));

      // 配置选项
      const option = {
        tooltip: {
          trigger: 'item',
          formatter: '{b}: {c}人 ({d}%)'
        },
        series: [
          {
            type: 'pie',
            radius: ['45%', '70%'],
            avoidLabelOverlap: true,
            itemStyle: {
              borderRadius: 8,
              borderColor: '#fff',
              borderWidth: 2
            },
            label: {
              show: true,
              position: 'outside',
              formatter: '{b}\n{d}%',
              fontSize: 12
            },
            emphasis: {
              label: {
                show: true,
                fontSize: 14,
                fontWeight: 'bold'
              },
              itemStyle: {
                shadowBlur: 10,
                shadowOffsetX: 0,
                shadowColor: 'rgba(0, 0, 0, 0.5)'
              }
            },
            data: chartData
          }
        ]
      };

      this.pieChart.setOption(option);
    },
    handleResize() {
      if (this.pieChart) {
        this.pieChart.resize();
      }
    },
    getPercentage(count) {
      if (!this.stats.total_staff) return 0;
      return ((count / this.stats.total_staff) * 100).toFixed(1);
    },
    getHospitalPercentage(count) {
      if (!this.stats.total_staff) return 0;
      return ((count / this.stats.total_staff) * 100).toFixed(1);
    },
    getBarClass(title) {
      if (!title) return 'bg-gray';
      if (title.includes('医')) return 'bg-blue';
      if (title.includes('护')) return 'bg-green';
      return 'bg-orange';
    }
  }
};
</script>

<style scoped>
.staff-statistics {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
  color: #333;
}

.header-section {
  margin-bottom: 30px;
  border-bottom: 1px solid #eee;
  padding-bottom: 10px;
}

/* 概览卡片 */
.stats-overview {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 20px;
  margin-bottom: 30px;
}

.stat-card {
  background: white;
  padding: 20px;
  border-radius: 10px;
  box-shadow: 0 2px 10px rgba(0,0,0,0.05);
  text-align: center;
  border-left: 5px solid #ccc;
}

.doctor-card { border-left-color: #3498db; }
.nurse-card { border-left-color: #2ecc71; }
.other-card { border-left-color: #f39c12; }
.total-card { border-left-color: #34495e; }

.stat-value {
  font-size: 2.5rem;
  font-weight: bold;
  margin: 10px 0;
  color: #2c3e50;
}

.stat-label {
  color: #7f8c8d;
  font-size: 0.9rem;
  text-transform: uppercase;
}

/* 内容网格 */
.content-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 20px;
  margin-bottom: 30px;
}

.panel {
  background: white;
  padding: 20px;
  border-radius: 10px;
  box-shadow: 0 2px 10px rgba(0,0,0,0.05);
}

.panel h2 {
  font-size: 1.2rem;
  margin-bottom: 20px;
  color: #2c3e50;
  border-left: 4px solid #3498db;
  padding-left: 10px;
}

/* 职称结构列表 */
.structure-item {
  margin-bottom: 15px;
}

.structure-info {
  display: flex;
  justify-content: space-between;
  margin-bottom: 5px;
  font-weight: 500;
}

.progress-bg {
  background: #f0f0f0;
  height: 10px;
  border-radius: 5px;
  overflow: hidden;
}

.progress-bar {
  height: 100%;
  border-radius: 5px;
  transition: width 0.5s ease;
}

.bg-blue { background-color: #3498db; }
.bg-green { background-color: #2ecc71; }
.bg-orange { background-color: #f39c12; }
.bg-gray { background-color: #bdc3c7; }

/* 医院分布列表 */
.hospital-list {
  max-height: 400px;
  overflow-y: auto;
}

.hospital-item {
  padding: 12px;
  border-bottom: 1px solid #f0f0f0;
}

.hospital-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 8px;
}

.hospital-header h3 {
  margin: 0;
  font-size: 1rem;
  color: #333;
}

.total-badge {
  background: #f8f9fa;
  padding: 2px 8px;
  border-radius: 12px;
  font-size: 0.85rem;
  color: #666;
}

.hospital-stats {
  display: flex;
  gap: 15px;
  font-size: 0.9rem;
  color: #666;
}

.dot {
  display: inline-block;
  width: 8px;
  height: 8px;
  border-radius: 50%;
  margin-right: 5px;
}
.doctor-dot { background: #3498db; }
.nurse-dot { background: #2ecc71; }

/* 环形图部分 */
.chart-section {
  margin-bottom: 30px;
}

.chart-container {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 30px;
  align-items: center;
}

.pie-chart {
  width: 100%;
  height: 400px;
}

.chart-legend {
  max-height: 400px;
  overflow-y: auto;
  padding: 10px;
}

.legend-item {
  display: flex;
  align-items: center;
  padding: 8px 0;
  border-bottom: 1px solid #f0f0f0;
  gap: 10px;
}

.legend-color {
  width: 16px;
  height: 16px;
  border-radius: 3px;
  flex-shrink: 0;
}

.legend-name {
  flex: 1;
  font-weight: 500;
  color: #333;
}

.legend-value {
  color: #666;
  font-size: 0.9rem;
}

/* 表格部分 */
.panel-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 15px;
}

.refresh-btn {
  padding: 6px 12px;
  background: #3498db;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: background 0.3s;
}

.refresh-btn:hover {
  background: #2980b9;
}

.table-container {
  overflow-x: auto;
}

table {
  width: 100%;
  border-collapse: collapse;
}

th, td {
  padding: 12px;
  text-align: left;
  border-bottom: 1px solid #eee;
}

th {
  background: #f9fafb;
  color: #666;
  font-weight: 600;
}

.tag {
  display: inline-block;
  padding: 2px 8px;
  border-radius: 4px;
  font-size: 0.85rem;
  color: white;
}

@media (max-width: 768px) {
  .stats-overview { grid-template-columns: 1fr 1fr; }
  .content-grid { grid-template-columns: 1fr; }
  .chart-container {
    grid-template-columns: 1fr;
  }
  .pie-chart {
    height: 300px;
  }
}
</style>