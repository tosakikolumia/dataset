import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/public/HomeView.vue'
import { useAuthStore } from '@/stores/auth'

// Public routes
const routes = [
  {
    path: '/',
    name: 'home',
    component: HomeView
  },
  {
    path: '/hospitals',
    name: 'hospital-list',
    component: () => import('../views/public/HospitalListView.vue')
  },
  {
    path: '/hospital/:id',
    name: 'hospital-detail',
    component: () => import('../views/public/HospitalDetailView.vue'),
    props: true
  },
  {
    path: '/login',
    name: 'login',
    component: () => import('../views/auth/LoginView.vue')
  },
  // Hospital admin routes
  {
    path: '/hospital-admin',
    name: 'hospital-admin',
    component: () => import('../views/admin/HospitalAdminView.vue'),
    meta: { requiresAuth: true, role: 'hospital_admin' }
  },
  {
    path: '/hospital-admin/info',
    name: 'hospital-info',
    component: () => import('../views/hospital_admin/HospitalInfoView.vue'),
    meta: { requiresAuth: true, role: 'hospital_admin' }
  },
  {
    path: '/hospital-admin/resources',
    name: 'hospital-resources',
    component: () => import('../views/hospital_admin/HospitalResourcesView.vue'),
    meta: { requiresAuth: true, role: 'hospital_admin' }
  },
  {
    path: '/hospital-admin/staff',
    name: 'hospital-staff',
    component: () => import('../views/hospital_admin/HospitalStaffView.vue'),
    meta: { requiresAuth: true, role: 'hospital_admin' }
  },
  {
    path: '/hospital-admin/events',
    name: 'hospital-events',
    component: () => import('../views/hospital_admin/HospitalEventsView.vue'),
    meta: { requiresAuth: true, role: 'hospital_admin' }
  },
  {
    path: '/hospital-admin/scores',
    name: 'hospital-scores',
    component: () => import('../views/hospital_admin/HospitalScoresView.vue'),
    meta: { requiresAuth: true, role: 'hospital_admin' }
  },
  // Municipal admin routes
  {
    path: '/municipal-admin',
    name: 'municipal-admin',
    component: () => import('../views/admin/MunicipalAdminView.vue'),
    meta: { requiresAuth: true, role: 'municipal_admin' }
  },
  {
    path: '/municipal-admin/hospitals',
    name: 'municipal-hospitals',
    component: () => import('../views/municipal_admin/HospitalManagementView.vue'),
    meta: { requiresAuth: true, role: 'municipal_admin' }
  },
  {
    path: '/municipal-admin/departments',
    name: 'municipal-departments',
    component: () => import('../views/municipal_admin/DepartmentManagementView.vue'),
    meta: { requiresAuth: true, role: 'municipal_admin' }
  },
  {
    path: '/municipal-admin/resources',
    name: 'municipal-resources',
    component: () => import('../views/municipal_admin/ResourceOverviewView.vue'),
    meta: { requiresAuth: true, role: 'municipal_admin' }
  },
  {
    path: '/municipal-admin/staff',
    name: 'municipal-staff',
    component: () => import('../views/municipal_admin/StaffStatisticsView.vue'),
    meta: { requiresAuth: true, role: 'municipal_admin' }
  },
  {
    path: '/municipal-admin/events',
    name: 'municipal-events',
    component: () => import('../views/municipal_admin/EventManagementView.vue'),
    meta: { requiresAuth: true, role: 'municipal_admin' }
  },
  {
    path: '/municipal-admin/levels',
    name: 'municipal-levels',
    component: () => import('../views/municipal_admin/LevelManagementView.vue'),
    meta: { requiresAuth: true, role: 'municipal_admin' }
  },
  {
    path: '/departments',
    name: 'department-index',
    component: () => import('../views/public/DepartmentIndexView.vue')
  },
  {
  path: '/municipal-admin/resources',
  name: 'municipal-resources',
  component: () => import('../views/municipal_admin/ResourceOverviewView.vue'),
  meta: { requiresAuth: true, role: 'municipal_admin' } // 市政专用
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// Navigation guard for authentication and roles
router.beforeEach((to, from, next) => {
  const authStore = useAuthStore()
  authStore.checkAuth() // Check if token exists in localStorage

  const requiresAuth = to.matched.some(record => record.meta?.requiresAuth)
  const userRole = authStore.user?.role

  if (requiresAuth && !authStore.isAuthenticated) {
    // Redirect to login in a real app
    if(to.name !== 'login') {
      console.log('Authentication required, redirecting to login')
      next('/login')
    } else {
      next()
    }
  } else if (requiresAuth && to.meta.role && userRole !== to.meta.role) {
    // Redirect to unauthorized page or home
    console.log(`Access denied for role: ${userRole}, required: ${to.meta.role}`)
    next('/')
  } else {
    next()
  }
})

export default router