<template>
  <div class="dept-container">
    <div v-if="loading" class="loading">加载科室中...</div>

    <div v-else-if="departments.length === 0" class="empty">
      暂无科室信息
    </div>

    <div v-else class="dept-grid">
      <div
        v-for="dept in departments"
        :key="dept.id"
        class="dept-card"
        @click="openDetail(dept.dept)"
      >
        <h4>{{ dept.dept_name }}</h4>
        <div class="dept-brief">
          <span>📍 {{ dept.floor || '楼层未知' }}</span>
          <span>🚪 {{ dept.room_count || 0 }} 诊室</span>
        </div>
      </div>
    </div>

    <div v-if="showModal" class="modal-overlay" @click.self="closeModal">
      <div class="modal-content">
        <header class="modal-header">
          <h3>{{ currentDept.dept_name }} - 详细信息</h3>
          <button class="close-btn" @click="closeModal">×</button>
        </header>

        <div v-if="detailLoading" class="detail-loading">
          数据加载中...
        </div>

        <div v-else class="detail-body">
          <div class="section">
            <h5>🏥 基础概况</h5>
            <p><strong>标准代码:</strong> {{ currentDept.standard_code || '无' }}</p>
            <p><strong>所在楼层:</strong> {{ currentDept.floor || '未设置' }}</p>
            <p><strong>诊室数量:</strong> {{ currentDept.room_count }} 间</p>
          </div>

          <div class="section resource-section">
            <h5>🚑 医疗资源</h5>
            <div class="res-grid">
              <div class="res-item">
                <span class="res-num">{{ currentDept.bed_count }}</span>
                <span class="res-label">床位</span>
              </div>
              <div class="res-item">
                <span class="res-num">{{ currentDept.device_count }}</span>
                <span class="res-label">专业设备</span>
              </div>
              <div class="res-item">
                <span class="res-num">{{ currentDept.daily_capacity }}</span>
                <span class="res-label">日接诊量</span>
              </div>
            </div>
          </div>
        </div>

        <div class="modal-footer">
          <button @click="closeModal">关闭</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import api from '@/services/api'; // 假设你封装了 axios

export default {
  name: 'HospitalDepartmentList',
  props: {
    hospitalId: {
      type: [Number, String],
      required: true
    }
  },
  data() {
    return {
      departments: [],
      loading: false,

      // 弹窗相关数据
      showModal: false,
      detailLoading: false,
      currentDept: {}
    };
  },
  watch: {
    hospitalId: {
      immediate: true,
      handler(newVal) {
        if (newVal) {
          this.fetchDepartments();
        }
      }
    }
  },
  methods: {
    // 获取列表 (已有接口)
    async fetchDepartments() {
      this.loading = true;
      try {
        // GET /api/hospitals/{id}/departments/
        const res = await api.hospital.getHospitalDepartments(this.hospitalId);
        if (res.data.code === 0) {
          this.departments = res.data.data;
        }
      } catch (error) {
        console.error("获取科室列表失败", error);
      } finally {
        this.loading = false;
      }
    },

    // 获取详情 (新接口)
    async openDetail(deptId) {
      this.showModal = true;
      this.detailLoading = true;
      this.currentDept = {}; // 清空旧数据

      try {
        // GET /api/hospitals/{id}/department_detail/?dept_id={deptId}
        const res = await api.hospital.getDepartmentDetail(this.hospitalId, deptId);

        if (res.data.code === 0) {
          this.currentDept = res.data.data;
        }
      } catch (error) {
        console.error("获取详情失败", error);
        this.currentDept = { dept_name: '加载失败' };
      } finally {
        this.detailLoading = false;
      }
    },

    closeModal() {
      this.showModal = false;
    }
  }
};
</script>

<style scoped>
/* 列表样式 */
.dept-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 15px;
  padding: 10px 0;
}

.dept-card {
  border: 1px solid #eee;
  border-radius: 8px;
  padding: 15px;
  cursor: pointer;
  transition: all 0.3s;
  background: #fff;
  box-shadow: 0 2px 4px rgba(0,0,0,0.05);
}

.dept-card:hover {
  transform: translateY(-3px);
  box-shadow: 0 5px 12px rgba(0,0,0,0.1);
  border-color: #4CAF50;
}

.dept-card h4 {
  margin: 0 0 10px 0;
  color: #333;
}

.dept-brief {
  font-size: 0.9em;
  color: #666;
  display: flex;
  justify-content: space-between;
}

/* 弹窗样式 (简单的自定义 Modal) */
.modal-overlay {
  position: fixed;
  top: 0; left: 0;
  width: 100%; height: 100%;
  background: rgba(0,0,0,0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.modal-content {
  background: white;
  width: 500px;
  max-width: 90%;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 4px 15px rgba(0,0,0,0.2);
}

.modal-header {
  padding: 15px 20px;
  background: #f8f9fa;
  border-bottom: 1px solid #eee;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.close-btn {
  background: none;
  border: none;
  font-size: 1.5rem;
  cursor: pointer;
}

.detail-body {
  padding: 20px;
}

.section {
  margin-bottom: 20px;
}

.section h5 {
  border-left: 4px solid #4CAF50;
  padding-left: 10px;
  margin-bottom: 10px;
  color: #2c3e50;
}

/* 资源数据网格 */
.res-grid {
  display: flex;
  justify-content: space-around;
  background: #f0f7f1;
  padding: 15px;
  border-radius: 8px;
}

.res-item {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.res-num {
  font-size: 1.4em;
  font-weight: bold;
  color: #4CAF50;
}

.res-label {
  font-size: 0.85em;
  color: #666;
}

.modal-footer {
  padding: 10px 20px;
  text-align: right;
  border-top: 1px solid #eee;
}

.modal-footer button {
  padding: 8px 20px;
  background: #eee;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.modal-footer button:hover {
  background: #ddd;
}
</style>