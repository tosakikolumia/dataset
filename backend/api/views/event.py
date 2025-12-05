# backend/api/views/event.py
from rest_framework import viewsets, permissions
from api.models import EmergencyEvent, HospitalEvent
from api.permission import IsCityAdmin, IsHospitalAdmin, IsCityOrHospitalAdmin, ReadOnly
from api.serializers import EmergencyEventSerializer, HospitalEventSerializer

# 1. 突发事件定义
class EmergencyEventViewSet(viewsets.ModelViewSet):
    queryset = EmergencyEvent.objects.all().order_by('-report_time') # 默认按时间倒序
    serializer_class = EmergencyEventSerializer
    permission_classes = [IsCityOrHospitalAdmin | ReadOnly]

    def get_queryset(self):
        queryset = super().get_queryset()
        # 获取 URL 参数中的 hospital_id
        hospital_id = self.request.query_params.get('hospital_id')
        if hospital_id:
            # 筛选出 该医院参与的 事件
            queryset = queryset.filter(hospital_participations__hospital_id=hospital_id).distinct()
        return queryset

# 2. 医院参与事件记录
class HospitalEventViewSet(viewsets.ModelViewSet):
    queryset = HospitalEvent.objects.all()
    serializer_class = HospitalEventSerializer # 使用新的序列化器
    permission_classes = [IsCityOrHospitalAdmin]

    def perform_create(self, serializer):
        user = self.request.user
        if hasattr(user, 'profile') and user.profile.role == 'hospital_admin':
            serializer.save(hospital=user.profile.hospital)
        else:
            serializer.save()