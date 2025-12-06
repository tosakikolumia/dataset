# backend/api/views/staff.py
from django.db import transaction, models
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Count, Q
from api.models import Staff, HospitalStaff
from api.serializers import (
    StaffSerializer, HospitalStaffSerializer,HospitalStaffReadSerializer,
    HospitalStaffCreateCompositeSerializer,StaffDetailSerializer)
from django.utils import timezone
from api.permission import IsCityAdmin, IsHospitalAdmin

# 1. 员工基础信息表
class StaffViewSet(viewsets.ModelViewSet):
    queryset = Staff.objects.all()
    serializer_class = StaffSerializer
    permission_classes = [IsCityAdmin | IsHospitalAdmin]

    def get_serializer_class(self):
    # 根据不同的action动作返回不同的序列化器类
    # 如果当前动作是'retrieve'（获取详情），则返回StaffDetailSerializer
        if self.action == 'retrieve':
            return StaffDetailSerializer
    # 默认情况下返回StaffSerializer
        return StaffSerializer
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
# 2. 员工-医院 执业关系表
class HospitalStaffViewSet(viewsets.ModelViewSet):
    queryset = HospitalStaff.objects.all()
    permission_classes = [IsCityAdmin | IsHospitalAdmin]

    def get_serializer_class(self):
        # 读操作返回详细嵌套结构
        if self.action in ['list', 'retrieve']:
            return HospitalStaffReadSerializer
        # 创建操作使用复合序列化器（如果需要自定义create）或者默认
        return HospitalStaffSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated and hasattr(user, 'profile') and user.profile.role == 'hospital_admin':
            # 仅返回本院的员工
            return HospitalStaff.objects.filter(hospital=user.profile.hospital)
        return super().get_queryset()

    def create(self, request, *args, **kwargs):
        """
        重写 create 方法，支持直接创建 Staff 并关联到本院
        """
        user = request.user
        if not (hasattr(user, 'profile') and user.profile.role == 'hospital_admin' and user.profile.hospital):
            return Response({"detail": "只有医院管理员可以执行此操作"}, status=status.HTTP_403_FORBIDDEN)

        serializer = HospitalStaffCreateCompositeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        hospital = user.profile.hospital

        with transaction.atomic():
            # 1. 获取或创建 Staff 对象
            existing_id = data.get('existing_staff_id')
            if existing_id:
                try:
                    staff = Staff.objects.get(pk=existing_id)
                except Staff.DoesNotExist:
                    return Response({"detail": "指定的员工ID不存在"}, status=status.HTTP_400_BAD_REQUEST)
            else:
                # 自动生成递增的 staff_id
                max_staff_id = Staff.objects.aggregate(max_id=models.Max('staff_id'))['max_id']
                new_id = (max_staff_id or 0) + 1

                staff = Staff.objects.create(
                    staff_id=new_id,
                    name=data['name'],
                    gender=data.get('gender'),
                    title=data.get('title'),
                    phone=data.get('phone'),
                    hire_date=timezone.now().date()  # 使用当前日期
                )

            # 2. 创建关联关系 (HospitalStaff)
            if HospitalStaff.objects.filter(hospital=hospital, staff=staff).exists():
                return Response({"detail": "该员工已在本院任职"}, status=status.HTTP_400_BAD_REQUEST)

            hospital_staff = HospitalStaff.objects.create(
                hospital=hospital,
                staff=staff,
                employment_type=data.get('employment_type')
            )

        # 返回读取序列化器的数据
        read_serializer = HospitalStaffReadSerializer(hospital_staff)
        return Response(read_serializer.data, status=status.HTTP_201_CREATED)