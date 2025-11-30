# api/views/staff.py
from rest_framework import viewsets
from api.models import Staff, HospitalStaff
from api.serializers import StaffSerializer, HospitalStaffSerializer
from api.permission import IsCityAdmin, IsHospitalAdmin

# 1. 员工基础信息表
class StaffViewSet(viewsets.ModelViewSet):
    queryset = Staff.objects.all()
    serializer_class = StaffSerializer
    permission_classes = [IsCityAdmin | IsHospitalAdmin] # 居民不可见

# 2. 员工-医院 执业关系表
class HospitalStaffViewSet(viewsets.ModelViewSet):
    queryset = HospitalStaff.objects.all()
    serializer_class = HospitalStaffSerializer
    permission_classes = [IsCityAdmin | IsHospitalAdmin]

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated and user.profile.role == 'hospital_admin':
            return HospitalStaff.objects.filter(hospital=user.profile.hospital)
        return super().get_queryset()

    def perform_create(self, serializer):
        # 医院管理员添加员工，自动关联到本院
        user = self.request.user
        if user.profile.role == 'hospital_admin':
            serializer.save(hospital=user.profile.hospital)
        else:
            serializer.save()