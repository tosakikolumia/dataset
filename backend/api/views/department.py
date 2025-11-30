# api/views/department.py
from rest_framework import viewsets, permissions
from api.models import Department, DepartmentResource, DepartmentStaff
from api.serializers import *
from api.permission import IsCityAdmin, IsHospitalAdmin, IsCityOrHospitalAdmin,ReadOnly

# 标准科室库 (市政管理，居民只读)
class DepartmentViewSet(viewsets.ModelViewSet):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    permission_classes = [IsCityAdmin | ReadOnly]

# 🏥 4.9 科室资源 (床位/设备)
class DepartmentResourceViewSet(viewsets.ModelViewSet):
    serializer_class = DepartmentResourceSerializer
    permission_classes = [IsCityAdmin | IsHospitalAdmin | ReadOnly]
    queryset = DepartmentResource.objects.all()
    def get_queryset(self):
        # 医院管理员只能看到自己医院的资源
        user = self.request.user  # 获取当前请求用户
        if user.is_authenticated and hasattr(user, 'profile') and user.profile.role == 'hospital_admin':  # 检查用户是否已认证且角色为医院管理员
            return DepartmentResource.objects.filter(hospital=user.profile.hospital)  # 返回用户所在医院的部门资源
        return DepartmentResource.objects.all()  # 返回所有部门资源

    def perform_create(self, serializer):
        # 强制绑定当前医院
        user = self.request.user
        if user.profile.role == 'hospital_admin':
            serializer.save(hospital=user.profile.hospital)
        else:
            serializer.save()

# 🏥 4.10 (部分) 员工在科室的任职
class DepartmentStaffViewSet(viewsets.ModelViewSet):
    queryset = DepartmentStaff.objects.all()
    serializer_class = DepartmentStaffSerializer
    permission_classes = [IsCityAdmin | IsHospitalAdmin] 
    # 注意：这个表没有 hospital_id，逻辑上需要前端传正确的 dept_id
    # 在 0基础阶段，先不写复杂的跨表校验