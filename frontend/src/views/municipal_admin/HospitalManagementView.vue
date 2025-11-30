<template>
  <div class="hospital-management">
    <h1>医院管理</h1>
    <p>市政管理员可对医院进行增删改操作</p>
    
    <div class="management-header">
      <h3>医院列表</h3>
      <button @click="showAddHospitalModal = true" class="add-btn">新增医院</button>
    </div>
    
    <div class="hospitals-table">
      <table>
        <thead>
          <tr>
            <th>医院名称</th>
            <th>地址</th>
            <th>电话</th>
            <th>等级</th>
            <th>成立时间</th>
            <th>操作</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="hospital in hospitals" :key="hospital.hospital_id">
            <td>{{ hospital.name }}</td>
            <td>{{ hospital.address }}</td>
            <td>{{ hospital.phone || '未设置' }}</td>
            <td>{{ hospital.level?.level_name || hospital.level_name || '未设置' }}</td>
            <td>{{ formatDate(hospital.established_year) }}</td> <td>
              <button @click="editHospital(hospital)" class="edit-btn">编辑</button>
              <button @click="deleteHospital(hospital.hospital_id)" class="delete-btn">删除</button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <div v-if="showAddHospitalModal" class="modal-overlay" @click="showAddHospitalModal = false">
      <div class="modal-content" @click.stop>
        <h3>{{ editingHospital ? '编辑医院' : '新增医院' }}</h3>
        <form @submit.prevent="saveHospital">
          <div class="form-group">
            <label>医院名称:</label>
            <input v-model="currentHospital.name" type="text" required />
          </div>
          <div class="form-group">
            <label>行政区:</label>
            <select v-model="currentHospital.district_id" required>
              <option value="">请选择行政区</option>
              <option v-for="dist in districts" :key="dist.district_id" :value="dist.district_id">
                {{ dist.district_name }}
              </option>
            </select>
          </div>
          <div class="form-group">
            <label>地址:</label>
            <input v-model="currentHospital.address" type="text" required />
          </div>
          <div class="form-group">
            <label>电话:</label>
            <input v-model="currentHospital.phone" type="text" />
          </div>

          <div class="form-group">
            <label>成立年份:</label>
            <input v-model="currentHospital.established_year" type="number" placeholder="例如: 1990" />
          </div>

          <div class="form-group">
            <label>医院等级:</label>
            <select v-model="currentHospital.level_id">
              <option value="">请选择等级</option>
              <option v-for="level in hospitalLevels" :key="level.level_id" :value="level.level_id">
                {{ level.level_name }}
              </option>
            </select>
          </div>
          <div class="form-group">
            <label>总床位数:</label>
            <input v-model.number="currentHospital.bed_total" type="number" />
          </div>
          <div class="form-group">
            <label>日门诊量:</label>
            <input v-model.number="currentHospital.outpatient_capacity" type="number" />
          </div>

          <div class="form-actions">
            <button type="submit" class="save-btn">
              {{ editingHospital ? '更新' : '添加' }}
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
  name: 'HospitalManagementView',
  data() {
    return {
      hospitals: [],
      hospitalLevels: [],
      showAddHospitalModal: false,
      editingHospital: false,
      districts: [],
      currentHospital: {
        hospital_id: null, // 👇 修改点 4: 改名
        name: '',
        district_id: null,
        address: '',
        phone: '',
        established_year: null, // 👇 修改点 5: 对齐后端字段
        level_id: null,
        bed_total: null,        // 👇 修改点 6: 对齐后端字段
        outpatient_capacity: null // 👇 修改点 7: 对齐后端字段
      }
    };
  },
  async created() {
    await this.loadData();
  },
  methods: {
    async loadData() {
      await this.loadHospitals();
      await this.loadHospitalLevels();
      await this.loadDistricts();
    },
    async loadDistricts() {
      try {
        const response = await api.district.getAllDistricts();
        this.districts = response.data.data || response.data;
      } catch (error) {
        console.error('Error loading districts:', error);
      }
    },
    async loadHospitals() {
      try {
        const response = await api.hospital.getAllHospitals();
        // 处理后端返回格式，可能是 response.data.data 或者 response.data
        this.hospitals = response.data.data || response.data;
      } catch (error) {
        console.error('Error loading hospitals:', error);
      }
    },
    async loadHospitalLevels() {
      try {
        const response = await api.hospitalLevel.getAllLevels();
        this.hospitalLevels = response.data.data || response.data;
      } catch (error) {
        console.error('Error loading hospital levels:', error);
      }
    },
    editHospital(hospital) {
      this.editingHospital = true;
      // 复制对象，确保字段名对齐
      this.currentHospital = {
        ...hospital,
        // 如果后端返回的 level 是对象，提取 id
        level_id: hospital.level ? hospital.level.level_id : hospital.level_id,
        district_id: hospital.district ? hospital.district.district_id : hospital.district_id
      };
      this.showAddHospitalModal = true;
    },
    async saveHospital() {
      try {
        if (this.editingHospital) {
          // 👇 修改点 8: 使用 hospital_id
          await api.hospital.updateHospital(this.currentHospital.hospital_id, this.currentHospital);
        } else {
          await api.hospital.createHospital(this.currentHospital);
        }

        await this.loadHospitals();
        this.cancelEdit();
      } catch (error) {
        console.error('Error saving hospital:', error);
        alert("保存失败，请检查数据格式或权限");
      }
    },
    async deleteHospital(id) {
      if (confirm('确定要删除这个医院吗？删除后将无法恢复！')) {
        try {
          await api.hospital.deleteHospital(id);
          await this.loadHospitals();
        } catch (error) {
          console.error('Error deleting hospital:', error);
          alert("删除失败");
        }
      }
    },
    cancelEdit() {
      this.showAddHospitalModal = false;
      this.editingHospital = false;
      this.resetHospitalForm();
    },
    resetHospitalForm() {
      this.currentHospital = {
        hospital_id: null,
        name: '',
        district_id: null,
        address: '',
        phone: '',
        established_year: null,
        level_id: null,
        bed_total: null,
        outpatient_capacity: null
      };
    },
    formatDate(year) {
      if (!year) return '未设置';
      return year + '年';
    }
  }
};
</script>

<style scoped>
/* 样式保持不变 */
.hospital-management {
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
.hospitals-table {
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
  width: 600px;
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