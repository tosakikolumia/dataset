<template>
  <div class="hospital-info">
    <h1>🏥 本院基础信息管理</h1>

    <div v-if="loading" class="loading">加载中...</div>

    <div v-else-if="hospital" class="info-card">
      <form @submit.prevent="updateInfo">
        <div class="form-item">
          <label>医院名称：</label>
          <input v-model="hospital.name" disabled /> </div>

        <div class="form-item">
          <label>地址：</label>
          <input v-model="hospital.address" />
        </div>

        <div class="form-item">
          <label>等级：</label>
          <span>{{ hospital.level_name }}</span> </div>

        <div class="form-item">
          <label>总床位数：</label>
          <input type="number" v-model="hospital.bed_total" />
        </div>

        <div class="form-item">
          <label>日门诊承载量：</label>
          <input type="number" v-model="hospital.outpatient_capacity" />
        </div>

        <button type="submit" class="save-btn">保存修改</button>
      </form>
    </div>

    <div v-else class="empty">
      未找到医院信息，请确认该账号是否已绑定医院。
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import api from '@/services/api';
import { useAuthStore } from '@/stores/auth';

const hospital = ref(null);
const loading = ref(true);
const authStore = useAuthStore();

// 获取数据
const fetchHospitalInfo = async () => {
  try {
    // 假设：我们先获取所有医院，然后过滤出自己所在的医院
    // (更高级的做法是后端直接提供 /api/hospitals/me/，但为了配合你现有的通用接口，我们先这样做)
    // ⚠️ 注意：这里有一个逻辑断层。
    // 如果是 doc_zhang (id=101)，我们需要知道他的 hospital_id。
    // 简单起见，我们假设 doc_zhang 登录后，我们暂时硬编码 fetch id=1 的医院，
    // 或者你可以先在 Postman 里看 /api/hospitals/ 返回的列表，找到你创建的那个医院 ID。

    // 暂时策略：获取 ID=1 的医院（你之前造数据时的市一医院）进行演示
    const res = await api.hospital.getHospitalById(1);
    if (res.data.code === 0) {
        hospital.value = res.data.data; // 你的后端返回格式是 {code:0, data: {...}}
    } else {
        // 如果后端直接返回对象（ModelViewSet默认行为），则用 res.data
        hospital.value = res.data;
    }
  } catch (err) {
    console.error("获取医院信息失败", err);
    alert("获取信息失败，请检查 Token 或网络");
  } finally {
    loading.value = false;
  }
};

// 更新数据
const updateInfo = async () => {
  try {
    // 调用 PATCH 接口
    await api.hospital.updateHospital(hospital.value.hospital_id, {
      address: hospital.value.address,
      bed_total: hospital.value.bed_total,
      outpatient_capacity: hospital.value.outpatient_capacity
    });
    alert("保存成功！");
  } catch (err) {
    console.error("保存失败", err);
    alert("保存失败，可能权限不足");
  }
};

onMounted(() => {
  fetchHospitalInfo();
});
</script>

<style scoped>
.info-card {
  max-width: 600px;
  margin: 20px auto;
  padding: 20px;
  border: 1px solid #ddd;
  border-radius: 8px;
  background: white;
}
.form-item {
  margin-bottom: 15px;
  text-align: left;
}
.form-item label {
  display: inline-block;
  width: 120px;
  font-weight: bold;
}
.form-item input {
  padding: 8px;
  width: 300px;
}
.save-btn {
  background-color: #42b983;
  color: white;
  padding: 10px 20px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}
</style>