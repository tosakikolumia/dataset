<template>
  <div class="staff-statistics">
    <h1>全市人员统计</h1>
    <p>医生人数、护士人数、各医院人员分布</p>
    
    <div class="stats-overview">
      <div class="stat-card">
        <h3>医生总数</h3>
        <p class="stat-value">{{ stats.totalDoctors }}</p>
      </div>
      
      <div class="stat-card">
        <h3>护士总数</h3>
        <p class="stat-value">{{ stats.totalNurses }}</p>
      </div>
      
      <div class="stat-card">
        <h3>总员工数</h3>
        <p class="stat-value">{{ stats.totalStaff }}</p>
      </div>
    </div>
    
    <div class="staff-distribution">
      <h2>各医院人员分布</h2>
      <div class="hospital-staff-list">
        <div 
          v-for="hospitalStaff in hospitalStaffDistribution" 
          :key="hospitalStaff.hospitalId" 
          class="hospital-staff-card"
        >
          <h3>{{ hospitalStaff.hospitalName }}</h3>
          <div class="staff-breakdown">
            <div class="staff-type">
              <span class="type-label">医生:</span>
              <span class="type-value">{{ hospitalStaff.doctorsCount }}</span>
            </div>
            <div class="staff-type">
              <span class="type-label">护士:</span>
              <span class="type-value">{{ hospitalStaff.nursesCount }}</span>
            </div>
            <div class="staff-type">
              <span class="type-label">其他:</span>
              <span class="type-value">{{ hospitalStaff.otherCount }}</span>
            </div>
            <div class="staff-type total">
              <span class="type-label">总计:</span>
              <span class="type-value">{{ hospitalStaff.total }}</span>
            </div>
          </div>
        </div>
      </div>
    </div>
    
    <div class="staff-list-section">
      <h2>所有医护人员</h2>
      <div class="staff-table">
        <table>
          <thead>
            <tr>
              <th>姓名</th>
              <th>工号</th>
              <th>职位</th>
              <th>职称</th>
              <th>科室</th>
              <th>所属医院</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="staff in allStaff" :key="staff.id">
              <td>{{ staff.name }}</td>
              <td>{{ staff.staff_id }}</td>
              <td>{{ staff.position || '未设置' }}</td>
              <td>{{ staff.title || '未设置' }}</td>
              <td>{{ staff.department_name || '未设置' }}</td>
              <td>{{ getHospitalNameForStaff(staff.id) }}</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script>
import api from '@/services/api';

export default {
  name: 'StaffStatisticsView',
  data() {
    return {
      allStaff: [],
      hospitalStaffs: [],
      hospitals: [],
      stats: {
        totalDoctors: 0,
        totalNurses: 0,
        totalStaff: 0
      },
      hospitalStaffDistribution: []
    };
  },
  async created() {
    await this.loadData();
  },
  methods: {
    async loadData() {
      await Promise.all([
        this.loadAllStaff(),
        this.loadHospitalStaffs(),
        this.loadHospitals()
      ]);
      this.processStaffData();
    },
    async loadAllStaff() {
      try {
        const response = await api.staff.getAllStaffs();
        this.allStaff = response.data.data;
      } catch (error) {
        console.error('Error loading staff:', error);
      }
    },
    async loadHospitalStaffs() {
      try {
        const response = await api.staff.getHospitalStaffs({});
        this.hospitalStaffs = response.data.data;
      } catch (error) {
        console.error('Error loading hospital staffs:', error);
      }
    },
    async loadHospitals() {
      try {
        const response = await api.hospital.getAllHospitals();
        this.hospitals = response.data.data;
      } catch (error) {
        console.error('Error loading hospitals:', error);
      }
    },
    processStaffData() {
      // Calculate overall statistics
      this.stats.totalDoctors = this.allStaff.filter(staff => 
        staff.position && staff.position.toLowerCase().includes('医生')
      ).length;
      
      this.stats.totalNurses = this.allStaff.filter(staff => 
        staff.position && staff.position.toLowerCase().includes('护士')
      ).length;
      
      this.stats.totalStaff = this.allStaff.length;
      
      // Group hospital staffs by hospital
      const grouped = {};
      
      this.hospitalStaffs.forEach(hs => {
        const hospitalId = hs.hospital?.id || hs.hospital_id;
        const hospitalName = this.getHospitalName(hospitalId);
        
        if (!grouped[hospitalId]) {
          grouped[hospitalId] = {
            hospitalId,
            hospitalName,
            doctorsCount: 0,
            nursesCount: 0,
            otherCount: 0,
            total: 0
          };
        }
        
        // Get the staff member to determine their role
        const staffMember = this.allStaff.find(s => 
          s.id === hs.staff?.id || s.id === hs.staff_id
        );
        
        if (staffMember) {
          if (staffMember.position && staffMember.position.toLowerCase().includes('医生')) {
            grouped[hospitalId].doctorsCount++;
          } else if (staffMember.position && staffMember.position.toLowerCase().includes('护士')) {
            grouped[hospitalId].nursesCount++;
          } else {
            grouped[hospitalId].otherCount++;
          }
          grouped[hospitalId].total++;
        }
      });
      
      this.hospitalStaffDistribution = Object.values(grouped);
    },
    getHospitalName(hospitalId) {
      const hospital = this.hospitals.find(h => h.id === hospitalId);
      return hospital ? hospital.name : '未知医院';
    },
    getHospitalNameForStaff(staffId) {
      const hospitalStaff = this.hospitalStaffs.find(hs => 
        hs.staff?.id === staffId || hs.staff_id === staffId
      );
      
      if (hospitalStaff) {
        return this.getHospitalName(hospitalStaff.hospital?.id || hospitalStaff.hospital_id);
      }
      return '未分配';
    }
  }
};
</script>

<style scoped>
.staff-statistics {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

.stats-overview {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 20px;
  margin-bottom: 30px;
}

.stat-card {
  background: #f8f9fa;
  padding: 20px;
  border-radius: 8px;
  text-align: center;
  border: 1px solid #dee2e6;
}

.stat-card h3 {
  margin: 0 0 10px 0;
  color: #495057;
}

.stat-value {
  font-size: 2em;
  font-weight: bold;
  color: #007bff;
  margin: 0;
}

.staff-distribution h2 {
  margin-bottom: 20px;
  color: #343a40;
}

.hospital-staff-list {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 20px;
  margin-bottom: 30px;
}

.hospital-staff-card {
  border: 1px solid #ddd;
  border-radius: 8px;
  padding: 15px;
  background: white;
}

.hospital-staff-card h3 {
  margin-top: 0;
  color: #007bff;
  border-bottom: 1px solid #eee;
  padding-bottom: 10px;
}

.staff-breakdown {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 10px;
}

.staff-type {
  display: flex;
  justify-content: space-between;
  padding: 5px 0;
  border-bottom: 1px dashed #eee;
}

.staff-type.total {
  font-weight: bold;
  border-top: 1px solid #dee2e6;
  border-bottom: none;
}

.staff-type .type-label {
  color: #495057;
}

.staff-type.total .type-label {
  color: #007bff;
}

.staff-type .type-value {
  font-weight: bold;
}

.staff-list-section h2 {
  margin-top: 40px;
  margin-bottom: 20px;
  color: #343a40;
}

.staff-table {
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
</style>