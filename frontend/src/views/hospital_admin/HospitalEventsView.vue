<template>
  <div class="hospital-events">
    <h1>突发事件响应中心</h1>
    <p>医院用于上报/参与突发事件</p>
    
    <div class="events-tabs">
      <button 
        :class="{ active: activeTab === 'all-events' }"
        @click="activeTab = 'all-events'"
      >
        全部突发事件列表
      </button>
      <button 
        :class="{ active: activeTab === 'my-events' }"
        @click="activeTab = 'my-events'"
      >
        本院参与的事件
      </button>
    </div>
    
    <!-- 全部事件标签页 -->
    <div v-if="activeTab === 'all-events'" class="tab-content">
      <div class="events-header">
        <h3>全部突发事件</h3>
      </div>
      
      <div class="events-list">
        <div 
          v-for="event in allEvents" 
          :key="event.id" 
          class="event-card"
        >
          <h4>{{ event.title }}</h4>
          <p><strong>类型:</strong> {{ event.event_type || '未分类' }}</p>
          <p><strong>发生时间:</strong> {{ formatDate(event.occurrence_time) }}</p>
          <p><strong>状态:</strong> {{ event.status || '进行中' }}</p>
          <p><strong>描述:</strong> {{ event.description || '暂无描述' }}</p>
          
          <div class="event-actions">
            <button 
              v-if="!isEventParticipated(event.id)" 
              @click="participateInEvent(event)"
              class="participate-btn"
            >
              参与事件
            </button>
            <span v-else class="participated">已参与</span>
          </div>
        </div>
        
        <div v-if="allEvents.length === 0" class="no-events">
          暂无突发事件
        </div>
      </div>
    </div>
    
    <!-- 本院参与的事件标签页 -->
    <div v-if="activeTab === 'my-events'" class="tab-content">
      <div class="my-events-header">
        <h3>本院参与的事件</h3>
      </div>
      
      <div class="my-events-list">
        <div 
          v-for="hospitalEvent in myEvents" 
          :key="hospitalEvent.id" 
          class="my-event-card"
        >
          <h4>{{ hospitalEvent.event?.title || hospitalEvent.event_title }}</h4>
          <p><strong>类型:</strong> {{ hospitalEvent.event?.event_type || hospitalEvent.event_type || '未分类' }}</p>
          <p><strong>发生时间:</strong> {{ formatDate(hospitalEvent.event?.occurrence_time) }}</p>
          <p><strong>参与时间:</strong> {{ formatDate(hospitalEvent.participation_date) }}</p>
          <p><strong>处理进度:</strong> {{ hospitalEvent.progress_status || '未开始' }}</p>
          <p><strong>备注:</strong> {{ hospitalEvent.notes || '无' }}</p>
          
          <div class="event-actions">
            <button @click="updateEventProgress(hospitalEvent)" class="update-btn">
              更新进度
            </button>
            <button @click="removeParticipation(hospitalEvent.id)" class="remove-btn">
              退出参与
            </button>
          </div>
        </div>
        
        <div v-if="myEvents.length === 0" class="no-events">
          本院暂未参与任何突发事件
        </div>
      </div>
    </div>
    
    <!-- 更新进度模态框 -->
    <div v-if="showUpdateModal" class="modal-overlay" @click="showUpdateModal = false">
      <div class="modal-content" @click.stop>
        <h3>更新事件进度</h3>
        <form @submit.prevent="confirmUpdateProgress">
          <div class="form-group">
            <label>处理进度:</label>
            <select v-model="updateData.progress_status" required>
              <option value="planning">计划中</option>
              <option value="in_progress">进行中</option>
              <option value="completed">已完成</option>
              <option value="cancelled">已取消</option>
            </select>
          </div>
          <div class="form-group">
            <label>备注:</label>
            <textarea 
              v-model="updateData.notes" 
              rows="4"
              placeholder="请输入处理情况备注..."
            ></textarea>
          </div>
          <div class="form-actions">
            <button type="submit" class="save-btn">更新</button>
            <button type="button" @click="showUpdateModal = false" class="cancel-btn">取消</button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
import api from '@/services/api';
import { useAuthStore } from '@/stores/auth';

export default {
  name: 'HospitalEventsView',
  data() {
    return {
      activeTab: 'all-events',
      allEvents: [],
      myEvents: [],
      showUpdateModal: false,
      currentEventId: null,
      updateData: {
        progress_status: '',
        notes: ''
      },
      authStore: useAuthStore()
    };
  },
  async created() {
    await this.loadData();
  },
  methods: {
    async loadData() {
      await this.loadAllEvents();
      await this.loadMyEvents();
    },
    async loadAllEvents() {
      try {
        const response = await api.event.getAllEvents();
        this.allEvents = response.data.data;
      } catch (error) {
        console.error('Error loading all events:', error);
      }
    },
    async loadMyEvents() {
      try {
        // In a real app, we would get the hospital ID from the authenticated user's profile
        const hospitalId = this.authStore.user?.hospital_id || 1;
        const response = await api.event.getHospitalEvents({ hospital: hospitalId });
        this.myEvents = response.data.data;
      } catch (error) {
        console.error('Error loading my events:', error);
      }
    },
    isEventParticipated(eventId) {
      return this.myEvents.some(he => he.event?.id === eventId);
    },
    async participateInEvent(event) {
      try {
        // In a real app, we would get the hospital ID from the authenticated user's profile
        const hospitalId = this.authStore.user?.hospital_id || 1;
        
        await api.event.createHospitalEvent({
          event: event.id,
          hospital: hospitalId,
          participation_date: new Date().toISOString().split('T')[0],
          progress_status: 'planning'
        });
        
        // Refresh the list
        await this.loadMyEvents();
        await this.loadAllEvents(); // To update the participated status
      } catch (error) {
        console.error('Error participating in event:', error);
        // In a real app, show user-friendly error message
      }
    },
    updateEventProgress(hospitalEvent) {
      this.currentEventId = hospitalEvent.id;
      this.updateData.progress_status = hospitalEvent.progress_status || 'planning';
      this.updateData.notes = hospitalEvent.notes || '';
      this.showUpdateModal = true;
    },
    async confirmUpdateProgress() {
      try {
        await api.event.updateHospitalEvent(this.currentEventId, {
          progress_status: this.updateData.progress_status,
          notes: this.updateData.notes
        });
        
        // Refresh the list
        await this.loadMyEvents();
        this.showUpdateModal = false;
      } catch (error) {
        console.error('Error updating event progress:', error);
        // In a real app, show user-friendly error message
      }
    },
    async removeParticipation(eventId) {
      if (confirm('确定要退出参与此事件吗？')) {
        try {
          await api.event.deleteHospitalEvent(eventId); // Note: API doesn't have deleteHospitalEvent in our service
          await this.loadMyEvents();
          await this.loadAllEvents(); // To update the participated status
        } catch (error) {
          console.error('Error removing participation:', error);
        }
      }
    },
    formatDate(dateString) {
      if (!dateString) return '未设置';
      const date = new Date(dateString);
      return date.toLocaleDateString('zh-CN');
    }
  }
};
</script>

<style scoped>
.hospital-events {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

.events-tabs {
  display: flex;
  margin-bottom: 20px;
}

.events-tabs button {
  padding: 10px 20px;
  border: 1px solid #ddd;
  background: #f8f9fa;
  cursor: pointer;
  border-radius: 4px 4px 0 0;
  margin-right: 5px;
}

.events-tabs button.active {
  background: #007bff;
  color: white;
  border-color: #007bff;
}

.tab-content {
  background: #f8f9fa;
  padding: 20px;
  border-radius: 0 4px 4px 4px;
}

.events-header, .my-events-header {
  margin-bottom: 20px;
}

.event-card, .my-event-card {
  border: 1px solid #ddd;
  border-radius: 8px;
  padding: 15px;
  margin-bottom: 15px;
  background: white;
}

.event-card h4, .my-event-card h4 {
  margin-top: 0;
  color: #007bff;
}

.event-actions {
  margin-top: 15px;
  text-align: right;
}

.participate-btn, .update-btn, .remove-btn, .save-btn, .cancel-btn {
  padding: 6px 12px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  margin-left: 10px;
  text-decoration: none;
  display: inline-block;
}

.participate-btn, .save-btn {
  background-color: #007bff;
  color: white;
}

.update-btn {
  background-color: #28a745;
  color: white;
}

.remove-btn, .cancel-btn {
  background-color: #dc3545;
  color: white;
}

.participated {
  color: #28a745;
  font-weight: bold;
}

.no-events {
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