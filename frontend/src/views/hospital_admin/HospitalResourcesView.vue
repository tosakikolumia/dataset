<template>
  <div class="hospital-resources">
    <div class="page-header">
      <h1>科室资源管理</h1>
      <p>管理医院各科室的床位、设备及查看医护人员配置</p>
    </div>

    <div class="resources-container">
      <div class="departments-panel">
        <div class="panel-header">
          <h3>本院科室列表</h3>
          <button class="btn-refresh" @click="loadResources" title="刷新列表">↻</button>
        </div>

        <div v-if="loading" class="loading-state">数据加载中...</div>

        <ul v-else class="departments-list">
          <li
            v-for="resource in resources"
            :key="resource.dept_res_id"
            :class="{ active: selectedResource?.dept_res_id === resource.dept_res_id }"
            @click="selectResource(resource)"
          >
            <div class="dept-name">{{ resource.dept_name }}</div>
            <div class="dept-summary">
              <small>床位: {{ resource.bed_count || 0 }} | 设备: {{ resource.device_count || 0 }}</small>
            </div>
          </li>
          <li v-if="resources.length === 0" class="empty-list">
            暂无相关科室资源数据
          </li>
        </ul>
      </div>

      <div class="resources-panel">
        <div class="panel-header">
          <h3>
            资源详情
            <span v-if="selectedResource" class="highlight-text">
              - {{ selectedResource.dept_name }}
            </span>
          </h3>
        </div>

        <div v-if="selectedResource" class="resources-content">

          <div class="resources-form">
            <div class="form-info-banner">
              正在编辑 <strong>{{ selectedResource.hospital_name }}</strong> 的资源信息
            </div>

            <div class="form-row">
              <div class="form-group">
                <label>总床位数 (Bed Count):</label>
                <input
                  type="number"
                  min="0"
                  v-model.number="formData.bed_count"
                  placeholder="请输入数字"
                />
              </div>

              <div class="form-group">
                <label>医疗设备数量 (Device Count):</label>
                <input
                  type="number"
                  min="0"
                  v-model.number="formData.device_count"
                  placeholder="请输入数字"
                />
              </div>
            </div>

            <div class="form-row">
              <div class="form-group">
                <label>日最大接诊能力 (Daily Capacity):</label>
                <input
                  type="number"
                  min="0"
                  v-model.number="formData.daily_capacity"
                  placeholder="人次/天"
                />
              </div>
              <div class="form-group action-group">
                 <button class="btn-save" @click="saveChanges" :disabled="saving">
                  <span v-if="saving">保存中...</span>
                  <span v-else>保存资源修改</span>
                </button>
              </div>
            </div>
          </div>

          <div class="staff-section">
            <h4>在该科室就职的医护人员 (只读)</h4>

            <div v-if="loadingStaff" class="loading-text">加载人员名单中...</div>

            <table v-else-if="staffList.length > 0" class="staff-table">
              <thead>
                <tr>
                  <th>姓名</th>
                  <th>性别</th>
                  <th>职称 (Title)</th>
                  <th>雇佣类型 (Employment)</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="staff in staffList" :key="staff.id">
                  <td>{{ staff.staff_name }}</td>
                  <td>{{ staff.staff_gender || '-' }}</td>
                  <td>
                    <span class="tag title-tag">{{ staff.staff_title || '未定级' }}</span>
                  </td>
                  <td>
                    <span class="tag type-tag">{{ staff.employment_type || '标准' }}</span>
                  </td>
                </tr>
              </tbody>
            </table>

            <div v-else class="empty-staff">
              该科室暂无关联的医护人员记录。
            </div>
          </div>

        </div>

        <div v-else class="no-selection">
          <div class="empty-state-content">
            <i class="icon-placeholder">👈</i>
            <p>请从左侧列表选择一个科室进行管理</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import api from '@/services/api';
import { useAuthStore } from '@/stores/auth';

export default {
  name: 'HospitalResourcesView',
  data() {
    return {
      resources: [], // 资源列表
      selectedResource: null, // 当前选中资源
      formData: {
        bed_count: 0,
        device_count: 0,
        daily_capacity: 0
      },
      staffList: [], // [新增] 医护人员列表
      loading: false,
      loadingStaff: false, // [新增] 人员加载状态
      saving: false,
      authStore: useAuthStore()
    };
  },
  async created() {
    await this.loadResources();
  },
  methods: {
    // 1. 加载资源列表
    async loadResources() {
      this.loading = true;
      try {
        const response = await api.department.getDepartmentResources();
        this.resources = Array.isArray(response.data) ? response.data : (response.data.results || []);

        // 保持选中状态
        if (this.selectedResource) {
          const found = this.resources.find(r => r.dept_res_id === this.selectedResource.dept_res_id);
          if (found) this.selectResource(found);
        }
      } catch (error) {
        console.error('加载科室资源失败:', error);
        alert('无法获取科室资源列表');
      } finally {
        this.loading = false;
      }
    },

    // 2. 选中资源
    selectResource(resource) {
      this.selectedResource = resource;
      this.formData = {
        bed_count: resource.bed_count,
        device_count: resource.device_count,
        daily_capacity: resource.daily_capacity
      };

      // [新增] 选中科室后，加载该科室的人员
      this.loadDeptStaff(resource.dept);
    },

    // [新增] 3. 加载科室人员
    async loadDeptStaff(deptId) {
      if (!deptId) return;
      this.loadingStaff = true;
      this.staffList = [];
      try {
        // 调用 staffAPI，传入 dept_id 参数
        const response = await api.staff.getHospitalStaffs({ dept_id: deptId });
        this.staffList = Array.isArray(response.data) ? response.data : (response.data.results || []);
      } catch (error) {
        console.error('加载科室人员失败:', error);
      } finally {
        this.loadingStaff = false;
      }
    },

    // 4. 保存修改
    async saveChanges() {
      if (!this.selectedResource) return;

      this.saving = true;
      try {
        const resourceId = this.selectedResource.dept_res_id;
        const payload = {
          bed_count: this.formData.bed_count,
          device_count: this.formData.device_count,
          daily_capacity: this.formData.daily_capacity,
          hospital: this.selectedResource.hospital,
          dept: this.selectedResource.dept
        };

        const response = await api.department.updateDepartmentResource(resourceId, payload);

        const index = this.resources.findIndex(r => r.dept_res_id === resourceId);
        if (index !== -1) {
          this.resources[index] = { ...this.resources[index], ...response.data };
          this.selectedResource = this.resources[index];
        }

        alert('科室资源更新成功！');
      } catch (error) {
        console.error('更新失败:', error);
        alert('保存失败，请重试。');
      } finally {
        this.saving = false;
      }
    }
  }
};
</script>

<style scoped>
.hospital-resources {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
  color: #333;
}

.page-header h1 {
  margin-bottom: 5px;
  color: #2c3e50;
}

.page-header p {
  color: #7f8c8d;
  margin-top: 0;
}

.resources-container {
  display: flex;
  gap: 20px;
  margin-top: 20px;
  height: calc(100vh - 150px);
}

/* 左侧面板 */
.departments-panel {
  flex: 1;
  min-width: 250px;
  max-width: 300px;
  background: #fff;
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  display: flex;
  flex-direction: column;
}

.panel-header {
  padding: 15px;
  border-bottom: 1px solid #eee;
  display: flex;
  justify-content: space-between;
  align-items: center;
  background-color: #f8f9fa;
  border-radius: 8px 8px 0 0;
}

.btn-refresh {
  border: 1px solid #ddd;
  background: white;
  border-radius: 4px;
  cursor: pointer;
}

.departments-list {
  list-style: none;
  padding: 0;
  margin: 0;
  overflow-y: auto;
  flex: 1;
}

.departments-list li {
  padding: 15px;
  border-bottom: 1px solid #f0f0f0;
  cursor: pointer;
  transition: background-color 0.2s;
}

.departments-list li:hover {
  background-color: #f5f7fa;
}

.departments-list li.active {
  background-color: #e6f7ff;
  border-left: 4px solid #1890ff;
}

.dept-name {
  font-weight: 600;
  margin-bottom: 4px;
}

.dept-summary {
  font-size: 12px;
  color: #888;
}

/* 右侧面板 */
.resources-panel {
  flex: 3;
  background: #fff;
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  display: flex;
  flex-direction: column;
}

.resources-content {
  padding: 20px;
  overflow-y: auto;
}

.form-info-banner {
  background-color: #e6f7ff;
  border: 1px solid #91d5ff;
  color: #0050b3;
  padding: 10px 15px;
  border-radius: 4px;
  margin-bottom: 20px;
}

.form-row {
  display: flex;
  gap: 20px;
  margin-bottom: 15px;
  align-items: flex-end;
}

.form-group {
  flex: 1;
}

.form-group label {
  display: block;
  margin-bottom: 6px;
  font-weight: 500;
  color: #2c3e50;
}

.form-group input {
  width: 100%;
  padding: 8px 10px;
  border: 1px solid #d9d9d9;
  border-radius: 4px;
  box-sizing: border-box;
}

.action-group {
  display: flex;
  justify-content: flex-end;
}

.btn-save {
  padding: 9px 20px;
  background-color: #1890ff;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-weight: 500;
}

.btn-save:hover {
  background-color: #40a9ff;
}

/* 医护人员表格部分 */
.staff-section {
  margin-top: 30px;
  border-top: 2px solid #f0f0f0;
  padding-top: 20px;
}

.staff-section h4 {
  margin-bottom: 15px;
  color: #333;
  font-size: 16px;
}

.staff-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 14px;
}

.staff-table th, .staff-table td {
  padding: 12px;
  text-align: left;
  border-bottom: 1px solid #eee;
}

.staff-table th {
  background-color: #fafafa;
  font-weight: 600;
  color: #555;
}

.tag {
  display: inline-block;
  padding: 2px 8px;
  border-radius: 12px;
  font-size: 12px;
}

.title-tag {
  background-color: #f6ffed;
  border: 1px solid #b7eb8f;
  color: #52c41a;
}

.type-tag {
  background-color: #e6f7ff;
  border: 1px solid #91d5ff;
  color: #1890ff;
}

.empty-staff, .loading-text {
  padding: 20px;
  text-align: center;
  color: #999;
  background-color: #fafafa;
  border-radius: 4px;
}

.no-selection {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #999;
  background: #fafafa;
}

.empty-state-content {
  text-align: center;
}

.icon-placeholder {
  font-size: 40px;
  display: block;
  margin-bottom: 10px;
}
</style>