from rest_framework import viewsets
from api.models import Department, DepartmentResource, DepartmentStaff
from api.serializers import DepartmentSerializer, DepartmentResourceSerializer, DepartmentStaffSerializer
from api.permission import IsCityAdmin, IsHospitalAdmin, ReadOnly


# =========================================================
# 1. 标准科室库 (市政管理，居民只读) - [恢复原代码]
# =========================================================
class DepartmentViewSet(viewsets.ModelViewSet):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    permission_classes = [IsCityAdmin | ReadOnly]


# =========================================================
# 2. 科室资源 (床位/设备) - [使用更新后的逻辑]
# =========================================================
class DepartmentResourceViewSet(viewsets.ModelViewSet):
    """
    科室资源管理接口
    - List: 医院管理员只能看到自己医院的资源。
    - Update: 允许修改床位、设备数等。
    """
    serializer_class = DepartmentResourceSerializer
    # 权限控制：市级管理员、医院管理员可写，其他人只读
    permission_classes = [IsCityAdmin | IsHospitalAdmin | ReadOnly]
    # 默认查询集
    queryset = DepartmentResource.objects.all()

    def get_queryset(self):
        user = self.request.user
        # 如果是匿名用户，返回空或只读(取决于全局配置，这里设为安全起见返回空)
        if not user.is_authenticated:
            return DepartmentResource.objects.none()

        # 医院管理员逻辑：只返回关联医院的资源
        if hasattr(user, 'profile') and user.profile.role == 'hospital_admin':
            if user.profile.hospital:
                return DepartmentResource.objects.filter(hospital=user.profile.hospital)
            return DepartmentResource.objects.none()

        # 市政管理员或超级用户可以看到所有
        return DepartmentResource.objects.all()

    def perform_create(self, serializer):
        # 创建时的逻辑
        user = self.request.user
        if hasattr(user, 'profile') and user.profile.role == 'hospital_admin':
            # 强制绑定到当前管理员的医院
            serializer.save(hospital=user.profile.hospital)
        else:
            serializer.save()


# =========================================================
# 3. 员工在科室的任职 - [恢复原代码]
# =========================================================
class DepartmentStaffViewSet(viewsets.ModelViewSet):
    queryset = DepartmentStaff.objects.all()
    serializer_class = DepartmentStaffSerializer
    permission_classes = [IsCityAdmin | IsHospitalAdmin]