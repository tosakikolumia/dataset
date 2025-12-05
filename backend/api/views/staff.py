# backend/api/views/staff.py
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Count, Q
from api.models import Staff, HospitalStaff
from api.serializers import StaffSerializer, HospitalStaffSerializer
from api.permission import IsCityAdmin, IsHospitalAdmin

# 1. 员工基础信息表
class StaffViewSet(viewsets.ModelViewSet):
    queryset = Staff.objects.all()
    serializer_class = StaffSerializer
    permission_classes = [IsCityAdmin | IsHospitalAdmin]

    @action(detail=False, methods=['get'])
    def statistics(self, request):
        """
        统计接口：返回全市人员规模、职称结构、各医院分布
        """
        # 1. 规模统计 (基于 title 字段模糊匹配)
        total_staff = Staff.objects.count()
        # 假设 title 包含 "医" 为医生，包含 "护" 为护士
        doctors_count = Staff.objects.filter(title__contains='医').count()
        nurses_count = Staff.objects.filter(title__contains='护').count()
        others_count = total_staff - doctors_count - nurses_count

        # 2. 职称结构 (Group By title)
        # 过滤掉空职称
        title_structure = Staff.objects.exclude(title__isnull=True).exclude(title='').values('title').annotate(
            count=Count('staff_id')
        ).order_by('-count')

        # 3. 各医院人员分布 (通过中间表 HospitalStaff 关联)
        # 统计每家医院的总人数、医生数、护士数
        hospital_stats = HospitalStaff.objects.values(
            'hospital__hospital_id',
            'hospital__name'
        ).annotate(
            total=Count('staff_id'),
            doctors_count=Count('staff_id', filter=Q(staff__title__contains='医')),
            nurses_count=Count('staff_id', filter=Q(staff__title__contains='护'))
        ).order_by('-total')

        data = {
            'overview': {
                'total_staff': total_staff,
                'total_doctors': doctors_count,
                'total_nurses': nurses_count,
                'total_others': others_count,
            },
            'title_structure': title_structure,
            'hospital_distribution': hospital_stats
        }
        return Response(data)

# 2. 员工-医院 执业关系表
class HospitalStaffViewSet(viewsets.ModelViewSet):
    queryset = HospitalStaff.objects.all()
    serializer_class = HospitalStaffSerializer
    permission_classes = [IsCityAdmin | IsHospitalAdmin]

    def get_queryset(self):
        user = self.request.user
        # 必须先判断 user 是否有 profile 属性，防止 Admin 用户登录报错
        if user.is_authenticated and hasattr(user, 'profile') and user.profile.role == 'hospital_admin':
            return HospitalStaff.objects.filter(hospital=user.profile.hospital)
        return super().get_queryset()

    def perform_create(self, serializer):
        # 医院管理员添加员工，自动关联到本院
        user = self.request.user
        if hasattr(user, 'profile') and user.profile.role == 'hospital_admin':
            serializer.save(hospital=user.profile.hospital)
        else:
            serializer.save()