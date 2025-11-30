# api/views/event.py
from rest_framework import viewsets, permissions
from api.models import EmergencyEvent, HospitalEvent
from api.permission import IsCityAdmin, IsHospitalAdmin, IsCityOrHospitalAdmin,ReadOnly
from api.serializers import (
    HospitalSerializer, HospitalLevelSerializer,
    HospitalDepartmentSerializer, HospitalServiceScoreSerializer,
    EmergencyEventSerializer
)
# 1. 突发事件定义
class EmergencyEventViewSet(viewsets.ModelViewSet):
    queryset = EmergencyEvent.objects.all()
    serializer_class = EmergencyEventSerializer
    # 所有人可看，市政或医院可新建(上报)
    permission_classes = [IsCityOrHospitalAdmin | ReadOnly]

# 2. 医院参与事件记录
class HospitalEventViewSet(viewsets.ModelViewSet):
    queryset = HospitalEvent.objects.all()
    serializer_class = EmergencyEventSerializer
    permission_classes = [IsCityOrHospitalAdmin]

    def perform_create(self, serializer):
        # 医院响应事件，自动填医院ID
        user = self.request.user
        if user.profile.role == 'hospital_admin':
            serializer.save(hospital=user.profile.hospital)
        else:
            serializer.save()