<template>
  <div class="hospital-scores">
    <h1>医院评分上报</h1>
    <p>用于医院向市政府提交自评结果（检查结果、得分）</p>
    
    <div class="scores-header">
      <h3>评分记录</h3>
      <button @click="showAddScoreModal = true" class="add-btn">上报新评分</button>
    </div>
    
    <div class="scores-list">
      <div 
        v-for="score in scores" 
        :key="score.id" 
        class="score-card"
      >
        <h4>评分: {{ score.score }}/100</h4>
        <p><strong>检查日期:</strong> {{ formatDate(score.last_inspection_date) }}</p>
        <p><strong>检查内容:</strong> {{ score.inspection_content || '无' }}</p>
        <p><strong>备注:</strong> {{ score.remarks || '无' }}</p>
        <p><strong>上报时间:</strong> {{ formatDate(score.created_at) }}</p>
      </div>
      
      <div v-if="scores.length === 0" class="no-scores">
        暂无评分记录
      </div>
    </div>
    
    <!-- 上报新评分模态框 -->
    <div v-if="showAddScoreModal" class="modal-overlay" @click="showAddScoreModal = false">
      <div class="modal-content" @click.stop>
        <h3>上报新评分</h3>
        <form @submit.prevent="submitScore">
          <div class="form-group">
            <label>评分 (0-100):</label>
            <input 
              v-model.number="newScore.score" 
              type="number" 
              min="0" 
              max="100" 
              required 
            />
          </div>
          <div class="form-group">
            <label>检查日期:</label>
            <input v-model="newScore.last_inspection_date" type="date" required />
          </div>
          <div class="form-group">
            <label>检查内容:</label>
            <textarea 
              v-model="newScore.inspection_content" 
              rows="3"
              placeholder="请输入检查的具体内容..."
            ></textarea>
          </div>
          <div class="form-group">
            <label>备注:</label>
            <textarea 
              v-model="newScore.remarks" 
              rows="3"
              placeholder="请输入备注信息..."
            ></textarea>
          </div>
          <div class="form-actions">
            <button type="submit" class="submit-btn">上报评分</button>
            <button type="button" @click="showAddScoreModal = false" class="cancel-btn">取消</button>
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
  name: 'HospitalScoresView',
  data() {
    return {
      scores: [],
      showAddScoreModal: false,
      newScore: {
        score: 0,
        last_inspection_date: '',
        inspection_content: '',
        remarks: ''
      },
      authStore: useAuthStore()
    };
  },
  async created() {
    await this.loadScores();
  },
  methods: {
    async loadScores() {
      try {
        // In a real app, we would get the hospital ID from the authenticated user's profile
        const hospitalId = this.authStore.user?.hospital_id || 1;
        const response = await api.score.getScores({ hospital: hospitalId });
        this.scores = response.data.data;
      } catch (error) {
        console.error('Error loading scores:', error);
      }
    },
    async submitScore() {
      try {
        // In a real app, we would get the hospital ID from the authenticated user's profile
        const hospitalId = this.authStore.user?.hospital_id || 1;
        
        await api.score.createScore({
          ...this.newScore,
          hospital: hospitalId
        });
        
        await this.loadScores();
        this.resetScoreForm();
        this.showAddScoreModal = false;
      } catch (error) {
        console.error('Error submitting score:', error);
        // In a real app, show user-friendly error message
      }
    },
    resetScoreForm() {
      this.newScore = {
        score: 0,
        last_inspection_date: '',
        inspection_content: '',
        remarks: ''
      };
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
.hospital-scores {
  max-width: 1000px;
  margin: 0 auto;
  padding: 20px;
}

.scores-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.add-btn, .submit-btn, .cancel-btn {
  padding: 8px 16px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  text-decoration: none;
  display: inline-block;
}

.add-btn, .submit-btn {
  background-color: #007bff;
  color: white;
}

.cancel-btn {
  background-color: #6c757d;
  color: white;
  margin-left: 10px;
}

.scores-list {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 20px;
}

.score-card {
  border: 1px solid #ddd;
  border-radius: 8px;
  padding: 15px;
  background: white;
}

.score-card h4 {
  margin-top: 0;
  color: #007bff;
}

.no-scores {
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