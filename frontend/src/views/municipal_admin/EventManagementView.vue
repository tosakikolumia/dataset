<template>
  <div class="event-management">
    <h1>突发事件管理</h1>
    <p>市政管理员可新建突发事件，查看所有事件处理情况</p>
    
    <div class="management-header">
      <h3>突发事件列表</h3>
      <button @click="showAddEventModal = true" class="add-btn">新建突发事件</button>
    </div>
    
    <div class="events-list">
      <div 
        v-for="event in events" 
        :key="event.id" 
        class="event-card"
      >
        <h3>{{ event.title }}</h3>
        <div class="event-details">
          <p><strong>类型:</strong> {{ event.event_type || '未分类' }}</p>
          <p><strong>发生时间:</strong> {{ formatDate(event.occurrence_time) }}</p>
          <p><strong>状态:</strong> 
            <span :class="'status-' + (event.status || 'unknown')">
              {{ event.status || '未知' }}
            </span>
          </p>
          <p><strong>描述:</strong> {{ event.description || '暂无描述' }}</p>
        </div>
        
        <div class="event-hospital-stats">
          <h4>参与医院统计</h4>
          <p>共有 {{ getHospitalCountForEvent(event.id) }} 家医院参与</p>
        </div>
      </div>
      
      <div v-if="events.length === 0" class="no-events">
        暂无突发事件
      </div>
    </div>
    
    <!-- 新建事件模态框 -->
    <div v-if="showAddEventModal" class="modal-overlay" @click="showAddEventModal = false">
      <div class="modal-content" @click.stop>
        <h3>新建突发事件</h3>
        <form @submit.prevent="createEvent">
          <div class="form-group">
            <label>事件标题:</label>
            <input v-model="newEvent.title" type="text" required />
          </div>
          <div class="form-group">
            <label>事件类型:</label>
            <select v-model="newEvent.event_type">
              <option value="epidemic">疫情</option>
              <option value="accident">事故灾难</option>
              <option value="public_health">公共卫生</option>
              <option value="social_security">社会安全</option>
              <option value="other">其他</option>
            </select>
          </div>
          <div class="form-group">
            <label>发生时间:</label>
            <input v-model="newEvent.occurrence_time" type="datetime-local" />
          </div>
          <div class="form-group">
            <label>事件状态:</label>
            <select v-model="newEvent.status">
              <option value="active">进行中</option>
              <option value="resolved">已解决</option>
              <option value="closed">已关闭</option>
            </select>
          </div>
          <div class="form-group">
            <label>事件描述:</label>
            <textarea 
              v-model="newEvent.description" 
              rows="4"
              placeholder="请输入事件详细描述..."
            ></textarea>
          </div>
          <div class="form-actions">
            <button type="submit" class="create-btn">创建事件</button>
            <button type="button" @click="cancelAdd" class="cancel-btn">取消</button>
          </div>
        </form>
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
      events: [],
      hospitalEvents: [],
      showAddEventModal: false,
      newEvent: {
        title: '',
        event_type: 'other',
        occurrence_time: '',
        status: 'active',
        description: ''
      }
    };
  },
  async created() {
    await this.loadData();
  },
  methods: {
    async loadData() {
      await Promise.all([
        this.loadEvents(),
        this.loadHospitalEvents()
      ]);
    },
    async loadEvents() {
      try {
        const response = await api.event.getAllEvents();
        this.events = response.data.data;
      } catch (error) {
        console.error('Error loading events:', error);
      }
    },
    async loadHospitalEvents() {
      try {
        const response = await api.event.getHospitalEvents({});
        this.hospitalEvents = response.data.data;
      } catch (error) {
        console.error('Error loading hospital events:', error);
      }
    },
    async createEvent() {
      try {
        await api.event.createEvent(this.newEvent);
        await this.loadEvents();
        this.cancelAdd();
      } catch (error) {
        console.error('Error creating event:', error);
        // In a real app, show user-friendly error message
      }
    },
    getHospitalCountForEvent(eventId) {
      return this.hospitalEvents.filter(he => he.event?.id === eventId).length;
    },
    cancelAdd() {
      this.showAddEventModal = false;
      this.newEvent = {
        title: '',
        event_type: 'other',
        occurrence_time: '',
        status: 'active',
        description: ''
      };
    },
    formatDate(dateString) {
      if (!dateString) return '未设置';
      const date = new Date(dateString);
      return date.toLocaleString('zh-CN');
    }
  }
};
</script>

<style scoped>
.event-management {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

.management-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.add-btn, .create-btn, .cancel-btn {
  padding: 8px 16px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  text-decoration: none;
  display: inline-block;
}

.add-btn, .create-btn {
  background-color: #007bff;
  color: white;
}

.cancel-btn {
  background-color: #6c757d;
  color: white;
  margin-left: 10px;
}

.events-list {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
  gap: 20px;
}

.event-card {
  border: 1px solid #ddd;
  border-radius: 8px;
  padding: 15px;
  background: white;
}

.event-card h3 {
  margin-top: 0;
  color: #007bff;
  border-bottom: 1px solid #eee;
  padding-bottom: 10px;
}

.event-details p {
  margin: 8px 0;
}

.status-active {
  color: #28a745;
  font-weight: bold;
}

.status-resolved {
  color: #17a2b8;
  font-weight: bold;
}

.status-closed {
  color: #6c757d;
  font-weight: bold;
}

.event-hospital-stats {
  margin-top: 15px;
  padding-top: 15px;
  border-top: 1px solid #eee;
}

.event-hospital-stats h4 {
  margin: 0 0 10px 0;
  color: #495057;
}

.no-events {
  grid-column: 1 / -1;
  text-align: center;
  padding: 40px;
  color: #666;
}

.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.modal-content {
  background: white;
  padding: 20px;
  border-radius: 8px;
  width: 500px;
  max-width: 90%;
}

.form-group {
  margin-bottom: 15px;
}

.form-group label {
  display: block;
  margin-bottom: 5px;
  font-weight: bold;
}

.form-group input,
.form-group select,
.form-group textarea {
  width: 100%;
  padding: 8px 12px;
  border: 1px solid #ddd;
  border-radius: 4px;
  box-sizing: border-box;
}

.form-actions {
  text-align: right;
  margin-top: 20px;
}
</style>