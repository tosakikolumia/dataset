import axios from 'axios';

// Create an axios instance
const API_BASE_URL = 'http://localhost:8000/api'; // Backend API base URL

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor to add auth token if available
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor to handle responses globally
api.interceptors.response.use(
  (response) => {
    return response;
  },
  (error) => {
    // Handle global error responses here
    if (error.response?.status === 401) {
      // Redirect to login or clear auth data
      localStorage.removeItem('token');
      localStorage.removeItem('user');
    }
    return Promise.reject(error);
  }
);

// Public API endpoints
const publicAPI = {
  // Search hospitals
  searchHospitals: (filters) => api.post('/public/search_hospital/', filters),
};

// Hospital API endpoints
const hospitalAPI = {
  // Hospital CRUD operations
  getAllHospitals: () => api.get('/hospitals/'),
  getHospitalById: (id) => api.get(`/hospitals/${id}/`),
  createHospital: (data) => api.post('/hospitals/', data),
  updateHospital: (id, data) => api.patch(`/hospitals/${id}/`, data),
  deleteHospital: (id) => api.delete(`/hospitals/${id}/`),
  
  // Hospital specific endpoints
  getHospitalDepartments: (id) => api.get(`/hospitals/${id}/departments/`),
  getHospitalScores: (id) => api.get(`/hospitals/${id}/scores/`),
  getHospitalEvents: (id) => api.get(`/hospitals/${id}/events/`),

  getDepartmentDetail: (hospitalId, deptId) => api.get(`/hospitals/${hospitalId}/department_detail/`, {
    params: { dept_id: deptId }
  }),
};

// Department API endpoints
const departmentAPI = {
  getAllDepartments: () => api.get('/departments/'),
  createDepartment: (data) => api.post('/departments/', data),
  deleteDepartment: (id) => api.delete(`/departments/${id}/`),
  
  // Department resources
  getDepartmentResources: (params) => api.get('/department_resources/', { params }),
  createDepartmentResource: (data) => api.post('/department_resources/', data),
  updateDepartmentResource: (id, data) => api.patch(`/department_resources/${id}/`, data),
};

// Staff API endpoints
const staffAPI = {
  getAllStaffs: () => api.get('/staffs/'),
  createStaff: (data) => api.post('/staffs/', data),

  // 新增：获取人员统计信息
  getStatistics: () => api.get('/staffs/statistics/'),

  // Hospital staff relationships
  getHospitalStaffs: (params) => api.get('/hospital_staffs/', { params }),
  createHospitalStaff: (data) => api.post('/hospital_staffs/', data),
};

// Event API endpoints
const eventAPI = {
  // 修改这里：接收 params 参数，用于筛选
  getAllEvents: (params) => api.get('/events/', { params }),
  createEvent: (data) => api.post('/events/', data),

  // Hospital events
  getHospitalEvents: (params) => api.get('/hospital_events/', { params }),
  createHospitalEvent: (data) => api.post('/hospital_events/', data),
};

// Hospital level API endpoints
const hospitalLevelAPI = {
  getAllLevels: () => api.get('/hospital_levels/'),
  createLevel: (data) => api.post('/hospital_levels/', data),
  updateLevel: (id, data) => api.patch(`/hospital_levels/${id}/`, data),
  deleteLevel: (id) => api.delete(`/hospital_levels/${id}/`),
};

// Hospital scores API endpoints
const scoreAPI = {
  getScores: (params) => api.get('/scores/', { params }),
  createScore: (data) => api.post('/scores/', data),
};
// Authentication API endpoints
const authAPI = {
  // 对应后端的 POST /api/token/
  login: (credentials) => api.post('/token/', credentials),
  // 对应后端的 POST /api/token/refresh/
  refreshToken: (refresh) => api.post('/token/refresh/', { refresh }),
};

const districtAPI = {
  getAllDistricts: () => api.get('/districts/'),
};

// ... 前面代码不变

const statisticsAPI = {
  getDashboard: () => api.get('/statistics/dashboard/'),
  getHospitalRank: (params) => api.get('/statistics/hospital_rank/', { params }),
};




export default {
  public: publicAPI,
  hospital: hospitalAPI,
  department: departmentAPI,
  staff: staffAPI,
  event: eventAPI,
  hospitalLevel: hospitalLevelAPI,
  score: scoreAPI,
  district: districtAPI,
  auth: authAPI,
  statistics: statisticsAPI,
};