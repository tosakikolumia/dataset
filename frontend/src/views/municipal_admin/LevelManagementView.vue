<template>
  <div class="level-management">
    <h1>等级设置管理</h1>
    <p>管理医院等级库</p>
    
    <div class="management-header">
      <h3>医院等级列表</h3>
      <button @click="showAddLevelModal = true" class="add-btn">新增等级</button>
    </div>
    
    <div class="levels-table">
      <table>
        <thead>
          <tr>
            <th>等级名称</th>
            <th>描述</th>
            <th>创建时间</th>
            <th>操作</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="level in levels" :key="level.id">
            <td>{{ level.name }}</td>
            <td>{{ level.description || '无描述' }}</td>
            <td>{{ formatDate(level.created_at) }}</td>
            <td>
              <button @click="editLevel(level)" class="edit-btn">编辑</button>
              <button @click="deleteLevel(level.id)" class="delete-btn">删除</button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
    
    <!-- 添加/编辑等级模态框 -->
    <div v-if="showAddLevelModal" class="modal-overlay" @click="showAddLevelModal = false">
      <div class="modal-content" @click.stop>
        <h3>{{ editingLevel ? '编辑等级' : '新增等级' }}</h3>
        <form @submit.prevent="saveLevel">
          <div class="form-group">
            <label>等级名称:</label>
            <input v-model="currentLevel.name" type="text" required />
          </div>
          <div class="form-group">
            <label>描述:</label>
            <textarea 
              v-model="currentLevel.description" 
              rows="3"
              placeholder="请输入等级描述..."
            ></textarea>
          </div>
          <div class="form-actions">
            <button type="submit" class="save-btn">
              {{ editingLevel ? '更新' : '添加' }}
            </button>
            <button type="button" @click="cancelEdit" class="cancel-btn">取消</button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
import api from '@/services/api';

export default {
  name: 'LevelManagementView',
  data() {
    return {
      levels: [],
      showAddLevelModal: false,
      editingLevel: false,
      currentLevel: {
        id: null,
        name: '',
        description: ''
      }
    };
  },
  async created() {
    await this.loadLevels();
  },
  methods: {
    async loadLevels() {
      try {
        const response = await api.hospitalLevel.getAllLevels();
        this.levels = response.data.data;
      } catch (error) {
        console.error('Error loading levels:', error);
      }
    },
    editLevel(level) {
      this.editingLevel = true;
      this.currentLevel = { ...level };
      this.showAddLevelModal = true;
    },
    async saveLevel() {
      try {
        if (this.editingLevel) {
          await api.hospitalLevel.updateLevel(this.currentLevel.id, this.currentLevel);
        } else {
          await api.hospitalLevel.createLevel(this.currentLevel);
        }
        
        await this.loadLevels();
        this.cancelEdit();
      } catch (error) {
        console.error('Error saving level:', error);
        // In a real app, show user-friendly error message
      }
    },
    async deleteLevel(id) {
      if (confirm('确定要删除这个等级吗？删除后将影响所有使用此等级的医院！')) {
        try {
          await api.hospitalLevel.deleteLevel(id);
          await this.loadLevels();
        } catch (error) {
          console.error('Error deleting level:', error);
        }
      }
    },
    cancelEdit() {
      this.showAddLevelModal = false;
      this.editingLevel = false;
      this.resetLevelForm();
    },
    resetLevelForm() {
      this.currentLevel = {
        id: null,
        name: '',
        description: ''
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
.level-management {
  max-width: 1000px;
  margin: 0 auto;
  padding: 20px;
}

.management-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.add-btn, .edit-btn, .delete-btn, .save-btn, .cancel-btn {
  padding: 6px 12px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  text-decoration: none;
  display: inline-block;
}

.add-btn, .save-btn {
  background-color: #007bff;
  color: white;
}

.edit-btn {
  background-color: #ffc107;
  color: #212529;
}

.delete-btn, .cancel-btn {
  background-color: #dc3545;
  color: white;
  margin-left: 10px;
}

.levels-table {
  overflow-x: auto;
}

table {
  width: 100%;
  border-collapse: collapse;
}

th, td {
  padding: 12px;
  text-align: left;
  border-bottom: 1px solid #ddd;
}

th {
  background-color: #f8f9fa;
  font-weight: bold;
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