<template>
  <div class="event-management">
    <h1>突发事件管理</h1>
    <p>管理市政突发事件，指派主责医院及协同单位。</p>

    <div class="management-header">
      <div class="filters">
        <label>筛选参与医院:</label>
        <select v-model="filterHospitalId" @change="loadEvents">
          <option value="">全部医院</option>
          <option v-for="h in hospitals" :key="h.hospital_id" :value="h.hospital_id">
            {{ h.name }}
          </option>
        </select>
      </div>
      <button @click="openAddModal" class="add-btn">➕ 新建突发事件</button>
    </div>

    <div class="events-list">
      <div v-if="loading" class="loading">加载中...</div>

      <div
        v-else
        v-for="event in events"
        :key="event.event_id"
        class="event-card"
        @click="showEventDetails(event)"
      >
        <div class="card-header">
          <h3>{{ event.event_type || '未命名事件' }}</h3>
          <span :class="['severity-badge', getSeverityClass(event.severity)]">
            {{ event.severity }}
          </span>
        </div>

        <div class="event-details">
          <p><strong>上报时间:</strong> {{ formatDate(event.report_time) }}</p>
          <p><strong>参与医院:</strong> {{ event.participating_hospitals ? event.participating_hospitals.length : 0 }} 家</p>
        </div>

        <div class="card-actions">
          <button class="view-btn">查看详情</button>
        </div>
      </div>

      <div v-if="!loading && events.length === 0" class="no-events">
        暂无相关突发事件
      </div>
    </div>

    <div v-if="showAddEventModal" class="modal-overlay" @click.self="showAddEventModal = false">
      <div class="modal-content large-modal">
        <h3>🚨 新建突发事件</h3>
        <form @submit.prevent="createEvent">
          <div class="form-row">
            <div class="form-group">
              <label>事件类型/标题:</label>
              <input v-model="newEvent.event_type" type="text" placeholder="例如：流感爆发、交通事故" required />
            </div>
            <div class="form-group">
              <label>严重程度:</label>
              <select v-model="newEvent.severity">
                <option value="一般">一般 (IV级)</option>
                <option value="较大">较大 (III级)</option>
                <option value="重大">重大 (II级)</option>
                <option value="特别重大">特别重大 (I级)</option>
              </select>
            </div>
          </div>

          <div class="form-group">
            <label>发生时间:</label>
            <input v-model="newEvent.report_time" type="datetime-local" required />
          </div>

          <div class="participants-section">
            <div class="section-header">
              <label>参与医院及角色:</label>
              <button type="button" @click="addParticipantRow" class="small-btn">+ 添加医院</button>
            </div>

            <div v-for="(item, index) in newEvent.participants" :key="index" class="participant-row">
              <select v-model="item.hospital_id" required>
                <option value="" disabled>选择医院</option>
                <option v-for="h in hospitals" :key="h.hospital_id" :value="h.hospital_id">
                  {{ h.name }}
                </option>
              </select>

              <select v-model="item.role" required>
                <option value="primary">主责医院</option>
                <option value="support">支援医院</option>
                <option value="reporting">报告医院</option>
                <option value="transfer">转诊医院</option>
                <option value="screening">排查医院</option>
              </select>

              <button type="button" @click="removeParticipantRow(index)" class="del-btn" v-if="newEvent.participants.length > 1">×</button>
            </div>
          </div>

          <div class="form-actions">
            <button type="button" @click="showAddEventModal = false" class="cancel-btn">取消</button>
            <button type="submit" class="create-btn">立即发布</button>
          </div>
        </form>
      </div>
    </div>

    <div v-if="selectedEvent" class="modal-overlay" @click.self="selectedEvent = null">
      <div class="modal-content">
        <h3>{{ selectedEvent.event_type }} - 详细信息</h3>
        <p class="meta-info">发生时间: {{ formatDate(selectedEvent.report_time) }}</p>
        <p class="meta-info">严重程度: {{ selectedEvent.severity }}</p>

        <h4>🏥 参与医院列表</h4>
        <table class="detail-table">
          <thead>
            <tr>
              <th>医院名称</th>
              <th>承担角色</th>
              <th>响应时间</th>
              <th>接诊人数</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="ph in selectedEvent.participating_hospitals" :key="ph.id">
              <td>{{ ph.hospital_name }}</td>
              <td>
                <span :class="['role-tag', ph.role]">{{ ph.role_display }}</span>
              </td>
              <td>{{ formatDate(ph.response_time) || '-' }}</td>
              <td>{{ ph.affected_patient_count || 0 }}</td>
            </tr>
            <tr v-if="!selectedEvent.participating_hospitals?.length">
              <td colspan="4" style="text-align:center; color:#999;">暂无医院参与记录</td>
            </tr>
          </tbody>
        </table>

        <div class="form-actions">
          <button @click="selectedEvent = null" class="create-btn">关闭</button>
        </div>
      </div>
    </div>

  </div>
</template>

<script>
import api from '@/services/api';

export default {
  name: 'EventManagementView',
  data() {
    return {
      loading: false,
      events: [],
      hospitals: [],
      filterHospitalId: '',
      showAddEventModal: false,
      selectedEvent: null,

      // 新建表单数据
      newEvent: {
        event_type: '',
        severity: '一般',
        report_time: '',
        participants: [
          { hospital_id: '', role: 'primary' }
        ]
      }
    };
  },
  async created() {
    // 页面加载时获取数据
    await this.fetchHospitals();
    await this.loadEvents();
  },
  methods: {
    async fetchHospitals() {
      try {
        // ✅ 修正：使用 api.hospital.getAllHospitals()
        const res = await api.hospital.getAllHospitals();
        this.hospitals = res.data;
      } catch (err) {
        console.error("获取医院列表失败", err);
      }
    },
    async loadEvents() {
      this.loading = true;
      try {
        const params = {};
        if (this.filterHospitalId) {
          params.hospital_id = this.filterHospitalId;
        }
        // ✅ 修正：使用 api.event.getAllEvents(params)
        // 注意：先确保按上面第1步修改了 api.js 支持传参
        const res = await api.event.getAllEvents(params);
        this.events = res.data;
      } catch (err) {
        console.error("加载事件失败", err);
      } finally {
        this.loading = false;
      }
    },
    openAddModal() {
      this.newEvent = {
        event_type: '',
        severity: '一般',
        report_time: new Date().toISOString().slice(0, 16),
        participants: [{ hospital_id: '', role: 'primary' }]
      };
      this.showAddEventModal = true;
    },
    addParticipantRow() {
      this.newEvent.participants.push({ hospital_id: '', role: 'support' });
    },
    removeParticipantRow(index) {
      this.newEvent.participants.splice(index, 1);
    },
    async createEvent() {
      if (!this.newEvent.event_type) return alert("请填写事件类型");

      const validParticipants = this.newEvent.participants.filter(p => p.hospital_id);

      const payload = {
        event_type: this.newEvent.event_type,
        severity: this.newEvent.severity,
        report_time: this.newEvent.report_time,
        participants: validParticipants
      };

      try {
        // ✅ 修正：使用 api.event.createEvent(payload)
        await api.event.createEvent(payload);
        this.showAddEventModal = false;
        await this.loadEvents();
        alert("事件创建成功");
      } catch (err) {
        console.error("创建失败", err);
        alert("创建失败，请检查网络或输入");
      }
    },
    showEventDetails(event) {
      this.selectedEvent = event;
    },
    formatDate(str) {
      if (!str) return '';
      return new Date(str).toLocaleString('zh-CN', { hour12: false });
    },
    getSeverityClass(severity) {
      const map = {
        '一般': 'sev-low',
        '较大': 'sev-mid',
        '重大': 'sev-high',
        '特别重大': 'sev-critical'
      };
      return map[severity] || '';
    }
  }
};
</script>

<style scoped>
.event-management {
  padding: 20px;
  background-color: #f5f7fa;
  min-height: 100vh;
}

.management-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  background: white;
  padding: 15px;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.05);
}

.filters select {
  padding: 8px;
  border: 1px solid #ddd;
  border-radius: 4px;
  margin-left: 10px;
}

.add-btn {
  background-color: #3498db;
  color: white;
  border: none;
  padding: 10px 20px;
  border-radius: 4px;
  cursor: pointer;
  font-weight: bold;
}

.events-list {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 20px;
}

.event-card {
  background: white;
  border-radius: 8px;
  padding: 15px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.05);
  cursor: pointer;
  transition: transform 0.2s;
  border-left: 4px solid #3498db;
}

.event-card:hover {
  transform: translateY(-3px);
  box-shadow: 0 5px 15px rgba(0,0,0,0.1);
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10px;
  border-bottom: 1px solid #eee;
  padding-bottom: 8px;
}

.card-header h3 {
  margin: 0;
  font-size: 1.1em;
  color: #2c3e50;
}

.severity-badge {
  font-size: 0.8em;
  padding: 2px 6px;
  border-radius: 4px;
  color: white;
  background: #95a5a6;
}
.sev-low { background: #27ae60; }
.sev-mid { background: #f39c12; }
.sev-high { background: #e67e22; }
.sev-critical { background: #c0392b; }

.event-details p {
  margin: 5px 0;
  color: #666;
  font-size: 0.9em;
}

.card-actions {
  margin-top: 15px;
  text-align: right;
}

.view-btn {
  background: none;
  border: 1px solid #3498db;
  color: #3498db;
  padding: 4px 10px;
  border-radius: 4px;
  cursor: pointer;
}

/* Modal Styles */
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
  padding: 25px;
  border-radius: 8px;
  width: 500px;
  max-width: 90%;
  max-height: 90vh;
  overflow-y: auto;
}

.large-modal {
  width: 700px;
}

.form-row {
  display: flex;
  gap: 15px;
}
.form-row .form-group {
  flex: 1;
}

.form-group {
  margin-bottom: 15px;
}
.form-group label {
  display: block;
  margin-bottom: 5px;
  font-weight: bold;
}
.form-group input, .form-group select {
  width: 100%;
  padding: 8px;
  border: 1px solid #ddd;
  border-radius: 4px;
  box-sizing: border-box;
}

.participants-section {
  background: #f8f9fa;
  padding: 10px;
  border-radius: 4px;
  margin-bottom: 15px;
}

.section-header {
  display: flex;
  justify-content: space-between;
  margin-bottom: 10px;
}

.participant-row {
  display: flex;
  gap: 10px;
  margin-bottom: 8px;
}
.participant-row select {
  flex: 1;
}

.small-btn {
  padding: 2px 8px;
  font-size: 0.8em;
  background: #2ecc71;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.del-btn {
  background: #e74c3c;
  color: white;
  border: none;
  width: 30px;
  border-radius: 4px;
  cursor: pointer;
}

.detail-table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 10px;
}
.detail-table th, .detail-table td {
  padding: 10px;
  border-bottom: 1px solid #eee;
  text-align: left;
}
.detail-table th {
  background-color: #f8f9fa;
}

.role-tag {
  display: inline-block;
  padding: 2px 6px;
  border-radius: 4px;
  font-size: 0.85em;
  background: #eee;
}
.role-tag.primary { background: #e74c3c; color: white; } /* 主责：红 */
.role-tag.support { background: #3498db; color: white; } /* 支援：蓝 */
.role-tag.reporting { background: #95a5a6; color: white; } /* 报告：灰 */
.role-tag.transfer { background: #f1c40f; color: white; } /* 转诊：黄 */
.role-tag.screening { background: #9b59b6; color: white; } /* 排查：紫 */

.form-actions {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
  margin-top: 20px;
}
.cancel-btn {
  padding: 8px 16px;
  background: #ccc;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}
.create-btn {
  padding: 8px 16px;
  background: #3498db;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}
</style>