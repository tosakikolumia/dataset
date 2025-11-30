# api/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter

# 引入所有 ViewSet
from api.views.hospital import HospitalViewSet, HospitalLevelViewSet, HospitalDepartmentViewSet, HospitalServiceScoreViewSet
from api.views.department import DepartmentViewSet, DepartmentResourceViewSet, DepartmentStaffViewSet
from api.views.staff import StaffViewSet, HospitalStaffViewSet
from api.views.event import EmergencyEventViewSet, HospitalEventViewSet
from api.views.public import PublicViewSet

router = DefaultRouter()

# 🏥 医院模块
router.register(r'hospitals', HospitalViewSet)
router.register(r'hospital_levels', HospitalLevelViewSet)
router.register(r'hospital_departments', HospitalDepartmentViewSet)
router.register(r'scores', HospitalServiceScoreViewSet)

# 🏛 科室模块
router.register(r'departments', DepartmentViewSet)
router.register(r'department_resources', DepartmentResourceViewSet)
router.register(r'department_staffs', DepartmentStaffViewSet)

# 👨‍⚕️ 人员模块
router.register(r'staffs', StaffViewSet)
router.register(r'hospital_staffs', HospitalStaffViewSet)

# 🚨 事件模块
router.register(r'events', EmergencyEventViewSet)
router.register(r'hospital_events', HospitalEventViewSet)

# 🌏 公共模块 (注意：basename是必须的，因为它是ViewSet不是ModelViewSet)
router.register(r'public', PublicViewSet, basename='public')

urlpatterns = [
    path('', include(router.urls)),
]